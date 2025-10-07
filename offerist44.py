import os
from datetime import datetime
import fpdf
from fpdf import FPDF
from tkinter import ttk
from tkinter import *
from tkinter import filedialog

outText = ''
client = ''
pic=[]
folder = 'pic'
data = []

# baza kartinok
for current, subdirs, files in os.walk(folder): # создание списка изображений
    for file in files:
        pic.append(str(file.replace('.jpeg','')))

def sort_data():
    global data
    for k in range(len(data)): #fix price
        if ',' in data[k][2]:
            data[k][2] = data[k][2].replace(',','.')
        if not '.' in data[k][2]:
            data[k][2]+= '.00'
        elif len(data[k][2]) - data[k][2].find('.') == 2:
            data[k][2]+= '0'
        elif data[k][2] == '':
            data[k][2] == '0.00'
    dt = data
    data = []
    for i in dt:
        if not i in data:
            data.append(i)
    data = sorted(data, key=lambda i: float(i[2])) # sort price
    tree.delete(*tree.get_children()) # очистка tree
    for i in data: 
        i = tuple(i)
        tree.insert("", END, values=i)
    
def save_path(filepath):
    # save last path
    if '.' in filepath:
        fp_dir = filepath[0: filepath.rfind('/')]
    else:
        fp_dir = filepath
    if fp_dir != work_dir:
        with open( 'set.txt', 'w', encoding = 'UTF-8') as f:
            f.write(company_name + '\n' + fp_dir + '\n' + offer_number + '\n' )
  
def save_data():
    global data
    f_name =  'Offer' + offer_number
    filepath = filedialog.asksaveasfilename(initialdir = work_dir, initialfile = f_name, defaultextension = 'csv', confirmoverwrite = 'y')
    if filepath != "":
        save_path(filepath)
        with open(filepath , "w", encoding="UTF-8") as f:
            for i in data:
                row_text = ','.join(i) + '\n'  # Создаем строку с разделителями-запятыми, добавляя символ новой строки, чтобы знать, когда строка заканчивается
                f.write(row_text)
                
def load_data():
    global data
    data = []
    filepath = filedialog.askopenfilename(initialdir = work_dir, initialfile = '*.csv')
    if filepath != "":
        save_path(filepath)
    
    with open(filepath, "r", encoding='UTF-8') as f:
        a = ''
        for i in f:
            a+= str(i)
    a = a.split('\n')
    for i in a:
        if "'" in i: # fix excell bug
            i+= ','
        i = i.split(',')
        if len(i) < 3:
            a.pop(-1)
            break
        i[0] = i[0].replace('"', '').replace("'", '')
        i[1] = i[1].replace('"', '').replace("'", '')
        i[2] = i[2].replace('"', '').replace("'", '')
        if len(i) < 4:
            i.append('')
        elif len(i) > 4:
            i[3] = i[3].replace('"', '').replace("'", '')
            if i[2].isdigit and i[3].isdigit:
                if len(i[3]) == 1:
                    i[3]+= '0'
                i[2]+= '.' + i[3]
                i[3] = i[4]
        if not '.' in i[2]:
            i[2]+= '.00'
        b = []
        b.append(i[0])
        b.append(i[1])
        b.append(i[2])
        b.append(i[3])
        data.append(b)
        
    # отрисовка деревa
    tree.delete(*tree.get_children()) 
    for i in data: 
        i = tuple(i)
        tree.insert("", END, values=i)
    return
            
def d_now():
    dt_in=(str(datetime.now()))
    dt=dt_in[8:10]+'.'+dt_in[5:7]+'.'+dt_in[:4]+' '+dt_in[11:16]
    return dt

def pdf_out():
    global  dt,client, offer_number, pic, company_name, data
    cepure = ['Artikuls', 'Apraksts', 'Cena', 'Piezīmes']
    td1 = data
    td = []
    data = []
    for k in td1:
        if k != cepure and not k in td:
            td.append(k)
    for j in range(len(td)):
        if j%8 == 0:
            data.append(cepure)
        if td[j] != cepure and not td[j] in data:
            data.append(td[j])
    
    pdf = FPDF()
    pdf.add_font('Hasklig-Light', '', 'Font/Finlandica-Regular.ttf', uni=True)
    pdf.add_font('Hasklig-Bold', '', 'Font/Finlandica-Bold.ttf', uni=True)
    
    pdf.add_page()
    image_path ='logo.png' #логотип
    pdf.image(image_path, x=10, y=7, w=40)
    pdf.set_font('Hasklig-Light', size=12)
    pdf.ln(0)  # ниже
    pdf.line(5, 5, 5, 292)
    pdf.line(5, 292, 205, 292)
    pdf.line(5, 5, 205, 5)
    pdf.line(205, 5, 205, 292)
    pdf.line(5, 19, 205, 19)
    pdf.set_font('Hasklig-Bold', size=20)
    pdf.cell(190, 0, txt="PIEDĀVĀJUMS", ln=1, align="C")
    pdf.set_font('Hasklig-Light', size=8)
    client = entry.get()
    comp = company_name + "     Piedāvājuma numurs " + offer_number + "     Klients: " + client + '    ' + dt
    pdf.cell(220, 15, txt = comp , ln=1, align="C")
    pdf.set_font('Hasklig-Light', size=8)
   
    spacing = 1
    row_height = 12 #pdf.font_size
    
    pic_y = 18#18
    r = 0#счётчик строк
    
    for row in data:
        r+=1
        pdf.cell(40, row_height*spacing, txt=row[0], border=0)
        img = ''
        imis = False
        
        for i in pic:   #poisk v spiske kartinok
            if i in (row[1]).upper().replace('/','_'):
                img= 'pic//' + i + '.jpeg'
                pdf.image(img, x=30, y=pic_y, w=18)
                pic_y += 25
                imis = True
                break
        if imis == False:
            pdf.image('none.jpeg', x=30, y=pic_y, w=18)
            pic_y += 25
       
                
        if len(row[1])<50:
            pdf.cell(120, row_height*spacing, txt=row[1], border=0,align="C")
            pdf.cell(15, row_height*spacing, txt=row[2]+' €', border=0)
            pdf.cell(15, row_height*spacing, txt=row[3], border=0)
            pdf.ln(row_height*spacing)
            pdf.ln(row_height*spacing)
        else:
            pn = (row[1])[49:]
            pn1 = (row[1])[:49]
            pdf.cell(120, row_height*spacing, txt=pn1, border=0,align="C")
            pdf.cell(15, row_height*spacing, txt=row[2]+' €', border=0)
            pdf.ln(row_height*spacing)
            pdf.cell(35, row_height*spacing, txt=' ', border=0)
            pdf.cell(120, row_height*spacing, txt=pn, border=0,align="C")
            pdf.cell(15, row_height*spacing, txt=row[3], border=0)
            pdf.ln(row_height*spacing)

            # new page
        if r == 9:
            r = 0
            pdf.add_page()
            image_path = 'logo.png' # логотип
            pdf.image(image_path, x=10, y=7, w=40)
            pdf.set_font('Hasklig-Light', size=12)
            pdf.ln(0)  # ниже
            pdf.line(5, 5, 5, 292)
            pdf.line(5, 292, 205, 292)
            pdf.line(5, 5, 205, 5)
            pdf.line(205, 5, 205, 292)
            pdf.line(5, 19, 205, 19)
            pdf.set_font('Hasklig-Bold', size=20)
            pdf.cell(190, 0, txt="PIEDĀVĀJUMS", ln=1, align="C")
            pdf.set_font('Hasklig-Light', size=8)
            client = entry.get()
            pdf.cell(220, 15, txt= company_name +"     Piedāvājuma numurs "+offer_number+"     Klients: "+client+'    '+dt, ln=1, align="C")
            pdf.set_font('Hasklig-Light', size=8)
            spacing = 1
            row_height = 12 # pdf.font_size
            pic_y = 18 # 18
    f_name =  'Offer' + offer_number
    filepath = filedialog.asksaveasfilename(initialdir = "offers", initialfile = f_name, defaultextension = 'pdf', confirmoverwrite = 'y' )
    if filepath != "":
        save_path(filepath)
        pdf.output(filepath)
    #window.destroy()
    return

def plus():
    global data
    lendata = len(data)
    outText = ''
    data1 = [str(entry1.get()).replace(',','.'), str(entry1a.get()).replace(',','.'), str(entry1b.get()).replace(',','.'), str(entry1c.get()).replace(',','.')]
    if str(entry1a.get())=='':
        return
    
    if '\n' in str(entry1a.get()):
        a = str(entry1a.get())
        a = a[0:len(a) ]
        a = a.split('\n')
        b = str(entry1b.get())
        b = b[0:len(b) ]
        b = b.split('\n')
        c = str(entry1c.get())
        c = c[0:len(c) ]
        c = c.split('\n')
        d = str(entry1.get())
        d = d[0:len(d) ]
        d = d.split('\n')
        for i in range(len(a)):
            dt = ['', '', '', '']
            try:
                dt[0] = d[i]
            except:
                dt[0] = ''
            try:
                dt[1] = a[i]
            except:
                dt[1] = ''
            try:
                dt[2] = b[i].replace(',', '.')
            except:
                dt[2] = ''
            try:
                dt[3] = c[i]
            except:
                dt[3] = ''
            data.append(dt)
    else:
        data.append(data1)
    entry1.delete(0,END)
    entry1a.delete(0,END)
    entry1b.delete(0,END)
    entry1c.delete(0,END)
    for i in data:
        outText += '\n'
        for j in i:
            outText = outText + j + '    '

    tree.delete(*tree.get_children())# очистка tree
    for i in data:
        i = tuple(i)
        tree.insert("", END, values=i)
    return

with open( 'set.txt', 'r', encoding = 'UTF-8') as f:
    company_name = (f.readline()).replace('\n','')
    work_dir = (f.readline()).replace('\n','')
    o_num = (f.readline()).replace('\n','')
offer_number = str((int(o_num))+1)
with open( 'set.txt', 'w', encoding = 'UTF-8') as f:
    f.write(company_name + '\n' + work_dir + '\n' + offer_number)
    
dt = d_now()

window = Tk()
window.title("Offerist")
window.geometry("1000x600")
#window.configure(background="grey")

f0 = Frame(window)
f_0 = Frame(window)
ff = Frame(window)
f_1 = Frame(window)
f_2 = Frame(window)
f0.pack()
f_0.pack()
ff.pack()
f_1.pack()
f_2.pack()

columns = ("code", "name", "price", 'decription')
tree = ttk.Treeview(columns=columns, show=" ")
tree.column('#1', width = 60, minwidth = 60, stretch = YES, anchor = W)
tree.column('#2', width = 600, minwidth = 600, stretch = YES, anchor = W)
tree.column('#3', width = 50, minwidth = 50, stretch = YES, anchor = W)
scrollbar = ttk.Scrollbar(orient="vertical", command=tree.yview)
scrollbar.pack(side=RIGHT, fill=Y)
tree.pack(fill=BOTH, expand=1)  

labelk = Label(f0, width=10, text = 'Client: ')
labelk.pack(side=LEFT, pady=0)

entry = Entry(f0, width=40)
entry.pack(side=LEFT, pady=10)
entry1 = Entry(f_1, width=10)
entry1.focus()
entry1.pack(side=LEFT, pady=10)
entry1a = Entry(f_1, width=80)
entry1a.pack(side=LEFT, pady=10)
entry1b = Entry(f_1, width=10)
entry1b.pack(side=LEFT, pady=10)
entry1c = Entry(f_1, width=20)
entry1c.pack(side=LEFT, pady=10)

labelf1 = Label(ff, width=12, text = 'Code')
labelf1.pack(side=LEFT, pady=0)
labelf1a = Label(ff, width=65, text = 'Description')
labelf1a.pack(side=LEFT, pady=0)
labelf1b = Label(ff, width=10, text = 'Price')
labelf1b.pack(side=LEFT, pady=0)
labelf1c = Label(ff, width=15, text = 'Remark')
labelf1c.pack(side=LEFT, pady=0)

button1 = Button(f_2,width=15, text="PDF", command=pdf_out)
button1.pack(side=RIGHT, expand=1)
button3 = Button(f_2,width=15, text="Save", command=save_data)
button3.pack(side=RIGHT, expand=1)
button4 = Button(f_2,width=15, text="Load", command=load_data)
button4.pack(side=RIGHT, expand=1)
button0 = Button(f_2,width=15, text="Sort", command = sort_data)
button0.pack(side=RIGHT, expand=1)
button2 = Button(f_2,width=15, text="+", command=plus)
button2.pack(side=RIGHT, expand=1)

window.mainloop()
