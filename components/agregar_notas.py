from reactpy import component, html

@component
def AgregarNotas():
    return html.div(
        html.h2("Agregar Notas"),
        html.p("Aquí irá el formulario para ingresar las notas.")
    )
