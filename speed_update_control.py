import win32api

import datetime
from psychopy import visual
import sys, os, csv
import numpy as np
from psychopy import core, gui, event
import speed_updating_task as sut

#define base path
basepath=os.path.normpath(os.getcwd() + os.sep + os.pardir)




def updateNames(d, path,num=1):
        #save dict to data file
    if 'Subj_Log_File_'+str(num)+'.csv' in os.listdir(path):
        #updates names for subject
        with open(path+os.sep+'Subj_Log_File_'+str(num)+'.csv', 'ab') as f: 
            w = csv.DictWriter(f, d.keys())
            w.writerow(d)
    else:
        #make a new one for changed numbers of stims
        with open(path+os.sep+'Subj_Log_File_'+str(num)+'.csv', 'wb') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, d.keys())
            w.writeheader()
            w.writerow(d)
#subject data

subinfo={"Participant ID": 'test','Group':'test4','Experimenter':['MJ', 'Other', 'Other'], 'Practice':'True'}
key_order=["Participant ID",'Group','Practice','Experimenter']

if not gui.DlgFromDict(dictionary=subinfo, order=key_order).OK:
    core.quit()

subinfo['target_size']=2
subinfo['drag_size']=.5
subinfo['position_radius']=7
subinfo['position_number']=8
subinfo['train_number']=10
subinfo['train_speed']=2
subinfo['update_number']=10
subinfo['update_speed']=15
subinfo['drag_file']='cartoon_dog_1.png'
subinfo['target_file']='cartoon_dog_house_1.png'


if win32api.EnumDisplayDevices().DeviceString == 'Intel(R) HD Graphics 620':
    window=visual.Window([1024,768], monitor='Acer_Pers', color=.25, units='deg', fullscr=True, allowGUI=False, screen=1)
else:
    window=visual.Window([1024,768], monitor='Asus', color=subinfo['scrn_bright'], units='deg', fullscr=True, allowGUI=False, screen=0)
   
  
 
'''functions for the name assignments'''
#house keeping things in the begining
subinfo['Date']=datetime.datetime.now() 

data_path=os.path.join(basepath,'data','Run_'+subinfo['Group'], subinfo['Participant ID'], 'beh')

#make a group folder if one doesn't exists
if not os.path.isdir(os.path.join(basepath,'data','Run_'+subinfo['Group'], subinfo['Participant ID'])):
    os.makedirs(os.path.join(basepath,'data','Run_'+subinfo['Group'], subinfo['Participant ID'], 'beh'))
#update names to group
updateNames(subinfo, os.path.join(basepath,'data','Run_'+subinfo['Group']), num=subinfo['Group'])


#call the instruction pages 
instructions=[visual.ImageStim(window, image=os.path.join(os.getcwd(), 'instructions', pic), name=None, units='deg', pos=(0,0), size=(25,15)) \
                                        for pic in os.listdir(os.path.join(os.getcwd(), 'instructions'))]


instructions[0].draw()
window.flip()
pressed=event.waitKeys(keyList=['q','space'], timeStamped=False)

if subinfo['Practice']=='True':
    
    while True: 
        sut.run_speed_updating(win=window,drag_file=os.path.join(os.getcwd(), 'images', subinfo['drag_file']), 
        drag_size=subinfo['drag_size'], target_file=os.path.join(os.getcwd(), 'images', subinfo['target_file']), 
                        target_size=subinfo['target_size'], position_radius=subinfo['position_radius'],
                        position_numbers=subinfo['position_number'], train_number=4, train_speed=10, 
                        update_number=0, update_speed=1, subject_id=subinfo['Participant ID'], 
                        save_path=data_path, practice=True)
                        
        instructions[1].draw()
        window.flip()
        continue_key=event.waitKeys(maxWait='inf', keyList=['g', 'l'])
        if continue_key[0]=='l':
            break

sut.run_speed_updating(win=window,drag_file=os.path.join(os.getcwd(), 'images', subinfo['drag_file']), 
        drag_size=subinfo['drag_size'], target_file=os.path.join(os.getcwd(), 'images', subinfo['target_file']), 
                        target_size=subinfo['target_size'], position_radius=subinfo['position_radius'],
                        position_numbers=subinfo['position_number'], train_number=subinfo['train_number'], train_speed=subinfo['train_speed'], 
                        update_number=subinfo['update_number'], update_speed=subinfo['update_speed'], subject_id=subinfo['Participant ID'], 
                        save_path=data_path, practice=False)
