import random

# entidad otros seres personajes y demás 
class entidad:
   
    def __init__(self, nombre: str, dialogos, vida:float,descripcion:str=None, rutinas=None, nivel_combate=4, habilidades:dict = {"atacar": 5, "defender": 5}, animo="normal"):
        self.nombre = nombre
        # los dialogos deben ser un diccionario como clave el tipo de diálogo y como valor un diccionario con las opciones de respuesta
        self.dialogos = dialogos
        self.vida = vida
        self.descripcion = descripcion
        self.animo = animo
        self.rutinas = rutinas
        self.habilidades = habilidades
        self.nivel_combate = nivel_combate
        self.defensa_activa = False
        
    def estadisticas(self):
        print(" ")
        print("⊢---------------ENTIDY_INFO-------------------⊣")
        print(f"☺ Nombre: {self.nombre}")
        print(f"🎔 Vida: {self.vida}")
        print(f"⍚ Nivel de combate: {self.nivel_combate}")
        print(f"❖ Habilidades: Ataque:{self.habilidades['atacar']} Defensa:{self.habilidades['defender']}")
        print("⊢---------------------------------------------⊣")
      
    def hablar(self):
        """aqui el sujeto tendrá una lista de diccionarios qué tendrán textos que mostrará según el carácter de la entidad, y otro diccionario que tendrá las respuestas que el usuario puede darle"""
        match self.animo:
            case "normal":
                respuesta = random.choice(self.dialogos["normal"])
                print(f"{self.nombre} dice: {respuesta}")
            case "feliz":
                respuesta = random.choice(self.dialogos["content"])
                print(f"{self.nombre} dice: {respuesta}")
            case "triste":
                respuesta = random.choice(self.dialogos["triste"])
                print(f"{self.nombre} dice: {respuesta}")
            case "enojado":
                respuesta = random.choice(self.dialogos["enojado"])
                print(f"{self.nombre} dice: {respuesta}")
            case "repetido":
                respuesta = random.choice(self.dialogos["repetido"])
                print(f"{self.nombre} dice: {respuesta}")
        """while True:
            print(" ")
            
            comando = str(input("> ")).lower().split()"""

    # aqui van las rutinas de la entidad lo que hace, aun no se como hacerlo
    def rutina_activada(self, rutina):
        pass

    def presentacion(self):
        """esta funcion presenta la entidad, lo ideal es que se extienda esta clase deacuerdo a la raza o tipo de entidad"""
        print(f"✧{self.nombre} es una entidad sin clase")
        print(f"✧{self.descripcion}")
    def calcular_ventaja(self, contrincante):
        """esta funcion devuelve si hay ventaja en el combate y devuelve true si hay ventaja y false si no hay ventaja y iguales si son iguales"""
        #cuando el nivel de combate del jugador es mayor al del contrincante
        if self.nivel_combate > contrincante.nivel_combate:
            print(f"⌘¡{self.nombre} tiene ventaja sobre {contrincante.nombre}!")
            print(" ")
            return True
        #cuando el nivel de combate del contrincante es mayor al del jugador
        elif self.nivel_combate < contrincante.nivel_combate:
            print(f"⌘¡{contrincante.nombre} tiene ventaja sobre {self.nombre}!")
            print(" ")
            return False
        #cuando los niveles son iguales
        elif self.nivel_combate == contrincante.nivel_combate:
            print("⌘Niveles iguales - combate justo")
            print(" ")
            return "iguales"
     
    def atacar(self, contrincante):
        """Ataca a un contrincante basado en el nivel de combate"""
        #validamos si el contrincante ya está muerto si ya lo esta que retorne
        if contrincante.vida <= 0:
            print(f"{contrincante.nombre} ya está muerto")
            return
        # Validamos la ventaja según nivel de combate
        ventaja = self.calcular_ventaja(contrincante)
        print(ventaja)
        #cuando el nivel de combate del jugador es mayor al del contrincante
        if ventaja == True:
            #validamos si el contrincante se esta defendiendo
            if contrincante.defensa_activa:
                defenza_contrincante = contrincante.habilidades["defender"]*0.7
            else:
                defenza_contrincante = 0
            #sacamos la diferencia de nivel entre rivales y generamos ventaja
            diferencial_nivel = self.nivel_combate - contrincante.nivel_combate
            daño_base = self.habilidades["atacar"] * diferencial_nivel
            daño_minimo = daño_base // 2
            daño_final = random.randint(daño_minimo, daño_base) - defenza_contrincante
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            print(f"⌘{self.nombre} ha causado {daño_final} de daño a {contrincante.nombre}")
            return daño_final
        #cuando el nivel de combate del contrincante es mayor al del jugador
        elif ventaja == False:
            #validamos si el contrincante se esta defendiendo
            if contrincante.defensa_activa:
                defenza_contrincante = contrincante.habilidades["defender"]*0.7
            else:
                defenza_contrincante = 0
            #sacamos la diferencia de nivel entre rivales y generamos desventaja
            daño_base = self.habilidades["atacar"] - diferencial_nivel
            daño_minimo = daño_base // 2
            daño_final = (random.randint(daño_minimo, daño_base)-defenza_contrincante)
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            print(f"⌘{self.nombre} ha causado {daño_final} de daño a {contrincante.nombre} (reducido por defenza enemiga)")
            return daño_final
        #cuando los niveles son iguales
        elif ventaja == "iguales":
            #validamos si el contrincante se esta defendiendo
            if contrincante.defensa_activa:
                defenza_contrincante = contrincante.habilidades["defender"]*0.7
            else:
                defenza_contrincante = 0
            daño_minimo = self.habilidades["atacar"] // 2
            daño_final = random.randint(daño_minimo, self.habilidades["atacar"]) - defenza_contrincante
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            contrincante.vida = max(0, contrincante.vida - daño_final)
            print(f"⌘{self.nombre} ha causado {daño_final} de daño a {contrincante.nombre}")
            return daño_final
        
    def defender(self):
        """esta funcion hace que el jugador se defienda cambie el booleano de defensa_activa a True pero al final de su turno se debe desactivar desde afuera"""
        self.defensa_activa = True
        print(f"{self.nombre} se defiende")
        print(" ")
        
        
# -----------ENTIDADESSSSSSS----------------------------------------------
#estendemos la clase entidad para crear razas o tipos de entidades
#humanos
class humano(entidad):
    def __init__(self, nombre, dialogos, vida, descripcion = None, rutinas=None, nivel_combate=5, habilidades = { "atacar": 5,"defender": 5 }):
        super().__init__(nombre, dialogos, vida, descripcion, rutinas, nivel_combate, habilidades)
    def presentacion(self):
        print(f"{self.nombre} es un humano")
#ELFOS  
class elfo(entidad):
    def __init__(self, nombre, dialogos, vida, descripcion = None, rutinas=None, nivel_combate=8, habilidades = { "atacar": 8,"defender": 15 }):
        super().__init__(nombre, dialogos, vida, descripcion, rutinas, nivel_combate, habilidades)
    def presentacion(self):
        print(f"{self.nombre} es un elfo")
#ORCOS
class orco(entidad):
    def __init__(self, nombre, dialogos, vida, descripcion = None, rutinas=None, nivel_combate=3, habilidades = { "atacar": 15,"defender": 12 }):
        super().__init__(nombre, dialogos, vida, descripcion, rutinas, nivel_combate, habilidades)
    def presentacion(self):
        print(f"{self.nombre} es un orco")


   
# aqui creamos los dialogos de la entidad para que pueda hablar cuando llamemos a la función de la clase estos son una base y deberían modificarse o añadir un diccionario de listas más especializado para cada entidad

feliz = [
    "¡Hoy es un gran día!",
    "Me siento increíblemente bien.",
    "No puedo dejar de sonreír.",
    "Todo parece ir perfectamente.",
    "La vida es maravillosa.",
    "Estoy lleno de energía y alegría.",
    "Hoy todo me sale bien.",
    "Me siento agradecido por todo lo que tengo.",
    "¡Qué felicidad me da este momento!"
]

# Lista de frases neutras
neutro = [
    "Hoy es un día como cualquier otro.",
    "No tengo nada especial que comentar.",
    "Todo parece normal.",
    "Ni bien ni mal, simplemente neutral.",
    "No siento nada en particular.",
    "Hoy no tengo emociones fuertes.",
    "Todo está tranquilo y sin cambios.",
    "No hay nada nuevo bajo el sol.",
    "Sigo mi rutina como siempre."
]

# Lista de frases enojadas
enojado = [
    "¡Estoy furioso!",
    "No puedo creer que esto esté pasando.",
    "Todo me está saliendo mal.",
    "¡Estoy harto de esta situación!",
    "No quiero hablar con nadie.",
    "La gente me está sacando de quicio.",
    "No soporto más esta injusticia.",
    "Estoy a punto de explotar de rabia.",
    "¡Basta ya, no aguanto más!"
]

# Lista de frases repetitivas
repetitivo = [
    "Lo mismo de siempre.",
    "Otra vez lo mismo.",
    "No hay nada nuevo que decir.",
    "Siempre es igual.",
    "Repitiendo lo mismo una y otra vez.",
    "Cada día es una repetición del anterior.",
    "No hay cambios, todo sigue igual.",
    "Me aburro de tanta monotonía.",
    "Otra vez la misma historia."
]

# Lista de frases tristes
triste = [
    "Hoy me siento muy mal.",
    "No tengo ganas de hacer nada.",
    "Todo parece gris y sin sentido.",
    "No puedo dejar de llorar.",
    "Me siento solo y abandonado.",
    "La tristeza me invade por completo.",
    "No encuentro consuelo en nada.",
    "Siento que el mundo está en mi contra.",
    "No sé cómo salir de este pozo."
]

dialogos_ejemplos = {
    "normal": neutro,
    "content": feliz,
    "triste": triste,
    "enojado": enojado,
    "repetido": repetitivo
}

#aqui creamos a los personajes
marcelito = humano("marcelito", dialogos_ejemplos, 100, "Un chico joven. muy reservado, cabello corto y lentes arcaicos, con fuerte sentido de moral y justicia.", nivel_combate=7, habilidades={"atacar":5,"defender":4})
laura = humano("laura", dialogos_ejemplos, 100, "Una chica joven y alegre, optimista y energica, morena cabello largo negro, y una sonrisa sin igual.",nivel_combate=9,habilidades={"atacar":8,"defender":10})


if __name__ == "__main__":
    # aqui creamos la entidad
    marcelito = humano("marcelito", dialogos_ejemplos, 100)
    marcelito.presentacion()
    marcelito.hablar("repetido")

