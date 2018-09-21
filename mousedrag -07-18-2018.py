#import everything
from psychopy import visual
import sys, os, csv

from psychopy import gui, core ,event

import tobii_research as tbr

import mousedragtask


#find the path for the base folder
basepath=os.path.normpath(os.getcwd() + os.sep + os.pardir)

#goes in the moduels folder 
sys.path.append(os.path.join(basepath, 'Modules'))
import datetime


'''#######################FUNCTIONS####################################'''
def updateNames(d, path,num=1):
        #save dict to data file
    if 'Subj_Log_File_'+str(num)+'.csv' in os.listdir(path):
        #updates names for subject
        with open(path+'Subj_Log_File_'+str(num)+'.csv', 'ab') as f: 
            w = csv.DictWriter(f, d.keys())
            w.writerow(d)
    else:
        #make a new one for changed numbers of stims
        with open(path+'Subj_Log_File_'+str(num)+'.csv', 'wb') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, d.keys())
            w.writeheader()
            w.writerow(d)

'''run stuff'''

#get subject information before we start the experiment
subinfo={"Subject ID": ''}
        
if not gui.DlgFromDict(dictionary=subinfo, order=["Subject ID"]).OK:
    core.quit()
    
subinfo['Date']=datetime.datetime.now()



updateNames(subinfo, basepath+'/Data/', num='3' )




# task 
window=visual.Window([1024,768], monitor='testMonitor', color=0, units='deg', fullscr=True, allowGUI=False, screen=0)



