#import everything
from psychopy import visual
import sys, os, csv
from psychopy import gui, core ,event

import numpy as np
import random 

import ctypes
import time
import glob



def circle_pos(N=1, radius=2, origin=(0,0)):
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

def make_trials(train_number, train_speed, update_number, update_speed, targets):
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
        trial_list[tr_number]['clicked']=list([])
        trial_list[tr_number]['mouse_position']=list([])
        trial_list[tr_number]['RT']='NA'
        trial_list[tr_number]['target_image']=np.random.choice(targets, 1)
        trial_list[tr_number]['mouse_x']=np.random.choice(targets, 1)
        trial_list[tr_number]['mouse_y']=np.random.choice(targets, 1)
    return trial_list
    
    
def drag_and_drop(trial, win, drag, target_circle, mouse):
    
    #set the image for the trail
    drag.setImage(trial['target_image'][0])
    
    #start a clock so we can independatnly measure RT
    trial_clock=core.Clock()
    trial_start=trial_clock.getTime()
    
    while True:
        # check to see if mouse press matches this array so that it only 
        # works for pressing the left mouse button without having to 
        #assign a varaible'
        change_speed(10)
        
        
        # see if q is pressed in case we 
        # need to quit
        if event.getKeys(['q']):
            wait=event.waitKeys(maxWait='inf', keyList=['q','t'])
            if wait[0]=='t':
                event.clearEvents()
                pass
            else:
                core.quit()
            
        while drag.contains(mouse) and mouse.getPressed() == [1, 0, 0]:
            change_speed(trial['speed'])
            drag.pos=mouse.getPos()
            
        
            target_circle.draw()
            drag.draw()
            
            win.flip()
                
            trial['mouse_position'].append(mouse.getPos())
            trial['clicked'].append(1)

        
        event.mouseButtons=[0,0,0]

        
        if target_circle.contains(drag.pos):
            break
            change_speed(10)
        
        else:
            trial['mouse_position'].append(mouse.getPos())
            trial['clicked'].append(0)
            target_circle.draw()
            drag.draw()
            win.flip()
    
    trial['RT']=trial_clock.getTime()-trial_start


def run_speed_updating(win,drag_files, drag_size, target_file,target_size,  position_radius, position_numbers,  
                          train_number, train_speed, update_number, update_speed, subject_id, save_path, practice): 
    
    """
    Primary function to run the speed_updating_task. Subjects move a drag circle in
    into the target circle to complete the trial

    Keyword arguments:
    win : window object 
    drag_file : string -- full path and file name of the dragable stimulus
    drag_size: tuple -- x,y dimension lengths for drag stimulus
    target_file : string -- full path and file name of the target 
    target_size : tuple -- x,y dimension lengths for target stimulus
    position_radius : int/floar -- distand of drag onset positions from center
    position_numbers : int -- number of possible drag onset positions
    train_number : int -- number of trials to train on
    train_speed  : int -- mouse speed for the training trials 
    test_number  : int -- number of trials to train on
    test_speed   : int -- mouse speed for the training trials         
    """
    #objects
    drag=visual.ImageStim(win, image=None, units='deg', size=(drag_size[0], drag_size[1]))
    target_circle=visual.ImageStim(win, image=target_file, units='deg', size=(target_size[0], target_size[1]), pos=(0,0))
    
    #initiate a mouse
    mouse=event.Mouse()
    mouse.setPos((0,0))
    
    
    targets=glob.glob(drag_files)


    trials=make_trials(train_number, train_speed, update_number, update_speed, targets)

    #create a csv object for saving the data
    
    circ_pos=circle_pos(N=position_numbers, radius=position_radius, origin=(0,0))

    for trial in trials:
        
        if not practice:
            f= open(os.path.join(save_path , subject_id +'_task-speed-update_beh_trial-number-'+str(trial['trial_number'])+'.csv'), 'ab')
        else: 
            f= open(os.path.join(save_path , subject_id +'_task-practice-speed-update_beh_trial-number-'+str(trial['trial_number'])+'.csv'), 'ab')

        

        
        #drag and drop task
        drag.pos=random.choice(circ_pos)
        drag_and_drop(trial,win, drag, target_circle, mouse)
        
        trial['mouse_position']=list(trial['mouse_position'])
        trial['clicked']=list(trial['clicked'])
        
        #re-make set of dictionaries for data writing
        final_set=[{'mouse_x':trial['mouse_position'][tr][0],'mouse_y':trial['mouse_position'][tr][1],
        'clicked':trial['clicked'][tr],'RT':trial['RT'], 'target_image':trial['target_image'], 
        'trial_number':trial['trial_number']} for tr in range(len(trial['clicked']))]
        
        w = csv.DictWriter(f, final_set[0].keys())
        w.writeheader()
        
        w.writerows(final_set)
        
        f.close()
    
        
    
    change_speed(10)
if __name__ == '__main__':
    print 'Run this through "speed_updating_control.py"'
    