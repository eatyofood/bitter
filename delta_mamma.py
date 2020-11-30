#if input('clear list?') == 'y':
results = []

from datetime import datetime
start = datetime.now()

import pandas as pd
import numpy as np
import cufflinks as cf
cf.go_offline(connected=False)
import seaborn as sns
import os
from backend import checkpoint

## imports
from backend import scale_close
from backend import make_sma_targets, delta_maker
from backend import atr_exits,plot_grid,backtest,load_data,smac_with_confirmation,compile_signals,hl

'''FUNCTION WILL START HERE. '''

def delta_momma_loop(path,var1_name,var2_name,var3_name,var_1s,var_2s,slow):

    df   = load_data(path)

    results_list = []


    def buy_delta(df,THRESH,SELL):


        df  = delta_maker(df,THRESH)

        BUY = 'delta_ab_thresh'
        df['buy'] = (df[BUY].shift()==False) & ( df[BUY]==True)
        df['sell'] = (df[SELL].shift()==False) & ( df[SELL]==True)
        df = compile_signals(df)
        result = backtest(df,
                           plot_capital=False,
                           strat_name='delta_experiments'
                          )

        result['delta_thresh'] = THRESH
        return result

    results = []

    df    = load_data(path)

    def all_delta_and_what_not(df,fast,slow,THRESH):
        '''
        TAKES:
            1.df
            2.fastma variable
            3.slowma variable
            4.DELTA THRESH
            5.sell
        '''
        df    = df[['open','low','high','close']]
        df    = make_sma_targets(df,fast,slow)
        sell   = 'was_ab_now_bl'
        result = buy_delta(df,THRESH,sell)
        result['fast'] = fast
        result['slow'] = slow
        result['delta_thresh'] = THRESH

        return result

    #FUNCTION - DONT DELEAT
    batch_time = datetime.now()
    grid = np.zeros((len(var_1s),len(var_2s)))
    gdf  = pd.DataFrame(grid,columns=var_2s)
    gdf.index = var_1s
    gdf

    print('shape is:',grid.shape)
    for var_1 in var_1s:
        for var_2 in var_2s:
            #[[[[[[[[[[[[[[[[[[STAT FUNCTION]]]]]]]]]]]]]]]]]]]]]]] 
            result = all_delta_and_what_not(df,var_2,slow,var_1)


            #[[[[[[[[[[[[[[[[[[[[[[[[[[ENDS HERE]]]]]]]]]]]]]]]]]]]]]]]]]]


            #SAVE GRID
            final_pnl         = result['final_pnl'][0]
            
            print('final_pnl:',final_pnl)
            print(gdf)
            #ADD STUFF TO RESULTS
            result['batch_time'] = batch_time
            result['run_time']   = datetime.now()
            #result['run_time']     = datetime.now()
            gdf[var_2][var_1] = final_pnl
            results.append(result)
    gdf
    print(gdf)
    #TIME TO RUN
    time_delta = datetime.now()-batch_time

    #ADD SOME BASIC INFO TO THE SHEET
    print('loop ran in:',time_delta)
    rdf = pd.concat(results).sort_values('final_pnl')[::-1]
    rdf['save_name'] = path.replace('data/','').replace('.csv','').replace(' ','_')
    rdf['time_delta'] = time_delta
    rdf['buyholdpnl'] = ((df['close'][-1]- df['close'][0])/df['close'][0])*100
    rdf['sheet_path'] = path
    rdf['var_1'] = var1_name
    rdf['var_2'] = var2_name
    rdf['var_3'] = var3_name

    #print('final_pnl:',rdf.final_pnl[0])
    print()
    pd.DataFrame(rdf.iloc[0]).drop(['batch_time','run_time'],axis=0)

    # the goal is to find the center of this thing


    # CREATE DIRECTORYS

    #NAME PATH TO SAVE RESULTS
    master_out  = 'output/'
    if not os.path.exists(master_out):
        os.mkdir(master_out)
    output_path = master_out + path.replace('data/','').replace('.csv','/').replace(' ','_') 
    #CREATE DIRECTORY IF IT DOESNT EXIST
    if not os.path.exists(output_path):
        os.mkdir(output_path)
        print('created:',output_path)
    else:
        print('directory exists!',output_path)
    #CREATE A DIRECTORY TO SAVE GRID
    grid_path = output_path + 'grids/'
    if not os.path.exists(grid_path):
        os.mkdir(grid_path)
        print('created:',grid_path)
    else:
        print('directory exists!:',grid_path)


    #.............................................................................................

    #SAVE GRID


    


    # DESCRIBE VARIABLE RANGE
    var1_name =var1_name +str(var_1s).replace(' ','')
    var2_name =var2_name +str(var_2s).replace(' ','')
    var3_name =var3_name +str(slow).replace(' ','')
    #CREATE GRID NAME
    grid_name=  grid_path+var1_name+var2_name+var3_name+'.csv'
    # SAVE GRID
    gdf.to_csv(grid_name)
    print('saved grid to:',grid_name)

    #if in a notebook plot the grid
    #import seaborn as sns
    #sns.heatmap(gdf)
    #gdf

    # SAVE RESULTS

    rdf = rdf.set_index('run_time')
    # establish results path name. 
    results_path = output_path + 'results.csv'
    print(results_path)

    # if path doesnt exists just save the reuslts
    if not os.path.exists(results_path):
        rdf.to_csv(results_path)
        print('results dataframe created:',results_path)
    else:
        print('results dataframe exists!',results_path)
        rdf
        #load old results
        old_results = pd.read_csv(results_path).set_index('run_time')
        #append old results
        results_mixed = old_results.append(rdf)
        #save combined results
        results_mixed.to_csv(results_path)
        print('updated:',results_path)

    # SAVE INFO

    #taking the best preforming strat for info archive
    info = pd.DataFrame(rdf.set_index('batch_time').iloc[0])
    info.index.name = 'batch_time'
    info = info.T
    info.index.name = 'batch_time'
    info

    info_path = output_path+'info.csv'
    if not os.path.exists(info_path):
        print('creating info sheet')
        info.to_csv(info_path)
    else:
        print('info sheet exists!',info_path)
        old_info = pd.read_csv(info_path).set_index('batch_time')
        old_info
        idf = info
        #idf.index.name = 'batch_time'
        idf

        mixed_info = old_info.append(idf)
        mixed_info.to_csv(info_path)
        print('info sheet updated!')

    ## LAST STEP IS TO APPEND THE ALL RESULTS

    ## save all results in Aggrigate! 

    output_path = 'Aggrigate/'
    #CREATE DIRECTORY IF DOESNT EXISTS
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    #rdf = rdf.set_index('run_time')
    # establish results path name. 
    results_path = output_path + 'results.csv'
    print(results_path)

    # if path doesnt exists just save the reuslts
    if not os.path.exists(results_path):
        rdf.to_csv(results_path)
        print('results dataframe created:',results_path)
    else:
        print('results dataframe exists!',results_path)
        rdf
        #load old results
        old_results = pd.read_csv(results_path).set_index('run_time')
        #append old results
        results_mixed = old_results.append(rdf)
        #save combined results
        results_mixed.to_csv(results_path)
        print('updated:',results_path)

    info_path = output_path+'info.csv'
    if not os.path.exists(info_path):
        print('creating info sheet')
        info.to_csv(info_path)

    else:
        print('info sheet exists!',info_path)
        old_info = pd.read_csv(info_path).set_index('batch_time')
        old_info

        idf = info.T
        idf.index.name = 'batch_time'
        idf

        mixed_info = old_info.append(idf)
        mixed_info.to_csv(info_path)
        print('info sheet updated!',info_path)



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
var_1s = [1.5,2,2.5,3,4,5,6]
#FAST_MAS
var_2s = [5,6,7,8,9,10,12]
slows = [20,30,40,50,80,100]
#slows = [80,100]




for path in os.listdir('data/'):
    path = 'data/'+path
    for slow in slows:
        delta_momma_loop(path,var1_name,var2_name,var3_name,var_1s,var_2s,slow)
        eng.say('the variable three iteration is compleate')
        eng.runAndWait()
eng.say('the path iterations is compleate, setting up the next path')
    
