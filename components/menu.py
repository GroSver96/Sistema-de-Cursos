from reactpy import component, html, use_state
from components.agregar_usuario import AgregarUsuario
from components.agregar_curso import AgregarCurso
from components.agregar_notas import AgregarNotas
from components.ver_notas import VerNotas

@component
def Menu():
    current_view, set_current_view = use_state("inicio")

    views = {
        "inicio": lambda: html.p("Bienvenido al sistema de cursos. Elige una opción del menú."),
        "agregar_usuario": AgregarUsuario,
        "agregar_curso": AgregarCurso,
        "agregar_notas": AgregarNotas,
        "ver_notas": VerNotas,
    }

    def render_view():
        # Llamamos a la función/componente correspondiente
        view_component = views.get(current_view, views["inicio"])
        return view_component() if callable(view_component) else view_component

    def button_style(active):
        base = {
            "padding": "10px 15px",
            "border": "1px solid #ccc",
            "borderRadius": "5px",
            "cursor": "pointer",
            "backgroundColor": "#f0f0f0",
            "transition": "background-color 0.3s",
        }
        if active:
            base.update({
                "backgroundColor": "#4CAF50",
                "color": "white",
                "borderColor": "#4CAF50",
                "fontWeight": "bold",
            })
        return base

    return html.div(
        {"style": {"padding": "20px", "fontFamily": "Arial", "maxWidth": "800px", "margin": "auto"}},
        html.h1("🎓 Sistema de Cursos Online"),
        html.div(
            {"style": {"marginBottom": "15px", "display": "flex", "gap": "10px", "flexWrap": "wrap"}},
            *[
                html.button(
                    {
                        "on_click": lambda _, v=view_key: set_current_view(v),
                        "style": button_style(current_view == view_key),
                        "aria-pressed": str(current_view == view_key).lower()
                    },
                    label
                )
                for view_key, label in [
                    ("inicio", "Inicio"),
                    ("agregar_usuario", "Agregar Usuario"),
                    ("agregar_curso", "Agregar Curso"),
                    ("agregar_notas", "Agregar Notas"),
                    ("ver_notas", "Notas"),
                ]
            ]
        ),
        html.hr(),
        render_view()
    )
