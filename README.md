 ![Badge en Desarollo](https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green)
 
# GAME_POO

_Aqui he ceado el sistema para la creacion y manipulacion de un mundo virtual, sin graficos, ya que mi gusto por el juego d emeza calobozos y dragones y su inmensa creatividad me inspiraron para afianzar los conceptos t practicas de la programacion orientada a objeto en python, a travez de un juego con estas caracteristicas._

## Actualizaciones 📈

* `0.1 vercion `: Esta es la vercion en la que comienzo a documentar el proceso de creacion en una etapa algo desarrollada del proyecto. 

## Ejecuta y prueba el avance 🚀
_Para ejecutar y probar el sistema, ejecute como raiz el archivo game.py junto a todas sus dependencias, dentro del escenario puede hacer muchas cosas de las cuales es mejor tener un manual de comandos a la mano._

## Pre-requisitos y Prueba 📋
* [PYTHON 3.1+](https://www.python.org/downloads/) - Python 3.13.2
* Terminal Integrado con Python

_Descarga la version del proyecto junto a todas sus dependencias, luego ejecuta el archivo principal `game.py` en tu terminal de windows o en el depurador de Visual Estudio Code para que cargen los caracteres unicode que decoran el flujo del juego.
```
python game.py
```
## COMANDOS BASICOS 🗒️

  * ir: comando basico para cambiar el lugar actual en el que se encuentra el personaje dentro del mundo, debe ser una direccion disponible o acorde a la que se muestra en el navegador
```
>ir "este".
```
  * hablar: comando basico para hablar con los personajes dentro de la escena, estos dependiendo del estado de animo tendran diferentes comentarios predefinidos (normal, feliz, triste y enojado).
```
>hablar "nombre del personaje con quien hablar"
```
  * tomar: comando basico para tomar objetos tirados dentro del escenario y luego seran añadidos al inventario del jugador, puedes tomar de todo, siempre y cuando no sea un almacenador o recipiente (cofres).
```
>tomar "nombre del objeto"
```
  * inventario: comando basico para mostrar el contenido del inventario del jugador dentro de un escenario, este enlistara los objetos y su cantidad, SYNTAXIS inventario #tener en cuenta agregar limite de objetos, basado en peso para cada objeto dentro del inventario.

  * abrir: comando basico para abrir un recipiente o cofre, este comando muestra y lista el contenido dentro del recipiente, dentro de el puedes:
    
    - `tomar:` comando basico para agregar el objeto a tu inventario. 
    - `dejar:` comando basico para dejar un objeto dentro del recipiente. 
    - `salir:` comando basico para salir del listado de objetos de un recipiente. 

  * informacion: comando basico para mostrar la informacion y estadisticas de un objeto dentro de tu inventario.
```
>informacion "nombre de objeto"
```
  * registros: comando basico para mostrar y listar los registros de combate, un pequeño histrial de lo acontecido.

## COMANDOS EN ATAQUE ⚔️

  * atacar: comando basico para iniciar un combate contra un personaje, el combate funciona por turnos en dode se puede atacar y defender, usando como base las habilidades de lucha y la diferencia de nivel entre los contrincantes, al iniciar un combate entraras en un bucle en donde solo podras salir muestro o victorioso, ya que batirce a duelo contra alguien mas no da chance a intentarlo mas tarde.
```
>atacar "nombre de la entidad a luchar"
```

_Una vez dentro podras ejecutar los siguientes comandos:_

* atacar: este comando tendra en cuenta el estado del enemigo si esta defendiendoze o no, para luego hacerle daño al contrincante, el sistema de daño se basa en lo siguiente:

1. primero se calcula la ventaja de acurdo al nivel de pelea, en este hay tres estados mayor, menr o igual, en dado caso sea ventaja verdadera, el daño se calcula de la siguiente manera.
```
      daño_base = self.habilidades["atacar"] * diferencial_nivel
      daño_minimo = daño_base // 2
      daño_final = random.randint(int(daño_minimo), int(daño_base)) - defenza_contrincante
```
      
3. efectuamos daño teniendo en cuenta si esta o no activada la defenza del enemigo, dado caso que la defenza este activa la defenza del contricante se calcula con la habilidad de defenza del contrincante al 70% y se resta al ataque final:
```
      defenza_contrincante = contrincante.habilidades["defender"]*0.7
```

5. en el segundo caso es que este en desventaja el daño se calcula restando la diferencia de nivel, asi si hay mas difeencia de nivel mas desventaja tendra con respecto a sus habilidades de combate y defenza siguiendo las siguientes formula:
```
            daño_base = self.habilidades["atacar"] - diferencial_nivel
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base)) - defenza_contrincante
```
   
6. el daño final siempre sera un numero alazar entre un rango de la mitad de la habilidad de daño y la habilidad completa de daño, para el jugador y el NPC el daño se calcula igual.

* defender: este comando activa el modo defenza del jugador y se reinicia una vez halla terminado una ronda de turnos por el contrincante y el jugador.

## MAPA 🧭
![Mapa-Wordl](https://github.com/user-attachments/assets/95c7bddc-ec3c-4a8e-800d-a97454dfbf9c)

_⚠️ Este mapa esta sujeto a cambios y correcciones deacuerdo a la historia en desarrollo._

# Autores ✒️

* [Ellechugista](https://github.com/Ellechugista) - ellechugista(Github)
