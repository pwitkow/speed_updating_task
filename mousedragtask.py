#import everything
from psychopy import visual
import sys, os, csv
from psychopy import gui, core ,event
import tobii_research as tbr

import numpy as np
import random 


def circlePos(N=1, radius=2, origin=(0,0)):
    #generates N number of evenly spaced points in a circle around Origin
    rads=np.arange(0,2,(2.0/N))
    newx=origin[0]+radius*np.cos(rads*np.pi)
    newy=origin[1]+radius*np.sin(rads*np.pi)
    posList=zip(newx, newy)
   
    #incase you get 1 extra
    if len(posList) > N:
        posList.remove(posList[len(posList)-1])
    
    return posList




def do_mouse_drag(win, drag_radius, target_radius): 
    
    
    #objects
    drag=visual.Circle(win, radius=drag_radius, lineColorSpace='rgb255', lineColor=(0,0,225), units='deg')
    target_circle=visual.Circle(win, radius=target_radius, lineColorSpace='rgb255', lineColor=(0,255, 0), units='deg')
    
    #initiate a mouse
    mouse=event.Mouse()
    mouse.setPos((0,0))
    
    
    #possible position around the target_circle
    circ_pos=circlePos(10, radius=8, origin =(0,0))
    
    drag.pos=random.choice(circ_pos)
    
    while True:

        m1, m2, m3 = mouse.getPressed()
        if m1:
            while drag.contains(mouse):
                drag.pos=mouse.getPos()
                drag.draw()
                target_circle.draw()
                win.flip()
            event.mouseButtons=[0,0,0]
        else:
            drag.draw()
            target_circle.draw()
            win.flip()
        
            
if __name__ == '__main__':
    window=visual.Window([1024,768], monitor='testMonitor', color=0, units='deg', fullscr=True, allowGUI=False, screen=0)
    do_mouse_drag(win=window, drag_radius=1, target_radius=2)