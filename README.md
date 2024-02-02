# CreadorPDF
Programa con 5 herramientas útiles para personas que deseen crear PDFs a partir de imágenes escaneadas dándoles márgenes para su posterior impresión.
## Herramientas
* Creacion de PDF seleccionando la carpeta contenedora de las imagenes a anexar. Esta opcion agrega dos veces cada imagen en la misma pagina, ya que esto es util para las personas que quieren obtener dos ejemplares usando una sola hoja de papel que por lo general se corta a la mitad utilizando una guillotina _Permite elegir la orientacion de pa pagina_.
* Creacion de PDF seleccionando la carpeta contenedora de las imagenes a anexar. Esta opcion agrega una imagen por cada pagina _Permite elegir la orientacion de pa pagina_.
* Herramienta que permite la union de dos archivos PDF, agregando primero las paginas del primer archivo seleccionado y despues las de el segundo archivo seleccionado.
* Herramienta que permite invertir el orden de las paginas, creando un nuevo PDF que su primero pagina sera la ultima del archivo original, y asi sucesivamente.
* Herramienta que permite girar todas las paginas de un documento PDF seleccionado los grados ingresados __en multiplos de 90__

### Librerias necesarias
* **opencv**
* **PyPDF2**
* **reportlab**
* **tkinter**

_Probado y desarrollado en un sistema Windows 11 usando la version de python 3.11.5_
