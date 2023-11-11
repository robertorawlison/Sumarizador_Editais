import fitz #PyMuPDF: biblioteca para leitura de pdfs

pdf_path = 'caminho_do_pdf.pdf'

pdf_file = fitz.open(pdf_path)

image = pdf_file[0].get_pixmap() #parametro dpi define a resolução da imagem set = 10

image.save("#pdf_image.png")
