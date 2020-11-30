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
statust['fast']    = 6
statust['slow']    = 42
statust['thresh']  = 2.5

statust['engaged'] = statust['trac']
status = statust.T


def candel_hits(df,riz_thresh=40):
    import talib
    import pandas_ta as pta
    df['SHORTLINE'] = talib.CDLSHORTLINE(df.open,df.high,df.low,df.close)


    df['RSI-2'] = pta.rsi(df.close,legnth=2)
    df['candel_hit'] = (df['SHORTLINE'] == 100) & (df['RSI-2']<riz_thresh)


    df['candelscale'] = df['candel_hit'].replace(True,1).replace(1,df.close)

    df[['high','low','candelscale']].iplot(theme='solar',fill=True,title='SHORTLINE CANDEL')


    candel_control = df.drop(['open','high','low'],axis=1)
    candel_hit = candel_control['candel_hit'][-1]==True
    print(candel_hit)
    candel_control = pd.DataFrame(candel_control.iloc[-1])

    import pyttsx3

    eng = pyttsx3.init()
    eng.setProperty("rate",150)


    if candel_hit==True:
        eng.say("WE HAVE {} CANDEL HIT ON D M T K ".format(candel_name))
        eng.runAndWait()
    return candel_control

candel_control = candel_hits(df,riz_thresh=40)
