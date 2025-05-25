from reactpy import component, html, use_state, event
import httpx

@component
def AgregarNotas():
    tipo_evaluacion, set_tipo_evaluacion = use_state("examen")
    nota, set_nota = use_state("")
    id_leccion, set_id_leccion = use_state("")
    id_usuario, set_id_usuario = use_state("")
    mensaje, set_mensaje = use_state("")
    es_exito, set_es_exito = use_state(False)
    cargando, set_cargando = use_state(False)

    @event(prevent_default=True)
    async def guardar_evaluacion(event):
        set_cargando(True)
        set_mensaje("")

        try:
            if not all([tipo_evaluacion, nota, id_leccion, id_usuario]):
                set_mensaje("❌ Todos los campos son obligatorios")
                set_es_exito(False)
                return

            try:
                nota_int = int(nota)
                if not 0 <= nota_int <= 100:
                    set_mensaje("❌ La nota debe estar entre 0 y 100")
                    set_es_exito(False)
                    return
            except ValueError:
                set_mensaje("❌ La nota debe ser un número válido")
                set_es_exito(False)
                return

            evaluacion = {
                "tipo": tipo_evaluacion,
                "nota": nota_int,
                "id_leccion": int(id_leccion),
                "id_usuario": int(id_usuario)
            }

            async with httpx.AsyncClient() as client:
                response = await client.post("http://localhost:8000/api/guardar-evaluacion", json=evaluacion)
                data = response.json()

            if response.status_code == 200:
                set_mensaje("✅ Evaluación guardada correctamente")
                set_es_exito(True)
                set_nota("")
                set_id_leccion("")
                set_id_usuario("")
            else:
                set_mensaje(f"❌ {data.get('detail', 'Error desconocido')}")
                set_es_exito(False)

        except Exception as e:
            set_mensaje(f"❌ Error: {str(e)}")
            set_es_exito(False)
        finally:
            set_cargando(False)

    return html.div(
        {"style": {
            "maxWidth": "500px",
            "margin": "0 auto",
            "padding": "20px",
            "border": "1px solid #ddd",
            "borderRadius": "5px",
            "backgroundColor": "#f9f9f9"
        }},
        html.h2("Agregar Evaluación"),
        html.form(
            {"on_submit": guardar_evaluacion},
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label("Tipo de Evaluación:"),
                html.select(
                    {
                        "value": tipo_evaluacion,
                        "on_change": lambda e: set_tipo_evaluacion(e["target"]["value"]),
                        "style": {
                            "width": "100%",
                            "padding": "8px",
                            "marginTop": "5px",
                            "border": "1px solid #ddd",
                            "borderRadius": "4px"
                        }
                    },
                    html.option({"value": "examen"}, "Examen"),
                    html.option({"value": "tarea"}, "Tarea"),
                    html.option({"value": "quiz"}, "Quiz")
                )
            ),
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label("Nota (0-100):"),
                html.input({
                    "type": "number",
                    "value": nota,
                    "on_change": lambda e: set_nota(e["target"]["value"]),
                    "required": True,
                    "min": 0,
                    "max": 100,
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
                html.label("ID Lección:"),
                html.input({
                    "type": "number",
                    "value": id_leccion,
                    "on_change": lambda e: set_id_leccion(e["target"]["value"]),
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
                html.label("ID Usuario:"),
                html.input({
                    "type": "number",
                    "value": id_usuario,
                    "on_change": lambda e: set_id_usuario(e["target"]["value"]),
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
                "Guardar Evaluación"
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
        )
    )
