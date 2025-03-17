from objects import *
from personajes import *
class lugar:  
    def __init__(self, nombre:str, descripcion:str, bloqueado:bool=False):
        self.nombre = nombre
        self.descripcion = descripcion
        self.presentes = []
        self.objetos = []
        self.conexiones = {}
        self.bloqueado = bloqueado

    def presentar_conexiones(self):
        """esto es para mostrar las conexiones disponibles del lugar"""
        print("Puedes ir a:")
        for direccion, lugar in self.conexiones.items():
            print(f" ⵥ {direccion}: {lugar.nombre}")

    # objetos en el lugar
    def agregar_objeto(self, objeto):
        """esta funcion sirve para agregar un objeto al lugar, solo uno a la vez"""
        for item in self.objetos:
            if item.nombre == objeto.nombre:
                item.cantidad += objeto.cantidad
                return True
        else:
            self.objetos.append(objeto)
            return True

    def quitar_objeto(self, objeto):
        if objeto in self.objetos:
            self.objetos.remove(objeto)
            return True
        else:
            return False

    def presentar_lugar(self):
        """esto es para mostrar la info del lugar"""
        # informacion del lugar
        print(f"》Te encuentras en {self.nombre}")
        print(" ")
        print(self.descripcion)
        print(" ")
        # objetos presentes
        if self.objetos:
            print("Aqui hay:")
            for item in self.objetos:
                if item.cantidad == 1:
                    print(f"ⵚ {item.nombre}")
                else:
                    print(f"ⵚ {item.nombre} (x{item.cantidad})")
        else:
            print("⌘No hay items en este lugar")
        print(" ")
        # presentar los presentes
        if self.presentes:
            print("Puedes ver:")
            for p in self.presentes:
                print(f" ¤ {p.nombre}")
        else:
            print("⌘Aqui no hay nadie")
        print(" ")
        self.presentar_conexiones()
        print(" ")

    # agregar un personaje a un lugar, es decir, agregar un presente
    def agregar_entidad(self, personaje):  
        self.presentes.append(personaje)

    def quitar_entidad(self, personaje):
        self.presentes.remove(personaje)

    def conectar_lugar(self, direccion:str, lugar_destino):
        """esto añade al diccionario direcciones la direccion correspondiente y el objeto lugar para conectarlos"""
        self.conexiones[direccion] = lugar_destino

#valle lidien
casa = lugar("Tu casa", "Esta es tu casa aqui vas a lograr ver tus lugros y dormir para reponerte de tu aventura")
cumbre_rocosa = lugar("Cumbre rocosa", "Una sobra se alza en el horizonte, es la cumbre de una seca e infertil montalla, donde el viento sopla con fuerza gritando los nombres de los perdidos")
valle_lidien = lugar("Valle de Lidien", "Un valle amarillo y seco, refleja un deterioro con el tiempo como si la estacion del lugar fuera siempre la nostalgia de un crudo otoño, su poblacion tambien se ve disminuida mostrando solo unas cuantas casas de madera secas y desgastadas")
#conectando lugares
casa.conectar_lugar("oeste", cumbre_rocosa)
casa.conectar_lugar("este", valle_lidien)
cumbre_rocosa.conectar_lugar("este", casa)
valle_lidien.conectar_lugar("oeste", casa)
#agregrando objetos a los lugares
cofre_normal = cofre()
cofre_normal.agregar([monedax10.clonar(), guantes_cuero.clonar()])
casa.agregar_objeto(cofre_normal)
casa.agregar_objeto(botas_cuero.clonar())
#agregamos a los personajes
#casa.agregar_entidad(laura)


#rue Marques
rue_marquez = lugar("Rue Marquez", "Una calle empedrada y estrecha, con bodegas de ladrillo a los lados, en el centro de la calle hay un canal de agua negra que corre con escases, el ambiente es frio y humedo, prestijios de una zona industril muy sobresplotada.")
negocios_osloy = lugar("Negocios Osloy", "Una fabrica adinerada de un consorcio de duendes que diariamente expulsa humo, es lujoso y lujurioso de negocios de toda clase, donde los vendedores privilejiados cierran tratos con sus engañosas ofertas, el olor a comida y a sudor se mezcla en el aire, el lugar es bullicioso y lleno de borazes almas rapaces y ambiciosas, el lugar da una sencacion de algo oscuro y peligroso")
entrada_master_place = lugar("Entrada Master Place", "Una entrada de marmol y oro, con un gran porton de madera tallada y pulida, el lugar es iluminado por antorchas de fuego azul, el lugar es un santuario de la ambicion y la codicia, el jefe de jefes se ha de encntrar ahi, dos guardias casi programados a cumplir palabra por palabra ordenes de una voz sin origen custodian la puerta, aunque desarmados, de seguro son los custodios del infierno.",True)
master_place = lugar("Master Place", "Una curioso habitacion brindada con todos los privilejios de la zona, donde destaca sus detaller realizados en fina madera de abeto y pino tallados y pulidos a mano, aunque bien iluminado la escena es sombria y misteriosa, el lugar es un santuario de la ambicion y la codicia, el jefe de jefes se encuentra  aqui.")
bodega_materializacion = lugar("Bodega de Materializacion", "Una bodega de ladrillo y madera, con un techo de tejas de barro, el lugar es oscuro y frio, el olor a humedad y a madera podrida se mezcla en el aire, aqui se preparan todas las materias primas para su comercio pero su fuerte es el tritio de cubalternos refinada, que traen directo de las minas de tritio")
poortown = lugar("Poortown", "Saliendo por detras de una pequeña y descuidada puerta de negocios Oslo, un lugar abandonado por toda humanidad y pesar de la vida, el lugar es un cementerio de edificaciones y de almas, el lugar es oscuro y frio, el olor a humedad y refineria podrida se mezcla en el aire, aqui se preparan todas las materias primas para su comercio, definitivamente los pocos obreros y trabajadores, dejan mucho que desear, mostrando la mal paga y precarias condiciones de gestion, en definitiva la poblacion fectada por la abaricia y deseos de los mas afortunados.")
#conectando lugares
valle_lidien.conectar_lugar("norte", rue_marquez)#conexion
rue_marquez.conectar_lugar("sur", valle_lidien)
rue_marquez.conectar_lugar("oeste", negocios_osloy)
negocios_osloy.conectar_lugar("este", rue_marquez)
negocios_osloy.conectar_lugar("norte", entrada_master_place)
negocios_osloy.conectar_lugar("sur", bodega_materializacion)
negocios_osloy.conectar_lugar("oeste", poortown)
entrada_master_place.conectar_lugar("sur", negocios_osloy)
entrada_master_place.conectar_lugar("oeste", master_place)
master_place.conectar_lugar("este", entrada_master_place)
bodega_materializacion.conectar_lugar("norte", negocios_osloy)
poortown.conectar_lugar("este", negocios_osloy)
#agregrando objetos a los lugares
#agregamos a los personajes

#palacio rodwin
colinas_chandel = lugar("Colinas Persiana", "Unas colinas de un verde intenso y brillante, con arboles de acazia de hojas grandes y frondosas, el lugar es tranquilo y silencioso, el olor a tierra humeda y a flores frescas se mezcla en el aire, el lugar es un santuario de la naturaleza y la vida, en las lejanias se ven casas que no temen presumir su humildad y bellesa estructural que se mezcla con el paisaje, el camino es de tierra marcada por el paso de comerciantes y guerreros.")
entrada_rodwind = lugar("Entrada Rodwind", "Una entrada majistral y vastante alta, donde carruajes y guerreros atraviezan el concurrido lugar, esta entrada es de marfil blanco como la luza llena que resplandece calurosamente a los rayos del sol y respeta una integracion homogenea con los verdes campos productores del reino, en sus costados hay dos estatuas, del rey elfo prit-wind y su hermano bram-wind, una señal que recuerda el honor respeto y coraje en batalla de aquellos antepazados.")
plaza_album = lugar("Plaza Album", "Un punto de reunion lo bastante grande como para que docenas de personas y carruajes tranciten diariamente, el blanco del camino empedrado con pidras de marmol y losas de oro, solo devuelven con calides y bellesa la luz del sol, el lugar es un santuario de la cultura y la historia, donde se encuentran los mas grandes monumentos y estatuas de los heroes del reino, en el centro de la plaza se encuentra la estatua del padre Caliostro fundador y progenitor de toda la realesa, la mas grande y majestuosa de todas.")
puesto_guardia_rodwind = lugar("Puesto de la Guardia de Rodwind", "")









if __name__ == "__main__":
    patio = lugar("Patio trasero", "un enorme porton abre un inmenso bosque verde con arboles")

    casa = lugar("Casa Mariano eximilianl Urrutia", "Esta es tu casa aqui vas a lograr ver tus lugros y dormir para reponerte de tu aventura")
    casa.conectar_lugar("este", patio)
    patio.conectar_lugar("oeste", casa)

    casa.presentar_lugar()
