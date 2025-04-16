from objects import *
from personajes import *
from utils import RegistroLugares
class lugar:  
    
    def __init__(self, nombre:str, descripcion:str):
        self.nombre = nombre
        self.descripcion = descripcion
        self.presentes = []
        self.objetos = []
        self.conexiones = {}
        self.bloqueado = False
        self.razon = None
        
        RegistroLugares.registrar(self)  # Registrar el lugar en el registro de lugares

    def presentar_conexiones(self):
        """esto es para mostrar las conexiones disponibles del lugar"""
        print("Puedes ir a:")
        #ordenamos las direcciones alfabeticamnte asi no cambiaran de orden
        ordenado = {
                    clave: valor for clave, valor in sorted(self.conexiones.items())
                    }
        for direccion, lugar in ordenado.items():
            print(f" ⵥ {direccion}: {lugar.nombre}")

    # objetos en el lugar
    def agregar_objeto(self, objeto):
        """esta funcion sirve para agregar un objeto al lugar, solo uno a la vez"""
        if isinstance(objeto, list):
            for nuevo_item in objeto:
                for item in self.objetos:
                    if item.nombre == nuevo_item.nombre:
                        item.cantidad += nuevo_item.cantidad
                        break
                else:
                    self.objetos.append(nuevo_item)
        else:
            for item in self.objetos:
                if item.nombre == objeto.nombre:
                    item.cantidad += objeto.cantidad
                    break
            else:
                self.objetos.append(objeto)

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
    def bloquear(self, razon:str):
        """esta funcion bloque el acceso el lugar y almacena en una variable la razon o motivo por el cual esta bloqueado el acceso al lugar"""
        self.bloqueado = True
        self.razon = razon
        
        

#------------------valle lidien-----------------

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

cumbre_rocosa.agregar_objeto([hacha.clonar(), escudo.clonar()])

valle_lidien.agregar_objeto(hacha.clonar())

#agregamos a los personajes

casa.agregar_entidad(laura)

valle_lidien.agregar_entidad(marcelito)

#--------------------rue Marques--------------


rue_marquez = lugar("Rue Marquez", "Una calle empedrada y estrecha, con bodegas de ladrillo malgastado en el horizonte, en el centro de la calle hay un canal de agua negra que corre con escases, el ambiente es frio y humedo, prestijios de una zona industrial muy sobresplotada.")

negocios_osloy = lugar("Negocios Osloy", "Una fabrica adinerada de un consorcio de duendes que diariamente expulsa humo, es lujoso y lujurioso de negocios de toda clase, donde los vendedores privilejiados cierran tratos con sus engañosas ofertas, el olor a comida y a sudor se mezcla en el aire, el lugar es bullicioso y lleno de borazes almas rapaces y ambiciosas, el lugar da una sencacion de algo oscuro y peligroso")

entrada_master_place = lugar("Entrada Master Place", "Una entrada de marmol y oro, con un gran porton de madera tallada y pulida, el lugar es iluminado por antorchas de fuego azul, el lugar es un santuario de la ambicion y la codicia, el jefe de jefes se ha de encntrar ahi, dos guardias casi programados a cumplir palabra por palabra ordenes de una voz sin origen custodian la puerta, aunque desarmados, de seguro son los custodios del infierno.")

master_place = lugar("Master Place", "Una curioso habitacion brindada con todos los privilejios de la zona, donde destaca sus detaller realizados en fina madera de abeto y pino tallados y pulidos a mano, aunque bien iluminado la escena es sombria y misteriosa, el lugar es un santuario de la ambicion y la codicia, el jefe de jefes se encuentra  aqui.")

master_place.bloquear("Solo los mas privilejiados pueden entrar")#bloquemos el acceso

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

#-------------Reino Rodwind------------------

colinas_chandel = lugar("Colinas Persiana", "Unas colinas de un verde intenso y brillante, con arboles de acazia de hojas grandes y frondosas, el lugar es tranquilo y silencioso, el olor a tierra humeda y a flores frescas se mezcla en el aire, el lugar es un santuario de la naturaleza y la vida, en las lejanias se ven casas que no temen presumir su humildad y bellesa estructural que se mezcla con el paisaje, el camino es de tierra marcada por el paso de comerciantes y guerreros.")

entrada_rodwind = lugar("Entrada Rodwind", "Una entrada majistral y vastante alta, donde carruajes y guerreros atraviezan el concurrido lugar, esta entrada es de marfil blanco como la luza llena que resplandece calurosamente a los rayos del sol y respeta una integracion homogenea con los verdes campos productores del reino, en sus costados hay dos estatuas, del rey elfo prit-wind y su hermano bram-wind, una señal que recuerda el honor respeto y coraje en batalla de aquellos antepazados.")

corridor_real = lugar("Corridor Real", "un pasillo estrecho al costad de la entrda principal, donde la roca y el malfil se confunden, el lugar parece dejado atras por la glamurosa entrada, le destacan la tierra seca y plantas secas.")

plaza_malfil = lugar("Plaza Malfil", "Un punto de reunion lo bastante grande como para que docenas de personas y carruajes tranciten diariamente, el blanco del camino empedrado con pidras de marmol y losas de oro, solo devuelven con calides y bellesa la luz del sol, el lugar es un santuario de la cultura y la historia, donde se encuentran los mas grandes monumentos y estatuas de los heroes del reino, en el centro de la plaza se encuentra la estatua del padre Caliostro fundador y progenitor de toda la realesa, la mas grande y majestuosa de todas.")

puesto_guardia_rodwind = lugar("Puesto de la Guardia de Rodwind", "Este es un puesto muy glamuroso y lleno de estatuas y valerosos guererros, aqui los soldados de Rodwind entrenan y planifican con la veraz estrategia de los elfos, para ejerser la proteccion y voluntad de su rey.")

mercado_rodwind = lugar("Mercado Rodwind", "Un mercado muy grande y lleno de gente, donde se venden todo tipo de cosas, el lugar es un santuario de la economia y la riqueza, donde se encuentran los mas grandes comerciantes y vendedores del reino, en el centro del mercado se encuentra la estatua del padre Caliostro fundador y progenitor de toda la realesa, la mas grande y majestuosa de todas.")

tienda_rodwind = lugar("Tienda Rodwind", "Una tienda ladrillo fino, con un techo de tejas de barro, del lugar se asoman herramientas, y subenires diarios para todos los habitantes, con estantes a los costados de la entrada que revosan de productos de todo el valle, solo deja claro que dentro encontraras lo que buscas.")

torre_magica_miracle = lugar("Torre Magica Miracle", "Una torre de roca pulida muy antigua que pese a su antiguedad se mantiene en pie, el lugar es un santuario de la magia y la sabiduria, donde se encuentran los mas grandes magos y hechiceros del reino, en el centro de la torre hay un pequeño jardin de hierbas misticas y flores que sobrepasan la imaginacion de los mortales.")

pacillo_real = lugar("Pacillo Real", "Un pasillo amplio y bien decorado que sigue defrente a la entrada del reino, a los costados casas muy bien acomodadas que no temen mostrar que sus dueños heredados o no, siempre han sido beneficiados por todas las situaciones del reino.")

castilo_olivergt = lugar("Castillo Olivergt", "Un gran catillo de pierra pulida bordado de marfil con siluetas de oro brillante como el mismo sol, en l puerta principal 3 leones ferozes baññados de oro escoltan con fiereza la entrada, el lugar es un santuario de la realeza y la justicia, dentro hay un sin fin de pasillos y habitaciones donde consejeros, sabios y nobles se reunen para discutir el proximo paso de todo el reino.")

#---------------CASTILLO-OLIVERGT---------------------

piso_1_castillo_olivergt = lugar("Primer Piso", "Un lugar central en el gran castillo del reino de los elfos de Rodwind, la mayoria te mira desconsertados y otros con desprecio.")

piso_2_castillo_olivergt = lugar("Segundo Piso", "Un lugar central en el gran castillo del reino de los elfos de Rodwind, la mayoria te mira desconsertados y otros con desprecio.")

oficina_cosejeria_olivergt = lugar("Oficina de Cosejeria", "Una habitacion bien acomodada con mapas diagramas y mucha informacion relacionada a las personas de la realeza, aqui suele estar el consejero real.")

puesto_guerra_olivergt = lugar("Puesto de Guerra", "En el centro una meza redonda con armas y armaduras de todo tipo, tambien planes estrategias y muchos puestos de combates en mapas, aqui se preparan los comandantes para la guerra.")

piso_3_castillo_olivergt = lugar("Tercer Piso", "Un lugar central en el gran castillo del reino de los elfos de Rodwind, la mayoria te mira desconsertados y otros con desprecio.")

habitacion_rey_olivergt = lugar("Habitacion del Rey", "Una habitacion muy grande y bien decorada, con una cama grande y comoda, con toda clase de lujosos muebles, una mesa con sillas y un gran balcon con una vista todo el reino, aqui duerme el rey y la reina cuando atiende su familia.")

habitacion_mago_odguerin = lugar("Habitacion del Mago Odguerin", "Una habitacion muy grande y bien decorada, con una cama grande y comoda, a su derecha un laboratorio especializado en las lecturas de los astros para las predicciones mas precisas del reino, estante de pociones y quimicos capazes de tener los olores mas desagradables de todo el mundo y una curioso muro resaltado con sal.")

fall_sky = lugar("Fall Sky", "Un lugar muy alto y frio, donde el viento sopla con fuerza y el suelo es de hielo, el lugar es un santuario de la soledad y la reflexion, donde se encuentran los mas grandes pensadores y filosofos del reino, en el centro del lugar se encuentra un gran abismo que se pierde en la oscuridad del cielo, la entrada a un lugar mejor.")

#conectando lugares

rue_marquez.conectar_lugar("norte", colinas_chandel)#conexion

colinas_chandel.conectar_lugar("sur", rue_marquez)

colinas_chandel.conectar_lugar("norte", entrada_rodwind)

entrada_rodwind.conectar_lugar("sur", colinas_chandel)

entrada_rodwind.conectar_lugar("oeste", corridor_real)

corridor_real.conectar_lugar("este", entrada_rodwind)

entrada_rodwind.conectar_lugar("norte", plaza_malfil)

plaza_malfil.conectar_lugar("sur", entrada_rodwind)

plaza_malfil.conectar_lugar("este", puesto_guardia_rodwind)

puesto_guardia_rodwind.conectar_lugar("oeste", plaza_malfil)

plaza_malfil.conectar_lugar("oeste", mercado_rodwind)

mercado_rodwind.conectar_lugar("este", plaza_malfil)

plaza_malfil.conectar_lugar("norte", pacillo_real)

pacillo_real.conectar_lugar("sur", plaza_malfil)

mercado_rodwind.conectar_lugar("sur", tienda_rodwind)

mercado_rodwind.conectar_lugar("norte", torre_magica_miracle)

tienda_rodwind.conectar_lugar("norte", mercado_rodwind)

torre_magica_miracle.conectar_lugar("sur", mercado_rodwind)

#------------------CASTILLO-OLIVERGT---------------------

pacillo_real.conectar_lugar("norte", castilo_olivergt)

castilo_olivergt.conectar_lugar("sur", pacillo_real)

castilo_olivergt.conectar_lugar("oeste", piso_1_castillo_olivergt)

piso_1_castillo_olivergt.conectar_lugar("este", castilo_olivergt)

piso_1_castillo_olivergt.conectar_lugar("arriba", piso_2_castillo_olivergt)

piso_2_castillo_olivergt.conectar_lugar("abajo", piso_1_castillo_olivergt)

piso_2_castillo_olivergt.conectar_lugar("norte", oficina_cosejeria_olivergt)

oficina_cosejeria_olivergt.conectar_lugar("sur", piso_2_castillo_olivergt)

piso_2_castillo_olivergt.conectar_lugar("oeste", puesto_guerra_olivergt)

puesto_guerra_olivergt.conectar_lugar("este", piso_2_castillo_olivergt)

piso_2_castillo_olivergt.conectar_lugar("arriba", piso_3_castillo_olivergt)

piso_3_castillo_olivergt.conectar_lugar("abajo", piso_2_castillo_olivergt)

piso_3_castillo_olivergt.conectar_lugar("norte", habitacion_rey_olivergt)

habitacion_rey_olivergt.conectar_lugar("sur", piso_3_castillo_olivergt)

piso_3_castillo_olivergt.conectar_lugar("sur", habitacion_mago_odguerin)

habitacion_mago_odguerin.conectar_lugar("norte", piso_3_castillo_olivergt)

habitacion_mago_odguerin.conectar_lugar("este", fall_sky)

fall_sky.conectar_lugar("oeste", habitacion_mago_odguerin)

#agregrando objetos a los lugares
#agregamos a los personajes

#------------------cumbre rocosa--------------
valle_lirios = lugar("Valle de los Lirios", "Un valle de lirios y flores de colores, el lugar es un santuario de la belleza y la armonia, donde se encuentran los mas grandes artistas y poetas del reino, en el centro del valle hay un gran lago de agua cristalina y pura, donde se pueden ver los lirios flotando en el agua, un lugar de profunda paz.")

risco_montañoso = lugar("Risco Montañoso", "Una montaña de roca y tierra muy imponente, el lugar es un sementerio de cuerpos, que alguna vez fueron novatos exploradores que no lograron pasar la dura vida en esta montaña, siempre se siente fria y nublada, aunque dasolador el poco sol que las nubes dejan pasar pega a la copa de todo este terreno montañoso que refleja tranquilidad en la cima.")

penumbre_aventureux = lugar("Penumbre Aventureux", "Un lugar aunque incomodo se puede descanzar sin temor a amenazs externas o climatologicas ya que el lugar es cubierto por un crater que partio una pequeña montaña partida en dos, ha apliado el camino con muros alrededor.")

brumosos_andes = lugar("Brumosos Andes", "La cuspide de la montaña mas alta de todo el pais, aqui hay una pequeña y humilde casa de madera y a su lado un extraño abeto que no crece en la region, donde parece haber habitado ahi hace mucho tiempo un carpintero o escrivano, la paz y silbido del viento conforme suplan las nubes y el sol plantean un escenario sin igual.")

sidewalk = lugar("Side Walk", "Un camino de piedra y tierra, que tiene senderos casi cambiantes, miras para un lado y miras para el otro y nunca es la misma direccion.")

sidewalk_1 = lugar("Side Walk 1", "Un camino de piedra y tierra, que tiene senderos casi cambiantes, miras para un lado y miras para el otro y nunca es la misma direccion.")

sidewalk_2 = lugar("Side Walk 2", "Un camino de piedra y tierra, que tiene senderos casi cambiantes, miras para un lado y miras para el otro y nunca es la misma direccion.")

sidewalk_3 = lugar("Side Walk 3", "Un camino de piedra y tierra, que tiene senderos casi cambiantes, miras para un lado y miras para el otro y nunca es la misma direccion.")

sidewalk_4 = lugar("Side Walk 4", "Un camino de piedra y tierra, que tiene senderos casi cambiantes, miras para un lado y miras para el otro y nunca es la misma direccion.")

sidewalk_5 = lugar("Side Walk 5", "Un camino de piedra y tierra, que tiene senderos casi cambiantes, miras para un lado y miras para el otro y nunca es la misma direccion.")

#conectando lugares

colinas_chandel.conectar_lugar("este", valle_lirios)#conexion

valle_lirios.conectar_lugar("oeste", colinas_chandel)

valle_lirios.conectar_lugar("norte", risco_montañoso)

risco_montañoso.conectar_lugar("sur", valle_lirios)

risco_montañoso.conectar_lugar("norte", penumbre_aventureux)

penumbre_aventureux.conectar_lugar("sur", risco_montañoso)

penumbre_aventureux.conectar_lugar("norte", sidewalk)

sidewalk.conectar_lugar("sur", penumbre_aventureux)

#aqui debemos crear un laberinto para que el jugador tenga que saber con que direccion puede salir y avanzar el laberinto


if __name__ == "__main__":
    patio = lugar("Patio trasero", "un enorme porton abre un inmenso bosque verde con arboles")

    casa = lugar("Casa Mariano eximilianl Urrutia", "Esta es tu casa aqui vas a lograr ver tus lugros y dormir para reponerte de tu aventura")
    casa.conectar_lugar("este", patio)
    patio.conectar_lugar("oeste", casa)

    casa.presentar_lugar()
    print(" ")
    for lugar in lugar.todas_instancias:
        print(f"- {lugar.nombre}: {lugar.descripcion}")
        print(" ")
