import pyxel as px
from os.path import realpath
from ressources.outils import *
from typing import Literal

CHEMIN_RES = f"{realpath("./ressources")}/"

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
        px.cls(1)
        self.perso.draw()
 
class Perso():
    def __init__(self) -> None:
        px.load(f"{CHEMIN_RES}perso.pyxres")
        self.img = px.images[0]

        self.x = 0
        self.y = 0
        self.sens = 1
        self.hitbox_x = 8
        self.hitbox_y = 8
        self._dep_x = 0
        self._dep_y = 0
        self._LIMITE = FPS//3

        self.delay_vitesse = 0
        self.tps_v_max = 5 * FPS
        self._REGULATEUR = FPS // 2
        self.essouflement = 3
        self.derapage = 0
        self._LIMITE_DERAPAGE = FPS // 6
        self._tps_stase = 0

        self.etat_perso: Literal["Stase", "Mvt", "Derapage"] = "Stase"
        self.etat_anim = 0
        self.LISTE_U = (0, 16, 32, 48, 64, 80, 96, 112)
        self.LIGNES_ANIMS = {"Stase": 0, "Mvt": 16, "Derapage": 32}

        self._block_mouv = False
        self._block_draw = False

    def placer_perso(self, x:int = 0, y:int = 0):
        """
        Place le personnage a un endroit spécifique du jeu. 

        :param x: Les coordonnées x du coin en haut à droite du perso.
        :type x: int
        :param y: Les coordonnées y du coin en haut à droite du perso.
        :type y: int
        """
        self.x = x
        self.y = y
        self.hitbox_x = x + 8
        self.hitbox_y = y + 8

    def update(self):
        etat_touches = CHEK_TOUCHES(DROITE, GAUCHE, HAUT)

        if not self._block_mouv:
            acceleration = self.delay_vitesse // self._REGULATEUR

            vitesse = acceleration if acceleration else 1

            augmentation_v = None
            
            if (etat_touches[DROITE] and etat_touches[GAUCHE] or 
                not etat_touches[DROITE] and not etat_touches[GAUCHE]):
                self.etat_perso = "Stase"
                augmentation_v = False
                self._tps_stase += 1
            elif etat_touches[DROITE]:
                augmentation_v = True
                self._dep_x += vitesse
                self.etat_perso = "Mvt"
                if self.sens == -1 and self._tps_stase < self._LIMITE_DERAPAGE:
                    self.derapage = self._LIMITE
                self.sens = 1
            elif etat_touches[GAUCHE]:
                augmentation_v = True
                self._dep_x -= vitesse
                self.etat_perso = "Mvt"
                if self.sens == 1 and self._tps_stase < self._LIMITE_DERAPAGE:
                    self.derapage = self._LIMITE
                self.sens = -1

            if self.derapage > 0:
                self.derapage -= 1
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

Jeu("Test")