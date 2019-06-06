# -*- coding:utf-8 -*-
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'E://Tesseract-OCR/tesseract.exe'

# 使用pytesseract对英文进行识别，lang参数可省略
# text = pytesseract.image_to_string(Image.open('E:\project\study_tornado\mm.jpg'), lang='eng')
# 使用pytesseract对中文（含英文，但识别率降低）进行识别
text = pytesseract.image_to_string(Image.open('E:\project\study_tornado\mm.jpg'), lang='chi_sim')
print text

# 参考：https://blog.csdn.net/u010134642/article/details/78747630
# 参考：https://blog.csdn.net/qq_38912819/article/details/80631154
# 参考：https://blog.csdn.net/helloc0de/article/details/80410250
# 参考：https://www.cnblogs.com/morwind/p/6867547.html
# 参考：https://blog.csdn.net/chengxuyuan997/article/details/80979737