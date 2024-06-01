import sys
sys.path.append(".")
sys.path.append("../Calculadora_Pensional")
from src.model.CodigoPension import *

def main():
    calculadora = CalculadoraPensional()

    print("Bienvenido a la calculadora pensional")

    while True:
        print("\nSeleccione una opción: ")
        print("1. Calcular ahorro pensional. ")
        print("2. Calcular pensión. ")
        print("3. Salir")

        opcion = input("Ingrese el número de la opción que desea: ")

        if opcion == "1":
            edad = int(input("Ingrese su edad (1-90): "))
            salario = float(input("Ingrese su salario mensual: "))
            semanas_laboradas = int(input("Ingrese el número de semanas laboradas: "))
            rentabilidad_fondo = float(input("Ingrese la rentabilidad del fondo (Como decimal (0.04)): "))
            tasa_administracion = float(input("Ingrese la tasa de administración (Como decimal (0.02)): "))

            ahorro_pensional = calculadora.calculo_ahorro_pensional(edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion)
            print(f"El ahorro pensional esperado es: {ahorro_pensional}")

        elif opcion == "2":
            edad = int(input("Ingrese su edad (1-90): "))
            ahorro_pensional_esperado = float(input("Ingrese el ahorro pensional esperado: "))         
            esperanza_vida = int(input("Ingrese su esperanza de vida: "))   
            sexo = input("Ingrese su sexo ('masculino' o 'femenino'): ")
            estado_civil = input("Ingrese su estado civil ('soltero' o 'casado'): ") 

            pension = calculadora.calculo_pension(edad, ahorro_pensional_esperado, sexo, estado_civil, esperanza_vida)
            print(f"La pensión esperada es: {pension}")

        elif opcion == "3":
            print("Gracias por usar la calculadora pensional!")
            break

        else:
            print("Opción no válida, seleccione una opción válida. ")    


if __name__ == "__main__":
    main()
