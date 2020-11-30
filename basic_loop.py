from backend import iteration_loop
import pandas as pd
import os
from backend import load_data
from backend import macd_backtest
from backend import emac_backtest
from backend import smac_backtest
from backend import rsi_backtest



#define the data list
path = 'data/'
dirli = os.listdir(path)
pd.DataFrame(dirli,columns=['data'])


for sheet in dirli:
    path = 'data/'+sheet
    print(path)

    # MACD backtest
    var1_name='macd_fast_small'
    var_1s = [5,10,15,20,25,30,35]
    var2_name='macd_slow_large'
    var_2s = [64,70,75,80,85,90,100,125,150]
    strat_function = macd_backtest
    iteration_loop(strat_function,path,var1_name,var2_name,var_1s,var_2s)

    # RSI backtest
    var1_name='rsi_lower'
    var2_name='rsi_upper'
    var_1s = [15,20,25,30,35,42,]
    var_2s = [55,60,65,70,85,90]
    strat_function = rsi_backtest
    iteration_loop(strat_function,path,var1_name,var2_name,var_1s,var_2s)

    # SMAC backtest
    var1_name='fast'
    var2_name='slow'
    var_1s = [5,10,15,20,25,30,35,40,]
    var_2s = [42,50,60,65,70,85,90,100,150]
    strat_function = smac_backtest
    iteration_loop(strat_function,path,var1_name,var2_name,var_1s,var_2s)

    # EMAC Backtest Loop
    var1_name='fast'
    var2_name='slow'
    var_1s = [5,10,15,20,25,30,35,40,]
    var_2s = [42,50,60,65,70,85,90]
    strat_function = emac_backtest
    iteration_loop(strat_function,path,var1_name,var2_name,var_1s,var_2s)


import delta_mamma