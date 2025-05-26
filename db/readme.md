# Sistema de Cursos Online 🎓

Aplicación full-stack para gestión de cursos, alumnos, lecciones y evaluaciones, construida con:
- **Backend**: FastAPI + MySQL
- **Frontend**: ReactPy (React-like en Python)

## 🚀 Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd sistema-cursos
Configurar entorno virtual (recomendado):

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Instalar dependencias:

bash
pip install -r requirements.txt

Configurar MySQL:

Importar la base de datos desde sistema_cursos.sql (usando Navicat o MySQL Workbench).

Asegurar que las credenciales en conexion.py coincidan con tu instalación.

Ejecutar la aplicación:

bash
uvicorn app:app --reload




##Notas adicionales:##
Para MySQL: Asegúrate de que el servicio de MySQL esté corriendo y que las credenciales en conexion.py sean correctas.

Variables de entorno: Si quieres usar .env para credenciales, agrega python-dotenv al requirements.txt y crea un archivo .env con:

env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=********
DB_NAME=sistema_cursos

Ejecución: El comando uvicorn app:app --reload habilita el modo desarrollo con recarga automática.