import os
def limpiar_consola():
    # Para Windows
    if os.name == 'nt':
        os.system('cls')

#clase para registrar entidades, como personajes o enemigos, en el juego
# Esta clase permite registrar personajes y acceder a ellos mediante su ID único.
class RegistroEntidades:
    _entidades = {}  # Diccionario para guardar personajes (como {"id_123": Pablo, "id_456": Mariano})

    @classmethod
    def registrar(cls, entidad):
        # Añade el personaje al cuaderno con su ID único
        cls._entidades[entidad.nombre] = entidad

    @classmethod
    def obtener_todos(cls):
        # Devuelve una lista de todos los personajes registrados
        return list(cls._entidades.values())

class RegistroLugares:
    _lugar = {}  # Diccionario para guardar personajes (como {"id_123": Pablo, "id_456": Mariano})

    @classmethod
    def registrar(cls, lugar):
        # Añade el personaje al cuaderno con su ID único
        cls._lugar[lugar.nombre] = lugar

    @classmethod
    def obtener_todos(cls):
        # Devuelve una lista de todos los personajes registrados
        return list(cls._lugar.values())
