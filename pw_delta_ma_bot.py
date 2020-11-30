from biterbackend import scale_close

from datetime import datetime
start = datetime.now()
import pandas as pd
import numpy as np
import cufflinks as cf
cf.go_offline(connected=False)
import seaborn as sns
import os
from biterbackend import atr_exits,plot_grid,backtest,load_data,smac_with_confirmation,compile_signals,hl
from biterbackend import sola
from biterbackend import buy_delta,all_delta_and_what_not
results= []

from biterbackend import delta_maker,make_sma_targets

from biterbackend import make_sma_targets,delta_maker


'''THIS MAKES YOUR STRAT A BOT ...'''
'''TRIL dont forget you are long'''
from biterbackend import get_some
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
fast  = 5
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
statust['win_pnl'] = '38%'
statust['equity']  = '199%'
statust['fast']    = fast
statust['slow']    = slow
statust['thresh']  = THRESH

statust['engaged'] = statust['trac']
status = statust.T

from biterbackend import atr_exits,compile_signals
df = atr_exits(df,
              dn_mul=0.5,
              up_mul=2)
#you have to specify which sell column to use 
df = compile_signals(df,sell='atr_sell')
#You must turn 'rerun_df' and 'plot_capital '
#to True in bck test if you want to plot plot
results2,df = backtest(df,
                   plot_capital=True,
                   strat_name='sma cross over-with atr sell',
                  return_df=True
                  )
stat = df[['trac','atr_stop','atr_targ','atr_sell']]
stat = pd.DataFrame(stat.iloc[-1]).T 
stat['euity'] =  '295%'
stat['win_pct']= '65%'
stat = stat.T
stat.index.name = 'sma_buy'
stat

if stat.T['trac'][0] == True:
    eng.say('a t r slow average buy is engaged')
    eng.runAndWait()
