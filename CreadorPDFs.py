import cv2, os
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from tkinter import filedialog

def crearPdfImagenesRepeticion(path, output_path, dosLados, margenesAnverso, margenesReverso, cartaOficio, tamanioPersonalizado):
    imagenes = [f for f in os.listdir(path) if f.endswith(('.jpg', '.JPG', '.png', '.jpeg'))]
    print(f"\nSe encontraron {len(imagenes)} imagenes.")
    with open(output_path, 'wb') as canvas_file:
        imagen_path = os.path.join(path, imagenes[0])
        img = cv2.imread(imagen_path)
        h, w, c = img.shape
        originalR = False
        esVertical = False
        if w > h:
            originalR = True
            esVertical = True
        print(f"Tamanio de la primera imagen original = {w} x {h}")
        w = 0
        h = 0
        if cartaOficio == 2:
            if originalR:
                w = 612
                h = 965 # oficio real
            else:
                w = 965 # oficio real
                h = 612
        elif cartaOficio == 3:
            if originalR:
                w = 210 * mm
                h = 340 * mm # 210mm x 340mm
            else:
                w = 340 * mm # 210mm x 340mm
                h = 210 * mm
        elif cartaOficio == 4:
            if originalR:
                w = 11 * inch
                h = 17 * inch
            else:
                w = 17 * inch
                h = 11 * inch
        elif cartaOficio == 5:
            if originalR:
                if tamanioPersonalizado[1] > tamanioPersonalizado[0]:
                    w = tamanioPersonalizado[0] * mm
                    h = tamanioPersonalizado[1] * mm
                else:
                    w = tamanioPersonalizado[1] * mm
                    h = tamanioPersonalizado[0] * mm
            else:
                if tamanioPersonalizado[1] > tamanioPersonalizado[0]:
                    w = tamanioPersonalizado[1] * mm
                    h = tamanioPersonalizado[0] * mm
                else:
                    w = tamanioPersonalizado[0] * mm
                    h = tamanioPersonalizado[1] * mm
        else:
            if originalR:
                w = 8.5 * inch
                h = 11 * inch
            else:
                w = 11 * inch
                h = 8.5 * inch
        print(f"\nAncho de la pagina en puntos = {w}, Alto de la pagina en puntos = {h}\n1 punto = 1/72 pulgada\n\nDebido a que las " +
            "unidades que usa esta libreria son estos dichosos puntos, en algunos casos no se podran " +
            "alcanzar las medidas exactas en funcion de los milimetros. :(")
        print("\nTrabajando en la union...\n")
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
            anversoX1 = margenesAnverso[0] * mm
            anversoX2 = margenesAnverso[0] * mm
            reversoX1 = margenesReverso[0] * mm
            reversoX2 = margenesReverso[0] * mm
            anversoY1 = margenesAnverso[3] * mm
            anversoY2 = round(anversoY1 + (h / 2))
            reversoY1 = margenesReverso[3] * mm
            reversoY2 = round(reversoY1 + (h / 2))
            tamanioAX = w - ((margenesAnverso[0] + margenesAnverso[2]) * mm)
            tamanioAY = round((h / 2) - ((margenesAnverso[1] + margenesAnverso[3]) * mm))
            tamanioRX = w - ((margenesReverso[0] + margenesReverso[2]) * mm)
            tamanioRY = round((h / 2) - ((margenesReverso[1] + margenesReverso[3]) * mm))
        else:
            anversoX1 = margenesAnverso[0] * mm
            anversoX2 = round((w / 2) + anversoX1)
            reversoX1 = margenesReverso[0] * mm
            reversoX2 = round((w / 2) + reversoX1)
            anversoY1 = margenesAnverso[3] * mm
            anversoY2 = anversoY1
            reversoY1 = margenesReverso[3] * mm
            reversoY2 = reversoY1
            tamanioAX = round((w / 2) - ((margenesAnverso[0] + margenesAnverso[2]) * mm))
            tamanioAY = h - ((margenesAnverso[1] + margenesAnverso[3]) * mm)
            tamanioRX = round((w / 2) - ((margenesReverso[0] + margenesReverso[2]) * mm))
            tamanioRY = h - ((margenesReverso[1] + margenesReverso[3]) * mm)
        pdf_canvas = canvas.Canvas(canvas_file, (w, h))
        contador = 0
        print("Inicio", end="")
        for imagen in imagenes:
            imagen_path = os.path.join(path, imagen)
            if dosLados == 1:
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
            print(f", {contador}", end="")
        pdf_canvas.save()
    return esVertical

def crearPdfImagenes(path, output_path, dosLados, margenesAnverso, margenesReverso, cartaOficio, tamanioPersonalizado):
    imagenes = [f for f in os.listdir(path) if f.endswith(('.jpg', '.JPG', '.png', '.jpeg'))]
    print(f"\nSe encontraron {len(imagenes)} imagenes.")
    with open(output_path, 'wb') as canvas_file:
        imagen_path = os.path.join(path, imagenes[0])
        img = cv2.imread(imagen_path)
        h, w, c = img.shape
        originalR = False
        esVertical = True
        if w > h:
            originalR = True
            esVertical = False
        print(f"Tamanio de la primera imagen original = {w} x {h}")
        w = 0
        h = 0
        if cartaOficio == 2:
            if originalR:
                w = 965
                h = 612
            else:
                w = 612
                h = 965
        elif cartaOficio == 3:
            if originalR:
                w = 340 * mm
                h = 210 * mm
            else:
                w = 210 * mm
                h = 340 * mm
        elif cartaOficio == 4:
            if originalR:
                w = 17 * inch
                h = 11 * inch
            else:
                w = 11 * inch
                h = 17 * inch
        elif cartaOficio == 5:
            if originalR:
                if tamanioPersonalizado[0] > tamanioPersonalizado[1]:
                    w = tamanioPersonalizado[0] * mm
                    h = tamanioPersonalizado[1] * mm
                else:
                    w = tamanioPersonalizado[1] * mm
                    h = tamanioPersonalizado[0] * mm
            else:
                if tamanioPersonalizado[0] > tamanioPersonalizado[1]:
                    w = tamanioPersonalizado[1] * mm
                    h = tamanioPersonalizado[0] * mm
                else:
                    w = tamanioPersonalizado[0] * mm
                    h = tamanioPersonalizado[1] * mm
        else:
            if originalR:
                w = 11 * inch
                h = 8.5 * inch
            else:
                w = 8.5 * inch
                h = 11 * inch
        print(f"\nAncho de la pagina en puntos = {w}, Alto de la pagina en puntos = {h}\n1 punto = 1/72 pulgada\n\nDebido a que las " +
            "unidades que usa esta libreria son estos dichosos puntos, en algunos casos no se podran " +
            "alcanzar las medidas exactas en funcion de los milimetros. :(")
        print("\nTrabajando en la union...\n")
        anversoX = margenesAnverso[0] * mm
        reversoX = margenesReverso[0] * mm
        anversoY = margenesAnverso[3] * mm
        reversoY = margenesReverso[3] * mm
        tamanioAX = w - ((margenesAnverso[0] + margenesAnverso[2]) * mm)
        tamanioAY = round(h - ((margenesAnverso[1] + margenesAnverso[3]) * mm))
        tamanioRX = w - ((margenesReverso[0] + margenesReverso[2]) * mm)
        tamanioRY = round(h - ((margenesReverso[1] + margenesReverso[3]) * mm))
        pdf_canvas = canvas.Canvas(canvas_file, (w, h))
        contador = 0
        print("Inicio", end="")
        for imagen in imagenes:
            imagen_path = os.path.join(path, imagen)
            if dosLados == 1:
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
            print(f", {contador}", end="")
        pdf_canvas.save()
    return esVertical

def unir_pdfs(archivo1, archivo2, archivo_salida):
    # Abrir los archivos PDF en modo binario
    with open(archivo1, 'rb') as file1, open(archivo2, 'rb') as file2:
        # Crear objetos PDF
        pdf1 = PyPDF2.PdfReader(file1)
        pdf2 = PyPDF2.PdfReader(file2)

        # Crear un objeto PDFWriter para el archivo de salida
        pdf_writer = PyPDF2.PdfWriter()

        # Agregar páginas del primer archivo
        for page_num in range(len(pdf1.pages)):
            page = pdf1.pages[page_num]
            pdf_writer.add_page(page)

        # Agregar páginas del segundo archivo
        for page_num in range(len(pdf2.pages)):
            page = pdf2.pages[page_num]
            pdf_writer.add_page(page)

        # Escribir el resultado en el archivo de salida
        with open(archivo_salida, 'wb') as output_file:
            pdf_writer.write(output_file)

def girarPaginas(archivo, grados):
    with open(archivo, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num].rotate(grados)
            pdf_writer.add_page(page)
        with open(archivo, 'wb') as output_file:
            pdf_writer.write(output_file)

def preguntarMargenes():
    margenesAnverso = [0, 0, 0, 0]
    margenesReverso = [0, 0, 0, 0]
    tamanioPersonalizado = [0, 0]
    cartaOficio = 0
    dosLados = 0
    hacerEnR = 0
    margen = 0
    enR = False
    while True:
        try:
            cartaOficio = int(input("\n¿Que tamanio de papel quiere usar?\n(1 = Carta, 2 = Oficio, 3 = 210mm x 340mm, 4 = Doble carta, 5 = Personalizado)\nRespuesta: "))
            break
        except ValueError:
            print("Debes de ingresar un numero 1, 2 o 3.")
    if cartaOficio == 5:
        while True:
            try:
                tamanioPersonalizado[0] = int(input("Ingrese el ancho del papel en mm: "))
                break
            except ValueError:
                print("El ancho del papel debe ser un número entero.")
        while True:
            try:
                tamanioPersonalizado[1] = int(input("Ingrese el alto del papel en mm: "))
                break
            except ValueError:
                print("El alto del papel debe ser un número entero.")
    while True:
        try:
            hacerEnR = int(input("\n¿Quiere que su documento este en R?\n(1 = Si, 2 = No)\nRespuesta: "))
            break
        except ValueError:
            print("Debes de ingresar un numero 1 o 2.")
    if hacerEnR == 1:
        enR = True
    while True:
        try:
            dosLados = int(input("\n¿Dos lados?\n(1 = Si, 2 = No)\nRespuesta: "))
            break
        except ValueError:
            print("Debes de ingresar un numero 1 o 2.")
    while True:
        try:
            margen = int(input("\nIngrese el margen anverso izquierdo en mm: "))
            break
        except ValueError:
            print("El margen anverso izquierdo debe ser un número entero.")
    margenesAnverso[0] = margen
    while True:
        try:
            margen = int(input("Ingrese el margen anverso superior en mm: "))
            break
        except ValueError:
            print("El margen anverso superior debe ser un número entero.")
    margenesAnverso[1] = margen
    while True:
        try:
            margen = int(input("Ingrese el margen anverso derecho en mm: "))
            break
        except ValueError:
            print("El margen anverso derecho debe ser un número entero.")
    margenesAnverso[2] = margen
    while True:
        try:
            margen = int(input("Ingrese el margen anverso inferior en mm: "))
            break
        except ValueError:
            print("El margen anverso inferior debe ser un número entero.")
    margenesAnverso[3] = margen
    if dosLados == 1:
        while True:
            try:
                margen = int(input("\nIngrese el margen reverso izquierdo en mm: "))
                break
            except ValueError:
                print("El margen reverso izquierdo debe ser un número entero.")
        margenesReverso[0] = margen
        while True:
            try:
                margen = int(input("Ingrese el margen reverso superior en mm: "))
                break
            except ValueError:
                print("El margen reverso superior debe ser un número entero.")
        margenesReverso[1] = margen
        while True:
            try:
                margen = int(input("Ingrese el margen reverso derecho en mm: "))
                break
            except ValueError:
                print("El margen reverso derecho debe ser un número entero.")
        margenesReverso[2] = margen
        while True:
            try:
                margen = int(input("Ingrese el margen reverso inferior en mm: "))
                break
            except ValueError:
                print("El margen reverso inferior debe ser un número entero.")
        margenesReverso[3] = margen
    print(cartaOficio, dosLados, margenesAnverso, margenesReverso, tamanioPersonalizado, enR)
    return cartaOficio, dosLados, margenesAnverso, margenesReverso, tamanioPersonalizado, enR

def invertirPDF(archivo, archivo_salida):
    # Abrir los archivos PDF en modo binario
    with open(archivo, 'rb') as file:
        # Crear objetos PDF
        pdf = PyPDF2.PdfReader(file)

        # Crear un objeto PDFWriter para el archivo de salida
        pdf_writer = PyPDF2.PdfWriter()

        # Agregar páginas del primer archivo
        print(len(pdf.pages))
        for page_num in range(len(pdf.pages)):
            page_num = page_num +1
            print(page_num)
            page = pdf.pages[-page_num]
            pdf_writer.add_page(page)

        # Escribir el resultado en el archivo de salida
        with open(archivo_salida, 'wb') as output_file:
            pdf_writer.write(output_file)


if __name__ == "__main__":
    os.system("cls")
    elegir = ""
    while elegir != "6":
        os.system("cls")
        print("Creador de PDFs\n1 = Repeticion\n2 = Crear PDF\n3 = Unir dos PDFs\n4 = Invertir numeracion PDF\n5 = Rotar PDF\n6 = Salir\n")
        print("Nota: para detener el programa en cualquier momento, presione \"Ctrl + C\".\n")
        elegir = input("Ingrese el numero de la opcion que desea ejecutar: ")
        os.system("cls")
        if elegir == "1":
            print("Este programa crea pdf's a partir de imagenes, repitiendo cada imagen 2 veces en cada pagina, dando la " +
                "oportunidad de elegir los margenes deseados para cada uno de los 4 lados de cada tipo de pagina (anverso y reverso)" +
                ", hay que destacar que los margenes deben de ser ingresados tomando la orientacion de la imagen original de referencia, " +
                "independientemente de la orientacion del pdf creado.\nSe agregaran las imagenes a las paginas en orden alfanumerico "
                "usando el nombre de las imagenes.\n")
            decision = input("1 = Elegir la carpeta que contiene las imagenes e iniciar\n0 = Salir\nIngrese: ")
            if decision != "1":
                salida = input("Presione enter para salir.")
                exit()
            try:
                path = filedialog.askdirectory()
                pdfSalida_path = filedialog.asksaveasfilename(defaultextension=".pdf")
                cartaOficio, dosLados, margenesAnverso, margenesReverso, tamanioPersonalizado, enR = preguntarMargenes()
                esVertical = crearPdfImagenesRepeticion(path, pdfSalida_path, dosLados, margenesAnverso, margenesReverso, cartaOficio, tamanioPersonalizado)
                if enR and esVertical:
                    girarPaginas(pdfSalida_path, 90)
                if not enR and not esVertical:
                    girarPaginas(pdfSalida_path, 270)
                print(f"\n\nEl pdf se ha creado en {pdfSalida_path}.")
            except Exception as e:
                print("Error :(\n", e)
            salida = input("Presione enter para salir.")
        elif elegir == "2":
            print("Este programa crea pdf's a partir de imagenes, agregando una imagen por pagina, dando la " +
                "oportunidad de elegir los margenes deseados para cada uno de los 4 lados de cada tipo de pagina (anverso y reverso)" +
                ", hay que destacar que los margenes deben de ser ingresados tomando la orientacion de la imagen original de referencia, " +
                "independientemente de la orientacion del pdf creado.\nSe agregaran las imagenes a las paginas en orden alfanumerico "
                "usando el nombre de las imagenes.\n")
            decision = input("1 = Elegir la carpeta que contiene las imagenes e iniciar\n0 = Salir\nIngrese: ")
            if decision != "1":
                salida = input("Presione enter para salir.")
                exit()
            try:
                path = filedialog.askdirectory()
                pdfSalida_path = filedialog.asksaveasfilename(defaultextension=".pdf")
                cartaOficio, dosLados, margenesAnverso, margenesReverso, tamanioPersonalizado, enR = preguntarMargenes()
                esVertical = crearPdfImagenes(path, pdfSalida_path, dosLados, margenesAnverso, margenesReverso, cartaOficio, tamanioPersonalizado)
                if enR and esVertical:
                    girarPaginas(pdfSalida_path, 90)
                if not enR and not esVertical:
                    girarPaginas(pdfSalida_path, 270)
                print(f"\n\nEl pdf se ha creado en {pdfSalida_path}.")
            except Exception as e:
                print("Error :(\n", e)
            salida = input("Presione enter para salir.")
        elif elegir == "3":
            print("Este programa une dos archivos PDF en uno solo.\n")
            try:
                input("Presione enter para elegir el primer archivo.")
                archivo1 = filedialog.askopenfilename()
                input("Presione enter para elegir el segundo archivo.")
                archivo2 = filedialog.askopenfilename()
                archivo_salida = filedialog.asksaveasfilename(defaultextension=".pdf")
                unir_pdfs(archivo1, archivo2, archivo_salida)
                print(f'Archivos unidos con éxito en {archivo_salida}')
            except Exception as e:
                print("Error :(\n", e)
            salida = input("Presione enter para salir.")
        elif elegir == "4":
            print("Este programa invierte la numeracion de las paginas de un PDF.\n")
            try:
                input("Presione enter para elegir el archivo.")
                archivo = filedialog.askopenfilename()
                archivo_salida = filedialog.asksaveasfilename(defaultextension=".pdf")
                invertirPDF(archivo, archivo_salida)
                print(f'Archivo invertido con éxito en {archivo_salida}')
            except Exception as e:
                print("Error :(\n", e)
            salida = input("Presione enter para salir.")
        elif elegir == "5":
            print("Este programa rota las paginas de un PDF.\n")
            try:
                input("Presione enter para elegir el archivo.")
                archivo = filedialog.askopenfilename()
                grados = 0
                while True:
                    try:
                        grados = int(input("Ingrese los grados a girar (90, 180, 270): "))
                        if grados % 90 != 0:
                            print("Ingrese un número entero múltiplo de 90")
                        else:
                            break
                    except:
                        print("Ingrese un número entero.")
                girarPaginas(archivo, grados)
                print(f'Archivo rotado con éxito en {archivo}')
            except Exception as e:
                print("Error :(\n", e)
            salida = input("Presione enter para salir.")
        else:
            exit()