import os

filename= 'temp001.txt'
pic=[]

picd = os.listdir('pic')
for i in picd:
    pic.append(str(i.replace('.jpeg','')))
#print(pic)

with open(filename,'r', encoding='UTF-8') as f:
    for i in f:
        #tmp1=f.readline()
        row = (str(i)).replace('\n','')
        #print(row)
        img=''
        for i in pic:
            if i in (row).upper().replace('/','_'):
                img='pic//'+i+'.jpeg'
                #print(row,'     ',img)
                break
        if img=='':
            print(row,'None!')
print('Ok')
        
