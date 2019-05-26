# -*- coding: UTF-8 -*-
#
#-----------------------------------------------------------------------------#
# Nom :         gif_dragon.py                                                 #
# Description : Programme générant un gif animé présentant la courbe du       #
#               dragon.                                                       #
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
zoom = 3/4
ax.set_ylim(1/6-zoom, 1/6+zoom) # (5/12, 1/6)
ax.set_xlim(5/12-zoom, 5/12+zoom)
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

class Courbe (object) :

    def __init__ (self) :
        self.points = [complex(0), complex(1)]
        coords = list(map(lambda x:[x.real,x.imag], self.points))
        self.line = ax.plot(*list(zip(*coords)), color="black", lw=1)[0]

    def figure_entre_deux_points (A, B, k) :
        return [A / 2 + B / 2 - k * (B - A) * 1j / 2]

    def etape_suivante (self) :
        M = []
        for i in range(len(self.points) - 1) :
            a, b = self.points[i:i+2]
            M.append(a)
            M.extend(Courbe.figure_entre_deux_points(a,b,(i%2)*2-1))
        M.append(self.points[-1])
        self.points = M.copy()
        coords = list(map(lambda x:[x.real,x.imag], self.points))
        self.line.set_data(*list(zip(*coords)))


# --------------------------------------------------------------------------- #


C = Courbe()


if 'temp' not in os.listdir() : os.mkdir('temp')

filename = 'temp/temp00.png'
plt.savefig(filename)

for k in range(1,16) :
    C.etape_suivante()
##    print(C.points)
    filename = 'temp/temp{:02d}.png'.format(k)
    plt.savefig(filename)


output = 'gif_dragon'
cmd = 'convert -delay 100 -loop 0 -alpha set -dispose previous -gravity south -crop 1:1 temp/*.png {}.gif'
os.system(cmd.replace('{}',output))


##shutil.rmtree('temp')
