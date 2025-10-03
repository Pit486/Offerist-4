import os

pic=[]

picd = os.listdir('pic')
for i in picd:
    pic.append(str(i.replace('.jpeg','')))
#print(pic)

while True:
    row=input()
    if row=='q':
        break
    img=''
    for i in pic:
        if i in (row).upper():
            img='pic//'+i+'.jpeg'
            print(row,img)
    if img=='':
            print('None!')

