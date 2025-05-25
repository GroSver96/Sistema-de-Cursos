from reactpy import component, html

@component
def Home():
    return html.div(
        {"style": {"padding": "20px", "fontFamily": "Arial"}},
        html.h1("Sistema de Cursos Online"),
        html.p("Bienvenido al sistema. Elige una opción del menú.")
    )
