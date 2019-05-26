# -*- coding: UTF-8 -*-
#
#-----------------------------------------------------------------------------#
# Nom :         gif_arbres.py                                                 #
# Description : Programme générant un gif animé présentant les arbres         #
#               en tant que fractales.                                        #
#                                                                             #
# Auteur :      Flobiz                                                        #
#                                                                             #
# Création :    23/05/2019 19:01:45                                           #
# Copyright :   (c) Flobiz 2019                                               #
# Licence :     MIT Licence                                                   #
#-----------------------------------------------------------------------------#
#
#!/usr/bin/env python
#
# ------------------------------ Importations ------------------------------- #

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os, shutil

# ------------------------------- Constantes -------------------------------- #

LONGUEUR_MINIMALE = 0.1
RAPPORT_LONGUEURS = 0.8
ANGLE0 = np.radians(30)
FRAMES = 240
H_MAX = 1 / (1 - RAPPORT_LONGUEURS) - 1

# --------------------------------------------------------------------------- #


# Initialisation de la figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim(1 - 0.55 * H_MAX, 1 + 1.05 * H_MAX)
ax.set_xlim(-0.8 * H_MAX, 0.8 * H_MAX)
ax.set_aspect('equal')
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
plt.axis('off')

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False)
fig.patch.set_alpha(0.)
fig.patch.set_visible(False)
ax.patch.set_visible(False)

# --------------------------------------------------------------------------- #

class Arbre :

    def __init__ (self, parent=None, sens=1, etape=0) :
        self.parent = parent
        self.sens = sens
        self.etape = etape
        self.calculer_debut(parent)
        self.calculer_fin()
        self.init_line()
        if RAPPORT_LONGUEURS * self.longueur > LONGUEUR_MINIMALE :
            self.ajouter_enfant()


    def calculer_debut (self, parent, angle=ANGLE0) :
        if parent is None :
            self.debut = np.array([0,0])
            self.longueur = 1
            self.angle = np.pi / 2
        else :
            self.debut = parent.fin
            self.longueur = RAPPORT_LONGUEURS * parent.longueur
            self.angle = parent.angle + self.sens * angle


    def calculer_fin (self) :
        direction = np.array([np.cos(self.angle), np.sin(self.angle)])
        self.fin = self.debut + self.longueur * direction


    def init_line (self) :
        self.line = ax.plot(*list(zip(self.debut,self.fin)), color="black", lw=1)[0]


    def maj_line (self) :
        self.line.set_data(*list(zip(self.debut,self.fin)))


    def ajouter_enfant (self) :
        self.gauche = Arbre(self, -1, self.etape+1)
        self.droite = Arbre(self,  1, self.etape+1)


    def maj_angle (self, nouvel_angle) :
        self.calculer_debut(self.parent, nouvel_angle)
        self.calculer_fin()
        self.maj_line()
        if hasattr(self, 'gauche') and hasattr(self, 'droite') :
            self.gauche.maj_angle(nouvel_angle)
            self.droite.maj_angle(nouvel_angle)

# --------------------------------------------------------------------------- #

# Création de l'arbre
A = Arbre()

#---------------------------------------------------------------------------- #

if 'temp' not in os.listdir() : os.mkdir('temp')


for theta in np.linspace(0, 2*np.pi, FRAMES) :
    print(int(50 * theta / np.pi), '%')
    filename = 'temp/temp{:03d}.png'.format(int(theta/2/np.pi*FRAMES))
    A.maj_angle(theta)
    plt.savefig(filename)


output = 'gif_arbres2'
cmd = 'convert -delay 2 -loop 0 -alpha set -dispose previous temp/*.png {}.gif'
os.system(cmd.replace('{}',output))


shutil.rmtree('temp')
