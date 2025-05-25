from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from reactpy.backend.fastapi import configure
import mysql.connector
from datetime import datetime
from mysql.connector import Error
from pydantic import BaseModel
import logging


# Importar el componente Menu desde su ubicación correcta
from components.menu import Menu

# Configuración básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelo para usuarios
class Usuario(BaseModel):
    nombre: str
    apellido: str
    email: str
    tipo_usuario: str
    contraseña: str

# Modelo para curso
class CursoModel(BaseModel):
    titulo: str
    descripcion: str
    fecha_inicio: str  # formato: YYYY-MM-DD
    fecha_fin: str
    id_usuario: int
    
# Modelo para lección
class LeccionModel(BaseModel):
    titulo: str
    contenido: str
    id_curso: int

# Modelo para inscripción
class InscripcionModel(BaseModel):
    id_usuario: int
    id_curso: int
    fecha_inscripcion: str  # formato: YYYY-MM-DD
    estado: str = 'activa'

# Agregar el modelo EvaluacionModel
class EvaluacionModel(BaseModel):
    tipo: str
    nota: int
    id_leccion: int
    id_usuario: int

# Configuración de FastAPI
app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a la base de datos
def get_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="Sistema_Cursos",
            autocommit=False
        )
    except Error as e:
        logger.error(f"Error de conexión: {e}")
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

# Endpoint para guardar usuarios
@app.post("/api/guardar-usuario")
async def guardar_usuario(usuario: Usuario):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Validaciones
        if usuario.tipo_usuario not in ["estudiante", "docente"]:
            raise HTTPException(status_code=400, detail="Tipo de usuario inválido")
        
        if len(usuario.contraseña) < 8:
            raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 8 caracteres")

        cursor.callproc("GuardarUsuario", [
            usuario.nombre,
            usuario.apellido,
            usuario.email,
            usuario.tipo_usuario,
            usuario.contraseña
        ])
        conn.commit()
        
        return {"success": True, "message": "Usuario registrado exitosamente"}
        
    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        if err.errno == 1062:  # Error de duplicado
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Guardar nuevo curso
@app.post("/api/guardar-curso")
async def guardar_curso(curso: CursoModel):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.callproc("GuardarCurso", [
            curso.titulo,
            curso.descripcion,
            curso.fecha_inicio,
            curso.fecha_fin,
            curso.id_usuario
        ])
        
        conn.commit()
        return {"success": True, "message": "✅ Curso registrado correctamente"}
    
    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        print(f"❌ Error al guardar curso: {err}")
        raise HTTPException(status_code=500, detail="Error en base de datos al guardar curso")
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Obtener cursos y sus lecciones
@app.get("/api/cursos-lecciones")
async def obtener_cursos_y_lecciones():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Curso")
        cursos = cursor.fetchall()

        resultado = []
        for curso in cursos:
            cursor.execute("SELECT * FROM Leccion WHERE id_curso = %s", (curso['id_curso'],))
            lecciones = cursor.fetchall()
            resultado.append({
                "curso": curso,
                "lecciones": lecciones
            })

        return resultado

    except Exception as e:
        print(f"❌ Error al obtener cursos/lecciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.post("/api/guardar-leccion")
async def guardar_leccion(leccion: LeccionModel):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Validar longitud del título
        if len(leccion.titulo) > 20:
            raise HTTPException(status_code=400, detail="El título no puede exceder 20 caracteres")

        cursor.callproc("GuardarLeccion", [
            leccion.titulo,
            leccion.contenido if leccion.contenido else "",
            leccion.id_curso
        ])
        conn.commit()
        return {"success": True, "message": "✅ Lección guardada"}

    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"❌ Error al guardar lección: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.post("/api/inscribir-alumno")
async def inscribir_alumno(inscripcion: InscripcionModel):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Validar estado
        if inscripcion.estado not in ['activa', 'inactiva']:
            raise HTTPException(status_code=400, detail="Estado de inscripción inválido")

        cursor.callproc("GuardarInscripcion", [
            inscripcion.id_usuario,
            inscripcion.id_curso,
            inscripcion.fecha_inscripcion,
            inscripcion.estado
        ])
        conn.commit()
        return {"success": True, "message": "✅ Alumno inscrito correctamente"}

    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"❌ Error al inscribir alumno: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Agregar este nuevo endpoint (junto con los otros endpoints)
@app.post("/api/guardar-evaluacion")
async def guardar_evaluacion(evaluacion: EvaluacionModel):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Evaluacion (tipo, nota, id_leccion, id_usuario) VALUES (%s, %s, %s, %s)",
            (evaluacion.tipo, evaluacion.nota, evaluacion.id_leccion, evaluacion.id_usuario)
        )
        conn.commit()
        return {"success": True, "message": "✅ Evaluación registrada"}
    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"❌ Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
# Obtener notas por alumno
@app.get("/api/notas-por-alumno")
async def notas_por_alumno(id_usuario: int = Query(..., description="ID del usuario")):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc("NotaPorAlumno", [id_usuario])

        for result in cursor.stored_results():
            notas = result.fetchall()

        return {"success": True, "data": notas}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"❌ Error al obtener notas del alumno: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Obtener notas por curso
@app.get("/api/notas-por-curso")
async def notas_por_curso(id_curso: int = Query(..., description="ID del curso")):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc("NotasPorCurso", [id_curso])

        for result in cursor.stored_results():
            notas = result.fetchall()

        return {"success": True, "data": notas}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"❌ Error al obtener notas por curso: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
# Configuración de ReactPy
configure(app, Menu)