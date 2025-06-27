# DINO GAME 3D
_____________________________________________________

# ////////////// COMPTE RENDUS du PROJET TSI 3ETI GRPA /////////////

RIVAUX Léonard / DZIOPA Raphaël

Ce projet de TSI consiste à utiliser la librairie OPENGL
et ses outil pour crée un simple jeux en trois dimension.

Nous avons choisis de reprendre l'idée du "Dino game", étant un 
jeux de course à obstacle, étant inspire du jeux intégré du browser
google chrome, accessible lors du manque de connexion.


Ce projet est séparée en 5 parties, étant les suivantes :\
I. La structure et l'utilisation de OPENGL\
II. La creation des objects et leurs sommets\
III. La logique de collision\
IV. La generation aléatoire des obstacles\
V. La mise en Jeux

_____________________________________________________
## I. La structure et l'utilisation de OPENGL

Premièrement le code du projet suit une structure standard pour l'utilisation d'OPENGL.
On utilise pour le jeux une Class "GAME()" pour les plusieurs variables différentes de 
la fenêtre OPENGL et necessaires du jeux.

main()

└── Game()
 	├── __init__(self)		← Création des varibles et textures	
     	├── init_window()		← Création de la fenêtre GLFW
     	├── init_context()     		← Activation d’OpenGL
     	├── init_programs()    		← Chargement des shaders
     	├── init_data()        		← Données des objects 3D (VAO, VBO, IBO) 
     	├── run()			← 
     	├── key_callback()		← 
     	├── main()			← 
	└── Fonctions à sommets		← 



_____________________________________________________
## II. La creation des objects et leurs sommets

Chaque object qui seras crée dans le jeux à 1 focntion attribuée qui est charger 
de crée les indices et vertices pour chaque object.

On à dus creer des sous fonctions pour faire des formes simple pour avoir un 
assemblage plus simple.
_____________________________________________________
## III. La logique de collision

_____________________________________________________
## IV. La generation aléatoire des obstacles

_____________________________________________________
## V. La mise en Jeux
