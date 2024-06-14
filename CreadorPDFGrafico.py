import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import cv2, os
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
import logging
import numpy as np

# Configuración del logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class GeneradorPDF:
    def __init__(self):
        self.pathDirectorio = ""
        self.pathPDF = ""
        self.pathsPDFs = []
        self.pathSalida = ""
        self.tipoPapel = 0
        self.tipoPersonalizado = [0, 0]
        self.margenesAnverso = [0, 0, 0, 0]
        self.margenesReverso = [0, 0, 0, 0]
        self.dosLados = False
        self.archivoSalidaEnR = False
        self.grados = 0

    def crearPdfImagenes(self):
        logging.info("Iniciando el proceso de creacion de PDF...")
        imagenes = [f for f in os.listdir(self.pathDirectorio) if f.endswith(('.jpg', '.JPG', '.png', '.jpeg', '.tif'))]
        logging.info(f"Se encontraron {len(imagenes)} imagenes.")
        with open(self.pathSalida, 'wb') as canvas_file:
            imagen_path = os.path.join(self.pathDirectorio, imagenes[0])
            img = cv2.imread(imagen_path)
            h, w, c = img.shape
            originalR = False
            if w > h:
                originalR = True
            logging.info(f"Tamanio de la primera imagen original = {w} x {h}")
            w = 0
            h = 0
            # Oficio
            if self.tipoPapel == 1:
                if originalR:
                    w = 965
                    h = 612
                else:
                    w = 612
                    h = 965
            # 340 x 210 mm
            elif self.tipoPapel == 2:
                if originalR:
                    w = 340 * mm
                    h = 210 * mm
                else:
                    w = 210 * mm
                    h = 340 * mm
            # Doble carta
            elif self.tipoPapel == 3:
                if originalR:
                    w = 17 * inch
                    h = 11 * inch
                else:
                    w = 11 * inch
                    h = 17 * inch
            # Legal
            elif self.tipoPapel == 4:
                if originalR:
                    w = 14 * inch
                    h = 8.5 * inch
                else:
                    w = 8.5 * inch
                    h = 14 * inch
            # Legal fake Ricoh
            elif self.tipoPapel == 5:
                if originalR:
                    w = 340.4 * mm
                    wF = 14 * inch
                    h = 8.5 * inch
                    hF = h
                else:
                    w = 8.5 * inch
                    wF = w
                    h = 340.4 * mm
                    hF = 14 * inch
            # Personalizado
            elif self.tipoPapel == 6:
                if originalR:
                    if self.tipoPersonalizado[0] > self.tipoPersonalizado[1]:
                        w = self.tipoPersonalizado[0] * mm
                        h = self.tipoPersonalizado[1] * mm
                    else:
                        w = self.tipoPersonalizado[1] * mm
                        h = self.tipoPersonalizado[0] * mm
                else:
                    if self.tipoPersonalizado[0] > self.tipoPersonalizado[1]:
                        w = self.tipoPersonalizado[1] * mm
                        h = self.tipoPersonalizado[0] * mm
                    else:
                        w = self.tipoPersonalizado[0] * mm
                        h = self.tipoPersonalizado[1] * mm
            # Carta
            else:
                if originalR:
                    w = 11 * inch
                    h = 8.5 * inch
                else:
                    w = 8.5 * inch
                    h = 11 * inch
            logging.info(f"\nAncho de la pagina en puntos = {w}")
            logging.info(f"Alto de la pagina en puntos = {h}")
            logging.info("punto = 1/72 pulgada")
            logging.info("Iniciando el proceso de creacion de PDF...")
            anversoX = self.margenesAnverso[0] * mm
            reversoX = self.margenesReverso[0] * mm
            anversoY = self.margenesAnverso[3] * mm
            reversoY = self.margenesReverso[3] * mm
            if originalR:
                if self.tipoPapel == 6:
                    anversoX = anversoX + (.6 * inch)
                    reversoX = reversoX + (.6 * inch)
            tamanioAX = w - ((self.margenesAnverso[0] + self.margenesAnverso[2]) * mm)
            tamanioAY = round(h - ((self.margenesAnverso[1] + self.margenesAnverso[3]) * mm))
            tamanioRX = w - ((self.margenesReverso[0] + self.margenesReverso[2]) * mm)
            tamanioRY = round(h - ((self.margenesReverso[1] + self.margenesReverso[3]) * mm))
            if self.tipoPapel == 6:
                pdf_canvas = canvas.Canvas(canvas_file, (wF, hF))
            else:
                pdf_canvas = canvas.Canvas(canvas_file, (w, h))
            contador = 0
            logging.info("Inicio")
            for imagen in imagenes:
                imagen_path = os.path.join(self.pathDirectorio, imagen)
                if self.dosLados == True:
                    if contador % 2 == 0:
                        # Anverso
                        pdf_canvas.drawImage(imagen_path, anversoX, anversoY, width=tamanioAX, height=tamanioAY)
                    else:
                        # Reverso
                        pdf_canvas.drawImage(imagen_path, reversoX, reversoY, width=tamanioRX, height=tamanioRY)
                else:
                    # Anverso solamente
                    pdf_canvas.drawImage(imagen_path, anversoX, anversoY, width=tamanioAX, height=tamanioAY)
                pdf_canvas.showPage()
                contador += 1
                logging.info(f"{contador}")
            pdf_canvas.save()
        if self.archivoSalidaEnR and not originalR:
            self.girarPaginas(self.pathSalida, 270)
        if not self.archivoSalidaEnR and originalR:
            self.girarPaginas(self.pathSalida, 90)
        logging.info(f"El pdf se ha creado en {self.pathSalida}.")
    
    def crearPdfImagenesRepeticion(self):
        logging.info("Iniciando el proceso de creacion de PDF en repeticion...")
        imagenes = [f for f in os.listdir(self.pathDirectorio) if f.endswith(('.jpg', '.JPG', '.png', '.jpeg', '.tif'))]
        logging.info(f"\nSe encontraron {len(imagenes)} imagenes.")
        with open(self.pathSalida, 'wb') as canvas_file:
            imagen_path = os.path.join(self.pathDirectorio, imagenes[0])
            img = cv2.imread(imagen_path)
            hP, wP, c = img.shape
            originalR = False
            if wP > hP:
                originalR = True
            logging.info(f"Tamanio de la primera imagen original = {wP} x {hP}")
            w = 0
            h = 0
            # Oficio
            if self.tipoPapel == 1:
                if originalR:
                    w = 612
                    h = 965
                else:
                    w = 965
                    h = 612
            # 340 x 210 mm
            elif self.tipoPapel == 2:
                if originalR:
                    w = 210 * mm
                    h = 340 * mm
                else:
                    w = 340 * mm
                    h = 210 * mm
            # Doble carta
            elif self.tipoPapel == 3:
                if originalR:
                    w = 11 * inch
                    h = 17 * inch
                else:
                    w = 17 * inch
                    h = 11 * inch
            # Legal
            elif self.tipoPapel == 4:
                if originalR:
                    w = 8.5 * inch
                    h = 14 * inch
                else:
                    w = 14 * inch
                    h = 8.5 * inch
            # Legal fake Ricoh
            elif self.tipoPapel == 5:
                if originalR:
                    w = 8.5 * inch
                    wF = w
                    h = 340.4 * mm
                    hF = 14 * inch
                else:
                    w = 340.4 * mm
                    wF = 14 * inch
                    h = 8.5 * inch
                    hF = h
            # Personalizado
            elif self.tipoPapel == 6:
                if originalR:
                    if self.tipoPersonalizado[0] > self.tipoPersonalizado[1]:
                        w = self.tipoPersonalizado[1] * mm
                        h = self.tipoPersonalizado[0] * mm
                    else:
                        w = self.tipoPersonalizado[0] * mm
                        h = self.tipoPersonalizado[1] * mm
                else:
                    if self.tipoPersonalizado[0] > self.tipoPersonalizado[1]:
                        w = self.tipoPersonalizado[0] * mm
                        h = self.tipoPersonalizado[1] * mm
                    else:
                        w = self.tipoPersonalizado[1] * mm
                        h = self.tipoPersonalizado[0] * mm
            # Carta
            else:
                if originalR:
                    w = 8.5 * inch
                    h = 11 * inch
                else:
                    w = 11 * inch
                    h = 8.5 * inch
            logging.info(f"\nAncho de la pagina en puntos = {w}")
            logging.info(f"Alto de la pagina en puntos = {h}")
            logging.info("punto = 1/72 pulgada")
            logging.info("Iniciando el proceso de creacion de PDF...")
            anversoX1 = 0
            anversoX2 = 0
            reversoX1 = 0
            reversoX2 = 0
            anversoY1 = 0
            anversoY2 = 0
            reversoY1 = 0
            reversoY2 = 0
            tamanioAX = 0
            tamanioAY = 0
            tamanioRX = 0
            tamanioRY = 0
            if originalR:
                anversoX1 = self.margenesAnverso[0] * mm
                anversoX2 = anversoX1
                reversoX1 = self.margenesReverso[0] * mm
                reversoX2 = reversoX1
                anversoY1 = self.margenesAnverso[3] * mm
                anversoY2 = round(anversoY1 + (h / 2))
                reversoY1 = self.margenesReverso[3] * mm
                reversoY2 = round(reversoY1 + (h / 2))
                tamanioAX = w - ((self.margenesAnverso[0] + self.margenesAnverso[2]) * mm)
                tamanioAY = round((h / 2) - ((self.margenesAnverso[1] + self.margenesAnverso[3]) * mm))
                tamanioRX = w - ((self.margenesReverso[0] + self.margenesReverso[2]) * mm)
                tamanioRY = round((h / 2) - ((self.margenesReverso[1] + self.margenesReverso[3]) * mm))
            else:
                anversoX1 = self.margenesAnverso[0] * mm
                anversoX2 = round((w / 2) + anversoX1)
                reversoX1 = self.margenesReverso[0] * mm
                reversoX2 = round((w / 2) + reversoX1)
                anversoY1 = self.margenesAnverso[3] * mm
                anversoY2 = anversoY1
                reversoY1 = self.margenesReverso[3] * mm
                reversoY2 = reversoY1
                if self.tipoPapel == 6:
                    anversoX1 = anversoX1 + (.6 * inch)
                    anversoX2 = anversoX2 + (.6 * inch)
                    reversoX1 = reversoX1 + (.6 * inch)
                    reversoX2 = reversoX2 + (.6 * inch)
                tamanioAX = round((w / 2) - ((self.margenesAnverso[0] + self.margenesAnverso[2]) * mm))
                tamanioAY = h - ((self.margenesAnverso[1] + self.margenesAnverso[3]) * mm)
                tamanioRX = round((w / 2) - ((self.margenesReverso[0] + self.margenesReverso[2]) * mm))
                tamanioRY = h - ((self.margenesReverso[1] + self.margenesReverso[3]) * mm)
            if self.tipoPapel == 6:
                pdf_canvas = canvas.Canvas(canvas_file, (wF, hF))
            else:
                pdf_canvas = canvas.Canvas(canvas_file, (w, h))
            contador = 0
            logging.info("Inicio")
            for imagen in imagenes:
                imagen_path = os.path.join(self.pathDirectorio, imagen)
                if self.dosLados == True:
                    if contador % 2 == 0:
                        # Anverso
                        pdf_canvas.drawImage(imagen_path, anversoX1, anversoY1, width=tamanioAX, height=tamanioAY)
                        pdf_canvas.drawImage(imagen_path, anversoX2, anversoY2, width=tamanioAX, height=tamanioAY)
                    else:
                        # Reverso
                        pdf_canvas.drawImage(imagen_path, reversoX1, reversoY1, width=tamanioRX, height=tamanioRY)
                        pdf_canvas.drawImage(imagen_path, reversoX2, reversoY2, width=tamanioRX, height=tamanioRY)
                else:
                    # Anverso solamente
                    pdf_canvas.drawImage(imagen_path, anversoX1, anversoY1, width=tamanioAX, height=tamanioAY)
                    pdf_canvas.drawImage(imagen_path, anversoX2, anversoY2, width=tamanioAX, height=tamanioAY)
                pdf_canvas.showPage()
                contador += 1
                logging.info(f"{contador}")
            pdf_canvas.save()
        if self.archivoSalidaEnR and originalR:
            self.girarPaginas(self.pathSalida, 270)
        if not self.archivoSalidaEnR and not originalR:
            self.girarPaginas(self.pathSalida, 90)
        logging.info(f"El pdf se ha creado en {self.pathSalida}.")
    
    def unirPDFs(self):
        logging.info("Iniciando el proceso de union de PDFs...")
        pdf_writer = PyPDF2.PdfWriter()
        logging.info(f"Se encontraron {len(self.pathsPDFs)} PDFs a unir.")
        for x in range(len(self.pathsPDFs)):
            logging.info(f"Uniendo PDF {self.pathsPDFs[x]}")
            with open(self.pathsPDFs[x], 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf.pages)):
                    page = pdf.pages[page_num]
                    pdf_writer.add_page(page)
        with open(self.pathSalida, 'wb') as output_file:
            pdf_writer.write(output_file)
        logging.info(f"El PDF se ha unido en {self.pathSalida}.")
    
    def girarPaginas(self):
        logging.info("Iniciando el proceso de rotacion de paginas...")
        logging.info(f"Se giraran las paginas del PDF {self.pathPDF} {self.grados} grados.")
        with open(self.pathPDF, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            pdf_writer = PyPDF2.PdfWriter()
            for page_num in range(len(pdf.pages)):
                logging.info(f"Rotando pagina {page_num + 1}")
                page = pdf.pages[page_num].rotate(self.grados)
                pdf_writer.add_page(page)
            with open(self.pathSalida, 'wb') as output_file:
                pdf_writer.write(output_file)
        logging.info(f"El PDF se ha girado en {self.pathSalida}.")

    def invertirPDF(self):
        logging.info("Iniciando el proceso de inversion de paginas...")
        logging.info(f"Se invertiran las paginas del PDF {self.pathPDF}.")
        with open(self.pathPDF, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            pdf_writer = PyPDF2.PdfWriter()
            logging.info(f"Se encontraron {len(pdf.pages)} paginas.")
            for page_num in range(len(pdf.pages)):
                page_num = page_num + 1
                logging.info(f"Invirtiendo pagina {page_num}")
                page = pdf.pages[-page_num]
                pdf_writer.add_page(page)
            with open(self.pathSalida, 'wb') as output_file:
                pdf_writer.write(output_file)
        logging.info(f"El PDF se ha invertido en {self.pathSalida}.")

    def borrarMargenes(self):
        logging.info("Iniciando el proceso de borrado de margenes...")
        logging.info(f"Se borraran los margenes de la ruta {self.pathDirectorio}.")
        imagenes = [f for f in os.listdir(self.pathDirectorio) if f.endswith(('.jpg', '.JPG', '.png', '.jpeg', '.tif'))]
        logging.info(f"Se encontraron {len(imagenes)} imagenes.")
        directorioBase = self.pathDirectorio + "Borrado"
        directorioIntento = directorioBase
        intento = 1
        while os.path.exists(directorioIntento):
            directorioIntento = directorioBase + str(intento)
            intento += 1
        os.makedirs(directorioIntento)
        logging.info(f"Carpeta creada exitosamente en {directorioIntento}.")
        xAnverso1, yAnverso1, xAnverso2, yAnverso2 = self.margenesAnverso[0], self.margenesAnverso[1], self.margenesAnverso[2], self.margenesAnverso[3]
        if self.dosLados:
            xReverso1, yReverso1, xReverso2, yReverso2 = self.margenesReverso[0], self.margenesReverso[1], self.margenesReverso[2], self.margenesReverso[3]
        contador = 1
        for imagen in imagenes:
            logging.info(f"Recortando imagen {imagen}")
            imagenPath = os.path.join(self.pathDirectorio, imagen)
            img = cv2.imread(imagenPath)
            h, w, c = img.shape
            imagenBlanca = np.ones_like(img) * 255
            if self.dosLados:
                if contador % 2 == 0:
                    recorte = img[yReverso1:h-yReverso2, xReverso1:w-xReverso2]
                    imagenBlanca[yReverso1:h-yReverso2, xReverso1:w-xReverso2] = recorte
                else:
                    recorte = img[yAnverso1:h-yAnverso2, xAnverso1:w-xAnverso2]
                    imagenBlanca[yAnverso1:h-yAnverso2, xAnverso1:w-xAnverso2] = recorte
            else:
                recorte = img[yAnverso1:h-yAnverso2, xAnverso1:w-xAnverso2]
                imagenBlanca[yAnverso1:h-yAnverso2, xAnverso1:w-xAnverso2] = recorte
            cv2.imwrite(os.path.join(directorioIntento, imagen), imagenBlanca)
            contador += 1
        logging.info(f"Las imagenes se han guardado en {directorioIntento}.")


class Ventana:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Creador de PDFs")
        self.ventana.geometry("800x600")
        self.ventana.configure(bg = "white")
        self.ventana.resizable(0,0)

        self.creadorPDF = GeneradorPDF()

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

        self.etiquetaGirarGrados = Label(self.pestania3, text = "Seleccionar los grados que quiere girar su documento a la derecha.", font = ("Arial", 12))
        self.etiquetaGirarGrados.place(x = 10, y = 50)
        self.spinboxGirarGrados = Spinbox(self.pestania3, from_=90, to=270, increment=90, width = 4, font = ("Arial", 12))
        self.spinboxGirarGrados.place(x = 490, y = 50)

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
            if proceso == 1: # Crear PDF desde imagenes
                self.creadorPDF.pathDirectorio = self.entryPath.get()
                self.creadorPDF.pathSalida = filedialog.asksaveasfilename(defaultextension=".pdf")
                self.creadorPDF.tipoPapel = self.comboboxTipoPapel.current()
                if self.comboboxTipoPapel.current() == 6:
                    self.creadorPDF.tipoPersonalizado = [int(self.spinboxTamanioX.get()), int(self.spinboxTamanioY.get())]
                self.creadorPDF.margenesAnverso = [int(self.spinboxMargenFrenteIzquierda.get()), int(self.spinboxMargenFrenteSuperior.get()), int(self.spinboxMargenFrenteDerecha.get()), int(self.spinboxMargenFrenteInferior.get())]
                if self.checkVarRepeticion.get():
                    self.creadorPDF.margenesReverso = [int(self.spinboxMargenVueltaIzquierda.get()), int(self.spinboxMargenVueltaSuperior.get()), int(self.spinboxMargenVueltaDerecha.get()), int(self.spinboxMargenVueltaInferior.get())]
                self.creadorPDF.dosLados = self.checkVarDosLados.get()
                self.creadorPDF.archivoSalidaEnR = self.checkVarR.get()
                if self.checkVarRepeticion.get():
                    self.creadorPDF.crearPdfImagenesRepeticion()
                else:
                    self.creadorPDF.crearPdfImagenes()
                tk.messagebox.showinfo("Informacion", f"PDF creado en {self.creadorPDF.pathSalida}")
            elif proceso == 2: # Unir PDFs
                self.creadorPDF.pathsPDFs = self.rutasPDFs
                self.creadorPDF.pathSalida = filedialog.asksaveasfilename(defaultextension=".pdf")
                self.creadorPDF.unirPDFs()
                tk.messagebox.showinfo("Informacion", f"PDF creado en {self.creadorPDF.pathSalida}")
            elif proceso == 3: # Girar PDF
                self.creadorPDF.pathPDF = self.entryPathGirar.get()
                self.creadorPDF.grados = int(self.spinboxGirarGrados.get())
                self.creadorPDF.pathSalida = filedialog.asksaveasfilename(defaultextension=".pdf")
                self.creadorPDF.girarPaginas()
                tk.messagebox.showinfo("Informacion", f"PDF creado en {self.creadorPDF.pathSalida}")
            elif proceso == 4: # Invertir PDF
                self.creadorPDF.pathPDF = self.entryPathInvertir.get()
                self.creadorPDF.pathSalida = filedialog.asksaveasfilename(defaultextension=".pdf")
                self.creadorPDF.invertirPDF()
                tk.messagebox.showinfo("Informacion", f"PDF creado en {self.creadorPDF.pathSalida}")
            elif proceso == 5: # Borrar margenes
                self.creadorPDF.pathDirectorio = self.entryPathBorrar.get()
                self.creadorPDF.margenesAnverso = [int(self.spinboxBorrarMargenFrenteIzquierda.get()), int(self.spinboxBorrarMargenFrenteSuperior.get()), int(self.spinboxBorrarMargenFrenteDerecha.get()), int(self.spinboxBorrarMargenFrenteInferior.get())]
                self.creadorPDF.margenesReverso = [int(self.spinboxBorrarMargenVueltaIzquierda.get()), int(self.spinboxBorrarMargenVueltaSuperior.get()), int(self.spinboxBorrarMargenVueltaDerecha.get()), int(self.spinboxBorrarMargenVueltaInferior.get())]
                self.creadorPDF.dosLados = self.checkVarBorrarDosLados.get()
                self.creadorPDF.borrarMargenes()
                tk.messagebox.showinfo("Informacion", "Margenes borrados correctamente")
            elif proceso == 6: # Variar densidad
                tk.messagebox.showinfo("Informacion", "Proceso no implementado")
        except Exception as e:
            logging.error(f"Error: {e}")
            tk.messagebox.showerror("Error en la ejecucion, revice el archivo log para encontrar el posible motivo.", f"Error: {e}")

if __name__ == "__main__":
    ventana = Ventana()