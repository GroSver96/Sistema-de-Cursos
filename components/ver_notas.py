from reactpy import component, html

@component
def VerNotas():
    return html.div(
        html.h2("Ver Notas"),
        html.ul(
            html.li("🧑‍🎓 Ver nota de alumno"),
            html.li("📚 Ver nota por curso")
        )
    )
