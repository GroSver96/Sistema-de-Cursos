from reactpy import component, html, use_state, event
import httpx

@component
def VerNotas():
    id_usuario, set_id_usuario = use_state("")
    id_curso, set_id_curso = use_state("")
    resultado_alumno, set_resultado_alumno = use_state([])
    resultado_curso, set_resultado_curso = use_state([])
    mensaje, set_mensaje = use_state("")
    cargando, set_cargando = use_state(False)

    @event(prevent_default=True)
    async def consultar_por_alumno(event):
        set_cargando(True)
        set_mensaje("")
        set_resultado_alumno([])

        try:
            if not id_usuario:
                set_mensaje("❌ Debes ingresar un ID de usuario")
                return

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://localhost:8000/api/notas-por-alumno",
                    params={"id_usuario": int(id_usuario)}
                )
                data = response.json()

            if response.status_code == 200 and data.get("success"):
                set_resultado_alumno(data["data"])
                if not data["data"]:
                    set_mensaje("ℹ️ No hay evaluaciones para este usuario")
            else:
                set_mensaje(f"❌ {data.get('detail', 'Error desconocido')}")

        except Exception as e:
            set_mensaje(f"❌ Error: {e}")
        finally:
            set_cargando(False)

    @event(prevent_default=True)
    async def consultar_por_curso(event):
        set_cargando(True)
        set_mensaje("")
        set_resultado_curso([])

        try:
            if not id_curso:
                set_mensaje("❌ Debes ingresar un ID de curso")
                return

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://localhost:8000/api/notas-por-curso",
                    params={"id_curso": int(id_curso)}
                )
                data = response.json()

            if response.status_code == 200 and data.get("success"):
                set_resultado_curso(data["data"])
                if not data["data"]:
                    set_mensaje("ℹ️ No hay notas registradas en este curso")
            else:
                set_mensaje(f"❌ {data.get('detail', 'Error desconocido')}")

        except Exception as e:
            set_mensaje(f"❌ Error: {e}")
        finally:
            set_cargando(False)

    def render_tabla_alumno():
        if not resultado_alumno:
            return None
        return html.table(
            {"style": {"width": "100%", "marginTop": "15px", "borderCollapse": "collapse"}},
            html.thead(
                html.tr(
                    html.th("ID Usuario"),
                    html.th("Nombre"),
                    html.th("Curso"),
                    html.th("Promedio")
                )
            ),
            html.tbody(*[
                html.tr(
                    html.td(r["id_usuario"]),
                    html.td(r["nombre_completo"]),
                    html.td(r["curso"]),
                    html.td(str(r["promedio_notas"]))
                ) for r in resultado_alumno
            ])
        )

    def render_tabla_curso():
        if not resultado_curso:
            return None
        return html.table(
            {"style": {"width": "100%", "marginTop": "15px", "borderCollapse": "collapse"}},
            html.thead(
                html.tr(
                    html.th("ID Curso"),
                    html.th("Curso"),
                    html.th("Alumno"),
                    html.th("Promedio")
                )
            ),
            html.tbody(*[
                html.tr(
                    html.td(r["id_curso"]),
                    html.td(r["curso"]),
                    html.td(r["nombre_completo"]),
                    html.td(str(r["promedio_alumno"]))
                ) for r in resultado_curso
            ])
        )

    return html.div(
        {"style": {
            "maxWidth": "600px",
            "margin": "0 auto",
            "padding": "20px",
            "border": "1px solid #ddd",
            "borderRadius": "5px",
            "backgroundColor": "#f9f9f9"
        }},
        html.h2("Ver Notas"),

        # --- Buscar por alumno ---
        html.form(
            {"on_submit": consultar_por_alumno, "style": {"marginBottom": "20px"}},
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label("ID Usuario:"),
                html.input({
                    "type": "number",
                    "value": id_usuario,
                    "on_change": lambda e: set_id_usuario(e["target"]["value"]),
                    "placeholder": "Ej: 1",
                    "style": {
                        "width": "100%", "padding": "8px", "marginTop": "5px",
                        "border": "1px solid #ddd", "borderRadius": "4px"
                    }
                })
            ),
            html.button({
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
            }, "🔍 Ver notas del alumno")
        ),

        # --- Buscar por curso ---
        html.form(
            {"on_submit": consultar_por_curso, "style": {"marginBottom": "20px"}},
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label("ID Curso:"),
                html.input({
                    "type": "number",
                    "value": id_curso,
                    "on_change": lambda e: set_id_curso(e["target"]["value"]),
                    "placeholder": "Ej: 2",
                    "style": {
                        "width": "100%", "padding": "8px", "marginTop": "5px",
                        "border": "1px solid #ddd", "borderRadius": "4px"
                    }
                })
            ),
            html.button({
                "type": "submit",
                "style": {
                    "width": "100%",
                    "padding": "10px",
                    "backgroundColor": "#ff9800",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer",
                    "fontSize": "16px"
                }
            }, "📚 Ver notas por curso")
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

        render_tabla_alumno(),
        render_tabla_curso()
    )
