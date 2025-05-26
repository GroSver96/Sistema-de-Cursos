from reactpy import component, html, use_state, event, hooks
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@component
def AgregarUsuario():
    nombre, set_nombre = use_state("")
    apellido, set_apellido = use_state("")
    email, set_email = use_state("")
    tipo_usuario, set_tipo_usuario = use_state("estudiante")
    contraseña, set_contraseña = use_state("")
    mensaje, set_mensaje = use_state("")

    alumnos_por_curso, set_alumnos_por_curso = use_state([])
    vista_seleccionada, set_vista_seleccionada = use_state("con_curso")  # Nueva variable

    async def cargar_datos_vista():
        try:
            url = (
                "http://localhost:8000/api/vista-alumnos-por-curso"
                if vista_seleccionada == "con_curso"
                else "http://localhost:8000/api/alumnos-sin-curso"
            )
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        set_alumnos_por_curso(data)
                    elif data.get("success"):
                        set_alumnos_por_curso(data["data"])
        except Exception as e:
            logger.error(f"Error al cargar vista: {e}")

    hooks.use_effect(cargar_datos_vista, [vista_seleccionada])

    @event(prevent_default=True)
    async def enviar_formulario(event):
        try:
            if not all([nombre, apellido, email, contraseña]):
                set_mensaje("❌ Todos los campos son obligatorios")
                return

            if len(contraseña) < 8:
                set_mensaje("❌ Contraseña muy corta (mínimo 8 caracteres)")
                return

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "http://localhost:8000/api/guardar-usuario",
                    json={
                        "nombre": nombre,
                        "apellido": apellido,
                        "email": email,
                        "tipo_usuario": tipo_usuario,
                        "contraseña": contraseña
                    }
                )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    set_mensaje("✅ Usuario registrado exitosamente")
                    set_nombre("")
                    set_apellido("")
                    set_email("")
                    set_tipo_usuario("estudiante")
                    set_contraseña("")
                    await cargar_datos_vista()
                else:
                    set_mensaje(f"❌ {data.get('message', 'Error desconocido')}")
            else:
                set_mensaje(f"❌ Error HTTP {response.status_code}")

        except httpx.RequestError as e:
            logger.error(f"Error de conexión: {e}")
            set_mensaje("❌ Error de conexión con el servidor")
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            set_mensaje("❌ Error interno")

    return html.div(
        {"style": {
            "maxWidth": "600px",
            "margin": "0 auto",
            "padding": "20px",
            "border": "1px solid #ddd",
            "borderRadius": "5px",
            "backgroundColor": "#f9f9f9"
        }},
        html.h2("Agregar Nuevo Usuario"),
        html.form(
            {"on_submit": enviar_formulario},
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label("Nombre:"),
                html.input({
                    "type": "text",
                    "value": nombre,
                    "on_change": lambda e: set_nombre(e["target"]["value"]),
                    "required": True,
                    "style": {
                        "width": "100%",
                        "padding": "8px",
                        "marginTop": "5px",
                        "border": "1px solid #ddd",
                        "borderRadius": "4px"
                    }
                })
            ),
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label("Apellido:"),
                html.input({
                    "type": "text",
                    "value": apellido,
                    "on_change": lambda e: set_apellido(e["target"]["value"]),
                    "required": True,
                    "style": {
                        "width": "100%",
                        "padding": "8px",
                        "marginTop": "5px",
                        "border": "1px solid #ddd",
                        "borderRadius": "4px"
                    }
                })
            ),
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label("Email:"),
                html.input({
                    "type": "email",
                    "value": email,
                    "on_change": lambda e: set_email(e["target"]["value"]),
                    "required": True,
                    "style": {
                        "width": "100%",
                        "padding": "8px",
                        "marginTop": "5px",
                        "border": "1px solid #ddd",
                        "borderRadius": "4px"
                    }
                })
            ),
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label("Tipo de Usuario:"),
                html.select(
                    {
                        "value": tipo_usuario,
                        "on_change": lambda e: set_tipo_usuario(e["target"]["value"]),
                        "style": {
                            "width": "100%",
                            "padding": "8px",
                            "marginTop": "5px",
                            "border": "1px solid #ddd",
                            "borderRadius": "4px"
                        }
                    },
                    html.option({"value": "estudiante"}, "Estudiante"),
                    html.option({"value": "docente"}, "Docente")
                )
            ),
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label("Contraseña:"),
                html.input({
                    "type": "password",
                    "value": contraseña,
                    "on_change": lambda e: set_contraseña(e["target"]["value"]),
                    "required": True,
                    "minLength": 8,
                    "style": {
                        "width": "100%",
                        "padding": "8px",
                        "marginTop": "5px",
                        "border": "1px solid #ddd",
                        "borderRadius": "4px"
                    }
                })
            ),
            html.button(
                {
                    "type": "submit",
                    "style": {
                        "width": "100%",
                        "padding": "10px",
                        "backgroundColor": "#0d6efd",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "4px",
                        "cursor": "pointer",
                        "fontSize": "16px"
                    }
                },
                "Registrar Usuario"
            )
        ),
        html.p(
            {"style": {
                "marginTop": "15px",
                "padding": "10px",
                "borderRadius": "4px",
                "backgroundColor": "#ffebee" if "❌" in mensaje else "#e8f5e9",
                "color": "#c62828" if "❌" in mensaje else "#2e7d32",
                "textAlign": "center"
            }},
            mensaje if mensaje else ""
        ),
        html.hr(),
        html.h3("📋 Alumnos"),
        html.div(
            {"style": {"marginBottom": "15px"}},
            html.label("Mostrar alumnos: "),
            html.select(
                {
                    "value": vista_seleccionada,
                    "on_change": lambda e: set_vista_seleccionada(e["target"]["value"]),
                    "style": {
                        "padding": "8px",
                        "borderRadius": "4px",
                        "marginLeft": "10px",
                        "border": "1px solid #ccc"
                    }
                },
                html.option({"value": "con_curso"}, "Con curso"),
                html.option({"value": "sin_curso"}, "Sin curso")
            )
        ),
        html.table(
            {"style": {
                "width": "100%",
                "marginTop": "15px",
                "borderCollapse": "collapse",
                "border": "1px solid #ccc"
            }},
            html.thead(
                html.tr(
                    *[
                        html.th("ID Alumno"),
                        html.th("Nombre"),
                        html.th("Email") if vista_seleccionada == "sin_curso" else html.th("ID Curso"),
                        html.th("Tipo Usuario") if vista_seleccionada == "sin_curso" else html.th("Curso"),
                        html.th("") if vista_seleccionada == "sin_curso" else html.th("Estado")
                    ]
                )
            ),
            html.tbody(*[
                html.tr(
                    *([
                        html.td(row.get("id_usuario", "")),
                        html.td(f"{row.get('nombre', '')} {row.get('apellido', '')}"),
                        html.td(row.get("email", "")),
                        html.td(row.get("tipo_usuario", ""))
                    ] if vista_seleccionada == "sin_curso" else [
                        html.td(row.get("id_alumno", "")),
                        html.td(f"{row.get('nombre_alumno', '')} {row.get('apellido_alumno', '')}"),
                        html.td(row.get("id_curso", "")),
                        html.td(row.get("curso", "")),
                        html.td(row.get("estado", ""))
                    ])
                ) for row in alumnos_por_curso
            ])
        )
    )
