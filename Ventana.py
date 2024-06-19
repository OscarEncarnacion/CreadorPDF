import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import GeneradorPDF as gp
import logging
import os


class Ventana:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Creador de PDFs")
        self.ventana.geometry("800x600")
        self.ventana.configure(bg = "white")
        self.ventana.iconbitmap("icono.ico")
        self.ventana.resizable(0,0)

        self.creadorPDF = gp.GeneradorPDF()

        # Crear un estilo para las pestañas
        self.style = ttk.Style()
        self.style.configure('TNotebook', background='white')
        self.style.configure('TNotebook.Tab', font=('Arial', 12), padding=[10, 5])

        # Agregar efectos de hover
        self.style.map('TNotebook.Tab', background=[('selected', '#dcdcdc'), ('active', '#e6e6e6')])

        self.controlPestanias = ttk.Notebook(self.ventana, style = 'TNotebook')
        self.pestania1 = ttk.Frame(self.controlPestanias)
        self.pestania2 = ttk.Frame(self.controlPestanias)
        self.pestania3 = ttk.Frame(self.controlPestanias)
        self.pestania4 = ttk.Frame(self.controlPestanias)
        self.pestania5 = ttk.Frame(self.controlPestanias)
        self.pestania6 = ttk.Frame(self.controlPestanias)
        
        self.controlPestanias.add(self.pestania1, text = "Crear PDF")
        self.controlPestanias.add(self.pestania2, text = "Unir PDFs")
        self.controlPestanias.add(self.pestania3, text = "Girar PDF")
        self.controlPestanias.add(self.pestania4, text = "Invertir PDF")
        self.controlPestanias.add(self.pestania5, text = "Borrar margenes")
        self.controlPestanias.add(self.pestania6, text = "Variar densidad")

        self.controlPestanias.pack(expand = 1, fill = "both")

        # Widgets Pestaña 1: Crear PDF desde imagenes
        self.etiquetaPath = Label(self.pestania1, text = "Ruta del directorio de las imagenes: ", font = ("Arial", 12))
        self.etiquetaPath.place(x = 10, y = 10)

        self.entryPath = Entry(self.pestania1, width = 50, font = ("Arial", 12))
        self.entryPath.place(x = 270, y = 10)

        self.botonPath = Button(self.pestania1, text = "...", font = ("Arial", 12), command=lambda: self.seleccionarDirectorio(opcion=1))
        self.botonPath.place(x = 735, y = 10, height=22)

        self.etiquetaTipoPapel = Label(self.pestania1, text = "Tipo de papel: ", font = ("Arial", 12))
        self.etiquetaTipoPapel.place(x = 10, y = 50)

        self.opcionesPapel = ["Carta", "Oficio", "340 x 210 mm", "Doble carta", "Legal", "Legal fake Ricoh", "Personalizado"]
        self.comboboxTipoPapel = ttk.Combobox(self.pestania1, values = self.opcionesPapel, state='readonly', font = ("Arial", 12))
        self.comboboxTipoPapel.current(0)
        self.comboboxTipoPapel.bind("<<ComboboxSelected>>", self.actualizarTipoPapel)
        self.comboboxTipoPapel.place(x = 125, y = 50)

        self.checkVarR = tk.BooleanVar()
        self.checkButtonR = Checkbutton(self.pestania1, text = "En R", variable = self.checkVarR, font = ("Arial", 12))
        self.checkButtonR.place(x = 340, y = 50)

        # Tipo de papel personalizado
        self.etiquetaPersonalizadoX = Label(self.pestania1, text = "Tamaño.   X: ", font = ("Arial", 12), state=DISABLED)

        self.spinboxTamanioX = Spinbox(self.pestania1, from_=33, to=5080, increment=1, width = 5, font = ("Arial", 12), state=DISABLED)

        self.etiquetaPersonalizadoXmm = Label(self.pestania1, text = "mm", font = ("Arial", 12), state=DISABLED)

        self.etiquetaPersonalizadoY = Label(self.pestania1, text = "Y: ", font = ("Arial", 12), state=DISABLED)

        self.spinboxTamanioY = Spinbox(self.pestania1, from_=33, to=5080, increment=1, width = 5, font = ("Arial", 12), state=DISABLED)

        self.etiquetaPersonalizadoYmm = Label(self.pestania1, text = "mm", font = ("Arial", 12), state=DISABLED)

        self.checkVarDosLados = tk.BooleanVar()
        self.checkVarDosLados.trace("w", self.actualizarDosLados)
        self.checkButtonDosLados = Checkbutton(self.pestania1, text = "Margenes diferentes para paginas nones y pares", variable = self.checkVarDosLados, font = ("Arial", 12))
        self.checkButtonDosLados.place(x = 10, y = 90)

        self.checkVarRepeticion = tk.BooleanVar()
        self.checkButtonRepeticion = Checkbutton(self.pestania1, text = "Repeticion", variable = self.checkVarRepeticion, font = ("Arial", 12), foreground="red")
        self.checkButtonRepeticion.place(x = 450, y = 90)

        # Margenes frente
        self.etiquetaMargenFrenteIzquierda = Label(self.pestania1, text = "mm", font = ("Arial", 12))
        self.etiquetaMargenFrenteIzquierda.place(x = 70, y = 245)
        self.spinboxMargenFrenteIzquierda = Spinbox(self.pestania1, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12))
        self.spinboxMargenFrenteIzquierda.place(x = 10, y = 245)

        self.etiquetaMargenFrenteSuperior = Label(self.pestania1, text = "mm", font = ("Arial", 12))
        self.etiquetaMargenFrenteSuperior.place(x = 200, y = 150)
        self.spinboxMargenFrenteSuperior = Spinbox(self.pestania1, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12))
        self.spinboxMargenFrenteSuperior.place(x = 140, y = 150)

        self.etiquetaMargenFrenteDerecha = Label(self.pestania1, text = "mm", font = ("Arial", 12))
        self.etiquetaMargenFrenteDerecha.place(x = 327, y = 245)
        self.spinboxMargenFrenteDerecha = Spinbox(self.pestania1, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12))
        self.spinboxMargenFrenteDerecha.place(x = 267, y = 245)

        self.etiquetaMargenFrenteInferior = Label(self.pestania1, text = "mm", font = ("Arial", 12))
        self.etiquetaMargenFrenteInferior.place(x = 200, y = 343)
        self.spinboxMargenFrenteInferior = Spinbox(self.pestania1, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12))
        self.spinboxMargenFrenteInferior.place(x = 140, y = 343)

        # Margenes vuelta
        self.etiquetaMargenVueltaIzquierda = Label(self.pestania1, text = "mm", font = ("Arial", 12), state = DISABLED)
        self.etiquetaMargenVueltaIzquierda.place(x = 465, y = 245)
        self.spinboxMargenVueltaIzquierda = Spinbox(self.pestania1, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12), state=DISABLED)
        self.spinboxMargenVueltaIzquierda.place(x = 405, y = 245)

        self.etiquetaMargenVueltaSuperior = Label(self.pestania1, text = "mm", font = ("Arial", 12), state = DISABLED)
        self.etiquetaMargenVueltaSuperior.place(x = 595, y = 150)
        self.spinboxMargenVueltaSuperior = Spinbox(self.pestania1, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12), state=DISABLED)
        self.spinboxMargenVueltaSuperior.place(x = 535, y = 150)

        self.etiquetaMargenVueltaDerecha = Label(self.pestania1, text = "mm", font = ("Arial", 12), state = DISABLED)
        self.etiquetaMargenVueltaDerecha.place(x = 722, y = 245)
        self.spinboxMargenVueltaDerecha = Spinbox(self.pestania1, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12), state=DISABLED)
        self.spinboxMargenVueltaDerecha.place(x = 662, y = 245)

        self.etiquetaMargenVueltaInferior = Label(self.pestania1, text = "mm", font = ("Arial", 12), state = DISABLED)
        self.etiquetaMargenVueltaInferior.place(x = 595, y = 343)
        self.spinboxMargenVueltaInferior = Spinbox(self.pestania1, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12), state=DISABLED)
        self.spinboxMargenVueltaInferior.place(x = 535, y = 343) # Como el halo jeje

        self.canvasCuadro1 = tk.Canvas(self.pestania1, width=151, height=151)
        self.canvasCuadro1.place(x=105, y=180)
        self.dibujarFigura(self.canvasCuadro1, 2, 2, 150)

        self.canvasCuadro2 = tk.Canvas(self.pestania1, width=151, height=151, state=DISABLED)
        self.canvasCuadro2.place(x=500, y=180)
        self.dibujarFigura(self.canvasCuadro2, 2, 2, 150)

        self.informacion = "Nota: los margenes deben de ser ingresados tomando la orientacion de la imagen original de referencia, independientemente de la " + \
        "orientacion del pdf creado. Ademas al seleccionar la opcion de repeticion, los margenes se repetiran en cada una de las dos partes de la repeticion."
        self.etiquetaInformacion = Label(self.pestania1, text = self.informacion, font = ("Arial", 12), wraplength=780, justify=LEFT)
        self.etiquetaInformacion.place(x = 10, y = 400)

        self.botonCrearPDF = Button(self.pestania1, text = "Crear PDF", font = ("Arial", 12), background="green", foreground="white", command=lambda: self.ejecutar(proceso=1))
        self.botonCrearPDF.place(x = 670, y = 500)

        # Widgets Pestaña 2: Unir PDFs
        self.etiquetaPathUnir = Label(self.pestania2, text = "Ruta del PDF: ", font = ("Arial", 12))
        self.etiquetaPathUnir.place(x = 10, y = 10)

        self.entryPathUnir = Entry(self.pestania2, width = 70, font = ("Arial", 10))
        self.entryPathUnir.place(x = 120, y = 10)

        self.botonPathUnir = Button(self.pestania2, text = "...", font = ("Arial", 12), command=lambda: self.seleccionarPDF(opcion=1))
        self.botonPathUnir.place(x = 623, y = 10, height=22)

        self.rutasPDFs = []
        self.botonAgregarUnir = Button(self.pestania2, text = "Agregar", font = ("Arial", 12), command = self.agregarNombrePDF)
        self.botonAgregarUnir.place(x = 660, y = 10, height=22)

        self.etiquetaListaPDFs = Label(self.pestania2, text = "", font = ("Arial", 11), wraplength=780, justify=LEFT)
        self.etiquetaListaPDFs.place(x = 10, y = 50)

        self.checkVarInvertir = tk.BooleanVar()
        self.checkButtonInvertir = Checkbutton(self.pestania2, text = "Invertir paginas al finalizar", variable = self.checkVarInvertir, font = ("Arial", 12))
        self.checkButtonInvertir.place(x = 10, y = 500)

        self.botonUnirPDFs = Button(self.pestania2, text = "Unir PDFs", font = ("Arial", 12), background="green", foreground="white", command=lambda: self.ejecutar(proceso=2))
        self.botonUnirPDFs.place(x = 670, y = 500)

        # Widgets Pestaña 3: Girar PDF
        self.etiquetaPathGirar = Label(self.pestania3, text = "Ruta del PDF: ", font = ("Arial", 12))
        self.etiquetaPathGirar.place(x = 10, y = 10)

        self.entryPathGirar = Entry(self.pestania3, width = 70, font = ("Arial", 10))
        self.entryPathGirar.place(x = 120, y = 10)

        self.botonPathGirar = Button(self.pestania3, text = "...", font = ("Arial", 12), command=lambda: self.seleccionarPDF(opcion=2))
        self.botonPathGirar.place(x = 623, y = 10, height=22)

        self.etiquetaGirarGrados = Label(self.pestania3, text = "Seleccionar los grados que quiere girar su documento.", font = ("Arial", 12))
        self.etiquetaGirarGrados.place(x = 10, y = 50)
        self.spinboxGirarGrados = Spinbox(self.pestania3, from_=0, to=270, increment=90, width = 4, font = ("Arial", 12))
        self.spinboxGirarGrados.place(x = 400, y = 50)

        self.checkVarGirarDiferente = tk.BooleanVar()
        self.checkVarGirarDiferente.trace("w", self.actualizarGirarDiferente)
        self.checkButtonGirarDiferente = Checkbutton(self.pestania3, text = "Girar diferentes grados para las paginas nones y pares.", variable = self.checkVarGirarDiferente, font = ("Arial", 12))
        self.checkButtonGirarDiferente.place(x = 10, y = 90)

        self.etiquetaGirarGradosPares = Label(self.pestania3, text = "Seleccionar los grados que quiere girar las paginas pares de su documento.", font = ("Arial", 12), state=DISABLED)
        self.etiquetaGirarGradosPares.place(x = 10, y = 130)
        self.spinboxGirarGradosPares = Spinbox(self.pestania3, from_=0, to=270, increment=90, width = 4, font = ("Arial", 12), state=DISABLED)
        self.spinboxGirarGradosPares.place(x = 550, y = 130)

        self.botonGirarPDF = Button(self.pestania3, text = "Girar PDF", font = ("Arial", 12), background="green", foreground="white", command=lambda: self.ejecutar(proceso=3))
        self.botonGirarPDF.place(x = 670, y = 500)

        # Widgets Pestaña 4: Invertir PDF
        self.etiquetaPathInvertir = Label(self.pestania4, text = "Ruta del PDF: ", font = ("Arial", 12))
        self.etiquetaPathInvertir.place(x = 10, y = 10)

        self.entryPathInvertir = Entry(self.pestania4, width = 70, font = ("Arial", 10))
        self.entryPathInvertir.place(x = 120, y = 10)

        self.botonPathInvertir = Button(self.pestania4, text = "...", font = ("Arial", 12), command=lambda: self.seleccionarPDF(opcion=3))
        self.botonPathInvertir.place(x = 623, y = 10, height=22)

        self.botonInvertirPDF = Button(self.pestania4, text = "Invertir PDF", font = ("Arial", 12), background="green", foreground="white", command=lambda: self.ejecutar(proceso=4))
        self.botonInvertirPDF.place(x = 670, y = 500)

        # Widgets Pestaña 5: Borrar margenes
        self.etiquetaPathBorrar = Label(self.pestania5, text = "Ruta del directorio de las imagenes: ", font = ("Arial", 12))
        self.etiquetaPathBorrar.place(x = 10, y = 10)

        self.entryPathBorrar = Entry(self.pestania5, width = 50, font = ("Arial", 12))
        self.entryPathBorrar.place(x = 270, y = 10)

        self.botonPathBorrar = Button(self.pestania5, text = "...", font = ("Arial", 12), command=lambda: self.seleccionarDirectorio(opcion=2))
        self.botonPathBorrar.place(x = 735, y = 10, height=22)

        self.checkVarBorrarDosLados = tk.BooleanVar()
        self.checkVarBorrarDosLados.trace("w", self.actualizarBorrarDosLados)
        self.checkButtonBorrarDosLados = Checkbutton(self.pestania5, text = "Borrar margenes diferentes para imagenes nones y pares", variable = self.checkVarBorrarDosLados, font = ("Arial", 12))
        self.checkButtonBorrarDosLados.place(x = 10, y = 50)

        # Borrar margenes frente
        self.etiquetaBorrarMargenFrenteIzquierda = Label(self.pestania5, text = "px", font = ("Arial", 12))
        self.etiquetaBorrarMargenFrenteIzquierda.place(x = 70, y = 205)
        self.spinboxBorrarMargenFrenteIzquierda = Spinbox(self.pestania5, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12))
        self.spinboxBorrarMargenFrenteIzquierda.place(x = 10, y = 205)

        self.etiquetaBorrarMargenFrenteSuperior = Label(self.pestania5, text = "px", font = ("Arial", 12))
        self.etiquetaBorrarMargenFrenteSuperior.place(x = 200, y = 110)
        self.spinboxBorrarMargenFrenteSuperior = Spinbox(self.pestania5, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12))
        self.spinboxBorrarMargenFrenteSuperior.place(x = 140, y = 110)

        self.etiquetaBorrarMargenFrenteDerecha = Label(self.pestania5, text = "px", font = ("Arial", 12))
        self.etiquetaBorrarMargenFrenteDerecha.place(x = 327, y = 205)
        self.spinboxBorrarMargenFrenteDerecha = Spinbox(self.pestania5, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12))
        self.spinboxBorrarMargenFrenteDerecha.place(x = 267, y = 205)

        self.etiquetaBorrarMargenFrenteInferior = Label(self.pestania5, text = "px", font = ("Arial", 12))
        self.etiquetaBorrarMargenFrenteInferior.place(x = 200, y = 303)
        self.spinboxBorrarMargenFrenteInferior = Spinbox(self.pestania5, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12))
        self.spinboxBorrarMargenFrenteInferior.place(x = 140, y = 303)

        # Borrar margenes vuelta
        self.etiquetaBorrarMargenVueltaIzquierda = Label(self.pestania5, text = "px", font = ("Arial", 12), state = DISABLED)
        self.etiquetaBorrarMargenVueltaIzquierda.place(x = 465, y = 205)
        self.spinboxBorrarMargenVueltaIzquierda = Spinbox(self.pestania5, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12), state=DISABLED)
        self.spinboxBorrarMargenVueltaIzquierda.place(x = 405, y = 205)

        self.etiquetaBorrarMargenVueltaSuperior = Label(self.pestania5, text = "px", font = ("Arial", 12), state = DISABLED)
        self.etiquetaBorrarMargenVueltaSuperior.place(x = 595, y = 110)
        self.spinboxBorrarMargenVueltaSuperior = Spinbox(self.pestania5, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12), state=DISABLED)
        self.spinboxBorrarMargenVueltaSuperior.place(x = 535, y = 110)

        self.etiquetaBorrarMargenVueltaDerecha = Label(self.pestania5, text = "px", font = ("Arial", 12), state = DISABLED)
        self.etiquetaBorrarMargenVueltaDerecha.place(x = 722, y = 205)
        self.spinboxBorrarMargenVueltaDerecha = Spinbox(self.pestania5, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12), state=DISABLED)
        self.spinboxBorrarMargenVueltaDerecha.place(x = 662, y = 205)

        self.etiquetaBorrarMargenVueltaInferior = Label(self.pestania5, text = "px", font = ("Arial", 12), state = DISABLED)
        self.etiquetaBorrarMargenVueltaInferior.place(x = 595, y = 303)
        self.spinboxBorrarMargenVueltaInferior = Spinbox(self.pestania5, from_=0, to=300, increment=1, width = 4, font = ("Arial", 12), state=DISABLED)
        self.spinboxBorrarMargenVueltaInferior.place(x = 535, y = 303)

        self.canvasBorrarCuadro1 = tk.Canvas(self.pestania5, width=151, height=151)
        self.canvasBorrarCuadro1.place(x=105, y=140)
        self.dibujarFigura(self.canvasBorrarCuadro1, 2, 2, 150)

        self.canvasBorrarCuadro2 = tk.Canvas(self.pestania5, width=151, height=151, state=DISABLED)
        self.canvasBorrarCuadro2.place(x=500, y=140)
        self.dibujarFigura(self.canvasBorrarCuadro2, 2, 2, 150)

        self.informacionBorrar = "Nota: los margenes deben de ser ingresados tomando la orientacion de la imagen original de referencia."
        self.etiquetaBorrarInformacion = Label(self.pestania5, text = self.informacionBorrar, font = ("Arial", 12), wraplength=780, justify=LEFT)
        self.etiquetaBorrarInformacion.place(x = 10, y = 360)

        self.botonBorrarMargenes = Button(self.pestania5, text = "Borrar margenes", font = ("Arial", 12), background="green", foreground="white", command=lambda: self.ejecutar(proceso=5))
        self.botonBorrarMargenes.place(x = 630, y = 500)

        # Widgets Pestaña 6: Variar densidad
        self.etiquetaPathDensidad = Label(self.pestania6, text = "Ruta del directorio: ", font = ("Arial", 12))
        self.etiquetaPathDensidad.place(x = 10, y = 10)

        self.entryPathDensidad = Entry(self.pestania6, width = 70, font = ("Arial", 10))
        self.entryPathDensidad.place(x = 150, y = 10)

        self.botonPathDensidad = Button(self.pestania6, text = "...", font = ("Arial", 12), command=lambda: self.seleccionarDirectorio(opcion=3))
        self.botonPathDensidad.place(x = 653, y = 10, height=22)

        self.etiquetaDensidad = Label(self.pestania6, text = "Seleccionar el nivel de densidad a sumar:", font = ("Arial", 12))
        self.etiquetaDensidad.place(x = 10, y = 50)
        self.spinboxDensidad = Spinbox(self.pestania6, from_=-254, to=254,increment=1, width = 5, font = ("Arial", 12))
        self.spinboxDensidad.delete(0, "end")
        self.spinboxDensidad.insert(0, 0)
        self.spinboxDensidad.place(x = 310, y = 50)

        self.etiquetaVariante = Label(self.pestania6, text = "Seleccionar la intensidad de blanco a ignorar:", font = ("Arial", 12))
        self.etiquetaVariante.place(x = 10, y = 90)
        self.spinboxVariante = Spinbox(self.pestania6, from_=0, to=255,increment=1, width = 5, font = ("Arial", 12))
        self.spinboxVariante.place(x = 338, y = 90)

        self.informacionDensidad = "Nota: El rango de aumento de densidad es de +-255 mientras que la variacion del blanco es de 0-255, sin embargo " + \
        "los pixeles que se consideran blancos la mayoria de las veces toman un valor mayor a 240"
        self.etiquetaInformacionDensidad = Label(self.pestania6, text = self.informacionDensidad, font = ("Arial", 12), wraplength=780, justify=LEFT)
        self.etiquetaInformacionDensidad.place(x = 10, y = 140)

        self.botonCrearDensidad = Button(self.pestania6, text = "Alterar densidad", font = ("Arial", 12), background="green", foreground="white", command=lambda: self.ejecutar(proceso=6))
        self.botonCrearDensidad.place(x = 630, y = 500)

        self.ventana.protocol("WM_DELETE_WINDOW", self.antesDeCerrar)
        
        logging.info("Ventana inicializada")

        self.ventana.mainloop()
    
    def antesDeCerrar(self):
        logging.info("Ventana cerrada")
        self.ventana.destroy()

    def seleccionarDirectorio(self, opcion):
        directorio = filedialog.askdirectory()
        if opcion == 1:
            if directorio:
                self.entryPath.delete(0, tk.END)
                self.entryPath.insert(0, directorio)
        elif opcion == 2:
            if directorio:
                self.entryPathBorrar.delete(0, tk.END)
                self.entryPathBorrar.insert(0, directorio)
        elif opcion == 3:
            if directorio:
                self.entryPathDensidad.delete(0, tk.END)
                self.entryPathDensidad.insert(0, directorio)

    def dibujarFigura(self, canvas, x1, y1, lado):
        x2 = x1 + lado
        y2 = y1 + lado
        canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
    
    def actualizarDosLados(self, *args):
        if self.checkVarDosLados.get():
            self.canvasCuadro2.config(state=NORMAL)
            self.etiquetaMargenVueltaIzquierda.config(state=NORMAL)
            self.spinboxMargenVueltaIzquierda.config(state=NORMAL)
            self.etiquetaMargenVueltaSuperior.config(state=NORMAL)
            self.spinboxMargenVueltaSuperior.config(state=NORMAL)
            self.etiquetaMargenVueltaDerecha.config(state=NORMAL)
            self.spinboxMargenVueltaDerecha.config(state=NORMAL)
            self.etiquetaMargenVueltaInferior.config(state=NORMAL)
            self.spinboxMargenVueltaInferior.config(state=NORMAL)
        else:
            self.canvasCuadro2.config(state=DISABLED)
            self.etiquetaMargenVueltaIzquierda.config(state=DISABLED)
            self.spinboxMargenVueltaIzquierda.config(state=DISABLED)
            self.etiquetaMargenVueltaSuperior.config(state=DISABLED)
            self.spinboxMargenVueltaSuperior.config(state=DISABLED)
            self.etiquetaMargenVueltaDerecha.config(state=DISABLED)
            self.spinboxMargenVueltaDerecha.config(state=DISABLED)
            self.etiquetaMargenVueltaInferior.config(state=DISABLED)
            self.spinboxMargenVueltaInferior.config(state=DISABLED)

    def actualizarBorrarDosLados(self, *args):
        if self.checkVarBorrarDosLados.get():
            self.canvasBorrarCuadro2.config(state=NORMAL)
            self.etiquetaBorrarMargenVueltaIzquierda.config(state=NORMAL)
            self.spinboxBorrarMargenVueltaIzquierda.config(state=NORMAL)
            self.etiquetaBorrarMargenVueltaSuperior.config(state=NORMAL)
            self.spinboxBorrarMargenVueltaSuperior.config(state=NORMAL)
            self.etiquetaBorrarMargenVueltaDerecha.config(state=NORMAL)
            self.spinboxBorrarMargenVueltaDerecha.config(state=NORMAL)
            self.etiquetaBorrarMargenVueltaInferior.config(state=NORMAL)
            self.spinboxBorrarMargenVueltaInferior.config(state=NORMAL)
        else:
            self.canvasBorrarCuadro2.config(state=DISABLED)
            self.etiquetaBorrarMargenVueltaIzquierda.config(state=DISABLED)
            self.spinboxBorrarMargenVueltaIzquierda.config(state=DISABLED)
            self.etiquetaBorrarMargenVueltaSuperior.config(state=DISABLED)
            self.spinboxBorrarMargenVueltaSuperior.config(state=DISABLED)
            self.etiquetaBorrarMargenVueltaDerecha.config(state=DISABLED)
            self.spinboxBorrarMargenVueltaDerecha.config(state=DISABLED)
            self.etiquetaBorrarMargenVueltaInferior.config(state=DISABLED)
            self.spinboxBorrarMargenVueltaInferior.config(state=DISABLED)

    def actualizarGirarDiferente(self, *args):
        if self.checkVarGirarDiferente.get():
            self.etiquetaGirarGradosPares.config(state=NORMAL)
            self.spinboxGirarGradosPares.config(state=NORMAL)
        else:
            self.etiquetaGirarGradosPares.config(state=DISABLED)
            self.spinboxGirarGradosPares.config(state=DISABLED)

    def agregarNombrePDF(self):
        if len(self.rutasPDFs) > 20:
            tk.messagebox.showerror("Error", "No se pueden agregar mas de 20 PDFs")
            self.entryPathUnir.delete(0, tk.END)
            return
        else:
            if self.entryPathUnir.get():
                self.rutasPDFs.append(self.entryPathUnir.get())
                self.entryPathUnir.delete(0, tk.END)
                self.etiquetaListaPDFs.config(text = "\n".join(self.rutasPDFs))

    def seleccionarPDF(self, opcion):
        rutaPDF = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if rutaPDF:
            if opcion == 1:
                self.entryPathUnir.delete(0, tk.END)
                self.entryPathUnir.insert(0, rutaPDF)
            elif opcion == 2:
                self.entryPathGirar.delete(0, tk.END)
                self.entryPathGirar.insert(0, rutaPDF)
            else:
                self.entryPathInvertir.delete(0, tk.END)
                self.entryPathInvertir.insert(0, rutaPDF)

    def actualizarTipoPapel(self, *args):
        if self.comboboxTipoPapel.current() == 6:
            self.etiquetaPersonalizadoX.config(state=NORMAL)
            self.spinboxTamanioX.config(state=NORMAL)
            self.etiquetaPersonalizadoXmm.config(state=NORMAL)
            self.etiquetaPersonalizadoY.config(state=NORMAL)
            self.spinboxTamanioY.config(state=NORMAL)
            self.etiquetaPersonalizadoYmm.config(state=NORMAL)
            self.etiquetaPersonalizadoX.place(x = 410, y = 50)
            self.spinboxTamanioX.place(x = 505, y = 50)
            self.etiquetaPersonalizadoXmm.place(x = 570, y = 50)
            self.etiquetaPersonalizadoY.place(x = 620, y = 50)
            self.spinboxTamanioY.place(x = 640, y = 50)
            self.etiquetaPersonalizadoYmm.place(x = 705, y = 50)
        else:
            self.etiquetaPersonalizadoX.config(state=DISABLED)
            self.spinboxTamanioX.config(state=DISABLED)
            self.etiquetaPersonalizadoXmm.config(state=DISABLED)
            self.etiquetaPersonalizadoY.config(state=DISABLED)
            self.spinboxTamanioY.config(state=DISABLED)
            self.etiquetaPersonalizadoYmm.config(state=DISABLED)
            self.etiquetaPersonalizadoX.place_forget()
            self.spinboxTamanioX.place_forget()
            self.etiquetaPersonalizadoXmm.place_forget()
            self.etiquetaPersonalizadoY.place_forget()
            self.spinboxTamanioY.place_forget()
            self.etiquetaPersonalizadoYmm.place_forget()
    
    def ejecutar(self, proceso):
        try:
            self.creadorPDF.limpiarAtributos()
            if proceso == 1: # Crear PDF desde imagenes
                self.creadorPDF.pathDirectorio = self.entryPath.get()
                self.creadorPDF.pathSalida = filedialog.asksaveasfilename(defaultextension=".pdf")
                self.creadorPDF.tipoPapel = self.comboboxTipoPapel.current()
                if self.comboboxTipoPapel.current() == 6:
                    self.creadorPDF.tipoPersonalizado = [int(self.spinboxTamanioX.get()), int(self.spinboxTamanioY.get())]
                self.creadorPDF.margenesAnverso = [int(self.spinboxMargenFrenteIzquierda.get()), int(self.spinboxMargenFrenteSuperior.get()), int(self.spinboxMargenFrenteDerecha.get()), int(self.spinboxMargenFrenteInferior.get())]
                if self.checkVarDosLados.get():
                    self.creadorPDF.margenesReverso = [int(self.spinboxMargenVueltaIzquierda.get()), int(self.spinboxMargenVueltaSuperior.get()), int(self.spinboxMargenVueltaDerecha.get()), int(self.spinboxMargenVueltaInferior.get())]
                self.creadorPDF.dosLados = self.checkVarDosLados.get()
                self.creadorPDF.archivoSalidaEnR = self.checkVarR.get()
                if self.checkVarRepeticion.get():
                    self.creadorPDF.crearPdfImagenesRepeticion()
                else:
                    self.creadorPDF.crearPdfImagenes()
                tk.messagebox.showinfo("Informacion", f"PDF creado en {self.creadorPDF.pathSalida}")
                os.startfile(self.creadorPDF.pathSalida)
            elif proceso == 2: # Unir PDFs
                self.creadorPDF.pathsPDFs = self.rutasPDFs
                self.creadorPDF.pathSalida = filedialog.asksaveasfilename(defaultextension=".pdf")
                self.creadorPDF.unirPDFs()
                tk.messagebox.showinfo("Informacion", f"PDF creado en {self.creadorPDF.pathSalida}")
                os.startfile(self.creadorPDF.pathSalida)
            elif proceso == 3: # Girar PDF
                self.creadorPDF.pathPDF = self.entryPathGirar.get()
                self.creadorPDF.grados = int(self.spinboxGirarGrados.get())
                self.creadorPDF.gradosPares = int(self.spinboxGirarGradosPares.get())
                self.creadorPDF.girarDiferente = self.checkVarGirarDiferente.get()
                self.creadorPDF.pathSalida = filedialog.asksaveasfilename(defaultextension=".pdf")
                self.creadorPDF.girarPaginas()
                tk.messagebox.showinfo("Informacion", f"PDF creado en {self.creadorPDF.pathSalida}")
                os.startfile(self.creadorPDF.pathSalida)
            elif proceso == 4: # Invertir PDF
                self.creadorPDF.pathPDF = self.entryPathInvertir.get()
                self.creadorPDF.pathSalida = filedialog.asksaveasfilename(defaultextension=".pdf")
                self.creadorPDF.invertirPDF()
                tk.messagebox.showinfo("Informacion", f"PDF creado en {self.creadorPDF.pathSalida}")
                os.startfile(self.creadorPDF.pathSalida)
            elif proceso == 5: # Borrar margenes
                self.creadorPDF.pathDirectorio = self.entryPathBorrar.get()
                self.creadorPDF.margenesAnverso = [int(self.spinboxBorrarMargenFrenteIzquierda.get()), int(self.spinboxBorrarMargenFrenteSuperior.get()), int(self.spinboxBorrarMargenFrenteDerecha.get()), int(self.spinboxBorrarMargenFrenteInferior.get())]
                self.creadorPDF.margenesReverso = [int(self.spinboxBorrarMargenVueltaIzquierda.get()), int(self.spinboxBorrarMargenVueltaSuperior.get()), int(self.spinboxBorrarMargenVueltaDerecha.get()), int(self.spinboxBorrarMargenVueltaInferior.get())]
                self.creadorPDF.dosLados = self.checkVarBorrarDosLados.get()
                self.creadorPDF.borrarMargenes()
                tk.messagebox.showinfo("Informacion", "Margenes borrados correctamente")
                os.startfile(self.creadorPDF.getDirectorioSalida())
            elif proceso == 6: # Variar densidad
                self.creadorPDF.pathDirectorio = self.entryPathDensidad.get()
                self.creadorPDF.densidad = -int(self.spinboxDensidad.get())
                self.creadorPDF.varianteBlanco = int(self.spinboxVariante.get())
                self.creadorPDF.variarDensidad()
                tk.messagebox.showinfo("Informacion", "Densidad alterada correctamente")
                os.startfile(self.creadorPDF.getDirectorioSalida())
        except Exception as e:
            logging.error(f"Error: {e}")
            tk.messagebox.showerror("Error en la ejecucion", f"Revice el archivo log para encontrar el posible motivo.\nError: {e}")