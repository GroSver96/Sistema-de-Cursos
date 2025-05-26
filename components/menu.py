from reactpy import component, html, hooks
from components.agregar_usuario import AgregarUsuario
from components.agregar_curso import AgregarCurso
from components.agregar_notas import AgregarNotas
from components.ver_notas import VerNotas

@component
def Menu():
    current_view, set_current_view = hooks.use_state("inicio")

    # Títulos para cada vista
    titles = {
        "inicio": "Sistema de Cursos - Inicio",
        "agregar_usuario": "Sistema de Cursos - Agregar Usuario",
        "agregar_curso": "Sistema de Cursos - Agregar Curso", 
        "agregar_notas": "Sistema de Cursos - Agregar Notas",
        "ver_notas": "Sistema de Cursos - Ver Notas",
    }

    # Efecto para cambiar el título cuando cambia la vista
    def change_title():
        title = titles.get(current_view, "Sistema de Cursos")
        # Cambiar el título usando JavaScript
        return html.script(f"document.title = '{title}';")
    
    hooks.use_effect(change_title, [current_view])

    views = {
        "inicio": lambda: html.p("Bienvenido al sistema de cursos. Elige una opción del menú."),
        "agregar_usuario": AgregarUsuario,
        "agregar_curso": AgregarCurso,
        "agregar_notas": AgregarNotas,
        "ver_notas": VerNotas,
    }

    def render_view():
        view_component = views.get(current_view, views["inicio"])
        return view_component() if callable(view_component) else view_component

    def button_style(active):
        base_style = {
            "padding": "10px 15px",
            "margin": "5px",
            "border": "none",
            "borderRadius": "5px",
            "cursor": "pointer",
            "backgroundColor": "#f8f9fa",
            "transition": "all 0.3s",
            "boxShadow": "0 2px 5px rgba(0,0,0,0.1)",
            "fontWeight": "500"
        }
        if active:
            base_style.update({
                "backgroundColor": "#0d6efd",
                "color": "white",
                "boxShadow": "0 2px 5px rgba(13, 110, 253, 0.3)",
                "transform": "translateY(-2px)"
            })
        return base_style

    return html.div(
        {"style": {
            "padding": "20px",
            "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            "maxWidth": "1200px",
            "margin": "0 auto",
            "minHeight": "100vh",
            "backgroundColor": "#f5f5f5"
        }},
        
        # Script para cambiar título dinámicamente
        html.script(f"document.title = '{titles.get(current_view, 'Sistema de Cursos')}';"),
        
        # Header
        html.div(
            {"style": {
                "backgroundColor": "#0d6efd",
                "color": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "marginBottom": "20px",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
            }},
            html.h1(
                {"style": {"margin": "0", "display": "flex", "alignItems": "center"}},
                html.span({"style": {"marginRight": "10px"}}, "🎓"),
                "Sistema de Cursos Online"
            )
        ),
            
        # Navigation
        html.div(
            {"style": {
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "10px",
                "marginBottom": "20px",
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"
            }},
            *[
                html.button(
                    {
                        "on_click": lambda _, v=view_key: set_current_view(v),
                        "style": button_style(current_view == view_key),
                        "key": view_key
                    },
                    label
                )
                for view_key, label in [
                    ("inicio", "🏠 Inicio"),
                    ("agregar_usuario", "👥 Agregar Usuario"),
                    ("agregar_curso", "📚 Agregar Curso"),
                    ("agregar_notas", "📝 Agregar Notas"),
                    ("ver_notas", "📊 Ver Notas"),
                ]
            ]
        ),
        
        # Main Content
        html.div(
            {"style": {
                "backgroundColor": "white",
                "padding": "25px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                "minHeight": "400px"
            }},
            render_view()
        ),
        
        # Footer
        html.div(
            {"style": {
                "marginTop": "20px",
                "textAlign": "center",
                "color": "#6c757d",
                "padding": "15px",
                "fontSize": "0.9em"
            }},
            "Sistema de Cursos © 2025 | Todos los derechos reservados | GroSveR en los controles"
        ),
        
        # Custom CSS
        html.style("""
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            button:active {
                transform: translateY(0);
            }
        """)
    )

__all__ = ['Menu']