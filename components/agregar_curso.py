from reactpy import component, html, use_state, use_effect
import httpx
import asyncio
from datetime import datetime

@component
def AgregarCurso():
    # Estados del formulario de curso
    titulo, set_titulo = use_state("")
    descripcion, set_descripcion = use_state("")
    fecha_inicio, set_fecha_inicio = use_state("")
    fecha_fin, set_fecha_fin = use_state("")
    id_usuario, set_id_usuario = use_state("")
    mensaje, set_mensaje = use_state("")
    
    # Estados para inscripción
    id_alumno, set_id_alumno = use_state("")
    mensaje_inscripcion, set_mensaje_inscripcion = use_state("")
    
    # Estados para la lista de cursos
    cursos, set_cursos = use_state([])
    expanded_cursos, set_expanded_cursos = use_state({})
    expanded_lecciones, set_expanded_lecciones = use_state({})
    
    # Estados para nuevas lecciones
    nueva_leccion, set_nueva_leccion = use_state({})
    mensaje_leccion, set_mensaje_leccion = use_state("")

    async def enviar_formulario(event):
        try:
            if not all([titulo, descripcion, fecha_inicio, fecha_fin, id_usuario]):
                set_mensaje("❌ Todos los campos son obligatorios")
                return

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/api/guardar-curso",
                    json={
                        "titulo": titulo,
                        "descripcion": descripcion,
                        "fecha_inicio": fecha_inicio,
                        "fecha_fin": fecha_fin,
                        "id_usuario": int(id_usuario)
                    }
                )

            if response.status_code == 200 and response.json().get("success"):
                set_mensaje("✅ Curso registrado correctamente")
                set_titulo("")
                set_descripcion("")
                set_fecha_inicio("")
                set_fecha_fin("")
                set_id_usuario("")
                await cargar_cursos()
            else:
                set_mensaje(f"❌ Error: {response.json().get('message', 'Error desconocido')}")
                
        except Exception as e:
            set_mensaje(f"❌ Error inesperado: {str(e)}")

    async def enviar_leccion(id_curso):
        try:
            if not nueva_leccion.get(id_curso):
                set_mensaje_leccion("❌ Título requerido para la lección")
                return

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/api/guardar-leccion",
                    json={
                        "titulo": nueva_leccion[id_curso],
                        "contenido": "",
                        "id_curso": id_curso
                    }
                )

            if response.status_code == 200 and response.json().get("success"):
                set_mensaje_leccion("✅ Lección guardada")
                set_nueva_leccion({**nueva_leccion, id_curso: ""})
                await cargar_cursos()
            else:
                set_mensaje_leccion(f"❌ Error: {response.json().get('message', 'Error desconocido')}")
                
        except Exception as e:
            set_mensaje_leccion(f"❌ Error inesperado: {str(e)}")

    async def inscribir_alumno(id_curso):
        try:
            if not id_alumno:
                set_mensaje_inscripcion("❌ ID de alumno requerido")
                return

            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/api/inscribir-alumno",
                    json={
                        "id_usuario": int(id_alumno),
                        "id_curso": id_curso,
                        "fecha_inscripcion": fecha_actual,
                        "estado": "activa"
                    }
                )

            if response.status_code == 200 and response.json().get("success"):
                set_mensaje_inscripcion("✅ Alumno inscrito correctamente")
                set_id_alumno("")
            else:
                set_mensaje_inscripcion(f"❌ Error: {response.json().get('message', 'Error desconocido')}")
                
        except Exception as e:
            set_mensaje_inscripcion(f"❌ Error inesperado: {str(e)}")

    async def cargar_cursos():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/cursos-lecciones")
                if response.status_code == 200:
                    set_cursos(response.json())
        except Exception as e:
            set_mensaje(f"❌ Error al cargar cursos: {str(e)}")

    def toggle_curso(id_curso):
        set_expanded_cursos({
            **expanded_cursos,
            id_curso: not expanded_cursos.get(id_curso, False)
        })

    def toggle_leccion(id_curso, id_leccion):
        set_expanded_lecciones({
            **expanded_lecciones,
            f"{id_curso}-{id_leccion}": not expanded_lecciones.get(f"{id_curso}-{id_leccion}", False)
        })

    use_effect(lambda: asyncio.ensure_future(cargar_cursos()), [])

    return html.div(
        {"style": {
            "maxWidth": "1000px",
            "margin": "0 auto",
            "padding": "20px",
            "fontFamily": "Arial"
        }},
        # Formulario para agregar curso
        html.div(
            {"style": {
                "marginBottom": "30px",
                "padding": "20px",
                "border": "1px solid #ddd",
                "borderRadius": "5px",
                "backgroundColor": "#f9f9f9"
            }},
            html.h2({"style": {"marginTop": "0"}}, "Agregar Nuevo Curso"),
            html.form(
                {"on_submit": lambda e: asyncio.ensure_future(enviar_formulario(e))},
                html.div(
                    {"style": {"marginBottom": "15px"}},
                    html.label("Título del Curso:"),
                    html.input({
                        "type": "text",
                        "value": titulo,
                        "on_change": lambda e: set_titulo(e["target"]["value"]),
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
                    html.label("Descripción:"),
                    html.textarea({
                        "value": descripcion,
                        "on_change": lambda e: set_descripcion(e["target"]["value"]),
                        "required": True,
                        "style": {
                            "width": "100%",
                            "padding": "8px",
                            "marginTop": "5px",
                            "border": "1px solid #ddd",
                            "borderRadius": "4px",
                            "minHeight": "100px"
                        }
                    })
                ),
                html.div(
                    {"style": {"display": "flex", "gap": "15px", "marginBottom": "15px"}},
                    html.div(
                        {"style": {"flex": "1"}},
                        html.label("Fecha de Inicio:"),
                        html.input({
                            "type": "date",
                            "value": fecha_inicio,
                            "on_change": lambda e: set_fecha_inicio(e["target"]["value"]),
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
                        {"style": {"flex": "1"}},
                        html.label("Fecha de Fin:"),
                        html.input({
                            "type": "date",
                            "value": fecha_fin,
                            "on_change": lambda e: set_fecha_fin(e["target"]["value"]),
                            "required": True,
                            "style": {
                                "width": "100%",
                                "padding": "8px",
                                "marginTop": "5px",
                                "border": "1px solid #ddd",
                                "borderRadius": "4px"
                            }
                        })
                    )
                ),
                html.div(
                    {"style": {"marginBottom": "15px"}},
                    html.label("ID del Instructor:"),
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
                    "Guardar Curso"
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
        ),
        
        # Lista de cursos con navegación jerárquica
        html.div(
            {"style": {
                "padding": "20px",
                "border": "1px solid #ddd",
                "borderRadius": "5px",
                "backgroundColor": "#f9f9f9"
            }},
            html.h2({"style": {"marginTop": "0"}}, "Cursos Disponibles"),
            
            # Formulario para inscribir alumno
            html.div(
                {"style": {
                    "marginBottom": "20px",
                    "padding": "15px",
                    "backgroundColor": "#fff8e1",
                    "borderRadius": "5px"
                }},
                html.h3("Inscribir Alumno a Curso"),
                html.div(
                    {"style": {"display": "flex", "gap": "10px", "alignItems": "center"}},
                    html.input({
                        "type": "number",
                        "placeholder": "ID del Alumno",
                        "value": id_alumno,
                        "on_change": lambda e: set_id_alumno(e["target"]["value"]),
                        "style": {
                            "padding": "8px",
                            "border": "1px solid #ddd",
                            "borderRadius": "4px",
                            "flex": "1"
                        }
                    }),
                    html.p(
                        {"style": {"margin": "0 10px"}},
                        "Seleccione un curso y haga clic en Inscribir"
                    )
                ),
                html.p(
                    {"style": {
                        "marginTop": "10px",
                        "padding": "10px",
                        "borderRadius": "4px",
                        "backgroundColor": "#ffebee" if "❌" in mensaje_inscripcion else "#e8f5e9",
                        "color": "#c62828" if "❌" in mensaje_inscripcion else "#2e7d32",
                        "textAlign": "center"
                    }},
                    mensaje_inscripcion if mensaje_inscripcion else ""
                )
            ),
            
            html.ul(
                {"style": {"listStyle": "none", "paddingLeft": "0"}},
                *[
                    html.li(
                        {"key": f"curso-{curso['curso']['id_curso']}", "style": {"marginBottom": "15px"}},
                        html.div(
                            {"style": {
                                "display": "flex",
                                "alignItems": "center",
                                "padding": "10px",
                                "backgroundColor": "#e3f2fd",
                                "borderRadius": "4px",
                            }},
                            html.button(
                                {
                                    "on_click": lambda _, id_curso=curso['curso']['id_curso']: toggle_curso(id_curso),
                                    "style": {
                                        "background": "none",
                                        "border": "none",
                                        "fontSize": "16px",
                                        "marginRight": "10px",
                                        "cursor": "pointer"
                                    }
                                },
                                "▶" if not expanded_cursos.get(curso['curso']['id_curso'], False) else "▼"
                            ),
                            html.span(
                                {"style": {"fontWeight": "bold", "flex": "1"}},
                                f"{curso['curso']['titulo']} (ID: {curso['curso']['id_curso']})"
                            ),
                            html.button(
                                {
                                    "on_click": lambda _, id_curso=curso['curso']['id_curso']: asyncio.ensure_future(inscribir_alumno(id_curso)),
                                    "style": {
                                        "padding": "8px 15px",
                                        "backgroundColor": "#ff9800",
                                        "color": "white",
                                        "border": "none",
                                        "borderRadius": "4px",
                                        "cursor": "pointer",
                                        "marginLeft": "10px"
                                    }
                                },
                                "Inscribir Alumno"
                            )
                        ),
                        
                        # Lecciones del curso (se muestra si está expandido)
                        html.ul(
                            {"style": {
                                "listStyle": "none",
                                "paddingLeft": "20px",
                                "display": "none" if not expanded_cursos.get(curso['curso']['id_curso'], False) else "block"
                            }},
                            # Formulario para agregar nueva lección
                            html.li(
                                {"style": {"margin": "10px 0"}},
                                html.div(
                                    {"style": {"display": "flex", "gap": "10px"}},
                                    html.input({
                                        "type": "text",
                                        "placeholder": "Nueva lección (máx. 20 caracteres)",
                                        "value": nueva_leccion.get(curso['curso']['id_curso'], ""),
                                        "on_change": lambda e, id_curso=curso['curso']['id_curso']: 
                                            set_nueva_leccion({**nueva_leccion, id_curso: e["target"]["value"]}),
                                        "style": {
                                            "flex": "1",
                                            "padding": "8px",
                                            "border": "1px solid #ddd",
                                            "borderRadius": "4px"
                                        },
                                        "maxLength": "20"
                                    }),
                                    html.button(
                                        {
                                            "on_click": lambda _, id_curso=curso['curso']['id_curso']: 
                                                asyncio.ensure_future(enviar_leccion(id_curso)),
                                            "style": {
                                                "padding": "8px 15px",
                                                "backgroundColor": "#2196F3",
                                                "color": "white",
                                                "border": "none",
                                                "borderRadius": "4px",
                                                "cursor": "pointer"
                                            }
                                        },
                                        "Agregar Lección"
                                    )
                                )
                            ),
                            
                            # Lista de lecciones existentes
                            *[
                                html.li(
                                    {"key": f"leccion-{leccion['id_leccion']}", "style": {"margin": "5px 0"}},
                                    html.div(
                                        {"style": {
                                            "display": "flex",
                                            "alignItems": "center",
                                            "padding": "8px",
                                            "backgroundColor": "#f5f5f5",
                                            "borderRadius": "4px"
                                        }},
                                        html.button(
                                            {
                                                "on_click": lambda _, id_curso=curso['curso']['id_curso'], id_leccion=leccion['id_leccion']: 
                                                    toggle_leccion(id_curso, id_leccion),
                                                "style": {
                                                    "background": "none",
                                                    "border": "none",
                                                    "fontSize": "14px",
                                                    "marginRight": "8px",
                                                    "cursor": "pointer"
                                                }
                                            },
                                            "▶" if not expanded_lecciones.get(f"{curso['curso']['id_curso']}-{leccion['id_leccion']}", False) else "▼"
                                        ),
                                        html.span(
                                            {"style": {"flex": "1"}},
                                            leccion['titulo']
                                        )
                                    ),
                                    # Contenido de la lección (se muestra si está expandido)
                                    html.div(
                                        {"style": {
                                            "padding": "10px",
                                            "marginLeft": "20px",
                                            "backgroundColor": "#fff",
                                            "border": "1px solid #eee",
                                            "borderRadius": "4px",
                                            "display": "none" if not expanded_lecciones.get(f"{curso['curso']['id_curso']}-{leccion['id_leccion']}", False) else "block"
                                        }},
                                        html.p(leccion.get('contenido', 'Sin contenido'))
                                    )
                                )
                                for leccion in curso['lecciones']
                            ]
                        )
                    )
                    for curso in cursos
                ]
            ),
            html.p(
                {"style": {
                    "marginTop": "15px",
                    "padding": "10px",
                    "borderRadius": "4px",
                    "backgroundColor": "#ffebee" if "❌" in mensaje_leccion else "#e8f5e9",
                    "color": "#c62828" if "❌" in mensaje_leccion else "#2e7d32",
                    "textAlign": "center"
                }},
                mensaje_leccion if mensaje_leccion else ""
            )
        )
    )