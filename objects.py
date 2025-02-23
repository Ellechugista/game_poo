class objeto:
    def __init__(self, nombre, descripcion, cantidad:int=1, efectos:dict={"ataque":0, "defensa":0, "vida":0}):
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.efectos = efectos

    def describir(self):
        print(" ")
        print("------------■ Descripcion del objeto ■------------")
        print(f"○Nombre: {self.nombre}")
        print(f"►Descripcion: {self.descripcion}")
        print(f"↨Efectos: {self.efectos}")
        print(f"Cantidad: {self.cantidad}")
        print("-------------------------------------------------")
        print(" ")

class contenedor:
    def __init__(self, nombre,descripcion:str="", contenido:list=[]):
        self.nombre = nombre
        self.contenido = contenido if contenido is not None else []
        self.descripcion = descripcion

    def describir(self):
        """esta funcion da una descripcion del contenedor"""
        print(" ")
        print(f"⌘{self.descripcion}")

    def abrir(self):
        """esta funcion imprime el contenido del contenedor"""
        print(" ")
        print(f"☺Contenido de {self.nombre}")
        for item in self.contenido:
            if item.cantidad == 1:
                print(f"- {item.nombre}")
            else:
                print(f"- {item.nombre} (x{item.cantidad})")
        print(" ")

    def agregar(self, objeto):
        """esta funcion agrega uno o varios objetos al contenedor, en caso de varios debe ser una lista"""
        if isinstance(objeto, list):
            for nuevo_item in objeto:
                for item in self.contenido:
                    if item.nombre == nuevo_item.nombre:
                        item.cantidad += nuevo_item.cantidad
                        break
                else:
                    self.contenido.append(nuevo_item)
        else:
            for item in self.contenido:
                if item.nombre == objeto.nombre:
                    item.cantidad += objeto.cantidad
                    break
            else:
                self.contenido.append(objeto)



#creamos objetos magicos
orbe_verde = objeto("Orbe verde", "objeto magico con modificador estadistico", efectos{"vida":10})
orbe_rojo = objeto("Orbe rojo", "objeto magico con modificador estadistico", efectos{"vida":-5, "ataque": 8, "defensa":2})


if __name__ == "__main__":
    monedax10 = objeto("moneda", "una moneda de oro", 10)
    monedax5 = objeto("moneda", "una moneda de oro", 5)
    monedax2 = objeto("moneda", "una moneda de oro", 2)
    orbe = objeto("orbe", "un orbe de poder")
    cofre = contenedor("cofre", "un cofre de madera")
    cofre.agregar([monedax10,orbe])
    cofre.abrir()
    cofre.agregar([monedax10, monedax10, orbe])
    cofre.abrir()

