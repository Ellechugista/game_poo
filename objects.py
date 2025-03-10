class objeto:
    def __init__(self, nombre, descripcion, cantidad:int=1,   efectos:dict={"ataque":0, "defensa":0, "vida":0}):
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.efectos = efectos
    def clonar(self):
        """Crea una nueva instancia del objeto con los mismos atributos, lo ideal es crear varias instancias del objeto para hacerlo acumulable y que sea funcional en los inventarios"""
        return objeto(self.nombre, self.descripcion, self.cantidad, self.efectos)

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
    def __init__(self, nombre,descripcion:str="", contenido:list=[], cantidad:int=1):
        self.nombre = nombre
        self.contenido = contenido
        self.descripcion = descripcion
        self.cantidad = cantidad

    def describir(self):
        """esta funcion da una descripcion del contenedor"""
        print(" ")
        print(f"⌘{self.descripcion}")

    def abrir(self):
        """esta funcion imprime el contenido del contenedor"""
        self.describir()
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
    def extraer(self, objeto):
        """esta funcion elimina un objeto del contenedor"""
        for item in self.contenido:
            if item.nombre == objeto.nombre:
                if item.cantidad > objeto.cantidad:
                    item.cantidad -= objeto.cantidad
                elif item.cantidad == objeto.cantidad:
                    self.contenido.remove(item)
                else:
                    print(f"No tienes suficiente cantidad de {objeto.nombre} en tu inventario")
                break
    def extraer_todos(self, objeto):
        """esta funcion elimina todos los objetos del contenedor"""
        for item in self.contenido:
            if item.nombre == objeto.nombre:
                self.contenido.remove(item)
                break
#creamos la clase cofres
class cofre(contenedor):
    def __init__(self, nombre="Cofre", descripcion:str="un cofre de madera y chapa de metal gastado", contenido:list=[], cantidad:int=1):
        super().__init__(nombre, descripcion, contenido, cantidad)
#creamos la clase armario
class armario(contenedor):
    def __init__(self, nombre:str="Armario", descripcion:str="un armario que almacena prendas para la vida cotidiana", contenido:list=[], cantidad:int=1):
        super().__init__(nombre, descripcion, contenido, cantidad)
        



#creamos objetos magicos
orbe_verde = objeto("Orbe verde", "objeto magico con modificador estadistico", efectos={"vida":10})
orbe_rojo = objeto("Orbe rojo", "objeto magico con modificador estadistico", efectos={"vida":-5, "ataque": 8, "defensa":2})
baston_curativo = objeto("baston_curativo", "Un baston de madera antiguo que rebosa de vida.", efectos={"vida":5})
#objetos generales que son acumulables
monedax10 = objeto("moneda", "una moneda de oro", 10)
monedax5 = objeto("moneda", "una moneda de oro", 5)
monedax2 = objeto("moneda", "una moneda de oro", 2)
moneda = objeto("moneda", "una moneda de oro")
orbe = objeto("orbe", "un orbe de poder")

#elementos de guerra
espada = objeto("Espada", "Una espada de acero", efectos={"ataque":5})
escudo = objeto("Escudo", "Un escudo de madera", efectos={"defensa":5})
acha = objeto("Acha", "Un hacha de guerra", efectos={"ataque":8})
lanza = objeto("Lanza", "Una lanza de hierro", efectos={"ataque":6})

#armaduras hierro
casco = objeto("Casco_hierro", "Un casco de hierro", efectos={"defensa":3})
coraza = objeto("Coraza_hierro", "Una coraza de hierro", efectos={"defensa":6})
botas = objeto("Botas_hierro", "Botas de hierro", efectos={"defensa":4})
guantes = objeto("Guantes_hierro", "Guantes de hierro", efectos={"defensa":3})
#armaduras cuero
casco_cuero = objeto("Casco_de_cuero", "Un casco de cuero", efectos={"defensa":2})
coraza_cuero = objeto("Coraza_de_cuero", "Una coraza de cuero", efectos={"defensa":3})
botas_cuero = objeto("botas_de_cuero", "Botas de cuero", efectos={"defensa":2})
guantes_cuero = objeto("Guantes_de_cuero", "Guantes de cuero", efectos={"defensa":1})




if __name__ == "__main__":
    monedax10 = objeto("moneda", "una moneda de oro", 10)
    monedax5 = objeto("moneda", "una moneda de oro", 5)
    monedax2 = objeto("moneda", "una moneda de oro", 2)
    moneda = objeto("moneda", "una moneda de oro")
    orbe = objeto("orbe", "un orbe de poder")
    cofre = contenedor("cofre", "un cofre de madera")
    cofre.agregar([monedax10.clonar(),orbe.clonar()])
    cofre.abrir()
    cofre.agregar([monedax10.clonar(), orbe.clonar()])
    cofre.abrir()
    cofre.extraer(monedax10)
    cofre.abrir()
    cofre.extraer(monedax10)
    cofre.abrir()

