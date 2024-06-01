import sys
sys.path.append("C:/Users/ASUS/testCalculadora/Calculadora_Pensional-3")
import psycopg2
from src.model.User import Usuario
import secret_config

class ControladorUsuarios:

    def crear_tablas(self):
        with self.ObtenerCursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                              id SERIAL PRIMARY KEY,
                              nombre TEXT NOT NULL,
                              apellido TEXT NOT NULL,
                              sexo TEXT NOT NULL,                              
                              edad INTEGER NOT NULL
                            );""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS resultados_calculos (
                              id SERIAL PRIMARY KEY,
                              id_usuario INTEGER REFERENCES usuarios(id),
                              nombre_usuario TEXT NOT NULL,
                              tipo_calculo TEXT NOT NULL,
                              resultado NUMERIC NOT NULL,
                              fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );""")
            cursor.connection.commit()

    def ObtenerCursor(self):
        connection = psycopg2.connect(database=secret_config.PGDATABASE, 
                                      user=secret_config.PGUSER, 
                                      password=secret_config.PGPASSWORD, 
                                      host=secret_config.PGHOST, 
                                      port=secret_config.PGPORT,
                                      options=f"endpoint=ep-polished-bread-a5xqec93")
        return connection.cursor()
    
    def InsertarUsuario(self, usuario):
        from src.view.console.consola_controlador import validate_nombre, validate_apellido, validate_sexo, validate_edad        
        try:
            validate_nombre(usuario.nombre)
            validate_apellido(usuario.apellido)
            validate_sexo(usuario.sexo)
            validate_edad(usuario.edad)
        except ValueError as e:
            raise ValueError(f"Error al insertar usuario: {e}")

        # Si todas las validaciones pasan, procedemos con la inserción del usuario
        with self.ObtenerCursor() as cursor:
            cursor.execute("""INSERT INTO usuarios (nombre, apellido, sexo, edad)
                              VALUES (%s, %s, %s, %s)""", (usuario.nombre, usuario.apellido, usuario.sexo, usuario.edad))
            cursor.connection.commit()

    def InsertarResultadoCalculo(self, id_usuario, tipo_calculo, resultado):
        # Obtener el nombre del usuario
        usuario = self.ObtenerUsuarioPorID(id_usuario)
        nombre_usuario = f"{usuario.nombre} {usuario.apellido}"

        # Insertar el resultado del cálculo en la base de datos
        with self.ObtenerCursor() as cursor:
            cursor.execute("""INSERT INTO resultados_calculos (id_usuario, nombre_usuario, tipo_calculo, resultado)
                            VALUES (%s, %s, %s, %s)""", (id_usuario, nombre_usuario, tipo_calculo, resultado))
            cursor.connection.commit()


    def ObtenerResultadosCalculo(self, id_usuario):
        try:
            usuario = self.ObtenerUsuarioPorID(id_usuario)
            if usuario:
                with self.ObtenerCursor() as cursor:
                    cursor.execute("""SELECT nombre_usuario, tipo_calculo, resultado, fecha
                                    FROM resultados_calculos
                                    WHERE id_usuario = %s""", (id_usuario,))
                    return cursor.fetchall()
            else:
                raise ValueError("El usuario con el ID especificado no existe.")
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError("Error al obtener los resultados de cálculo:", e)
        
    def EliminarTodosUsuarios(self):
        try:
            with self.ObtenerCursor() as cursor:
                # Eliminar todos los resultados de cálculos asociados a los usuarios
                cursor.execute("DELETE FROM resultados_calculos WHERE id_usuario IN (SELECT id FROM usuarios)")
                # Eliminar todos los usuarios
                cursor.execute("DELETE FROM usuarios")
                cursor.connection.commit()
        except Exception as e:
            # Manejar cualquier error que ocurra durante el proceso
            print("Error al eliminar todos los usuarios:", e)


    def ObtenerUsuarios(self):
        with self.ObtenerCursor() as cursor:
            cursor.execute("SELECT * FROM usuarios")
            usuarios = []
            for row in cursor.fetchall():
                usuario = Usuario(row[1], row[2], row[3], row[4])
                usuario.id = row[0]
                usuarios.append(usuario)
            return usuarios           

    def ObtenerHistorialCalculos(self):
        with self.ObtenerCursor() as cursor:
            cursor.execute("SELECT * FROM resultados_calculos")
            historial = []
            for row in cursor.fetchall():
                historial.append(row)
            return historial

    
    def ObtenerUsuarioPorID(self, id_usuario):
        with self.ObtenerCursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
            row = cursor.fetchone()
            if row:
                usuario = Usuario(row[1], row[2], row[3], row[4])
                usuario.id = row[0]
                return usuario
            else:
                raise ValueError("El usuario con el ID especificado no existe.")


    def ModificarUsuario(self, id_usuario, nombre, apellido, sexo, edad):
        from src.view.console.consola_controlador import validate_nombre, validate_apellido, validate_sexo, validate_edad

        # Verificar si el usuario con el ID especificado existe
        usuario_existente = self.ObtenerUsuarioPorID(id_usuario)
        if usuario_existente is None:
            raise ValueError("El usuario con el ID especificado no existe.")

        try:
            validate_nombre(nombre)
            validate_apellido(apellido)
            validate_sexo(sexo)
            validate_edad(edad)
        except ValueError as e:
            raise ValueError(f"Error al modificar usuario: {e}")

        with self.ObtenerCursor() as cursor:
            cursor.execute("""UPDATE usuarios
                            SET nombre = %s, apellido = %s, sexo = %s, edad = %s
                            WHERE id = %s""", (nombre, apellido, sexo, edad, id_usuario))
            cursor.connection.commit()

    def EliminarUsuario(self, id_usuario):
        with self.ObtenerCursor() as cursor:
            # Verificar si el usuario existe
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id = %s", (id_usuario,))
            existe_usuario = cursor.fetchone()[0] > 0

            if existe_usuario:
                # Eliminar el usuario si existe
                cursor.execute("""DELETE FROM resultados_calculos WHERE id_usuario = %s""", (id_usuario,))
                cursor.execute("""DELETE FROM usuarios WHERE id = %s""", (id_usuario,))
                cursor.connection.commit()
            else:
                # Lanzar una ValueError si el usuario no existe
                raise ValueError("El usuario con el ID especificado no existe.")


controlador_usuarios = ControladorUsuarios()
controlador_usuarios.crear_tablas()
