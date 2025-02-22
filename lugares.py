class lugar:  
   def __init__(self, nombre:str, descripcion:str):
     self.nombre= nombre
     self.descripcion= descripcion
     self.presentes = []
     self.objetos = []
     self.conexiones = {}

   def presentar_conexiones(self):
     """esto es para mostrar las conexiones disponibles del lugar"""
     print("Puedes ir a:")
     for direccion, lugar in self.conexiones.items():
       print(f" - {direccion}: {lugar.nombre}")
   #objetos en el lugar
   def agregar_objeto(self, objeto):
     self.objetos.append(objeto)
   def quitar_objeto(self, objeto):
     if objeto in self.objetos:
       self.objetos.remove(objeto)
       return True
     else:
       return False
       
   def presentar_lugar(self):
     """esto es para mostrar la info del lugar"""
     #informacion del lugar
     print(f"》Te encuentras en {self.nombre}")
     print(" ")
     print(self.descripcion)
     print(" ")
     #objetos presentes
     if self.objetos:
       print("Aqui hay:")
       for item in self.objetos:
         print(f"@ {item}")
     else:
       print("No hay items en este lugar")
     print(" ")
     #presentar los presentes
     if self.presentes:
       print("Puedes ver:")
       for p in self.presentes:
         print(f" ¤ {p.nombre}")
     else:
       print("Aqui no hay nadie")
     print(" ")
     self.presentar_conexiones()
     print(" ")
     

   
   #agregar un personaje a un lugar, es decir, agregar un presente
   def agregar_entidad(self, personaje):  
     self.presentes.append(personaje)

   def quitar_entidad(self, personaje):
     self.presentes.remove(personaje)

   def conectar_lugar(self,  direccion:str,lugar_destino):
     """esto añade al diccionario direcciones la direccion correspondiente y el objeto lugar para conectarlos"""
     self.conexiones[direccion] = lugar_destino

casa = lugar("Casa Mariano eximilianl Urrutia", "Esta es tu casa aqui vas a lograr ver tus lugros y dormir para reponerte de tu aventura")

if __name__ == "__main__":
   patio= lugar("Patio trasero", "un enorme porton abre un inmenso bosque verde con arboles")

   casa = lugar("Casa Mariano eximilianl Urrutia", "Esta es tu casa aqui vas a lograr ver tus lugros y dormir para reponerte de tu aventura")
   casa.conectar_lugar("este", patio)
   patio.conectar_lugar("oeste", casa)

   casa.presentar_lugar()
