import random # Pour les tirages aleatoires
import sys # Pour quitter proprement
import pygame # Le module Pygame
import pygame.freetype # Pour afficher du texte
import math
from constante import *
from classes import *
import datetime
import time
import csv

pygame.init()
pygame.mixer.init()

global Meilleur_score
Meilleur_score = {}


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
        self.ecran_nom = False
        self.nomjoueur = 'None'
        self.time = 0
    
    def quit_game(self,quit = True):

        if self.time == 0:
            self.time = time.time()-self.start

        if not quit: #On ajoute le meilleur score uniquement si la partie a été terminée
            fichier=open('Meilleur_score.txt','w')
            fichier.write(Meilleur_score['Nom']+'\n'+str(Meilleur_score['Score'])+'\n'+str(Meilleur_score['Temps']))
            fichier.close()

        #Update all_players
        csvfile =  open('all_players.csv', 'a', newline='')
        fieldnames = ['name', 'score','inGameTime','day','time','quitted']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #Update nom des colonnes si le fichier est vide
        file = open('all_players.csv', 'r', encoding='utf-8')
        empty = file.read()==''
        file.close()

        if empty:
            writer.writeheader()

        #Ajout du joueur courrant
        timecode = datetime.datetime.now()
        timecode = timecode.strftime('%d-%m-%Y %H:%M:%S')
        mydate,mytime = timecode.split()
        print(mytime[:7])
        writer.writerow({'name': self.nomjoueur, 'score': self.score,'inGameTime':round(self.time,3), 'day' : mydate,'time':mytime,'quitted':quit})
        csvfile.close()

        #On quitte
        pygame.quit()
        sys.exit()
        exit()

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
        else:
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
            self.afficher_ecran_debut()

        elif self.partie==False:
            if self.vies==0:
                self.afficher_ecran_defaite()
            else:
                self.afficher_ecran_victoire()

            self.time=time.time()-self.start
            if Meilleur_score['Score']<self.score or (Meilleur_score['Score']==self.score and Meilleur_score['Temps']>=self.time) :
                Meilleur_score['Nom']=self.nomjoueur
                Meilleur_score['Score']=self.score
                Meilleur_score['Temps']=self.time

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

    def afficher_ecran_debut(self):
        screen.fill(DEBUT)
        texte = 'LE MEILLEUR CASSE BRIQUES'
        texte = font2.render(texte,True,NOIR)
        screen.blit(texte,[XMAX//2-texte.get_rect().width//2,YMAX//2-60])
        texte = '( Vous allez être époustoufflés )'
        texte = font.render(texte,True,NOIR)
        screen.blit(texte,[XMAX//2-texte.get_rect().width//2,YMAX//2-30])
        texte = 'Pour commencer, appuyez sur espace'
        texte = font.render(texte,True,NOIR)
        screen.blit(texte,[XMAX//2-texte.get_rect().width//2,YMAX//2])
        screen.blit(font.render('Meilleur score détenu par ' +Meilleur_score['Nom']+
                                ' avec '+str(Meilleur_score['Score'])+' points en '+
                                str(round(Meilleur_score['Temps'],3))+' secondes',True,BLANC),[XMIN+10,YMIN+10])

    def afficher_ecran_defaite(self):
        screen.fill(DEFAITE)
        screen.blit(font2.render('Game over :(',True,NOIR),[XMAX//2-70,YMAX//3])
        screen.blit(font.render('Votre score : '+str(self.score),True,NOIR),[XMAX//2-60,YMAX//2])
        screen.blit(font.render('Rejouer ? o : oui, n : non',True,NOIR),[XMAX//2-100,YMAX//2+20])

    def afficher_ecran_victoire(self):
        screen.fill(VICTOIRE)
        screen.blit(font2.render('Fin de partie !',True,NOIR),[XMAX//2-70,YMAX//3])
        screen.blit(font.render('Votre score : '+str(self.score),True,NOIR),[XMAX//2-60,YMAX//2])
        screen.blit(font.render('Rejouer ? o : oui, n : non',True,NOIR),[XMAX//2-100,YMAX//2+20])

    def afficher_page_nom(self):
            
            # basic font for user typed 
            base_font = pygame.font.Font(None, 32) 
            user_text = '' 
            
            # create rectangle 
            input_rect = pygame.Rect(XMAX//4, YMAX//2, XMAX//2, 32) 
            
            # color_active stores color(lightskyblue3) which 
            # gets active when input box is clicked by user 
            color_active = pygame.Color('lightskyblue3') 
            
            # color_passive store color(chartreuse4) which is 
            # color of input box. 
            color_passive = pygame.Color('chartreuse4') 
            color = color_passive 
            
            active = False

            name_text = "Entrez votre nom, joueur !"
            name_text = font2.render(name_text,True,NOIR)
            name_text_position = [(XMAX//2)-(name_text.get_rect().width//2),YMAX//3]

            validation_text = "-- appuyez sur entrée pour valider --"
            validation_text = small_font.render(validation_text,True,NOIR)
            validation_text_position = [(XMAX//2)-(validation_text.get_rect().width//2),2*YMAX//3]

            has_max_char = False
            
            while True: 
                for event in pygame.event.get(): 
            
                # if user types QUIT then the screen will close 
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                        self.quit_game()
            
                    if event.type == pygame.MOUSEBUTTONDOWN: 
                        if input_rect.collidepoint(event.pos): 
                            active = True
                        else: 
                            active = False
            
                    if event.type == pygame.KEYDOWN: #traiter le cas ou on reste appuyé sur la touche

                        if event.key == pygame.K_RETURN:
                            return user_text
            
                        # Check for backspace 
                        if event.key == pygame.K_BACKSPACE: 
            
                            # get text input from 0 to -1 i.e. end. 
                            user_text = user_text[:-1]
                            if has_max_char:
                                has_max_char = False
            
                        # Unicode standard is used for string 
                        # formation 
                        else: 
                            if not has_max_char:
                                user_text += event.unicode

                
                # it will set background color of screen 
                screen.fill(DEBUT)
                screen.blit(name_text,name_text_position)
                screen.blit(validation_text,validation_text_position)
            
                if active: 
                    color = color_active 
                else: 
                    color = color_passive 
                    
                # draw rectangle and argument passed which should 
                # be on screen 
                pygame.draw.rect(screen, color, input_rect) 
            
                text_surface = base_font.render(user_text, True, (255, 255, 255)) 
                
                # render at position stated in arguments 
                screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
             
                # set width of textfield so that text cannot get 
                # outside of user's text input 
                # Pour ne pas dépasser la taille de la box
                if text_surface.get_width()+20 >= XMAX//2: 
                    has_max_char = True
                #input_rect.w = XMAX//2
                
                # display.flip() will update only a portion of the 
                # screen to updated, not full area 
                pygame.display.flip() 
                
                # clock.tick(60) means that for every second at most 
                # 60 frames should be passed. 
                clock.tick(60) 

    def get_nom(self):
        self.nomjoueur = self.afficher_page_nom()

    def gestion_evenements(self):
        # Gestion des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): #pour quitter, refait car ça crashait à chaque fois
                self.quit_game()
            elif self.ecran_debut==True:
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        self.ecran_debut=False
                        self.ecran_nom = True
                        self.get_nom()
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
                        self.quit_game(quit=False)


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

Meilleur_score['Nom']=contenu[0]
Meilleur_score['Score']=int(contenu[1])
Meilleur_score['Temps']=float(contenu[2])
#Nom=str(input('Entrez votre nom, joueur !'))
jeu = Jeu()
jeu.recup_briques('briques.txt')
musics=['mario-kart-wii.mp3','super-mario-64.mp3']
pygame.mixer.music.load(random.choice(musics))
pygame.mixer.music.play(-1)
pygame_icon = pygame.image.load('logo.png')
pygame.display.set_icon(pygame_icon)
while True:
    clock.tick(60) # envoi de l'image ÃƒÆ’Ã‚Â  la carte graphique
    pygame.display.flip() # on attend pour ne pas dÃƒÆ’Ã‚Â©passer 60 images/seconde
    jeu.gestion_evenements()
    jeu.mise_a_jour()
    jeu.affichage()



