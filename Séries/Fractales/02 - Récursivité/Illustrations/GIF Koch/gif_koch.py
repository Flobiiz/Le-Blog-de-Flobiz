# -*- coding: UTF-8 -*-
#
#-----------------------------------------------------------------------------#
# Nom :         gif_koch.py                                                   #
# Description : Programme générant un gif animé présentant la courbe de       #
#               von Koch.                                                     #
#                                                                             #
# Auteur :      Florent BREART                                                #
#                                                                             #
# Création :    26/05/2019 01:25:01                                           #
# Copyright :   (c) Florent BREART 2019                                       #
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
from math import sqrt

#---------------------------------------------------------------------------- #

# Initialisation de la figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim(-0.1, 1.1)
ax.set_xlim(-0.1, 1.1)
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

###########################
##                       ##
##           E           ##
##          / \          ##
##         /   \         ##
##   A----C     D----B   ##
##                       ##
###########################

class Courbe (object) :

    def __init__ (self) :
        self.points = [complex(0), complex(1)]
        coords = list(map(lambda x:[x.real,x.imag], self.points))
        self.line = ax.plot(*list(zip(*coords)), color="black", lw=1)[0]

    def figure_entre_deux_points (A, B) :
        C = A + 1/3 * (B - A)
        D = A + 2/3 * (B - A)
        E = C + (C-A) * (1/2 - (sqrt(3)/2j))
        return [C, E, D]

    def etape_suivante (self) :
        M = []
        for i in range(len(self.points) - 1) :
            a, b = self.points[i:i+2]
            M.append(a)
            M.extend(Courbe.figure_entre_deux_points(a,b))
        M.append(self.points[-1])
        self.points = M.copy()
        coords = list(map(lambda x:[x.real,x.imag], self.points))
        self.line.set_data(*list(zip(*coords)))


# --------------------------------------------------------------------------- #


C = Courbe()


if 'temp' not in os.listdir() : os.mkdir('temp')

filename = 'temp/temp00.png'
plt.savefig(filename)

for k in range(1,7) :
    C.etape_suivante()
    filename = 'temp/temp{:02d}.png'.format(k)
    plt.savefig(filename)


output = 'gif_koch'
cmd = 'convert -delay 100 -loop 0 -alpha set -dispose previous -gravity south -crop 1:1 temp/*.png {}.gif'
os.system(cmd.replace('{}',output))


shutil.rmtree('temp')
