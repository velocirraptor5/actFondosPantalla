import requests
import urllib.request
import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import webbrowser

direccion="c:/Users/luido/Pictures/posters"
direccion2="C:\\Users\\luido\\Pictures\\posters\\"

titulos=[]
links=[]
posters=[]
cartelera=[]

def yaesta(nombre):
    for file in os.listdir(direccion):
        if file==nombre+'.jpg':
            return True
    return False

def borrar():
    files=os.listdir(direccion)
    os.chdir(direccion)
    files.sort(key=os.path.getctime)
    if len(files)>50:
        os.remove(files[0])
        print("se borro "+ files[0])

def descargar(name,rootfoto,iPel):
    page_descarga=links[iPel]
    response = requests.get(page_descarga)
    soup= BeautifulSoup(response.content,'html.parser')
    pelicula=soup.find(class_='table table-hover')
    torrent=str(pelicula.find('a')['href'])
    webbrowser.open_new(torrent)
    rootfoto.destroy()

def poster(name):
    global my_img_grande 
    rootfoto=Toplevel()
    rootfoto.title(name)
    rootfoto.iconbitmap('C:/Users/luido/Pictures/fondo/favicon.ico')
    iPel=titulos.index(name.replace(".jpg",""))
    try:    
        img=Image.open(direccion+'/'+name)
        img= img.resize((419,600),Image.ANTIALIAS)
        my_img_grande = ImageTk.PhotoImage(img)
        my_label=Label(rootfoto,image=my_img_grande)
        #my_label=Label(rootfoto,text=name,padx=384,pady=216)
        my_label.grid(row=0,column=0,columnspan=1)
    except Exception as e:
        print(str(e))
        print("no compa ni idea de eso porque no descarga bien")
        my_label=Label(rootfoto,text=name)
        my_label.grid(row=0,column=0)
    botonDescargar =Button(rootfoto,text="Descargar",command=lambda rootfoto=rootfoto: descargar(name,rootfoto,iPel)).grid(row=1,column=0)
    rootfoto.mainloop()

def front():
    root= Tk()
    root.title("Pelicualas en cartera")
    root.iconbitmap('C:/Users/luido/Pictures/fondo/favicon.ico')
    container= Frame(root,width=1070,height=600)
    canva=Canvas(container,width=1050,height=600)
    scroll = Scrollbar(container,orient="vertical",command=canva.yview)
    frameScroll=Frame(canva)
    frameScroll.bind("<Configure>", lambda e: canva.configure(scrollregion=canva.bbox("all")))
    canva.create_window((0,0),window=frameScroll,anchor="nw")
    canva.configure(yscrollcommand=scroll.set)
    global my_img
    my_img=[]
    files=os.listdir(direccion)
    os.chdir(direccion)
    files.sort(key=os.path.getctime)
    cartelera=files[-1:-16:-1]
    indice=0
    indicePelicula=0
    for i,ima in enumerate(cartelera):
        print(ima)
        try:
            img=Image.open(direccion+'/'+ima)
            img= img.resize((210,300),Image.ANTIALIAS)
            my_img_temp = ImageTk.PhotoImage(img)
            my_img.append(my_img_temp)
            myBot=Button(frameScroll,image=my_img[indice],command= lambda i=i:poster(cartelera[i])).grid(row=int(i/5),column=i%5)
            indice+=1
        except Exception as e:
            print(str(e))
            messagebox.showinfo("la imagen no se pudo abrir","La imagen {} no se descargo bien".format(ima))
            myBot=Button(frameScroll,text=ima,command= lambda i=i:poster(cartelera[i])).grid(row=int(i/5),column=i%5)
    container.pack()
    canva.pack(side="left",fill="both",expand=True)
    scroll.pack(side="right",fill="y")
    root.geometry("1070x600")
    root.mainloop()
    


for i in range(5):
    page= "https://allcalidad.la/page/"+str(i+1)
    response = requests.get(page)
    soup= BeautifulSoup(response.content,'html.parser')
    for pelicula in soup.find_all(class_='ah-imagge',href=True):
        tituloTemp=str(pelicula.find('img')['title'])
        tituloTemp=tituloTemp.replace(":","=")
        if(len(tituloTemp)>35):
            tituloTemp=tituloTemp[0:35]
        titulos.append(tituloTemp)
        links.append(pelicula['href'])
        posters.append(pelicula.find('img')['data-src'])
        
for j in range(len(titulos)):
    if(yaesta(titulos[j])):
        print("Peliculas Actualizadas")
        front()
        input("precione enter para cerrar el programa")
        exit()
    print(titulos[j])
    img_poster=str(posters[j])
    img_poster=img_poster.replace(".webp","")
    #img_poster=img_poster.encode()
    #print(img_poster)
    img_poster=urllib.parse.quote(img_poster,safe=':/')
    print(img_poster)
    #urllib.request.urlretrieve(img_poster,direccion2+titulos[j]+'.jpg')
    """opener=urllib.request.URLopener()
    opener.addheader('User-Agent','Mozilla/5.0')
    filename,headers=opener.retrieve(img_poster,direccion2+titulos[j]+'.jpg')"""
    r=requests.get(img_poster)
    with open(direccion+'/'+titulos[j]+'.jpg','wb') as outfile:
        outfile.write(r.content)
    for t in range(1):
            print('.',end="",flush=True)
            time.sleep(1)
    borrar()

front()
"""
urllib.request.urlretrieve(tx,direccion2+imagen+'.jpg')
print(titulos)
print(links)
print(posters)"""
    
        