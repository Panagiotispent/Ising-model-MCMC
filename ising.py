# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 10:24:38 2020

@author: panay
"""

import numpy as np
from array2gif import write_gif
import random

#create the gif animation
def to_two_color(lattice):
    blue = np.ones(lattice.shape, dtype=np.int) * 255 
    red = np.zeros(lattice.shape, dtype=np.int)
    red[lattice < 0] = 255 
    green = red 
    return np.array([red, green, blue])

def output_to_gif(dataset, filename, fps):
    print("Frames: {}".format(len(dataset)))
    colors = []
    write_gif(
        [to_two_color(lattice) for lattice in dataset],
        filename,
        fps=fps
    )

#calculate the energy at the location that changes i.e. H = - Sum_<ij>(s_i s_j)    
def get_dH(lattice, trial_location):
    i, j = trial_location
    height, width = lattice.shape
    H, Hflip = 0, 0
    for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        ii = (i + di) % height
        jj = (j + dj) % width
        H -= lattice[ii, jj] * lattice[i, j]
        Hflip += lattice[ii, jj] * lattice[i, j]
    return Hflip - H

def standard_approach(T, width, height, N):
    # Randomly initialize the spins to either +1 or -1
    lattice = 2 * np.random.randint(2, size=(height, width)) - 1
    snapshots = []
    for snapshot in range(N):
        snapshots.append(to_two_color(lattice))
        print('{:2.0%} complete. Net magnetization: {:3.0%}'
              .format(snapshot / N,
                      abs(lattice.sum()) / lattice.size),
              end='\r')
        #this runs for 5*N
        for step in range(10):
        #For len of the lattice do
            for x in range(len(lattice)):
                # Randomly pick positions (i,j) from the lattice to change
                i=random.randint(0,height-1)
                j=random.randint(0,width-1)
                dH = get_dH(lattice, (i, j))
                if dH < 0:  # lower energy: flip for sure
                    lattice[i, j] = -lattice[i, j]
                else:  # Higher energy: flip sometimes
                    probability = np.exp(-dH / T)
                    if np.random.rand() < probability:
                        lattice[i, j] = -lattice[i, j]
    return snapshots

def run(T_over_Tc, width=200, height=200):
    Tc = 2.269  # Normalized T := kT/J
    T = T_over_Tc * Tc
    dataset = None
    fps=500
    dataset = standard_approach(T, width, height, N=1000)
    filename = ('ising_{}_{}x{}.gif'
                 .format(T_over_Tc, width, height))
    write_gif(dataset, filename, fps)


run(T_over_Tc=1.25)
run(T_over_Tc=.5)
