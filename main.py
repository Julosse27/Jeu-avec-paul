import pyxel as px

class Jeu():
    def __init__(self, title: str, width: int = 100, height: int = 100, fps: int = 30) -> None:
        px.init(width, height, title= title, fps= fps) # Initialise la fenètre de jeu (width et height taille de la fenètre, 
                                                       # title son titre et fps les nombre de vérification du code par secondes)

        px.run(self.update, self.draw) # Lance la fenètre de jeu

    def update(self):
        pass

    def draw(self):
        px.cls(7)
        px.mouse(True)
        px.rect(20, 20, 10, 50, 2)

class Perso():
    def __init__(self) -> None:
        self.images = () #Va contenir les images de persos présentes dans la tilemap


Jeu("Test")