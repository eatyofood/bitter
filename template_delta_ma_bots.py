from backend import scale_close

from datetime import datetime
start = datetime.now()
import pandas as pd
import numpy as np
import cufflinks as cf
cf.go_offline(connected=False)
import seaborn as sns
import os
from backend import atr_exits,plot_grid,backtest,load_data,smac_with_confirmation,compile_signals,hl
from backend import sola
from backend import buy_delta,all_delta_and_what_not
results= []

from backend import delta_maker,make_sma_targets

from backend import make_sma_targets,delta_maker


'''THIS MAKES YOUR STRAT A BOT ...'''
'''TRIL dont forget you are long'''
from backend import get_some
df = get_some('historical-chart/1hour','BEEM')
df

df = df.set_index('date')
df.index = pd.to_datetime(df.index)
df

df = df[::-1]
df

# now make it a bot!!!!!!!!!!!!


#dpath = 'data/'+sheet
#print(sheet)
#df    = load_data(dpath)

#LITERLLY ALL YOU HAVE TO DO TO MAKE THIS AN ACTIVE BOT IS 
#DOWNLOAD DATA RIGHT HERE!!!
THRESH= 2.5
fast  = 6
slow  = 30
df    = make_sma_targets(df,fast,slow)


SELL   = 'was_ab_now_bl'
result = buy_delta(df,THRESH,SELL)
results.append(result)
col   = 'delta_ab_thresh'
buy   = col+'scale'#'abovescale'
df    = scale_close(col,df)
sell   = SELL+'scale'#'abovescale'
df    = scale_close(SELL,df)
sola(df[['high','slow','close','fast',sell,buy]])
df.columns
result

sola(df[['high','low','fast','slow','tracscale']])

status = pd.DataFrame(df[['waiting','fast_delta','trac']].iloc[-1])
hl(status)

import pyttsx3
eng = pyttsx3.init()
eng.setProperty('rate',150)

if status.T['trac'][0] == True:
    eng.say("the BEEM Delta algo is engaged")
    eng.runAndWait()
if status.T['waiting'][0] == True:
    eng.say('the BEEM Delta Algo is Closed')

statust = status.T
statust['sharpe']  =  1.42648
statust['win_pnl'] = '71%'
statust['equity']  = '360%'
statust['fast']    = fast
statust['slow']    = slow
statust['thresh']  = THRESH

statust['engaged'] = statust['trac']
status = statust.T
