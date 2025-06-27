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

Chaque object qui seras crée dans le jeux à 1 fonction attribuée qui est chargé 
de crée les indices et vertices pour chaque object. On à dus creer des sous fonctions 
pour faire des formes simple pour avoir un assemblage plus simple.


On à crée plusieurs objests demandé par les different obstacles du jeux.
Premièrement on à crée le sol, qui agiras comme le terrain du jeu.
Définie dans la fonction: "create_plane" qui crée un carré grâce à 4 sommets.

Pour la suite des fonction de creation d'objects on à crée des sous programmes
qui génèrent des forms que l'on peut reutiliser plusieurs fois dans le même objet
ou dans d'autres objets. Leur structure est similaire. Ces fonctions sont :

**generate_sphere_mesh( _rayon_ , _nombre de segments de latitude_ , _nombre de segments de longitude_ )** 

Cette fonction nous à été fournie, mais calcule pour chaque sommet sa position en 
latitude et longitude grâce à des equation trigonométrique. On peut choisir en entrée 
le rayon de la sphere, et sa "resolution" soit le sombre de sommets total de la 
sphere qui la rends plus lisse si on augmente le nombre ou plus pointue en diminuant 
le nombre de sommets.
On fait attention comme dans les autres fonctions de creation de sommets pour éviter 
toute érreur de buffer de bien formater les indices et les vertices avec np.array().

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
des y pour imiter un movement de battement des ailes ensuite.On formate aussi les 
indices et les vertices avec np.array().

**generate_head_mesh( _taille_ , _inversion_ )**

Cette fonction crée une forme de tête, modifiable en taille, qui ici est deux triangles 
connectées par leur hypoténuse. Ici on crée donc 4 sommets avec 2 sommets qui sont 
partagées (ceux de l'hypoténuse). De plus on à remis l'option d'inverser le sens des 
triangles pour lequel 

    if inverted:
        indices = [
            0, 2, 1,  # ABC (inverted)
            0, 3, 2,  # ADC (inverted)
        ]
    else:
        indices = [
            1, 2, 0,  # ABC
            2, 3, 0,  # ACD
        ]

    return {
        'interlaced': np.array(vertices, dtype=np.float32),
        'faces': np.array(indices, dtype=np.uint32)
    }



Deuxièmement on à crée le joueur, soit le modèle du dinosaure. Ici pour simplifier
le modèle 3D de ce dinosaure, sachant que le joueur ne le véras que de dos, nous
avons choisi une forme simple compose de cylindres et d'une sphere pour la tête.
La fonction liée "generate_dino" fonctionne de la même manière que les fonctions
"generate_pterodactyl" et "generate_cactus".

def generate_dino():
    spacing = 1

    dino_pixels = [
        [0, 0, 1, 0, 0],
        [0, 0, 2, 0, 0],
        [0, 0, 2, 0, 0],
        [0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    dino_pixels = dino_pixels[::-1]

    full_vertices = []
    full_indices = []
    index_offset = 0

    for y, row in enumerate(dino_pixels):
        for x, val in enumerate(row):

            if val == 0:
                continue

            cx = -x * spacing
            cz = 0
            cy = y/2 * spacing

            size = 2

            if val == 1:
                mesh = generate_sphere_mesh(0.4, 16, 32)
            elif val == 2:
                mesh = generate_cylinder_mesh((size/6), 1.0, 16, False)

            vertices = np.array(mesh['interlaced'], dtype=np.float32).flatten().tolist()
            indices = mesh['faces'].flatten().tolist()

            # Translate vertices
            for i in range(0, len(vertices), 11):
                vertices[i + 0] += cx  # x
                vertices[i + 1] += cy  # y
                vertices[i + 2] += cz  # z

            # Offset and flatten indices
            flat_indices = [i + index_offset for i in indices]
            index_offset += len(vertices) // 11

            full_vertices.extend(vertices)
            full_indices.extend(flat_indices)

    return {
        'interlaced': np.array(full_vertices, dtype=np.float32),
        'faces': np.array(full_indices, dtype=np.uint32)
    }


def generate_pterodactyl(time):
    spacing = 1

    pterodactyl_pixels = [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 3, 1, 2, 0],
        [0, 0, 4, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    pterodactyl_pixels = pterodactyl_pixels[::-1]

    full_vertices = []
    full_indices = []
    index_offset = 0

    for y, row in enumerate(pterodactyl_pixels):
        for x, val in enumerate(row):

            if val == 0:
                continue

            cx = y * spacing
            cz = x * spacing
            cy = 0

            size = 3

            if val == 1:
                mesh = generate_cylinder_mesh((size/6), 1.0, 16, True)
            elif val == 2:
                mesh = generate_wing_mesh(size+1,False,time)
            elif val == 3:
                mesh = generate_wing_mesh(size+1,True,time)
            elif val == 4:
                mesh = generate_head_mesh(size,False)

            vertices = np.array(mesh['interlaced'], dtype=np.float32).flatten().tolist()
            indices = mesh['faces'].flatten().tolist()

            # Translate vertices
            for i in range(0, len(vertices), 11):
                vertices[i + 0] += cx  # x
                vertices[i + 1] += cy  # y
                vertices[i + 2] += cz  # z

            # Offset and flatten indices
            flat_indices = [i + index_offset for i in indices]
            index_offset += len(vertices) // 11

            full_vertices.extend(vertices)
            full_indices.extend(flat_indices)

    return {
        'interlaced': np.array(full_vertices, dtype=np.float32),
        'faces': np.array(full_indices, dtype=np.uint32)
    }

def generate_cactus():
    spacing = 1

    cactus_pixels = [
        [0, 0, 2, 0, 0],
        [0, 0, 1, 2, 0],
        [0, 2, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ]

    cactus_pixels = cactus_pixels[::-1]

    full_vertices = []
    full_indices = []
    index_offset = 0

    for y, row in enumerate(cactus_pixels):
        for x, val in enumerate(row):
            cx = x * spacing
            cy = y * spacing
            cz = 0

            if val == 2:
                mesh_sph = generate_sphere_mesh(0.5, 16, 32)
                vertices = np.array(mesh_sph['interlaced'], dtype=np.float32).flatten().tolist()
                indices = mesh_sph['faces']

            elif val == 1:
                mesh = generate_cylinder_mesh(0.5, 2, 16, False)
                vertices = np.array(mesh['interlaced'], dtype=np.float32).flatten().tolist()
                indices = mesh['faces']
            else:
                continue  # Skip zeros

            # Translate vertices
            for i in range(0, len(vertices), 11):
                vertices[i + 0] += cx  # x
                vertices[i + 1] += cy  # y
                vertices[i + 2] += cz  # z

            # Offset and flatten indices
            flat_indices = np.array(indices).flatten().tolist()
            flat_indices = [i + index_offset for i in flat_indices]

            index_offset += len(vertices) // 11
            full_vertices.extend(vertices)
            full_indices.extend(flat_indices)

    return {
        'interlaced': np.array(full_vertices, dtype=np.float32),
        'faces': np.array(full_indices, dtype=np.uint32)
    }


> [!IMPORTANT]
> Pour le bon fonctionnement des mesh chaque.
_____________________________________________________
## III. La logique de collision

_____________________________________________________
## IV. La generation aléatoire des obstacles

_____________________________________________________
## V. La mise en Jeux
