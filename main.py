import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Configuration de l'écran
LARGEUR = 800
HAUTEUR = 600
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('Jeu Snake - Vies et Score')

# Couleurs
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)

# Configuration du jeu
TAILLE_SERPENT = 20
FPS = 10

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class JeuSnake:
    def __init__(self):
        self.serpent = [(LARGEUR//2, HAUTEUR//2)]
        self.direction = (TAILLE_SERPENT, 0)
        self.nourriture = self.generer_nourriture()
        self.score = 0
        self.vies = 3
        self.jeu_termine = False
        self.pause = False
        
        
    def generer_nourriture(self):
        while True:
            x = random.randint(0, (LARGEUR-TAILLE_SERPENT)//TAILLE_SERPENT) * TAILLE_SERPENT
            y = random.randint(0, (HAUTEUR-TAILLE_SERPENT)//TAILLE_SERPENT) * TAILLE_SERPENT
            if (x, y) not in self.serpent:
                return (x, y)
    
    def deplacer_serpent(self):
        if self.pause or self.jeu_termine:
            return
            
        tete = self.serpent[0]
        nouvelle_tete = (tete[0] + self.direction[0], tete[1] + self.direction[1])
        
        # Vérifier les collisions avec les bords
        if (nouvelle_tete[0] < 0 or nouvelle_tete[0] >= LARGEUR or 
            nouvelle_tete[1] < 0 or nouvelle_tete[1] >= HAUTEUR):
            self.perdre_vie()
            return
            
        # Vérifier les collisions avec le serpent
        if nouvelle_tete in self.serpent:
            self.perdre_vie()
            return
            
        self.serpent.insert(0, nouvelle_tete)
        
        # Vérifier si le serpent mange la nourriture
        if nouvelle_tete == self.nourriture:
            self.score += 10
            self.nourriture = self.generer_nourriture()
            self.serpent.append(self.serpent[-5])
        else:
            self.serpent.pop()
            self.serpent.append(self.serpent[-1])
    
    def perdre_vie(self):
        self.vies -= 1
        if self.vies <= 0:
            self.jeu_termine = True
        else:
            # Remettre le serpent à sa position initiale
            self.serpent = [(LARGEUR//2, HAUTEUR//2)]
            self.direction = (TAILLE_SERPENT, 0)
    
    def changer_direction(self, nouvelle_direction):
        # Empêcher le serpent d'aller dans la direction opposée
        if (nouvelle_direction[0] * -1, nouvelle_direction[1] * -1) != self.direction:
            self.direction = nouvelle_direction
    
    def redemarrer(self):
        self.__init__()
    
    def dessiner(self):
        ecran.fill(NOIR)
        
        # Dessiner le serpent
        for segment in self.serpent:
            pygame.draw.rect(ecran, VERT, (segment[0], segment[1], TAILLE_SERPENT, TAILLE_SERPENT))
        
        # Dessiner la nourriture
        pygame.draw.rect(ecran, ROUGE, (self.nourriture[0], self.nourriture[1], TAILLE_SERPENT, TAILLE_SERPENT))
        
        # Afficher le score et les vies
        texte_score = font.render(f"Score: {self.score}", True, BLANC)
        texte_vies = font.render(f"Vies: {self.vies}", True, BLANC)
        ecran.blit(texte_score, (10, 10))
        ecran.blit(texte_vies, (10, 50))
        
        # Affichage des messages
        if self.jeu_termine:
            texte_game_over = font.render("GAME OVER - Appuyez sur R pour recommencer", True, ROUGE)
            rect = texte_game_over.get_rect(center=(LARGEUR//2, HAUTEUR//2))
            ecran.blit(texte_game_over, rect)
        elif self.pause:
            texte_pause = font.render("PAUSE - Appuyez sur ESPACE pour continuer", True, BLEU)
            rect = texte_pause.get_rect(center=(LARGEUR//2, HAUTEUR//2))
            ecran.blit(texte_pause, rect)
        elif self.jeu_termine:
            texte_game_over = font.render("GAME OVER - Appuyez sur R pour recommencer", True, ROUGE)
            rect = texte_game_over.get_rect(center=(LARGEUR//2, HAUTEUR//2))
            ecran.blit(texte_game_over, rect)
        
        # Instructions
        texte_instructions = font.render("Flèches: Mouvement | ESPACE: Pause | R: Recommencer", True, BLANC)
        ecran.blit(texte_instructions, (10, HAUTEUR - 30))

# Jeu principal
jeu = JeuSnake()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                jeu.changer_direction((0, -TAILLE_SERPENT))
            elif event.key == pygame.K_DOWN:
                jeu.changer_direction((0, TAILLE_SERPENT))
            elif event.key == pygame.K_LEFT:
                jeu.changer_direction((-TAILLE_SERPENT, 0))
            elif event.key == pygame.K_RIGHT:
                jeu.changer_direction((TAILLE_SERPENT, 0))
            elif event.key == pygame.K_SPACE:
                jeu.pause = not jeu.pause
            elif event.key == pygame.K_r:
                jeu.redemarrer()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_q:
                jeu.jeu_termine = True
            
    
    jeu.deplacer_serpent()
    jeu.dessiner()
    pygame.display.flip()
    clock.tick(FPS)