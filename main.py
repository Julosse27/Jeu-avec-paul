import pyxel as px
from os.path import realpath, dirname, join
from ressources.outils import *
from typing import Literal

CHEMIN_RES = f"{join(realpath(dirname(__file__)), "ressources")}/"

CHEK_TOUCHES: Touches

FPS: int

DROITE = px.KEY_D
GAUCHE = px.KEY_Q
HAUT = px.KEY_Z
BAS = px.KEY_S

class Jeu():
    """
    La structure principale du jeu.
    Elle contiendra tout les éléments du jeu complet.
    """
    def __init__(self, title: str, width: int = 100, height: int = 100, fps: int = 30) -> None:
        px.init(width, height, title= title, fps= fps) # Initialise la fenètre de jeu (width et height taille de la fenètre, 
                                                       # title son titre et fps les nombre de vérification du code par secondes)

        global CHEK_TOUCHES, FPS

        FPS = fps

        CHEK_TOUCHES = Touches(GAUCHE, DROITE, HAUT, BAS)

        self.perso = Perso()

        self.perso.placer_perso(y= 50)
        
        px.run(self.update, self.draw) # Lance la fenètre de jeu

    def update(self):
        """
        Cette fonction va contenir toutes les modifications de variables en tout genres.
        """
        CHEK_TOUCHES.update()

        self.perso.update()

    def draw(self):
        """
        Cette fonction va contenir toutes les commandes pour dessiner l'écran de jeu.
        """
        px.cls(0)
        self.perso.draw()
 
class Perso():
    def __init__(self, vitesse:int = 10) -> None:
        px.load(f"{CHEMIN_RES}perso.pyxres")
        self.img = px.images[0]

        self.x = 0
        self.y = 0
        self.sens = 1
        self.hitbox_x = 8
        self.hitbox_y = 8
        self._dep_x = 0
        self._dep_y = 0
        self._REG_VITESSE = vitesse # Réglage de la vitesse: à modifier en fonction de la taille finale
                                # de la fenètre et de la sensation de vitesse souhaité.
        self._LIMITE = (FPS//3) * 100

        self.delay_vitesse = 0
        self.tps_v_max = 5 * FPS
        self._REGULATEUR = FPS // 2
        self.essouflement = 3
        self.derapage = 0
        self.derap_sens = 0
        self._LIMITE_DERAPAGE_D = 2 * FPS // 3
        self._LIMITE_DERAPAGE = FPS // 4
        self._tps_stase = 0

        self.etat_perso: Literal["Stase", "Mvt", "Derapage"] = "Stase"
        self.etat_anim = 0
        self.LISTE_U = (0, 16, 32, 48, 64, 80, 96, 112)
        self.LIGNES_ANIMS = {"Stase": 0, "Mvt": 16, "Derapage": 32}

        self._block_mouv = False
        self._block_draw = False

    def placer_perso(self, x:int = 8, y:int = 8):
        """
        Place le personnage a un endroit spécifique du jeu. 

        :param x: Les coordonnées x du millieu du perso.
        :type x: int
        :param y: Les coordonnées y du milieu du perso.
        :type y: int
        """
        self.x = x - 8
        self.y = y - 8
        self.hitbox_x = x
        self.hitbox_y = y

    def update(self):
        """
        Fonction à éxécuter chaque frame pour faire fonctionner le perso.
        """
        self.mouvements_complets()

    def mouvements_complets(self):
        """
        Fonction qui gère tout les déplacements.
        """
        etat_touches = CHEK_TOUCHES(DROITE, GAUCHE, HAUT)

        if not self._block_mouv:
            acceleration = self.delay_vitesse * 100 // self._REGULATEUR

            vitesse = acceleration * self._REG_VITESSE
            
            # Vérifie si il y à eu un mouvement.
            if (etat_touches[DROITE] and etat_touches[GAUCHE] or 
                not etat_touches[DROITE] and not etat_touches[GAUCHE]):
                self.etat_perso = "Stase" # Définit l'état de l'animation en Stase.
                augmentation_v = False # Arrète l'augmentation de la vitesse.
                self._tps_stase += 1 # Met à jour le tps depuis le dernier mouvement.
            else:
                sens_mvt = 1 if etat_touches[DROITE] else -1 #Définit le sens du mouvement enregistré cette frame.
                augmentation_v = True #Déclenchement de l'accélération de cette frame.
                self.etat_perso = "Mvt" #Définit l'etat de l'animation du perso en mouvement.

                #Vérifie si on se trouve dans une situation de dérapage:
                #   - le dernier sens enregistré est le sens contraire;
                #   - le tps depuis le dernier mouvement est assez cour;
                #   - le dérapage ne se superpose pas à un autre.
                if self.sens != sens_mvt and self._tps_stase < self._LIMITE_DERAPAGE and self.derapage == 0:
                    self.derapage = self._LIMITE_DERAPAGE_D #Commence le dérapage.
                    self.derap_sens = sens_mvt

                self._tps_stase = 0 # Réinitialise le compteur du tps dans l'état Stase.

                self.sens = sens_mvt # Définit le sens du perso.
                if not self.derapage: # Si le perso ne dérape pas.
                    self._dep_x += vitesse * self.sens # Fait avancer le personnage.

            if self.derapage > 0:
                self.derapage -= 1
                self.delay_vitesse -= 2 if self.delay_vitesse > 0 else 0
                decallage_derapage = self.derapage * vitesse // (FPS // 30 * 20)
                self._dep_x -= decallage_derapage * self.derap_sens
                self.etat_perso = "Derapage"
                
            while abs(self._dep_x) >= self._LIMITE:
                self.x += px.sgn(self._dep_x)
                self._dep_x += -px.sgn(self._dep_x) * self._LIMITE

            while abs(self._dep_y) >= self._LIMITE:
                self.y += px.sgn(self._dep_y)
                self._dep_y = -px.sgn(self._dep_y) * self._LIMITE

            if augmentation_v:
                self.delay_vitesse = (self.delay_vitesse + 1) if self.delay_vitesse < self.tps_v_max else self.tps_v_max
            else:
                self.delay_vitesse = (self.delay_vitesse - self.essouflement) if self.delay_vitesse - self.essouflement > 0 else 0
        else:
            self.delay_vitesse = 0
            self._dep_x = 0
            self._dep_y = 0

    def draw(self):
        if not self._block_draw:
            px.blt(self.x, self.y, self.img, self.LISTE_U[self.etat_anim], self.LIGNES_ANIMS[self.etat_perso], 16, 16, 0)

        if px.frame_count % 4 * (FPS // 30) == 0:
            if self.etat_anim == 7:
                self.etat_anim = 0
            else:
                self.etat_anim += 1

Jeu("Test", 500, 100, 60)