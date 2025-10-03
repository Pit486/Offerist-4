import os
from PIL import Image

pic=[]
picd = os.listdir('oldpic')
for i in picd:
    pic.append(str(i))

for filename in pic:
    print(filename)
    img=Image.open('oldpic//'+filename)
    width, height = img.size
    img.load()
    type(img)
    isinstance(img, Image.Image)
    #сжатие
    new_img = img.resize((800,800))
            #low_res_img.show()
    #сохранение
    new_img.save("pic//"+filename)
print('Ok')
