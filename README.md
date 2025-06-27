# DINO GAME 3D
_____________________________________________________

# ////////////// COMPTE RENDUS du PROJET TSI 3ETI GRPA /////////////

RIVAUX Léonard / DZIOPA Raphaël

Ce projet de TSI consiste à utiliser la librairie OPENGL  
et ses outils pour créer un simple jeu en trois dimensions.

Nous avons choisi de reprendre l'idée du "Dino game", étant un  
jeu de course à obstacles, inspiré du jeu intégré du browser  
Google Chrome, accessible lors du manque de connexion.

Ce projet est séparé en 5 parties, étant les suivantes :  
I. La structure et l'utilisation d'OPENGL  
II. La création des objets et leurs sommets  
III. La logique de collision  
IV. La génération aléatoire des obstacles  
V. La mise en jeu

_____________________________________________________
## I. La structure et l'utilisation de OPENGL

Premièrement, le code du projet suit une structure standard pour l'utilisation d'OPENGL.  
On utilise pour le jeu une classe `GAME()` pour les plusieurs variables différentes de  
la fenêtre OPENGL et nécessaires du jeu.

main()

└── Game()
- ├── __init__(self)		← Création des varibles et textures	
- ├── init_window()		← Création de la fenêtre GLFW
- ├── init_context()     	← Activation d’OpenGL
- ├── init_programs()    	← Chargement des shaders
- ├── init_data()        	← Données des objects 3D (VAO, VBO, IBO) 
- ├── run()			← 
- ├── key_callback()		← 
- ├── main()			← 
- └── Fonctions à sommets	← 



_____________________________________________________
## II. La creation des objects et leurs sommets

Chaque objet qui sera créé dans le jeu a une fonction attribuée qui est chargée 
de créer les indices et vertices pour chaque object. On a dû créer des sous fonctions 
pour faire des formes simples pour avoir un assemblage plus simple. On a créé plusieurs 
objets demandés par les different obstacles du jeu.

### Création du sol et des formes simples ###

Premièrement on a créé le sol, qui agira comme le terrain du jeu.
Définie dans la fonction: **create_plane** qui crée un carré grâce à 4 sommets.

Pour la suite des fonction de création d'objets on à crée des sous programmes
qui génèrent des formes que l'on peut réutiliser plusieurs fois dans le même objet
ou dans d'autres objets. Leur structure est similaire. Ces fonctions sont :

**generate_sphere_mesh( _rayon_ , _nombre de segments de latitude_ , _nombre de segments de longitude_ )** 

Cette fonction nous a été fournie, mais calcule pour chaque sommet sa position en 
latitude et longitude grâce à des équations trigonométriques. On peut choisir en entrée 
le rayon de la sphere, et sa "resolution" soit le nombre de sommets totaux de la 
sphère qui la rend plus lisse si on augmente le nombre ou plus pointue en diminuant 
le nombre de sommets.
On fait attention comme dans les autres fonctions de creation de sommets pour éviter 
toute erreur de buffer de bien formater les indices et les vertices avec np.array().

**generate_cylinder_mesh( _rayon_ , _longueur_ , _segments_ , _inversion_)**

Cette fonction nous à aussi été fournie, mais nous avons ajouté quelques modifications.
La fonction crée des cylindres de rayon, taille et de "resolution" (le nombre de sommets,
similaire à la fonction de sphère) modifiables. Le calcul des sommets est fait grâce au 
cosinus et sinus et un variable sur x ou y pour la hauteur du cylindre. C'est ici que 
nous avons modifier la fonction, ajoutant un variable "d'invertion" pour choisir si le
cylindre est placer en longeur selon l'axe des x ou l'axe des y, dus au demandes pour 
les objets de jeux.
De même, il faut pour éviter toute érreur de buffer, bien formater les indices et les 
vertices avec np.array().

**generate_wing_mesh( _taille_ , _inversion_ , _temps_ )**

Cette fonction est simplement la creation d'un triangle entièrement modifiable de sa
taille et de son sens par inversion. L'inversion ici inverse les triangles possible
par symétrie selon le plan xy. Ceci change à la fois la position des sommets mais 
aussi les face haute et le basses du triangle ce qui est corrigé en inversant les
indices du triangle. De plus on ajoute dans la creation des sommets "time", ceci 
est pour crée un object dynamique, et varie donc 1 sommet du triangle sur l'axe
des y pour imiter un movement de battement des ailes ensuite. On formate aussi les 
indices et les vertices avec np.array().

**generate_head_mesh( _taille_ , _inversion_ )**

Cette fonction crée une forme de tête, modifiable en taille, qui ici est deux triangles 
connectées par leur hypoténuse. Ici on crée donc 4 sommets avec 2 sommets qui sont 
partagées (ceux de l'hypoténuse). De plus on à remis l'option d'inverser le sens des 
triangles. Il y à le même formatage des indices et les vertices avec np.array().

### Création des objets de jeux ###

Deuxièmement on à crée le joueur, soit le modèle du dinosaure. Ici pour simplifier
le modèle 3D de ce dinosaure, sachant que le joueur ne le véras que de dos, nous
avons choisi une forme simple compose de cylindres et d'une sphere pour la tête.
La fonction liée "generate_dino" fonctionne de la même manière que les fonctions
"generate_pterodactyl" et "generate_cactus".

Ces fonctions utilisent une matrice pour organiser le placement des divers objet
comme les cylindres, triangles ou sphère utilisées pour ce modèle. Par example, 
la matrice de la fonction generate_dino :\
dino_pixels = [\
        [0, 0, 1, 0, 0],\
        [0, 0, 2, 0, 0],\
        [0, 0, 2, 0, 0],\
        [0, 0, 2, 0, 0],\
        [0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0]]

Puis pour chaque modèle on definit les axes selon lesquels on veut diriger les modèle, 
ici étant la matrice de l'objet. Par example, le cactus pour être defini debout, il
est défini selon x et y. Donc la matrice montre un modèle sur une vue selon l'axe z. 

Puis pour lire la matrice on attribue diférentes valeurs pour différent object 
de bases, par example dans la fonction generate_dino, dans sa matrice on defini 
la valeur 1 pour creer un sphere qui ici est placé en haut du modèle. Cette partie
fait appèle au fonction de formes simples mentionnée précédament.
> [!IMPORTANT]
> Pour le bon fonctionnement des mesh de chaque objet on à du transformer un mesh
> séparé de chaque forme avec flatten() et to list().
> Puis on décale les indices des sommets selon leur placement de la matrice et on combine
> tout les sommets emsembles.

Puis on renvoie respectivement le VBO et l'IBO avec interlaced et faces, soit les
sommets eu même et leur indices.

_____________________________________________________
## III. La logique de collision

_____________________________________________________
## IV. La generation aléatoire des obstacles

_____________________________________________________
## V. La mise en Jeux
