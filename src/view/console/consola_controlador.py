import sys
sys.path.append(".")
sys.path.append("../Calculadora_Pensional")
import datetime
from src.model.User import Usuario
from src.controller.app_controller import ControladorUsuarios
from src.model.CodigoPension import *


def get_int_input(prompt):
    """Obtiene un valor entero válido del usuario"""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Error: Ingrese un número entero válido.")


def get_float_input(prompt):
    """Obtiene un valor flotante válido del usuario"""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Error: Ingrese un número válido.")


def format_number_with_dots(number):
    """Formatea el número agregando puntos para facilitar la lectura"""
    return "{:,.2f}".format(number)


def validate_nombre(nombre):
    if not nombre:
        raise ValueError("El nombre no puede estar vacío")
    if not nombre.isalpha():
        raise ValueError("El nombre solo puede contener letras.")


def validate_apellido(apellido):
    if not apellido:
        raise ValueError("El apellido no puede estar vacío")
    if not apellido.isalpha():
        raise ValueError("El apellido solo puede contener letras.")


def validate_sexo(sexo):
    if sexo.lower() not in ['masculino', 'femenino']:
        raise ValueError("El sexo debe ser 'masculino' o 'femenino'")

def validate_edad(edad):
    """Valida que la edad sea un entero positivo."""
    try:
        edad = int(edad)
        if edad <= 0:
            raise ValueError("La edad debe ser un entero positivo.")
    except ValueError:
        raise ValueError("La edad debe ser un entero positivo.")    

def print_user_list(usuarios):
    """Imprime la lista de usuarios con sus identificadores"""
    print("Usuarios disponibles:")
    for usuario in usuarios:
        print(f"ID: {usuario.id}, Nombre: {usuario.nombre}, Apellido: {usuario.apellido}, Sexo: {usuario.sexo}")


def select_user(controlador_usuarios):
    """Permite al usuario seleccionar un usuario de la lista"""
    usuarios = controlador_usuarios.ObtenerUsuarios()
    print_user_list(usuarios)
    while True:
        id_usuario = get_int_input("Ingrese el ID del usuario para realizar el cálculo: ")
        if any(usuario.id == id_usuario for usuario in usuarios):
            return id_usuario
        else:
            print("ID de usuario inválido. Intente nuevamente.")


def select_calculation_type():
    """Permite al usuario seleccionar el tipo de cálculo"""
    while True:
        print("Tipos de cálculo disponibles:")
        print("1. Ahorro pensional")
        print("2. Cálculo de pensión")
        opcion = input("Seleccione el tipo de cálculo que desea realizar: ")
        if opcion in ["1", "2"]:
            return opcion
        else:
            print("Opción inválida. Intente nuevamente.")

def show_calculation_history(controlador_usuarios):
    """Muestra el historial de cálculos"""
    historial = controlador_usuarios.ObtenerHistorialCalculos()
    if not historial:
        print("No hay registros de cálculos.")
    else:
        print("Historial de cálculos:")
        for registro in historial:
            print(f"ID: {registro[0]}, ID Usuario: {registro[1]}, Tipo de Cálculo: {registro[3]}, Resultado: {registro[4]}, Fecha: {registro[5]}")
            

def register_user(controlador_usuarios):
    """Registra un nuevo usuario"""
    nombre = input("Ingrese el nombre: ")
    apellido = input("Ingrese el apellido: ")
    sexo = input("Ingrese el sexo ('masculino' o 'femenino'): ")
    edad = get_int_input("Ingrese la edad: ")

    try:
        validate_nombre(nombre)
        validate_apellido(apellido)
        validate_sexo(sexo)
        validate_edad(edad)

    except ValueError as e:
        print(f"Error al registrar usuario: {e}")
        return

    usuario = Usuario(nombre, apellido, sexo, edad)
    controlador_usuarios.InsertarUsuario(usuario)
    print("Usuario registrado correctamente.")


def main():
    controlador_usuarios = ControladorUsuarios()
    controlador_usuarios.crear_tablas()

    while True:
        print("\nMenú principal:")
        print("1. Registrar nuevo usuario")
        print("2. Modificar usuario existente")
        print("3. Eliminar usuario")
        print("4. Listar usuarios")
        print("5. Realizar cálculo")
        print("6. Ver historial de cálculos")
        print("7. Salir")

        opcion = get_int_input("Ingrese una opción: ")

        if opcion == 1:
            register_user(controlador_usuarios)

        elif opcion == 2:
            # Modificar usuario existente
            usuarios = controlador_usuarios.ObtenerUsuarios()
            if not usuarios:
                print("No hay usuarios registrados.")
            else:
                print_user_list(usuarios)
                id_usuario = get_int_input("Ingrese el ID del usuario a modificar: ")

                try:
                    usuario = controlador_usuarios.ObtenerUsuarioPorID(id_usuario)
                    if usuario:
                        nombre = input("Ingrese el nuevo nombre: ")
                        apellido = input("Ingrese el nuevo apellido: ")
                        sexo = input("Ingrese el nuevo sexo ('masculino' o 'femenino'): ")
                        edad = get_int_input("Ingrese la nueva edad: ")

                        # Validar los nuevos valores antes de modificar el usuario
                        try:
                            validate_nombre(nombre)
                            validate_apellido(apellido)
                            validate_sexo(sexo)
                            validate_edad(edad)

                        except ValueError as e:
                            print(f"Error al modificar usuario: {e}")
                            continue

                        # Modificar el usuario con los nuevos valores
                        controlador_usuarios.ModificarUsuario(id_usuario, nombre, apellido, sexo, edad)
                        print("Usuario modificado correctamente.")
                    else:
                        print("El usuario con el ID especificado no existe.")
                except ValueError as e:
                    print(f"Error: {e}")


        elif opcion == 3:
            # Eliminar usuario
            usuarios = controlador_usuarios.ObtenerUsuarios()
            if not usuarios:
                print("No hay usuarios registrados.")
            else:
                print_user_list(usuarios)
                id_usuario = get_int_input("Ingrese el ID del usuario a eliminar: ")

                try:
                    if controlador_usuarios.ObtenerUsuarioPorID(id_usuario):
                        controlador_usuarios.EliminarUsuario(id_usuario)
                        print("Usuario eliminado correctamente.")
                    else:
                        print("Usuario inexistente")
                except ValueError as e:
                    print(f"Error: {e}")

        elif opcion == 4:
            # Listar usuarios
            usuarios = controlador_usuarios.ObtenerUsuarios()
            if not usuarios:
                print("No hay usuarios registrados.")
            else:
                print_user_list(usuarios)

        elif opcion == 5:
            # Listar usuarios antes de realizar el cálculo
            usuarios = controlador_usuarios.ObtenerUsuarios()
            if not usuarios:
                print("No hay usuarios registrados.")
            else:
                print_user_list(usuarios)
                id_usuario = get_int_input("Ingrese el ID del usuario para realizar el cálculo: ")
                usuario = controlador_usuarios.ObtenerUsuarioPorID(id_usuario)
                if usuario:
                    tipo_calculo = select_calculation_type()
                    if tipo_calculo == "1":
                        # Ahorro pensional
                        salario = get_float_input("Ingrese el salario: ")
                        semanas_laboradas = get_float_input("Ingrese las semanas laboradas: ")
                        rentabilidad_fondo = get_float_input("Ingrese la rentabilidad del fondo (Como decimal (0.04)): ")
                        tasa_administracion = get_float_input("Ingrese la tasa de administración (Como decimal (0.02)): ")
                        try:
                            ahorro_pensional = CalculadoraPensional().calculo_ahorro_pensional(usuario.edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion)
                            print(f"El ahorro pensional esperado es: {format_number_with_dots(ahorro_pensional)}")

                            # Insertar el resultado del cálculo en la base de datos
                            controlador_usuarios.InsertarResultadoCalculo(id_usuario, "ahorro_pensional", ahorro_pensional)
                            print(f"Ahorro agregado al historial. ")    
                        except Exception as e:
                            print(f"Error: {e}")
                

                    elif tipo_calculo == "2":
                        # Cálculo de pensión
                        try:
                            ahorro_pensional_esperado = get_float_input("Ingrese el ahorro pensional esperado: ")
                            esperanza_vida = get_float_input("Ingrese su esperanza de vida: ")
                            estado_civil = input("Ingrese su estado civil ('soltero' o 'casado'): ")
                            pension = CalculadoraPensional().calculo_pension(usuario.edad, ahorro_pensional_esperado, usuario.sexo, estado_civil, esperanza_vida)
                            print(f"La pensión esperada es: {format_number_with_dots(pension)}")
                            print(f"Pension agregada al historial. ")    

                            # Insertar el resultado del cálculo en la base de datos
                            controlador_usuarios.InsertarResultadoCalculo(id_usuario, "calculo_pension", pension)

                        except Exception as e:
                            print(f"Error: {e}")

                else:
                    print("Usuario inexistente")
        elif opcion == 6:
            show_calculation_history(controlador_usuarios)    

        elif opcion == 7:
            # Salir
            print("Gracias por usar la calculadora pensional!")
            break

        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == '__main__':
    main()
