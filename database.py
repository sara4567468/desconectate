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

def insertar_uso(minutos):
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

def obtener_historial():
    conn = conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT fecha, minutos FROM registros ORDER BY fecha DESC")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"❌ Error al obtener datos: {e}")
            return []
        finally:
            conn.close()
