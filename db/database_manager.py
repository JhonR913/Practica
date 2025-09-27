
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

class DatabaseManager:
    def __init__(self):
        """Inicializa el gestor de base de datos con la configuración del .env"""
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'port': int(os.getenv('DB_PORT', 3306))
        }
        self.connection = None

    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.db_config)
                print("Conexión a la base de datos establecida")
            return self.connection
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def close(self):
        """Cierra la conexión con la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a la base de datos cerrada")
            self.connection = None

    def get_camera_info(self, rtsp_url):
        """
        Obtiene la información de la cámara por su URL RTSP
        
        Args:
            rtsp_url (str): URL RTSP de la cámara
            
        Returns:
            dict: Información de la cámara o None si no se encuentra
        """
        try:
            conn = self.connect()
            if not conn:
                return None
                
            cursor = conn.cursor(dictionary=True)
            
            # Buscar la cámara por URL RTSP
            query = "SELECT id, ip, latitud, longitud FROM camaras WHERE url_rtsp = %s"
            cursor.execute(query, (rtsp_url,))
            camera = cursor.fetchone()
            cursor.close()
            
            return camera
        except Error as e:
            print(f"Error al obtener información de la cámara: {e}")
            return None

    def register_accident(self, camera_id, video_path, latitude=None, longitude=None, description=None):
        """
        Registra un accidente en la base de datos
        
        Args:
            camera_id (int): ID de la cámara
            video_path (str): Ruta del archivo de video
            latitude (float, optional): Latitud si es diferente a la de la cámara
            longitude (float, optional): Longitud si es diferente a la de la cámara
            description (str, optional): Descripción del accidente
            
        Returns:
            int: ID del accidente registrado o None si hay error
        """
        try:
            conn = self.connect()
            if not conn:
                return None
                
            cursor = conn.cursor()
            
            # Si no se proporcionan lat/long, obtenemos las de la cámara
            if latitude is None or longitude is None:
                camera_query = "SELECT latitud, longitud FROM camaras WHERE id = %s"
                cursor.execute(camera_query, (camera_id,))
                camera_info = cursor.fetchone()
                
                if camera_info:
                    latitude = latitude or camera_info[0]
                    longitude = longitude or camera_info[1]
            
            # Insertar registro de accidente
            query = """
            INSERT INTO accidentes 
            (id_camara, ruta_archivo, latitud, longitud, descripcion)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                camera_id, 
                video_path, 
                latitude, 
                longitude, 
                description or "Accidente detectado automáticamente"
            ))
            
            conn.commit()
            accident_id = cursor.lastrowid
            cursor.close()
            
            print(f"Accidente registrado con ID: {accident_id}")
            return accident_id
            
        except Error as e:
            print(f"Error al registrar accidente: {e}")
            if conn:
                conn.rollback()
            return None

# Instancia global del gestor de base de datos
db_manager = DatabaseManager()