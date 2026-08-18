from pyzbar.pyzbar import decode
from PIL import Image
img=Image.open('/Users/prashamsaghimire/Desktop/Projects/myqrcode1.png')
result=decode(img)
print(result)