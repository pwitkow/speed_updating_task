#import everything
from psychopy import visual
import sys, os, csv
from psychopy import gui, core ,event

import numpy as np
import random 

import ctypes



def circlePos(N=1, radius=2, origin=(0,0)):
    """
    Generates evenly spaced points in a circle around a point.

    Keyword arguments:
    N : int -- number of points (default 1)
    radius: int/float -- radius of the circle
    origin : tuple of int/float -- origin of the circle
            
            
    """
    
    rads=np.arange(0,2,(2.0/N))
    newx=origin[0]+radius*np.cos(rads*np.pi)
    newy=origin[1]+radius*np.sin(rads*np.pi)
    posList=zip(newx, newy)
   
    #incase you get 1 extra
    if len(posList) > N:
        posList.remove(posList[len(posList)-1])
    
    return posList


def change_speed(speed=3):
    #   1 - slow
    #   10 - standard
    #   20 - fast
    set_mouse_speed = 113   # 0x0071 for SPI_SETMOUSESPEED
    ctypes.windll.user32.SystemParametersInfoA(set_mouse_speed, 0, speed, 0)

def make_trials(train_number, train_speed, update_number, update_speed):
    '''
    Make the full set of trials for the task
    
    Keyword Arguments:
        train_number : int -- number of trials to train on
        train_speed  : int -- mouse speed for the training trials 
        test_number  : int -- number of trials to train on
        test_speed   : int -- mouse speed for the training trials 
    '''
    
    trial_list=[{'type': 'training', 'speed': train_speed} for _ in range(train_number)]
    trial_list.extend([{'type': 'update', 'speed': update_speed} for _ in range(update_number)])
    
    for tr_number, trial in enumerate(trial_list):
        trial_list[tr_number]['trial_number']=tr_number
        trial_list[tr_number]['mouse_position']=[]
        trial_list[tr_number]['clicked']=[]
    
    return trial_list
    
    
def drag_and_drop(trial, win, drag, target_circle, mouse):
    while True:
        # check to see if mouse press matches this array so that it only 
        # works for pressing the left mouse button without having to 
        #assign a varaible'
        change_speed(10)
        trial['mouse_position'].append(mouse.getPos())
        trial['clicked'].append(0)
        while drag.contains(mouse) and mouse.getPressed() == [1, 0, 0]:
            change_speed(trial['speed'])
            drag.pos=mouse.getPos()
            
            trial['mouse_position'].append(mouse.getPos())
            trial['clicked'].append(1)
        
            drag.draw()
            target_circle.draw()
            win.flip()
        
        event.mouseButtons=[0,0,0]
        
        if target_circle.contains(drag.pos):
            break
            change_speed(10)
        
        else:
            drag.draw()
            target_circle.draw()
            win.flip()


def run_speed_updating(win, drag_radius, target_radius, position_radius, position_numbers, 
                          train_number, train_speed, update_number, update_speed): 
    
    """
    Primary function to run the speed_updating_task. Subjects move a drag circle in
    into the target circle to complete the trial

    Keyword arguments:
    win : window object 
    drag radius: int/float -- radius movable circle
    target_radius : int/float -- radius of the target circle
    position_radius : int/floar -- distand of drag onset positions from center
    position_numbers : int -- number of possible drag onset positions
    train_number : int -- number of trials to train on
    train_speed  : int -- mouse speed for the training trials 
    test_number  : int -- number of trials to train on
    test_speed   : int -- mouse speed for the training trials         
    """
    #objects
    drag=visual.Circle(win, radius=drag_radius, lineColorSpace='rgb255', lineColor=(0,0,225), units='deg')
    target_circle=visual.Circle(win, radius=target_radius, lineColorSpace='rgb255', lineColor=(0,255, 0), units='deg')
    
    #get a path for the data 
    base_path=os.path.normpath(os.getcwd() + os.sep + os.pardir)
    data_path=base_path + os.pardir()
    
    #initiate a mouse
    mouse=event.Mouse()
    mouse.setPos((0,0))

    #create a csv object for saving the data
    f= open(data_path+subject_id+'_'+ '.csv', 'ab'): 
    w = csv.DictWriter(f, d.keys())
            
    

    for trial in trials:
        #drag and drop task
        drag.pos=random.choice(circ_pos)
        drag_and_drop(trial,win, drag, target_circle, mouse)
        w.writerow(trial)
    
            
if __name__ == '__main__':
    window=visual.Window([1024,768], monitor='testMonitor', color=0, units='deg', fullscr=True, allowGUI=False, screen=0)
    run_speed_updating(win=window, drag_radius=1, target_radius=2, position_radius=6, position_numbers=4, 
                        train_number=2, train_speed=1, update_number=2, update_speed=12)
    