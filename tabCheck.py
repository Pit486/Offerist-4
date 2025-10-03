#import os

filename= 'temp001.txt'

with open(filename,'r', encoding='UTF-8') as f:
    for i in f:
        row = (str(i)).replace('\t',' ')
        with open('tmpOut.txt','a', encoding='UTF-8') as fo:
            fo.write(row)
print('Ok')
