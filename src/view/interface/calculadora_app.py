import sys

sys.path.append(".")
sys.path.append("../Calculadora_Pensional")
from model.User import Usuario
from controller.app_controller import ControladorUsuarios
from src.model.CodigoPension import CalculadoraPensional
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window


class InterfazCalculadora(GridLayout):
    def __init__(self, **kwargs):
        super(InterfazCalculadora, self).__init__(**kwargs)
        self.cols = 1
        self.calculadora = CalculadoraPensional()
        self.estado_calculo = 'ahorro'
        self.controlador_usuarios = ControladorUsuarios()
        self.controlador_usuarios.crear_tablas()
        
        self.add_widget(Label(text='Bienvenido a la calculadora pensional'))
        
        self.botones = GridLayout(cols=3)
        
        self.boton_calcular_ahorro = Button(text='Calcular ahorro pensional')
        self.boton_calcular_ahorro.bind(on_press=self.calcular_ahorro_pensional)
        
        self.boton_calcular_pension = Button(text='Calcular pensión')
        self.boton_calcular_pension.bind(on_press=self.calcular_pension)
        
        self.boton_salir = Button(text='Salir')
        self.boton_salir.bind(on_press=self.salir)
        
        self.botones.add_widget(self.boton_calcular_ahorro)
        self.botones.add_widget(self.boton_calcular_pension)
        self.botones.add_widget(self.boton_salir)
        
        self.add_widget(self.botones)
        
        # Campos de texto para la entrada de datos
        self.edad_input = TextInput(multiline=False, hint_text='Edad (1-90)')
        self.salario_input = TextInput(multiline=False, hint_text='Salario mensual')
        self.semanas_input = TextInput(multiline=False, hint_text='Número de semanas laboradas')
        self.rentabilidad_input = TextInput(multiline=False, hint_text='Rentabilidad del fondo (Como decimal: 0.03)')
        self.tasa_input = TextInput(multiline=False, hint_text='Tasa de administración (Como decimal 0.02)')
        self.add_widget(self.edad_input)
        self.add_widget(self.salario_input)
        self.add_widget(self.semanas_input)
        self.add_widget(self.rentabilidad_input)
        self.add_widget(self.tasa_input)

        # Etiqueta para mostrar el resultado o el error
        self.resultado_o_error_label = Label(text='', color=(1, 0, 0, 1))  # Color rojo para los mensajes de error
        self.add_widget(self.resultado_o_error_label)

        # Botón para calcular y mostrar resultado
        self.boton_calcular_resultado = Button(text='Calcular Resultado')
        self.boton_calcular_resultado.bind(on_press=self.calcular_resultado)
        self.add_widget(self.boton_calcular_resultado)
    
    def calcular_ahorro_pensional(self, instance):
        self.estado_calculo = 'ahorro'
        self.limpiar_campos_texto()
        self.actualizar_labels_campos_texto('ahorro')
    
    def calcular_pension(self, instance):
        self.estado_calculo = 'pension'
        self.limpiar_campos_texto()
        self.actualizar_labels_campos_texto('pension')
    
    def limpiar_campos_texto(self):
        self.edad_input.text = ''
        self.salario_input.text = ''
        self.semanas_input.text = ''
        self.rentabilidad_input.text = ''
        self.tasa_input.text = ''
        self.resultado_o_error_label.text = ''

    def actualizar_labels_campos_texto(self, tipo_calculo):
        if tipo_calculo == 'ahorro':
            self.edad_input.hint_text = 'Edad (1-90)'
            self.salario_input.hint_text = 'Salario mensual'
            self.semanas_input.hint_text = 'Número de semanas laboradas'
            self.rentabilidad_input.hint_text = 'Rentabilidad del fondo (Como decimal 0.04)'
            self.tasa_input.hint_text = 'Tasa de administración (Como decimal 0.02)'
        elif tipo_calculo == 'pension':
            self.edad_input.hint_text = 'Edad (1-90)'
            self.salario_input.hint_text = 'Ahorro pensional esperado'
            self.semanas_input.hint_text = 'Esperanza de vida'
            self.rentabilidad_input.hint_text = 'Sexo (masculino o femenino)'
            self.tasa_input.hint_text = 'Estado civil (soltero o casado)'

    def salir(self, instance):
        App.get_running_app().stop()

    def calcular_resultado(self, instance):
        try:
            if self.estado_calculo == 'ahorro':
                edad = int(self.edad_input.text)
                salario = float(self.salario_input.text)
                semanas_laboradas = int(self.semanas_input.text)
                rentabilidad_fondo = float(self.rentabilidad_input.text)
                tasa_administracion = float(self.tasa_input.text)

                ahorro_pensional = self.calculadora.calculo_ahorro_pensional(edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion)

                self.resultado_o_error_label.text = f"El ahorro pensional esperado es: {ahorro_pensional}"
                self.controlador_usuarios.InsertarResultadoCalculo(id_usuario=None, tipo_calculo=self.estado_calculo, resultado=ahorro_pensional)
            elif self.estado_calculo == 'pension':
                edad = int(self.edad_input.text)
                ahorro_pensional_esperado = float(self.salario_input.text)         
                esperanza_vida = int(self.semanas_input.text)   
                sexo = self.rentabilidad_input.text.lower()  # asumiendo que el sexo se ingresa en minúsculas
                estado_civil = self.tasa_input.text.lower()  # asumiendo que el estado civil se ingresa en minúsculas

                pension = self.calculadora.calculo_pension(edad, ahorro_pensional_esperado, sexo, estado_civil, esperanza_vida)
                
                self.resultado_o_error_label.text = f"La pensión esperada es: {pension}"
                self.controlador_usuarios.InsertarResultadoCalculo(id_usuario=None, tipo_calculo=self.estado_calculo, resultado=ahorro_pensional)
        except (ValueError, TypeError) as e:
            self.resultado_o_error_label.text = f"Error, Ha ingresado un dato inválido: {e}"
        except Exception as e:
            self.resultado_o_error_label.text = f"Error: {str(e)}"


class CalculadoraPensionalApp(App):
    def build(self):
        return InterfazCalculadora()


if __name__ == '__main__':
    CalculadoraPensionalApp().run()
