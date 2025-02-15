import cv2, os
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
import logging
import numpy as np


class GeneradorPDF:
    def __init__(self):
        self.pathDirectorio = ""
        self.__pathDirectorioSalida = ""
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
        self.gradosPares = 0
        self.girarDiferente = False
        self.densidad = 0
        self.varianteBlanco = 0

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
                if self.dosLados:
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
        if os.path.isfile(self.pathSalida):
            self.pathPDF = self.pathSalida
        if self.archivoSalidaEnR and not originalR:
            self.grados = 270
            self.girarPaginas()
        if not self.archivoSalidaEnR and originalR:
            self.grados = 90
            self.girarPaginas()
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
            logging.info(f"Ancho de la pagina en puntos = {w}")
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
                if self.tipoPapel == 5:
                    # anversoY1 = anversoY1 + (.6 * inch)
                    # anversoY2 = anversoY2 + (.6 * inch)
                    reversoY1 = reversoY1 + (.6 * inch)
                    reversoY2 = reversoY2 + (.6 * inch)
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
                if self.tipoPapel == 5:
                    anversoX1 = anversoX1 + (.6 * inch)
                    anversoX2 = anversoX2 + (.6 * inch)
                    reversoX1 = reversoX1 + (.6 * inch)
                    reversoX2 = reversoX2 + (.6 * inch)
                tamanioAX = round((w / 2) - ((self.margenesAnverso[0] + self.margenesAnverso[2]) * mm))
                tamanioAY = h - ((self.margenesAnverso[1] + self.margenesAnverso[3]) * mm)
                tamanioRX = round((w / 2) - ((self.margenesReverso[0] + self.margenesReverso[2]) * mm))
                tamanioRY = h - ((self.margenesReverso[1] + self.margenesReverso[3]) * mm)
            if self.tipoPapel == 5:
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
        if os.path.isfile(self.pathSalida):
            self.pathPDF = self.pathSalida
        if self.archivoSalidaEnR and originalR:
            self.grados = 270
            self.girarPaginas()
        if not self.archivoSalidaEnR and not originalR:
            self.grados = 90
            self.girarPaginas()
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
        if self.girarDiferente:
            with open(self.pathPDF, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                contador = 1
                for page_num in range(len(pdf.pages)):
                    logging.info(f"Rotando pagina {page_num + 1}")
                    if contador % 2 == 1:
                        page = pdf.pages[page_num].rotate(self.grados)
                    else:
                        page = pdf.pages[page_num].rotate(self.gradosPares)
                    contador += 1
                    pdf_writer.add_page(page)
                with open(self.pathSalida, 'wb') as output_file:
                    pdf_writer.write(output_file)
        else:
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
        self.__pathDirectorioSalida = directorioIntento
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
    
    def variarDensidad(self):
        logging.info("Iniciando el proceso de cambio de intensidad...")
        logging.info(f"Se cambiara la intensidad de las imagenes de la ruta {self.pathDirectorio}.")
        imagenes = [f for f in os.listdir(self.pathDirectorio) if f.endswith(('.jpg', '.JPG', '.png', '.jpeg', '.tif'))]
        logging.info(f"Se encontraron {len(imagenes)} imagenes.")
        directorioBase = self.pathDirectorio + "Densidad"
        directorioIntento = directorioBase
        intento = 1
        while os.path.exists(directorioIntento):
            directorioIntento = directorioBase + str(intento)
            intento += 1
        os.makedirs(directorioIntento)
        self.__pathDirectorioSalida = directorioIntento
        logging.info(f"Carpeta creada exitosamente en {directorioIntento}.")
        for imagen in imagenes:
            logging.info(f"Cambiando intensidad de imagen {imagen}")
            imagenPath = os.path.join(self.pathDirectorio, imagen)
            img = cv2.imread(imagenPath)
            h, w, c = img.shape
            for i in range(h):
                for j in range(w):
                    pixel = img[i, j]
                    if pixel[0] < self.varianteBlanco and pixel[1] < self.varianteBlanco and pixel[2] < self.varianteBlanco:
                        for k in range(3):
                            if pixel[k] + self.densidad > 255:
                                pixel[k] = 255
                            elif pixel[k] + self.densidad < 0:
                                pixel[k] = 0
                            else:
                                pixel[k] = pixel[k] + self.densidad
            cv2.imwrite(os.path.join(directorioIntento, imagen), img)
        logging.info(f"Las imagenes se han guardado en {directorioIntento}.")
    
    def getDirectorioSalida(self):
        return self.__pathDirectorioSalida
    
    def limpiarAtributos(self):
        self.pathDirectorio = ""
        self.__pathDirectorioSalida = ""
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
        self.gradosPares = 0
        self.girarDiferente = False
        self.densidad = 0
        self.varianteBlanco = 0