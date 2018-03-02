from mesure import Mesure
from aisio import AISIO

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image, ImageDraw, ImageTk
from math import floor
        
class Ihm(Frame):

    def alert(self):
        showinfo("alerte", "Bravo!")

    def openFicEnc(self):
        self.fichier = askopenfilename(title="Ouvrir un fichier encodé")
        self.encoded = True

    def openFicDec(self):
        self.fichier = askopenfilename(title="Ouvrir un fichier décodé")

    def msgDec(self):
        
        if (self.aisio == None):
            showinfo("Attention", "Aucun message à sauvegarder")
        else :
            fic = asksaveasfilename(title="Enregistrer les messages dans un fichier")
            self.aisio.saveAll(fic, self.mesure)

    def exportMat(self):
        if (self.matGenerated == False):
            showinfo("Attention", "Matrice pas encore générée")
        else :
            fic = asksaveasfilename(title="Enregistrer la matrice dans un fichier csv")
            self.mesure.grille.writeMatrice(fic)

    def exportImage(self):
        if (self.photo == None):
            showinfo("Attention", "Carte pas encore générée")
        else :
            fic = asksaveasfilename(title="Enregistrer la carte au format png")
            self.image.save(fic)

     
    def __init__(self, fenetre, **kwargs):

        self.mesure = Mesure()
        self.aisio = None
        Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill=BOTH)
        fenetre.title('Suivi AIS')
        self.fichier=''
        self.encoded = False
        self.matGenerated = False
        self.photo = None
        # Création de nos widgets

        self.menubar = Menu(fenetre)

        #self.menu1 = Menu(self.menubar, tearoff=0)
        #self.menu1.add_command(label="Nouveau",command=self.alert)
        #self.menu1.add_command(label="Quitter",command=fenetre.quit)
        #self.menubar.add_cascade(label="Fichier",menu=self.menu1)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="Fichier encodé",command=self.openFicEnc)
        self.menu2.add_command(label="Fichier décodé",command=self.openFicDec)
        self.menubar.add_cascade(label="Ouvrir",menu=self.menu2)

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menu3.add_command(label="Messages décodés",command=self.msgDec)
        self.menu3.add_command(label="Matrice résultat",command=self.exportMat)
        self.menu3.add_command(label="Exporter l'image",command=self.exportImage)
        self.menubar.add_cascade(label="Enregistrer",menu=self.menu3)

        fenetre.config(menu=self.menubar)


        self.frameGauche = Frame(fenetre,width=840,height=480)
        self.frameGauche.pack(side=LEFT)

        self.frameDroite = Frame(fenetre)
        self.frameDroite.pack(side=RIGHT)

        self.frameDHaut = LabelFrame(self.frameDroite, text="Nom et coordonnées de la balise (degrés)")
        self.frameDHaut.pack(side=TOP)

        self.frameDMilieu = LabelFrame(self.frameDroite, text="Coordonnées de la grille (degrés)")
        self.frameDMilieu.pack(side=TOP)

        self.frameDBas = Frame(self.frameDroite,pady=4)
        self.frameDBas.pack()

        self.baliseValue = StringVar()
        self.longitudeBaliseV = DoubleVar()
        self.latitudeBaliseV = DoubleVar()
        self.longitudeOValue = DoubleVar()
        self.longitudeEValue = DoubleVar()
        self.latitudeNValue = DoubleVar()
        self.latitudeSValue = DoubleVar()
        self.lignesV = IntVar()
        self.colonnesV = IntVar()

        self.labelBalise = Label(self.frameDHaut, text="Nom de la Balise", justify='left').grid(row=1,column=1)

        self.balise = Entry(self.frameDHaut,textvariable=self.baliseValue).grid(row=1,column=2)


        self.labelLongitudeBalise = Label(self.frameDHaut, text="Longitude Balise", justify='left').grid(row=2,column=1)

        self.longitudeBalise = Entry(self.frameDHaut,textvariable=self.longitudeBaliseV).grid(row=2,column=2)

        
        self.labelLatitudeBalise = Label(self.frameDHaut, text="Latitude Balise", justify='left').grid(row=3,column=1)

        self.latitudeBalise = Entry(self.frameDHaut,textvariable=self.latitudeBaliseV).grid(row=3,column=2)
        


        self.labelLongitudeO = Label(self.frameDMilieu, text="Longitude Ouest", justify='left').grid(row=1,column=1)

        self.longitudeO = Entry(self.frameDMilieu,textvariable=self.longitudeOValue).grid(row=1,column=2)


        self.labelLongitudeE = Label(self.frameDMilieu, text="Longitude Est", justify='left').grid(row=2,column=1)

        self.longitudeE = Entry(self.frameDMilieu,textvariable=self.longitudeEValue).grid(row=2,column=2)

        
        self.labelLatitudeN = Label(self.frameDMilieu, text="Latitude Nord", justify='left').grid(row=3,column=1)

        self.latitudeN = Entry(self.frameDMilieu,textvariable=self.latitudeNValue).grid(row=3,column=2)


        self.labelLatitudeS = Label(self.frameDMilieu, text="Latitude Sud", justify='left').grid(row=4,column=1)

        self.latitudeS = Entry(self.frameDMilieu,textvariable=self.latitudeSValue).grid(row=4,column=2)


        self.labelLignes = Label(self.frameDMilieu, text="Lignes", justify='left').grid(row=5,column=1)

        self.lignes = Entry(self.frameDMilieu,textvariable=self.lignesV).grid(row=5,column=2)


        self.labelColonnes = Label(self.frameDMilieu, text="Colonnes", justify='left').grid(row=6,column=1)

        self.colonnes = Entry(self.frameDMilieu,textvariable=self.colonnesV).grid(row=6,column=2)



        self.buttonGenerate = Button(self.frameDBas,text="Générer", command=self.generate)
        self.buttonGenerate.pack()


        

    def generate(self):
        if self.fichier =='':
            showinfo("Attention", "Veuillez ouvrir un fichier")
        else :
            self.aisio = AISIO(self.baliseValue.get())
        
            param = dict()	
            param['long'] = self.longitudeOValue.get()
            param['lat'] = self.latitudeNValue.get()
            param['rows'] = self.colonnesV.get()
            param['lines'] = self.lignesV.get()
            param['pasH'] = (self.longitudeEValue.get() - self.longitudeOValue.get()) / self.colonnesV.get()
            param['pasV'] = -(self.latitudeNValue.get() - self.latitudeSValue.get()) / self.lignesV.get()

            if (self.encoded == True):
                self.aisio.createFromFile(self.fichier,self.mesure)
            else :
                self.aisio.loadAll(self.fichier,self.mesure)
                self.aisio.saveAll("nav2.log",self.mesure)

           

            self.mesure.createGrid(param)

            #print(self.mesure.grille.paramSTR())

            self.mesure.sortByCase()
 
            self.mesure.applyAlgo() 

            self.mesure.grille.fillMatrice()
            self.matGenerated = True
            #self.mesure.grille.writeMatrice("mat2.csv")

            #self.mesure.grille.printGrid('grid2.log')

            self.createMap()

    def createMap(self):
        m = Basemap(projection='merc',llcrnrlat=self.latitudeSValue.get(),urcrnrlat=self.latitudeNValue.get(), llcrnrlon=self.longitudeOValue.get(),urcrnrlon=self.longitudeEValue.get(),lat_ts=20,resolution='h')
        m.drawcoastlines()
        m.fillcontinents(color='burlywood',lake_color='darkcyan')

        m.drawmapboundary(fill_color='darkcyan')

        x,y = m(self.longitudeBaliseV.get(),self.latitudeBaliseV.get())
        m.plot(x,y,'bo',markersize=4)

        plt.savefig('carte.png',dpi=220,bbox_inches='tight',pad_inches=0.0,frameon=False)


        nbLignes = self.lignesV.get()
        nbColonnes = self.colonnesV.get()

        img = Image.open('carte.png')

        w = 840
        ratio = img.width/img.height
        h = floor(w / ratio)

        img = img.resize((w,h))
        
        img2 = img.crop((2,2,img.width-2,img.height-2))


        draw = ImageDraw.Draw(img2)

        y_start = 0
        y_end = img2.height
        step_size_x = int(img2.width / nbColonnes)

        for x in range(0, img2.width, step_size_x):
            line = ((x,y_start),(x,y_end))
            draw.line(line,fill=128)

        x_start = 0
        x_end = img2.width
        step_size_y = int(img2.height / nbLignes)

        for y in range(0, img2.height, step_size_y):
            line = ((x_start,y),(x_end,y))
            draw.line(line, fill=128)


        imgRouge = Image.new('RGBA', (step_size_x,step_size_y),(255,0,0,127))
        imgOrange = Image.new('RGBA', (step_size_x,step_size_y),(255,153,51,127))
        imgJaune = Image.new('RGBA', (step_size_x,step_size_y),(255,204,0,127))
        imgVerte = Image.new('RGBA', (step_size_x,step_size_y),(0,204,0,127))
        imgBleue = Image.new('RGBA', (step_size_x,step_size_y),(0,102,255,127))
        

        for i in range(0,nbLignes):
            for j in range(0,nbColonnes):
                val = int(self.mesure.grille.matrice[i,j]*100)
                print(val)
                if (val <= 100 and val > 85):
                    img2.paste(imgVerte,(j*step_size_x,i*step_size_y),imgVerte)
                elif (val <= 85 and val > 70):
                    img2.paste(imgJaune,(j*step_size_x,i*step_size_y),imgJaune)
                elif (val <= 70 and val > 40):
                    img2.paste(imgOrange,(j*step_size_x,i*step_size_y),imgOrange)
                elif (val <= 40 and val > 1):
                    img2.paste(imgRouge,(j*step_size_x,i*step_size_y),imgRouge)
                else :
                    img2.paste(imgBleue,(j*step_size_x,i*step_size_y),imgBleue)



        del draw

        #img2.save('carte2.png')
        self.image = img2
        self.photo = ImageTk.PhotoImage(img2)

        self.canvas = Canvas(self.frameGauche,width=img2.width,height=img2.height)
        self.canvas.create_image(0,0,anchor=NW,image=self.photo)

        self.canvas.pack()
        
        

        
fenetre = Tk()

ihm = Ihm(fenetre)

ihm.mainloop()
ihm.destroy()
