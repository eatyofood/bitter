



'''[[[[[[[[[[[THESE ARE CONTROL PANEL THINGS]]]]]]]]]]'''
import pyttsx3
eng = pyttsx3.init()

from delta_mamma import delta_momma_loop

import os

'''FUNCTION INPUTS'''

var1_name = 'delta_threshs:'
var2_name = 'fast_ma_preiods:'
var3_name = 'slow:'
slow      = 42
var_3      = slow

#DELTA  - THRESHES
var_1s = [1.5,2,2.5,3,4,5]
#FAST_MAS
var_2s = [5,6,10,5,6,7,8,9,10]
slows = [20,30,40,50]





for path in os.listdir('data/'):
    path = 'data/'+path
    for slow in slows:
        delta_momma_loop(path,var1_name,var2_name,var3_name,var_1s,var_2s,slow)
        eng.say('the variable three iteration is compleate')
        eng.runAndWait()
eng.say('the path iterations is compleate, setting up the next path')