import unittest
import sys
sys.path.append("C:/Users/ASUS/testCalculadora/Calculadora_Pensional-3")
from src.model.CodigoPension import *




class TestsCalculadoraPensional(unittest.TestCase):

    # Normales -> 7
    
    def setUp(self) -> None:
        self.calculadora = CalculadoraPensional()

    def test_normal_ahorro_pensional_empleado_promedio(self):
        resultado = self.calculadora.calculo_ahorro_pensional(edad=45, salario=2000000, semanas_laboradas=300, rentabilidad_fondo=0.06, tasa_administracion=0.02)
        resultado_esperado = 4233600.0
        self.assertAlmostEqual(resultado, resultado_esperado, places=2)
        print(f"El ahorro pensional esperado es: {round(resultado, 2)}")


    def test_normal_ahorro_pensional_empleado_cercano_jubilacion(self):
        resultado = self.calculadora.calculo_ahorro_pensional(edad=58, salario=3000000, semanas_laboradas=2080, rentabilidad_fondo=0.06,tasa_administracion=0.02)
        resultado_esperado = 44029440       
        self.assertAlmostEqual(resultado, resultado_esperado, places=10)
        print(f"El ahorro pensional esperado es: {resultado}")            

    def test_normal_ahorro_pensional_tasa_administracion_baja(self):
        resultado = self.calculadora.calculo_ahorro_pensional(edad=55, salario=2500000, semanas_laboradas=1825, rentabilidad_fondo=0.02,tasa_administracion=0.01)
        resultado_esperado = 10840500
        self.assertAlmostEqual(resultado, resultado_esperado, places=2)
        print(f"El ahorro pensional esperado es: {resultado}")

    def test_normal_ahorro_pensional_rentabilidad_baja(self):
        resultado = self.calculadora.calculo_ahorro_pensional(edad=45, salario=3000000, semanas_laboradas=1400, rentabilidad_fondo=0.01,tasa_administracion=0.02)
        resultado_esperado = 4939200
        self.assertAlmostEqual(resultado, resultado_esperado, places=2)
        print(f"El ahorro pensional esperado es: {resultado}")

    def test_normal_calculo_pension_normal(self):
        resultado = self.calculadora.calculo_pension(edad=35, ahorro_pensional_esperado=3000000, sexo='femenino', estado_civil='casado', esperanza_vida=85)
        resultado_esperado = 2289000.0
        self.assertAlmostEqual(resultado, resultado_esperado, places=2) 
        print(f"El calculo pensional esperado es: {resultado}")


    def test_normal_calculo_pension_empleado_nuevo(self):
        resultado = self.calculadora.calculo_pension(edad=25, ahorro_pensional_esperado = 700000,sexo='masculino', estado_civil='soltero',esperanza_vida=70)
        resultado_esperado = 412222.222
        self.assertAlmostEqual(resultado, resultado_esperado, places=2)
        print(f"El calculo pensional esperado es: {resultado}")

    def test_normal_calculo_pension_edad_esperanza_vida_baja(self):
        resultado = self.calculadora.calculo_pension(edad=25, ahorro_pensional_esperado = 500000,sexo='femenino', estado_civil='soltero',esperanza_vida=45)
        resultado_esperado = 668750.0
        self.assertAlmostEqual(resultado, resultado_esperado, places=2)
        print(f"El calculo pensional esperado es: {resultado}")


    # Excepcionales -> 7

    def test_excepcional_ahorro_pensional_edad_negativa(self):
        with self.assertRaises(EdadNegativa) as e:
            self.calculadora.calculo_ahorro_pensional(edad=-20, salario=1500000, semanas_laboradas=300, rentabilidad_fondo=0.05, tasa_administracion=0.02)
        print(str(e.exception))

    def test_excepcional_ahorro_pensional_semanas_laboradas_negativas(self):
        with self.assertRaises(SemanasLaboradasNegativas) as e:
            self.calculadora.calculo_ahorro_pensional(edad=30, salario=2300000, semanas_laboradas=-200, rentabilidad_fondo=0.04,tasa_administracion=0.02)
        print(str(e.exception))

    def test_excepcional_calculo_pension_edad_mayor_esperanza_vida(self):
        with self.assertRaises(EdadMayorAEsperanzaDeVida) as e:
            self.calculadora.calculo_pension(edad=45, ahorro_pensional_esperado=900000, sexo='masculino',estado_civil='soltero', esperanza_vida=40)
        print(str(e.exception))

    def test_excepcional_ahorro_pensional_salario_negativo(self):
        with self.assertRaises(SalarioNegativo) as e:
            self.calculadora.calculo_ahorro_pensional(edad=45, salario=0, semanas_laboradas=170, rentabilidad_fondo=0.06,tasa_administracion=0.02)
        print(str(e.exception))

    def test_excepcional_calculo_pension_edad_negativa(self):
        with self.assertRaises(EdadNegativa) as e:
            self.calculadora.calculo_pension(edad=-45, ahorro_pensional_esperado=5000000, sexo='masculino',estado_civil='soltero', esperanza_vida=80)
        print(str(e.exception))

    def test_excepcional_calculo_pension_edad_muy_alta(self):
        with self.assertRaises(EdadMayorA90) as e:
            self.calculadora.calculo_pension(edad=91, ahorro_pensional_esperado=1200000, sexo='masculino',estado_civil='soltero', esperanza_vida=100)
        print(str(e.exception))


    def test_excepcional_calculo_pension_esperanza_vida_negativa(self):
        with self.assertRaises(EsperanzaVidaNegativa) as e:
            self.calculadora.calculo_pension(edad=50, ahorro_pensional_esperado=2000000, sexo='masculino',estado_civil='soltero', esperanza_vida=-67)
        print(str(e.exception))


        # Errores -> 7

    def test_ahorro_pensional_semanas_laboradas_tipo_incorrecto(self):
        with self.assertRaises(SemanasLaboradasTipoIncorrecto) as e:
            self.calculadora.calculo_ahorro_pensional(edad=45, salario=3000000, semanas_laboradas="10", rentabilidad_fondo=0.03, tasa_administracion=0.02)
        print(str(e.exception))

    def test_ahorro_pensional_salario_tipo_incorrecto(self):
        with self.assertRaises(SalarioNoNumerico) as e:
            self.calculadora.calculo_ahorro_pensional(edad=40, salario="400000", semanas_laboradas=90, rentabilidad_fondo=0.04,tasa_administracion=0.02)
        print(str(e.exception))


    def test_calculo_pensional_edad__tipo_incorrecto(self):
        with self.assertRaises(EdadTipoIncorrecto) as e:
            self.calculadora.calculo_pension(edad="30", ahorro_pensional_esperado=250000, sexo='femenino',estado_civil='soltero', esperanza_vida='70')
        print(str(e.exception))

    def test_calculo_pension_esperanza_vida_tipo_incorrecto(self):
        with self.assertRaises(EsperanzaVidaTipoIncorrecto) as e:
            self.calculadora.calculo_pension(edad=45, ahorro_pensional_esperado=2500000, sexo='masculino',estado_civil='soltero', esperanza_vida='80')
        print(str(e.exception))

    def test_calculo_pension_ahorro_pensional_tipo_incorrecto(self):
        with self.assertRaises(AhorroPensionalTipoIncorrecto) as e:
            self.calculadora.calculo_pension(edad=45, ahorro_pensional_esperado='4200000', sexo='masculino',estado_civil='soltero', esperanza_vida=80)
        print(str(e.exception))

    def test_calculo_pension_sexo_tipo_incorrecto(self):
        with self.assertRaises(SexoTipoIncorrecto) as e:
            self.calculadora.calculo_pension(edad=45, ahorro_pensional_esperado=1200000, sexo=2,estado_civil='soltero', esperanza_vida=80)
        print(str(e.exception))

    def test_calculo_pension_estado_civil_tipo_incorrecto(self):
        with self.assertRaises(EstadoCivilTipoIncorrecto) as e:
            self.calculadora.calculo_pension(edad=35, ahorro_pensional_esperado=700000, sexo='femenino',estado_civil=3, esperanza_vida=70)
        print(str(e.exception))


if __name__ == '__main__':
    unittest.main()
