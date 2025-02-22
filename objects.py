class objeto:
    def __init__(self, nombre, descripcion, efectos:dict={"ataque":0, "defensa":0, "vida":0}):
        self.nombre = nombre
        self.descripcion = descripcion
        self.efectos = efectos
    
