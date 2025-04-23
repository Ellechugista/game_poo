 ![Badge en Desarollo](https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green)
 
# GAME_POO

_Aqui he ceado el sistema para la creacion y manipulacion de un mundo virtual, sin graficos, ya que mi gusto por el juego d emeza calobozos y dragones y su inmensa creatividad me inspiraron para afianzar los conceptos t practicas de la programacion orientada a objeto en python, a travez de un juego con estas caracteristicas._

## Ejecuta y prueba el avance 🚀

_Para ejecutar y probar el sistema, ejecute como raiz el archivo `game.py` junto a todas sus dependencias, dentro del escenario puede hacer muchas cosas de las cuales es mejor tener un manual de comandos a la mano._

_Te invito a que explores al maximo el desarrollo de este mundo_

## Pre-requisitos y Prueba 📋
* [PYTHON 3.1+](https://www.python.org/downloads/) - Python 3.13.2
* Terminal Integrado con Python

_Descarga la version del proyecto junto a todas sus dependencias, luego ejecuta el archivo principal `game.py` en tu terminal de windows o en el depurador de Visual Estudio Code para que cargen los caracteres unicode que decoran el flujo del juego._
```shell
python game.py
```
## COMANDOS BASICOS 🗒️

* Menu:
```shell
⊢---------------------Menu Principal----------------------⊣
⌘Bienvenido al juego de rol GAME-POO

⌘Iniciar juego
⌘Guardar juego
⌘Cargar juego
⌘Salir del juego
⌘Volver
----------------------------------------------------------⊣

>
```
_Puedes seleccionar entre `Iniciar`, lo cual iniciara una partida nueva por defecto desde 0, `Guardar`, este comando guardara el estado de la partida actual con nombre de datos como por defecto pero puedo añadirce el nombre del archivo save si se escribe luego de llamar guardar en consola, `Cargar`, esto cargara un estado guardado en la carpeta saves, pero si no la hay crea la carpeta y mencionciona que no hay partidas guardadas, `Salir`, esto saldra de la ejecucion del juego._

* Iniciar: pedira el nobre del jugador
  
```shell
> iniciar

⌘Cual sera el nombre del guerreo?
> elechugista
```

* Guardar:

```shell
> guardar nombre_de_la_partida
⌘Guardando datos...

⌘Datos guardados
```
* Cargar: listara las partidas guardadas:

```shell
> cargar
⌘Archivos de guardado disponibles:
⌘2025-04-11_datos.pkl
⌘2025-04-11_nombre_de_la_partida.pkl

⌘Cual archivo quieres cargar? (sin la extencion .pkl)
> 2025-04-11_nombre_de_la_partida
```

  * ir: comando basico para cambiar el lugar actual en el que se encuentra el personaje dentro del mundo, debe ser una direccion disponible o acorde a la que se muestra en el navegador
```shell
>ir "este".
```
  * hablar: comando basico para hablar con los personajes dentro de la escena, estos dependiendo del estado de animo tendran diferentes comentarios predefinidos (normal, feliz, triste y enojado).
```shell
>hablar "nombre del personaje con quien hablar"
```
  * tomar: comando basico para tomar objetos tirados dentro del escenario y luego seran añadidos al inventario del jugador, puedes tomar de todo, siempre y cuando no sea un almacenador o recipiente (cofres).
```shell
>tomar "nombre del objeto"
```
  * inventario: comando basico para mostrar el contenido del inventario del jugador dentro de un escenario, este enlistara los objetos y su cantidad, tambien mostrara su limite de peso para el jugador y dentro de el puedes hacer mas cosas:
```shell
>inventario
Tienes:
ⵚ moneda x10
ⵚ Manzana
----------------------------------1.5/20
>
```
   - `tirar` comando basico para soltar o quitar un objeto del inventario, con esto lo tiraras y lo dejaras en el lugar actual.
   - `usar` comando basico para aplicar los efectos de un objeto CONSUMIBLE
   - `informacion` tambien puedes mostrar la informacion directamente dentro del inventario funciona igual que informacion en plena ejecucion principal.

  * abrir: comando basico para abrir un recipiente o cofre, este comando muestra y lista el contenido dentro del recipiente, dentro de el puedes:
    
    - `tomar:` comando basico para agregar el objeto a tu inventario. 
    - `dejar:` comando basico para dejar un objeto dentro del recipiente. 
    - `salir:` comando basico para salir del listado de objetos de un recipiente.
    - `inventario:` este comando mostrara el meno de inventario con sus propias ejecuciones.

  * informacion: comando basico para mostrar la informacion y estadisticas de un objeto dentro de tu inventario.
```shell
>informacion "nombre de objeto"
```
  * registros: comando basico para mostrar y listar los registros de combate, un pequeño histrial de lo acontecido.
```shell
⊢---------------------Registros de Batallas----------------------⊣

⊢---------------------Informes----------------------⊣
⌘Batalla entre Mariano y Laura
⌘Turnos: 2
⌘Ganador: Mariano
⌘El contrincante ha sido destruido
⊢---------------------------------------------------⊣

⊢---------------------Informes----------------------⊣
⌘Batalla entre Mariano y Marcelito
⌘Turnos: 6
⌘Ganador: Mariano
⌘El contrincante ha sido dejado vivo
⊢---------------------------------------------------⊣
```
## COMANDOS EN ATAQUE ⚔️

  * atacar: comando basico para iniciar un combate contra un personaje, el combate funciona por turnos en dode se puede atacar y defender, usando como base las habilidades de lucha y la diferencia de nivel entre los contrincantes, al iniciar un combate entraras en un bucle en donde solo podras salir muestro o victorioso, ya que batirce a duelo contra alguien mas no da chance a intentarlo mas tarde.
```shell
>atacar "nombre de la entidad a luchar"
```

_Una vez dentro podras ejecutar los siguientes comandos:_

* atacar: este comando tendra en cuenta el estado del enemigo si esta defendiendoze o no, para luego hacerle daño al contrincante, el sistema de daño se basa en lo siguiente:

1. primero se calcula la ventaja de acurdo al nivel de pelea, en este hay tres estados mayor, menr o igual, en dado caso sea ventaja verdadera, el daño se calcula de la siguiente manera.
```python
      daño_base = self.habilidades["atacar"] * diferencial_nivel
      daño_minimo = daño_base // 2
      daño_final = random.randint(int(daño_minimo), int(daño_base)) - defenza_contrincante
```
      
2. efectuamos daño teniendo en cuenta si esta o no activada la defenza del enemigo, dado caso que la defenza este activa la defenza del contricante se calcula con la habilidad de defenza del contrincante al 70% y se resta al ataque final:
```python
      defenza_contrincante = contrincante.habilidades["defender"]*0.7
```

3. en el segundo caso es que este en desventaja el daño se calcula restando la diferencia de nivel, asi si hay mas difeencia de nivel mas desventaja tendra con respecto a sus habilidades de combate y defenza siguiendo las siguientes formula:
```python
            base_damage = self.skills["attack"] - level_differential
            dégâts_minimum = dégâts_de_base // 2
            final_damage = random.randint(int(minimum_damage), int(base_damage)) - opponent_defense
```
   
4. Les dégâts finaux seront toujours un nombre aléatoire compris entre la moitié des dégâts de compétence et les dégâts de compétence complets, pour le joueur et le PNJ, les dégâts sont calculés de la même manière.

* défendre : Cette commande active le mode défense du joueur et se réinitialise une fois qu'un tour de tours de l'adversaire et du joueur est terminé.

## CARTE 🧭
_⚠️ Cette carte est sujette à des changements et des corrections en fonction de l'évolution de l'histoire._

![Carte du monde](https://github.com/user-attachments/assets/95c7bddc-ec3c-4a8e-800d-a97454dfbf9c)

## Mises à jour 📈

<details>
  <summary>
    <code><strong> 0.1.3 bugs fixed</strong></code>
  </summary>
  <ul>
   <li>Esta versión mejora errores identificados en el flujo de código y también agrega un sistema de administración de peso al inventario del personaje.</li>
   <br>
   <li><b>NEW</b>: Sistema de inventario con gestión del peso de los artículos en el inventario del personaje.</li>
   <br>
   <li><b>NEW</b>: Se ha mejorado el sistema para agregar objetos a una ubicación, permitiendo agregar una lista de objetos o un objeto con el mismo método de la clase de ubicación, lo que ayuda a agregar muchos objetos dentro del mismo método.</li>
   <br>
   <li><b>NEW</b>: Se implementó un sistema de selección y gestión de inventario, ahora puedes soltar o usar elementos en tu inventario, también se agregó la capacidad de mostrar información sobre los elementos en el inventario, para que puedas usar elementos consumibles que modifican las estadísticas del jugador (nueva clase de Consumibles).</li>
   <br>
   <li><b>BUG</b>: Error al tomar varios articulos de la misma clase, anteriormente se sumaba la cantidad del articulo presente en el inventario y se agregaba uno nuevo con cantidad 1, lo cual al mostrar el inventario se mostraba el articulo X2 y articulo, lo cual duplicaba el articulo en el inventario.</li>
   <br>
   <li><b>BUG</b>: Error al decidir no dejar vivo al oponente, crash in game.</li>
   <br>
   <li><b>BUG</b>: Al implementar un nuevo sistema de gestión y visualización de inventario, se han corregido muchos errores en la lógica que agrega elementos al inventario del jugador y elimina elementos. Además, se ha mejorado la forma en que se muestra la información de los objetos añadiendo el peso que tienen con valores flotantes.</li>
  </ul>
</details>

<details>
  <summary>
    <code><strong>0.1.1 update</strong></code>
  </summary>
  <ul>
   <li> <b>NEW</b>: Se implementó el menú principal, permitiendo al jugador elegir iniciar un nuevo juego, guardar, cargar o salir del juego, implementando así el sistema de guardado.</li>
   <br>
   <li><b>NEW</b>: Sistema de lista de juegos guardados en la carpeta "saves" usando "pickler".</li>
   <br>
  </ul>
</details>
   
* `0.1 version `: Esta es la version en la que comienzo a documentar el proceso de creacion en una etapa algo desarrollada del proyecto. 


# Autores ✒️

* [Ellechugista](https://github.com/Ellechugista) - ellechugista(Github)
