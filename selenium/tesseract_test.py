# -*- coding: utf-8 -*-
import pytesseract
from PIL import Image

if __name__ == '__main__':
    image = Image.open('images/test_2017-06-25.png')
    code = pytesseract.image_to_string(image, lang='eng')
    print code