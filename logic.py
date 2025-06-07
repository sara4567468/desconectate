import sqlite3
from datetime import datetime

def conectar_bd():
    try:
        conn = sqlite3.connect("uso_redes.db")
        return conn
    except sqlite3.Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

def inicializar_bd():
    conn = conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS registros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    minutos INTEGER NOT NULL
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al crear tabla: {e}")
        finally:
            conn.close()

def registrar_uso(minutos):
    conn = conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            fecha = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO registros (fecha, minutos) VALUES (?, ?)", (fecha, minutos))
            conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al insertar datos: {e}")
        finally:
            conn.close()

async def obtener_mensaje_reactivo(minutos):
    if minutos > 180:
        return "⚠️ Estás usando demasiado tiempo en redes. Considera desconectarte."
    elif minutos > 60:
        return "⏳ Cuidado, ya llevas más de una hora. Toma un descanso."
    else:
        return "✅ Buen trabajo, tu uso está dentro de lo saludable."
