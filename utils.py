import os
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.progress import track
from rich.layout import Layout
from rich.text import Text
from rich.console import Group
import time
from PIL import Image

#declaramos obicaciones bases de los assets
objetos_ruta= os.path.join("assets","objetos")
vestimentas_ruta = os.path.join("assets", "objetos","vestimentas")
duendes_ruta = os.path.join("assets","duende")
elfos_ruta = os.path.join("assets","elfo")
humanos_ruta = os.path.join("assets","humano")
orco_ruta = os.path.join("assets","orco")


def limpiar_consola():
    """funcion que limpia toda la consola 
    """
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

#estlos personalizados
tema= Theme({
    "info": "italic cyan",
    "alert": "bright_red",
    "exito": "green4",
    "coin": "gold3"
})
consola = Console(theme=tema, height=33)

def bar_carga(tiempo:int, mensaje:str):
    for i in track(range(tiempo), mensaje, console=consola):
        time.sleep(0.2)

def imagen_assci(path, width=40,  stilos:str= "", **keys):
    img = Image.open(path).convert("L")  # escala de grises
    img = img.resize((width, int(width * img.height / img.width / 2)))

    ascii_chars = "$@B%8&WM#*zcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    pixels = img.getdata()

    result = []
    for i, pixel in enumerate(pixels):
        if i % img.width == 0:
            result.append("\n")
        result.append(ascii_chars[pixel * len(ascii_chars) // 256])
    return Text("".join(result), style=stilos, **keys)

if __name__ == "__main__":
    consola.print("Esto es una [bold]info[/bold]", style="info")
    consola.print("Esto es una [bold]alerta[/bold]", style="alert")
    consola.print("Esto es una [bold]exito[/bold]", style="exito")
    consola.print("Esto es una [bold]moneda[/bold]", style="coin")
    consola.print(Panel("contenido del panel guapo".upper(),style= "info",title="Este es mi titulo"))
    
    paginado = Layout()
    paginado.split_column(
        Layout(Panel(f"estoy tratando de renderisarme /n {consola.rule("[bold]Descripcion[/]")}", title="cabezera", style="green"),name="header"),
        Layout(name="body"),
        Layout(name="footer")
    )
    
    paginado["body"].split_row(
        Layout(Panel("soy la publicidad", title="ads", style="orange_red1 italic"),name="publisidad", ratio=1),
        Layout(Panel("loremp impust astf etdvhjba aksbdjasbdjab", style="blue"),name="contenido", ratio=2),
        Layout(Panel("esta vida me va a matar", title="comments", style="yellow"),name="opiniones", ratio=1)
    )
    
    paginado["footer"].split_row(
        Layout(name="cajita", ratio=1),
        Layout(name="links", ratio=4)
    )
    
    consola.print(paginado)
    consola.rule("[bold]Descripcion[/]")
    
    consola.print(imagen_assci(os.path.join("assets", "calabera.png")))
