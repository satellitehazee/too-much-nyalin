import pytesseract
from PIL import Image, ImageGrab, ImageEnhance, ImageFilter
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


im = ImageGrab.grabclipboard()
im.save('temp.png', 'PNG')


predicted_res = pytesseract.image_to_string(Image.open("../temp.png"), config='words')

print(predicted_res)
