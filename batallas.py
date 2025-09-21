from lugares import casa 
from personajes import *
from player import player
from utils import *
import random
# clase de batallas
class batalla:

    def __init__(self, jugador, contrincante):
        self.jugador = jugador
        self.contrincante = contrincante
        self.ganador = None
        self.vivo = None
        self.batalla_injusta = None
        self.turno = 0
        self.xp = None
        
    def informe_batalla(self):
        """esta funcion imprime el informe de la batalla, luego de que ya se ha terminado"""
        if not self.batalla_injusta:
            teto = f"[white]⌘ Batalla entre [b]{self.jugador.nombre} y {self.contrincante.nombre}[b]\n⌘ Turnos: {self.turno}\n⌘ Ganador: [orange3]{self.ganador}[/]\n⌘ Puntos de experiencia ganados: [bright_yellow]{self.xp}[/]\n{"⌘ El contrincante ha sido dejado [green]vivo[/]" if self.vivo else "⌘ El contrincante ha sido [red]destruido[/]"}[/white]"
        else:
            teto = f"[white]⌘ Batalla entre [b]{self.jugador.nombre} y {self.contrincante.nombre}[b]\n⌘ Turnos: {self.turno}\n⌘ Batalla Injusta: [blue]{self.batalla_injusta}[/][/white]"
            
        texto = Text.from_markup(teto)
        
        return Panel(texto, style="dodger_blue1", title=f"{self.jugador.nombre} VS {self.contrincante.nombre}")

    def validar_ganador(self):
        """esta funcion imprime si hay o no ventaja en el combate y devuelve true si hay ventaja y false si no hay ventaja y none"""
        if self.contrincante.vida == 0:
            print(f"{self.contrincante.nombre} ha muerto")
            return True
        elif self.jugador.vida == 0:
            print(f"{self.jugador.nombre} ha muerto")
            return False
        else:
            return "ninguno"

    def actualizar_vista(self):
        """esta funcion imprime la vista del combate"""
        print(" ")
        print("⊢---------------------------------------------⊣")
        print(f"tu vida {self.jugador.nombre}: {self.jugador.vida}")
        print(f"vida de {self.contrincante.nombre}: {self.contrincante.vida}")
        print("⊢---------------------------------------------⊣")
        print(" ")
        
    def mostrar_estadisticas(self):
        """esta funcion imprime las estadisticas del contrincante"""
        print(" ")
        print("⍚Estadisticas del contrincante")
        print("Nombre: ", self.contrincante.nombre)
        print("Vida: ", self.contrincante.vida)
        print(f"Habilidades:  Ataque: {self.contrincante.habilidades['atacar']} Defenza: {self.contrincante.habilidades['defender']}")
        print("Nivel de combate: ", self.contrincante.nivel_combate)

    def iniciar(self):
        """esta funcion controla todo el flujo de una batalla incluyendo turnos y acciones"""
        #GUI
        view = Layout()
        
        #seccionamos paneles
        view.split_column(
            Layout(name="response", size=3, visible=False),
            Layout(name="conten", size=20),
            Layout(Panel("Aqui comienza la batalla...", style="yellow", title="Informa de Batalla"),name="actua", size=8)
        )
        
        #contenido
        view["conten"].split_row(
            Layout(name="info_player", size=45),
            Layout(name="estadisticas"),
            Layout(name="contrincante", size=45)
        )
        
        # info estadisticas
        view["conten"]["estadisticas"].split_column(
            Layout(name="player"),
            Layout(name="contrin")
        )
        
        
        
        #aqui tenemos que cambiar el animo del personaje con quien peliemos a enojado
        self.contrincante.animo -= 35
        self.contrincante.calcular_animo()
        batalla_acabada = self.validar_ganador()
        limpiar_consola()
        
        if self.contrincante.vida <= 0:
            self.batalla_injusta = True
            
            #actualizamos GUI
            view["response"].update(Panel(f"{self.contrincante.nombre} esta incapacitado para el combate.", style="alert"))
            view["response"].visible = True
            
            #silenciamos los demas vaneres
            view["conten"].visible = False
            
            #actualizamos baner de otros
            view["actua"].update(Panel(f"Este combate es injusto, lo mas noble es permitir al oponente morivundo decidir su propio destino...", style="coin"))
            
            centra = Layout(Panel(view, style="bright_black"))
            
            consola.print(centra)
            #imprimimos el layout actualizado
            consola.input("⌬ Presiona cualquier cosita para continuar")
            return
        
        # cuando validar ganador sea "ninguno"
        while batalla_acabada == "ninguno":
            #actualizamos GUI
            
            #actualizamos GUI del jugador
            view["conten"]["info_player"].update(Panel(self.jugador.diseño["normal"], style="dodger_blue2", title=f"Jugador {self.jugador.nombre}"))
            
            view["conten"]["estadisticas"]["player"].update(self.jugador.estadisticas())
            
            #actualizamos GUI del contrincante
            view["conten"]["contrincante"].update(Panel(self.contrincante.diagrama, style="dark_orange3", title=f"Contrincante {self.contrincante.nombre}"))
            
            view["conten"]["estadisticas"]["contrin"].update(self.contrincante.estadisticas(False))
            
            centra = Layout(Panel(view, style="bright_black"))
            
            consola.print(centra)
            
            #self.actualizar_vista()
            respuesta = str(input("➥ ") ).lower().split()
            view["response"].visible = False
            
            #validamos que respuesta no sea nada
            if not respuesta:
                view["response"].update(Panel("⌘ Escribe una accion valida", style="alert"))
                view["response"].visible = True
                continue
            
            match respuesta[0]:
                case "atacar":
                    result = self.jugador.atacar(self.contrincante)
                    if isinstance(result, Panel):
                        view["response"].update(result)
                        view["response"].visible = True
                        continue
                    batalla_acabada = self.validar_ganador()
                case "defender":
                    result = self.jugador.defender()
                    if isinstance(result, Panel):
                        view["response"].update(result)
                        view["response"].visible = True
                        continue
                    batalla_acabada = self.validar_ganador()
                case _ :
                    view["response"].update(Panel("⌘ Escribe una accion valida", style="alert"))
                    view["response"].visible = True
                    continue
        
            # aqui va el movimiento enemigo
            eleccion = random.choice(["atacar", "defender"])
            
            
            result += "[yellow]⍾ Turno del enemigo[/]\n"
            
            if eleccion == "atacar":
                result += self.contrincante.atacar(self.jugador)
            else:
                result += self.contrincante.defender()
                
            #actualizamos flujo de actualizacion
            view["actua"].update(Panel(Text.from_markup(result), style="info", title="Informa de Batalla"))
            
            batalla_acabada = self.validar_ganador()
            self.turno += 1
            self.jugador.defensa_activa = False
            self.contrincante.defensa_activa = False
        
        # cuando batalla_acabada sea True osea gano el jugador
        if batalla_acabada:
            #actualizamos GUI
            view["actua"].update(Panel("⌘Has ganado la batalla", style="green"))
            
            #actualizamos estadisticas del jugador
            view["conten"]["estadisticas"]["player"].update(self.jugador.estadisticas())
            
            #actualizamos estadisticas del contrincante
            view["conten"]["estadisticas"]["contrin"].update(self.contrincante.estadisticas(False))
            
            #nombramos ganador al registro
            self.ganador = self.jugador.nombre
            
            #bucle de respuesta
            while True:
                limpiar_consola()
                centra = Layout(Panel(view, style="bright_black"))
                consola.print(centra)
                respuesta = str(input("⌘ ¿Deseas dejar vivo al contrincante? si/no > ")).lower().split()
                
                #validamos que haya escrito algo
                if not respuesta:
                    view["response"].update(Panel("⌘ Escribe una accion valida", style="alert"))
                    view["response"].visible = True
                    continue
                
                if respuesta[0] == "no":
                    consola.clear()
                    lugar_actual = self.jugador.lugar_actual
                    if self.contrincante in lugar_actual.presentes:
                        lugar_actual.quitar_entidad(self.contrincante)
                        self.vivo = False
                        
                        #actualizamos el baner informativo
                        view["actua"].update(Panel("⌘ Culminas el sufrimiento de tu contrincante, deseandole una mejor vida en el mas alla", style="info"))
                        
                        #actualizamos diagrama de personaje self.jugador.diseño["muerto"]
                        view["conten"]["contrincante"].update(imagen_assci(os.path.join("assets", "calabera.png"), 30))

                    else:
                        limpiar_consola()
                        print("El contrincante ya no se encuntra en el lugar.")
                        self.vivo = 0
                    
                    #imprimimos la actualizacion del view
                    consola.print(centra)
                    #antes de avanzar al luteador
                    consola.input("⌬ Presiona cualquier cosita para continuar")
                    
                    #ahora como el sujeto murio debe dropearnos su pequeño inventario
                    self.contrincante.luteador(self.jugador)
                    
                    #ocultamos el baner response para reiniciar el layout principal
                    view["response"].visible=False
                    break
                                        
                elif respuesta[0] == "si":
                    consola.clear()
                    self.vivo = True
                    
                    #aqui si hay una probabilidad de que el contrincante suelte un item de su inventario
                    recompensas = self.contrincante.soltar_azar()
                    if recompensas or not recompensas == None:
                        text_recom="[gold]Recompenzas: [/]\n"
                        for item in recompensas:
                            text_recom += f"⌘ [white]{self.contrincante.nombre} ha dejado caer[/] [yellow]{item.nombre}[/].\n"
                        self.jugador.lugar_actual.agregar_objeto(recompensas) 
                    else:
                        text_recom = f"⌘ [withe]{self.contrincante.nombre} no ha soltado ningun objeto.[/]"
                        
                    text_recom += "⌘ [bright_black]El contrincante se aleja gravemente herido[/]"
                    
                    view["actua"].update(Panel(Text.from_markup(text_recom), style="dark_green"))   
                    
                    consola.print(centra)
                    consola.input("⌬ Presiona cualquier cosita para continuar")
                    break
                else:
                    view["response"].update(Panel("⌘ Escribe una accion valida", style="alert"))
                    view["response"].visible = True
                    continue
                
            puntos = ((self.turno*0.25) + (self.jugador.vida)*0.50) * 0.20
            puntos = round(puntos, 2)
            self.jugador.nivel_combate += puntos
            self.xp = puntos
            
            #actualizamos GUI para ostrar experiencia ganada
            view["actua"].update(Panel(f"⌘ Has ganado [white]{puntos}[/] puntos de experiencia", style="coin", title="EXPERIENCIA ADQUIRIDA"))
            
            #imprimimos el baner actualizado
            consola.print(centra)
            
            #esperamos a que vea la info y salga
            consola.input("⌬ Presiona cualquier cosita para continuar")
        
        # cuando validar_ganador sea false osea perdio el jugador
        elif not batalla_acabada:
            #actualizamos GUI
            view["actua"].update(Panel("⌘Has ganado la batalla", style="green"))
            
            #actualizamos estadisticas del jugador
            view["conten"]["estadisticas"]["player"].update(self.jugador.estadisticas())
            
            #actualizamos estadisticas del contrincante
            view["conten"]["estadisticas"]["contrin"].update(self.contrincante.estadisticas(False))
            
            #se guarda el ganador al registro
            self.ganador = self.contrincante.nombre

            view["actua"].update(Panel("⌘ Has perdido la batalla", style="alert"))
            
            #imprimimos el layout actualizado
            consola.print(centra)
            
            #esperamos a que vea la info y salga
            consola.input("⌬ Presiona cualquier cosita para continuar")
            
            #debemos actualizar el animo del personaje con quien peliemos a feliz porque gano
            self.contrincante.animo += 50
            self.jugador.game_over()

# test
if __name__ == "__main__":
    lechuga = player("El Lechugista", casa,habilidades={"atacar": 10, "defender": 10},nivel_combate=18, vida=100)
    pablo = humano("pablo", dialogos_ejemplos, vida=100, nivel_combate=20, habilidades={"atacar": 10, "defender": 10})
    print(" ")
    batalla_1 = batalla(lechuga, pablo)
    batalla_1.iniciar()