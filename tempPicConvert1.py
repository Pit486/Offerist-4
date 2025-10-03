import os
from PIL import Image

picd = os.listdir('pic')
for i in picd:
    if 'png' in i or 'jpg' in i or 'gif' in i:
        with Image.open('pic//'+i) as img:
            img.load()
            name = i.split('.')[0]
            img = img.convert("L")
            img.save('pic//'+name+".jpeg")
            os.remove("pic//"+i)
