import random # Pour les tirages aleatoires
import sys # Pour quitter proprement
import pygame # Le module Pygame
import pygame.freetype # Pour afficher du texte
import math
from constante import *
from classes import *
import datetime
import time

pygame.init()
pygame.mixer.init()


class Jeu:
    def __init__(self):
        self.balle = Balle()
        self.raquette = Raquette()
        self.vies=3
        self.all_briques=[]
        self.stage=1
        self.score=0
        self.fin_stage=False
        self.start=None
        self.partie=True
        self.ecran_debut=True

    def stage_suivant(self):
        self.stage+=1
        if self.stage>=6:
            self.partie=False
        else:
            self.balle = Balle()
            self.raquette = Raquette()
            self.recup_briques('briques'+str(self.stage)+'.txt')
            self.fin_stage=False
            if self.stage==3 or self.stage==5:
                oneup=pygame.mixer.Sound('vie.ogg')
                oneup.play()
                self.vies+=1


    def rejouer(self):
        Nom=str(input('Entrez votre nom, joueur !'))
        self.ecran_debut=True
        self.balle=Balle()
        self.raquette = Raquette()
        self.vies=3
        self.all_briques=[]
        self.stage=1
        self.score=0
        self.fin_stage=False
        self.partie=True
        jeu.recup_briques('briques.txt')

    def mise_a_jour(self):
        if self.vies==0:
            self.partie=False
        x, y = pygame.mouse.get_pos()
        self.balle.deplacer(self.raquette)
        self.score=0
        self.fin_stage=True
        for brique in self.all_briques:
            if brique.en_vie():
                brique.collision_balle(self.balle,self.raquette)
                if brique.type!='Indestructible':
                    self.fin_stage=False
            else:
                self.score+=100
        if self.balle.y + RAYON_BALLE > YMAX:
            self.vies-=1
        self.raquette.deplacer(x)

    def affichage(self):
        screen.fill(FOND) # on efface l'écran
        if self.ecran_debut==True:
            screen.fill(DEBUT)
            screen.blit(font2.render('LE MEILLEUR CASSE BRIQUES',True,NOIR),[XMAX//4+30,YMAX//2-60])
            screen.blit(font.render('( Vous allez être époustoufflés )',True,NOIR),[XMAX//3+10,YMAX//2-30])
            screen.blit(font.render('Pour commencer, appuyez sur espace',True,NOIR),[XMAX//3-10,YMAX//2])
            screen.blit(font.render('Meilleur score détenu par ' +Meilleur_score['Nom']+' avec '+str(Meilleur_score['Score'])+' points en '+str(round(Meilleur_score['Temps'],3))+' secondes',True,BLANC),[XMIN+10,YMIN+10])
        elif self.partie==False:
            if self.vies==0:
                screen.fill(DEFAITE) #écran de défaite
                screen.blit(font2.render('Game over :(',True,NOIR),[XMAX//2-70,YMAX//3])
                screen.blit(font.render('Votre score : '+str(self.score),True,NOIR),[XMAX//2-60,YMAX//2])
                screen.blit(font.render('Rejouer ? o : oui, n : non',True,NOIR),[XMAX//2-100,YMAX//2+20])
            else:
                screen.fill(VICTOIRE)
                screen.blit(font2.render('Fin de partie !',True,NOIR),[XMAX//2-70,YMAX//3])
                screen.blit(font.render('Votre score : '+str(self.score),True,NOIR),[XMAX//2-60,YMAX//2])
                screen.blit(font.render('Rejouer ? o : oui, n : non',True,NOIR),[XMAX//2-100,YMAX//2+20])
            timer=time.time()-self.start
            if Meilleur_score['Score']<self.score :
                Meilleur_score['Nom']=Nom
                Meilleur_score['Score']=self.score
                Meilleur_score['Temps']=timer
            elif Meilleur_score['Score']==self.score and Meilleur_score['Temps']>=timer:
                Meilleur_score['Nom']=Nom
                Meilleur_score['Score']=self.score
                Meilleur_score['Temps']=timer
        elif self.fin_stage==True:
            self.stage_suivant()
        else:
            self.balle.afficher()
            self.raquette.afficher()
            for brique in self.all_briques:
                if brique.en_vie():
                    brique.afficher()
            tps=datetime.timedelta(seconds=time.time()-self.start)
            screen.blit(font.render('Vies : '+str(self.vies),True,BLANC),[XMAX-80,YMAX-20])
            screen.blit(font.render('Score : '+str(self.score),True,BLANC),[XMIN+10,YMAX-20])
            screen.blit(font.render(str(tps),True,BLANC),[XMAX//2-50,YMAX-20])
            screen.blit(font.render('Stage '+str(self.stage),True,STAGE),[XMAX//2-20,YMIN+2])


    def gestion_evenements(self):
        # Gestion des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #pour quitter, refait car ça crashait à chaque fois
                pygame.quit()
                sys.exit()
                exit()
            elif self.ecran_debut==True:
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        self.ecran_debut=False
                        self.start=time.time()
            elif event.type == pygame.MOUSEBUTTONDOWN: # On vient de cliquer sur la souris
                if event.button == 1: # Bouton gauche
                    if self.balle.sur_raquette:
                        self.balle.sur_raquette = False
                        self.balle.vitesse_par_angle(90)
            elif self.partie==False: #jouer son perdu ?
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_o:
                        self.rejouer()
                    elif event.key==pygame.K_n:
                        pygame.quit()
                        sys.exit()
                        exit()



    def recup_briques(self,fichier):
        doc=open(fichier)
        x,y=5,20
        for ligne in doc:
            for c in ligne:
                if c=='X': #brique classique
                    self.all_briques.append(Brique(x*10,y))
                    if x+5>=width:
                        y+=30
                        x=5
                    else:
                        x+=5
                elif c=='B': #Brique bleue +2 vie
                    self.all_briques.append(Brique(x*10,y,3,(0,100,200),'Trois_Coups'))
                    if x+5>=width:
                        y+=30
                        x=5
                    else:
                        x+=5
                elif c=="M" : #Brique agrandissante
                    self.all_briques.append(Brique(x*10,y,1,(200,0,150),'Upgrade'))
                    if x+5>=width:
                        y+=30
                        x=5
                    else:
                        x+=5
                elif c=='I': #brique indestructible
                    self.all_briques.append(Brique(x*10,y,float('inf'),(0,0,0),'Indestructible'))
                    if x+5>=width:
                        y+=30
                        x=5
                    else:
                        x+=5

                elif c=='J':#2 vies
                    self.all_briques.append(Brique(x*10,y,2,(225,191,24),'Deux_Coups'))
                    if x+5>=width:
                        y+=30
                        x=5
                    else:
                        x+=5

                elif c=='Y': #retour à la ligne
                    y+=30
                    x=5
                elif c==' ': #espace
                    if x+5>=width:
                        y+=30
                        x=5
                    else : x+=5



fichier=open('Meilleur_score.txt','r')
contenu=fichier.readlines()
fichier.close()
contenu[0]=contenu[0].replace('\n','')
contenu[0]=contenu[0].strip("'")
Meilleur_score={}
Meilleur_score['Nom']=contenu[0]
Meilleur_score['Score']=int(contenu[1])
Meilleur_score['Temps']=float(contenu[2])
Nom=str(input('Entrez votre nom, joueur !'))
jeu = Jeu()
jeu.recup_briques('briques.txt')
musics=['mario-kart-wii.mp3','super-mario-64.mp3']
pygame.mixer.music.load(random.choice(musics))
pygame.mixer.music.play(-1)
pygame_icon = pygame.image.load('logo.png')
pygame.display.set_icon(pygame_icon)
while True:
    jeu.gestion_evenements()
    jeu.mise_a_jour()
    jeu.affichage()
    pygame.display.flip() # envoi de l'image ÃƒÆ’Ã‚Â  la carte graphique
    clock.tick(60) # on attend pour ne pas dÃƒÆ’Ã‚Â©passer 60 images/seconde
    fichier=open('Meilleur_score.txt','w')
    fichier.write(Meilleur_score['Nom']+'\n'+str(Meilleur_score['Score'])+'\n'+str(Meilleur_score['Temps']))
    fichier.close()


