#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import numpy as np
import pyrr
import os
from gl_shader import compile_shader,create_program,create_program_from_file

class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):
        self.window = self.init_window()
        self.init_context()
        self.init_programs()
        self.init_data()
        self.R = 0
        self.G = 0
        self.B = 0
        self.UP = 0
        self.DOWN = 0
        self.LEFT = 0
        self.RIGHT = 0
        self.x = 0
        self.y = 0

        self.Rot_x1 = 0
        self.Rot_x2 = 0
        self.Rot_y1 = 0
        self.Rot_y2 = 0

        self.angle_x = 0
        self.angle_y = 0

        self.z = -5
        self.close = 0
        self.far = 0

    def init_window(self):
        # initialisation de la librairie glfw et du context opengl associé
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et parametrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # parametrage de la fonction de gestion des évènements
        glfw.set_key_callback(window, self.key_callback)
        return window

    def init_context(self):
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)

    def init_programs(self):
        program1 = create_program_from_file("shader.vert","shader.frag")
        GL.glUseProgram(program1)
        
    def init_data(self):
        # Création des sommmets de l'object principal
        #sommets = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0)), np.float32) # Simple triangle
        #sommets = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0),(0, 0, 0), (1, 0, 0), (0, 0, 1)), np.float32) # Double triangle
        
        p0 = (0, 0, 0) # Coin inf ́erieur gauche
        p1 = (1, 0, 0) # Coin inf ́erieur droit
        p2 = (1, 1, 0) # Coin sup ́erieur droit
        p3 = (0, 1, 0) # Coin sup ́erieur gauche
        n0 = (0, 0, 1) # Normale pour le plan sur l'axe Z
        n1 = (0, 0, 1) # Normale pour le plan sur l'axe Z
        n2 = (0, 0, 1) # Normale pour le plan sur l'axe Z
        n3 = (0, 0, 1) # Normale pour le plan sur l'axe Z
        c0 = (1, 0, 0) # Rouge
        c1 = (0, 1, 0) # Vert
        c2 = (0, 0, 1) # Bleu
        c3 = (1, 1, 0) # Jaune
        uv0 = (0, 0) # Coordonn ́ees de texture pour le coin inf ́erieur gauche
        uv1 = (1, 0) # Coordonn ́ees de texture pour le coin inf ́erieur droit
        uv2 = (1, 1) # Coordonn ́ees de texture pour le coin sup ́erieur droit
        uv3 = (0, 1) # Coordonn ́ees de texture pour le coin sup ́erieur gauche
        sommets = np.concatenate((p0, n0, c0, uv0, p1, n1, c1, uv1, p2, n2, c2, uv2, p3, n3, c3, uv3)) # CUBE

        # attribution d'une liste d'etat (1 indique la creation d'une seule liste) ´
        vao = GL.glGenVertexArrays(1)
        # affectation de la liste d'etat courante ´
        GL.glBindVertexArray(vao)
        # attribution d’un buffer de donnees (1 indique la creation d’un seul buffer) ´
        vbo = GL.glGenBuffers(1)
        # affectation du buffer courant
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        # copie des donnees des sommets sur la carte graphique
        GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets, GL.GL_STATIC_DRAW)

        # Les deux commandes suivantes sont stockees dans l'etat du vao courant ´
        # Active l'utilisation des donnees de positions ´
        # (le 0 correspond a la location dans le vertex shader) `
        GL.glEnableVertexAttribArray(0)
        # Indique comment le buffer courant (dernier vbo "binde") ´
        # est utilise pour les positions des sommets ´
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

    def run(self):   # --------144 FPS
        # boucle d'affichage
        while not glfw.window_should_close(self.window):

            tmps = glfw.get_time() #------------------- AFFICHE LA DUREE DE VIE DE LA FENETRE
            # Recupere l'identifiant du programme courant
            prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
            # Recupere l'identifiant de la variable translation dans le programme courant
            loc = GL.glGetUniformLocation(prog, "translation")
            new_color = GL.glGetUniformLocation(prog, "new_color")
            rot = GL.glGetUniformLocation(prog, "rotation")
            # Verifie que la variable existe
            if loc == -1 :
                print("Pas de variable uniforme : translation")
            # Modifie la variable pour le programme courant

            proj = GL.glGetUniformLocation(prog, "projection")

            self.x += (self.RIGHT - self.LEFT) / 100
            self.y += (self.UP - self.DOWN)/100

            self.angle_x += (self.Rot_x1 - self.Rot_x2)/100 * np.pi/2
            self.angle_y += (self.Rot_y1 - self.Rot_y2)/100 * np.pi/2

            self.z += (self.close-self.far)/50

            rot3x = pyrr.matrix33.create_from_x_rotation(self.angle_x)
            rot4x = pyrr.matrix44.create_from_matrix33(rot3x)
            rot3y = pyrr.matrix33.create_from_y_rotation(self.angle_y)
            rot4y = pyrr.matrix44.create_from_matrix33(rot3y)

            new_rot = pyrr.matrix44.multiply(rot4y,rot4x)

            proj4 = pyrr.matrix44.create_perspective_projection(50, 1, 0.5, 10)

            GL.glUniform4f(loc,self.x, self.y, self.z, 0)
            GL.glUniform4f(new_color, self.R,self.G,self.B,0)
            GL.glUniformMatrix4fv(rot, 1, GL.GL_FALSE, new_rot)
            GL.glUniformMatrix4fv(proj,1, GL.GL_FALSE, proj4)



            # choix de la couleur de fond
            #GL.glClearColor(0.5, 0.6, 0.9, 1.0)   #---------------------------FOND BLEU CLAIR
            GL.glClearColor(np.sin(tmps), np.cos(tmps), np.sin(tmps + np.pi), 1.0) #-----FONCTION DU TEMPS = FOND VARIABLE
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)#----------------DESSIN DES TRIANGLES DEFINIS DANS INIT PROGRAMS ET INIT DATA
            #REPLACER TRIANGLES PAR LINE_LOOP => JUSTE LES CONTOURS DU TRIANGLE
            #                        LINES => RELIE TOUS LES SOMMETS ENSEMBLES

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
    
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'echap'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        if key == glfw.KEY_R and action == glfw.PRESS:
            self.R = 1 if self.R == 0 else 0
        if key == glfw.KEY_G and action == glfw.PRESS:
            self.G = 1 if self.G == 0 else 0
        if key == glfw.KEY_B and action == glfw.PRESS:
            self.B = 1 if self.B == 0 else 0

        if key == glfw.KEY_UP and action == glfw.PRESS:
            self.UP = 1
        if key == glfw.KEY_UP and action == glfw.RELEASE:
            self.UP = 0
        if key == glfw.KEY_DOWN and action == glfw.PRESS:
            self.DOWN = 1
        if key == glfw.KEY_DOWN and action == glfw.RELEASE:
            self.DOWN = 0
        if key == glfw.KEY_LEFT and action == glfw.PRESS:
            self.LEFT = 1
        if key == glfw.KEY_LEFT and action == glfw.RELEASE:
            self.LEFT = 0
        if key == glfw.KEY_RIGHT and action == glfw.PRESS:
            self.RIGHT = 1
        if key == glfw.KEY_RIGHT and action == glfw.RELEASE:
            self.RIGHT = 0

        if key == glfw.KEY_I and action == glfw.PRESS:
            self.Rot_x1 = 1
        if key == glfw.KEY_I and action == glfw.RELEASE:
            self.Rot_x1 = 0

        if key == glfw.KEY_K and action == glfw.PRESS:
            self.Rot_x2 = 1
        if key == glfw.KEY_K and action == glfw.RELEASE:
            self.Rot_x2 = 0

        if key == glfw.KEY_J and action == glfw.PRESS:
            self.Rot_y1 = 1
        if key == glfw.KEY_J and action == glfw.RELEASE:
            self.Rot_y1 = 0

        if key == glfw.KEY_L and action == glfw.PRESS:
            self.Rot_y2 = 1
        if key == glfw.KEY_L and action == glfw.RELEASE:
            self.Rot_y2 = 0

        if key == glfw.KEY_Y and action == glfw.PRESS:
            self.far = 1
        if key == glfw.KEY_Y and action == glfw.RELEASE:
            self.far = 0

        if key == glfw.KEY_H and action == glfw.PRESS:
            self.close = 1
        if key == glfw.KEY_H and action == glfw.RELEASE:
            self.close = 0

def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main()