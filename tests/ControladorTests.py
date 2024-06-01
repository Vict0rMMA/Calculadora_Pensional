import sys
sys.path.append("C:/Users/ASUS/testCalculadora/Calculadora_Pensional-3")
import unittest
from src.model.User import Usuario

from src.controller.app_controller import ControladorUsuarios
from src.model.CodigoPension import *
from decimal import Decimal


class ControladorUsuariosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controlador = ControladorUsuarios()
        cls.controlador.crear_tablas()

    def setUp(self):
        self.controlador.EliminarTodosUsuarios()

    def test_insertar_usuario(self):
        usuario = Usuario("Juan", "Pérez", "Masculino", 30)
        self.controlador.InsertarUsuario(usuario)
        usuarios = self.controlador.ObtenerUsuarios()
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].nombre, "Juan")
        self.assertEqual(usuarios[0].apellido, "Pérez")
        self.assertEqual(usuarios[0].sexo, "Masculino")
        self.assertEqual(usuarios[0].edad, 30)

        usuario2 = Usuario("María", "González", "Femenino", 25)
        self.controlador.InsertarUsuario(usuario2)
        usuarios = self.controlador.ObtenerUsuarios()
        self.assertEqual(len(usuarios), 2)

    def test_insertar_usuario_error(self):
        usuario_invalido = Usuario("", "Pérez", "Masculino", 30)
        with self.assertRaises(ValueError):
            self.controlador.InsertarUsuario(usuario_invalido)

        usuario_invalido = Usuario("Juan", "Pérez", "Masculino", -10)
        with self.assertRaises(ValueError):
            self.controlador.InsertarUsuario(usuario_invalido)        


    def test_modificar_usuario(self):
        usuario = Usuario("Juan", "Pérez", "Masculino", 30)
        self.controlador.InsertarUsuario(usuario)
        usuario_id = self.controlador.ObtenerUsuarios()[0].id
        self.controlador.ModificarUsuario(usuario_id, "Juan", "Gómez", "Masculino", 35)
        usuario_modificado = self.controlador.ObtenerUsuarioPorID(usuario_id)
        self.assertEqual(usuario_modificado.nombre, "Juan")
        self.assertEqual(usuario_modificado.apellido, "Gómez")
        self.assertEqual(usuario_modificado.sexo, "Masculino")
        self.assertEqual(usuario_modificado.edad, 35)

        self.assertRaises(ValueError, self.controlador.ModificarUsuario, 999, "Juan", "Gómez", "Masculino", 35)

    def test_modificar_usuario_error(self):

        self.assertRaises(ValueError, self.controlador.ModificarUsuario, 999, "Juan", "Gómez", "Masculino", 35)
        usuario = Usuario("Juan", "Pérez", "Masculino", 30)
        self.controlador.InsertarUsuario(usuario)
        usuario_id = self.controlador.ObtenerUsuarios()[0].id
        with self.assertRaises(ValueError):
            self.controlador.ModificarUsuario(usuario_id, "", "Gómez", "Masculino", 35)

    def test_eliminar_usuario(self):
        usuario = Usuario("Juan", "Pérez", "Masculino", 30)
        self.controlador.InsertarUsuario(usuario)
        usuario_id = self.controlador.ObtenerUsuarios()[0].id
        self.controlador.EliminarUsuario(usuario_id)
        usuarios = self.controlador.ObtenerUsuarios()
        self.assertEqual(len(usuarios), 0)

        self.assertRaises(ValueError, self.controlador.EliminarUsuario, 999)

    def test_eliminar_usuario_error(self):
        self.assertRaises(ValueError, self.controlador.EliminarUsuario, 999)        

    def test_listar_usuarios(self):
        usuario1 = Usuario("Juan", "Pérez", "Masculino", 30)
        usuario2 = Usuario("María", "González", "Femenino", 25)
        self.controlador.InsertarUsuario(usuario1)
        self.controlador.InsertarUsuario(usuario2)
        usuarios = self.controlador.ObtenerUsuarios()
        self.assertEqual(len(usuarios), 2)
        self.assertIn(usuario1, usuarios)
        self.assertIn(usuario2, usuarios)

        self.controlador.EliminarTodosUsuarios()
        usuarios = self.controlador.ObtenerUsuarios()
        self.assertEqual(len(usuarios), 0)

    def test_listar_usuarios_error(self):
        usuarios = self.controlador.ObtenerUsuarios()
        self.assertEqual(len(usuarios), 0)
        with self.assertRaises(ValueError):
            self.controlador.ObtenerUsuarioPorID(999)        

    def test_realizar_calculo(self):
        usuario = Usuario("Juan", "Pérez", "masculino", 30)
        self.controlador.InsertarUsuario(usuario)
        usuario_id = self.controlador.ObtenerUsuarios()[0].id
        calculadora = CalculadoraPensional()
        ahorro_pensional = calculadora.calculo_ahorro_pensional(30, 2000, 52, 0.08, 0.02)
        self.controlador.InsertarResultadoCalculo(usuario_id, "Ahorro Pensional", ahorro_pensional)
        pension_esperada = calculadora.calculo_pension(30, ahorro_pensional, "masculino", "soltero", 75)
        self.controlador.InsertarResultadoCalculo(usuario_id, "Pensión Esperada", pension_esperada)
        historial = self.controlador.ObtenerHistorialCalculos()
        historial_simplificado = [(Decimal(str(hist[4])), hist[3], hist[1]) for hist in historial]
        self.assertIn((Decimal(str(ahorro_pensional)), "Ahorro Pensional", usuario_id), historial_simplificado)
        self.assertIn((Decimal(str(pension_esperada)), "Pensión Esperada", usuario_id), historial_simplificado)

    def test_realizar_calculo_error(self):
        usuario = Usuario("Juan", "Pérez", "masculino", 30)
        self.controlador.InsertarUsuario(usuario)
        usuario_id = self.controlador.ObtenerUsuarios()[0].id
        calculadora = CalculadoraPensional()

        # Prueba con un salario inválido
        with self.assertRaises(SalarioNegativo):
            ahorro_pensional = calculadora.calculo_ahorro_pensional(30, -100, 52, 0.08, 0.02)
            self.controlador.InsertarResultadoCalculo(usuario_id, "Ahorro Pensional", ahorro_pensional)

        # Prueba con una rentabilidad de fondo inválida
        with self.assertRaises(RentabilidadFondoInvalida):
            ahorro_pensional = calculadora.calculo_ahorro_pensional(30, 2000, 52, 1.2, 0.02)
            self.controlador.InsertarResultadoCalculo(usuario_id, "Ahorro Pensional", ahorro_pensional)

    def test_ver_historial_calculos(self):
        usuario = Usuario("Juan", "Pérez", "Masculino", 30)
        self.controlador.InsertarUsuario(usuario)
        usuario_id = self.controlador.ObtenerUsuarios()[0].id
        self.controlador.InsertarResultadoCalculo(usuario_id, "Ahorro Pensional", 1000.0)
        self.controlador.InsertarResultadoCalculo(usuario_id, "Pensión Esperada", 2000.0)
        historial = self.controlador.ObtenerHistorialCalculos()
        self.assertEqual(len(historial), 2)
        historial_simplificado = [(hist[4], hist[3], hist[1]) for hist in historial]
        self.assertIn((1000.0, "Ahorro Pensional", usuario_id), historial_simplificado)
        self.assertIn((2000.0, "Pensión Esperada", usuario_id), historial_simplificado)

        self.controlador.EliminarTodosUsuarios()
        historial = self.controlador.ObtenerHistorialCalculos()
        self.assertEqual(len(historial), 0)

    def test_ver_historial_calculos_error(self):
        with self.assertRaises(ValueError):
            self.controlador.ObtenerResultadosCalculo(999)

        
if __name__ == '__main__':
    unittest.main()