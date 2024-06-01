class Usuario:
    def __init__(self, nombre, apellido, sexo, edad):
        self.nombre = nombre
        self.apellido = apellido
        self.sexo = sexo
        self.edad = edad

    def __eq__(self, other):
        if not isinstance(other, Usuario):
            return False
        return (self.nombre == other.nombre and self.apellido == other.apellido and self.sexo == other.sexo and self.edad == other.edad)

    def __repr__(self):
        return f"Usuario('{self.nombre}', '{self.apellido}', '{self.sexo}', {self.edad})"