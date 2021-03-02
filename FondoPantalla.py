import requests
import bs4
import urllib.request
import time
import os
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image

direccion="C:/Users/luido/Pictures/fondo"
direccion2= 'C:\\Users\\luido\\Pictures\\fondo\\'

def yaesta(nombre):
    for file in os.listdir(direccion):
        if file==nombre+'.jpg':
            return True
    return False

def borrar():
    menor=9999999
    for file in os.listdir(direccion):
        temp=file
        file=file.split('_')
        try:
            numero=int(file[-1].replace(".jpg",""))
            if(numero<menor):
                menor=numero
                doc=temp
        except:
            continue
    if len(os.listdir(direccion))>300:
        os.remove(direccion+"/"+doc)
        print("se borro "+ doc)

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
    except:
        entrada= input("aparente mente no estas conectado a internet preciona:\n[F]     para salir\n[enter] para volver a intentar\n")
        if(entrada=='F'):
            exit()
        else:
            for t in range(5):
                print('.',end="",flush=True)
                time.sleep(1)
            print("\nAsegurate que estes conectado a una red")
            connect()



def guardar(name,rootfoto):
    newn=name.split('_')
    del newn[-1]
    slash="_"
    os.rename(direccion+'/'+name,direccion+'/'+slash.join(newn) + ".jpg")
    messagebox.showinfo(name,"la imagen {} ha sido guardada".format(slash.join(newn)))
    rootfoto.destroy()

def eliminar(name,rootfoto):
    os.remove(direccion+'/'+name)
    messagebox.showinfo(name,"la imagen {} ha sido eliminada".format(name))
    rootfoto.destroy()

def foto(name):
    global my_img_grande 
    rootfoto=Toplevel()
    rootfoto.title(name)
    rootfoto.iconbitmap(direccion+'/favicon.ico')
    img=Image.open(direccion+'/'+name)
    img= img.resize((384,216),Image.ANTIALIAS)
    my_img_grande = ImageTk.PhotoImage(img)
    my_label=Label(rootfoto,image=my_img_grande)
    #my_label=Label(rootfoto,text=name,padx=384,pady=216)
    my_label.grid(row=0,column=0,columnspan=2)
    
    botonGuardar =Button(rootfoto,text="Guardar",command=lambda rootfoto=rootfoto: guardar(name,rootfoto)).grid(row=1,column=0)
    botonEliminar =Button(rootfoto,text="Eliminar",command=lambda rootfoto=rootfoto: eliminar(name,rootfoto)).grid(row=1,column=1)
    
    rootfoto.mainloop()

def front():
    root= Tk()
    root.title("Fondo de Pantalla")
    root.iconbitmap(direccion+'/favicon.ico')
    container= Frame(root,width=980,height=540)
    canva=Canvas(container,width=960,height=540)
    scroll = Scrollbar(container,orient="vertical",command=canva.yview)
    frameScroll=Frame(canva)
    frameScroll.bind("<Configure>", lambda e: canva.configure(scrollregion=canva.bbox("all")))

    canva.create_window((0,0),window=frameScroll,anchor="nw")
    canva.configure(yscrollcommand=scroll.set)
    global my_img
    my_img=[]
    for i,ima in enumerate(nuevas):
        img=Image.open(direccion+'/'+ima)
        img= img.resize((192,108),Image.ANTIALIAS)
        my_img_temp = ImageTk.PhotoImage(img)
        my_img.append(my_img_temp)
        myBot=Button(frameScroll,image=my_img[i],command= lambda i=i:foto(nuevas[i])).grid(row=int(i/5),column=i%5)
    container.pack()
    canva.pack(side="left",fill="both",expand=True)
    scroll.pack(side="right",fill="y")
    root.geometry("980x540")
    root.mainloop()

connect()
global  nuevas
nuevas=[]
for i in range(10):
    page='https://wallpaperscraft.com/all/page'+str(i+1)
    response= requests.get(page)
    soup= bs4.BeautifulSoup(response.text,'html.parser')
    wallpapers_links= soup.select('.wallpapers__link')
    wallpapers = [wallpaper['href'] for wallpaper in wallpapers_links]
    nombreImagen=[]     
    for wallpaper in wallpapers:
        nombreImagen.append(wallpaper.split('/')[-1])

    for imagen in nombreImagen:
        if(yaesta(imagen)):
            print("fondos de pantalla actualizados")
            front()
            input("preciona enter para cerrar el programa")
            exit()

        tx='https://images.wallpaperscraft.com/image/'+imagen+'_1920x1080.jpg'
        print("Descargando imagen {} ".format(imagen))
        try:
            urllib.request.urlretrieve(tx,direccion2+imagen+'.jpg')
            for t in range(1):
                print('.',end="",flush=True)
                time.sleep(1)
            print("DONE")
            nuevas.append(imagen+'.jpg')
            borrar()
        except:
            print('la imagen no se puede descargar')
    



    
    