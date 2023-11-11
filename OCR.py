import cv2
import pytesseract
caminho_img = "caminho_img.png"
img = cv2.imread(caminho_img) #lendo a imagem

pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\Tesseract.exe"  #definindo o caminho para o executavel do tesseract

retorno = pytesseract.image_to_string(img, lang="por") #convertendo o texto da imagem numa string
print("imagem: ", caminho_img)
print(retorno)