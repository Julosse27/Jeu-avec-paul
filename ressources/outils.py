import pyxel as px

class Touches():
    """
    Gère toute la partie communication avec l'utilisateur avec les touches.

    Si cette classe est appelée elle renverra l'état de toutes les touches demandées.
    """
    def __init__(self, *touches_a_chek: int) -> None:
        self.touches: dict[int, float] = {}
        for touche in touches_a_chek:
            self.touches[touche] = 0.0
        self.TOUCHES_LISTE = touches_a_chek

    def __call__(self, *touches: int, tps: bool = True) -> dict[int, float | bool]:  
        """
        Récupère toutes les informations sur les touches que tu veut vérifier.

        :param touches: `(Nombre d'argument variables)` Toutes les touches dont tu veut 
        vérifier l'état.
        :type touches: int
        :param tps: Si il faut donner le temps de fonctionnement des touches (`True`)
        ou seulement l'état brut (`False`). Par défault `True`.
        :type tps: bool
        :return: Le dictionnaire de toutes les touches dont tu à demandé l'état.
        :rtype: dict[int, float | bool]
        """      
        touche_status: dict[int, float | bool] = {}

        touches_a_verifier = touches if touches else self.TOUCHES_LISTE

        for touche in touches_a_verifier:
            valeur = self.touches.get(touche, 0.0)
            if not tps:
                valeur = bool(valeur)
            touche_status[touche] = valeur
        
        return touche_status
    
    def update(self):
        """
        Met à jour toutes les valeurs pour toutes les touches données au démarage
        """
        touches_pressees = []

        for touche in self.TOUCHES_LISTE:
            if px.btn(touche):
                self.touches[touche] += 1
                touches_pressees.append(touche)
            else:
                self.touches[touche] = 0.0

    def chek_one(self, touche: int, *, tps: bool = True) -> float | bool:
        """
        Chek une seule touche et renvois son état.

        :param touche: La touche dont on veut vérifier l'état.
        :type touche: int
        :param tps: Si il faut donner le temps de fonctionnement des touches (`True`)
        ou seulement l'état brut (`False`). Par défault `True`.
        :type tps: bool
        :return: L'état de la touche demandée.
        :rtype: float | bool
        """
        
        valeur = self.touches.get(touche, 0.0)
        if not tps:
            valeur = bool(valeur)
        
        return valeur