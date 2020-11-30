import pandas as pd

df = pd.DataFrame()      
'''TARGETS!'''            
#STD TARGETS            
def std_targs(df=df,t1=0.5,t2=1,t3=2,roll_len=10,hi_rol_lo=10):
    #this reruns a data frame and targets with tuple unpacking...,
    #anything that could leak information has a:! in it...
    #roll_len = is the period of standard deviation
    #hi_rol_lo = is the rolling period of which to pull futur highs and lows
    df['STD'] = df['close'].rolling(roll_len).std()
    #name the up targets
    ut1 = ('STDR'+str(hi_rol_lo)+':up_target:_'+str(t1)+'!')
    ut2 = ('STDR'+str(hi_rol_lo)+':up_target:_'+str(t2)+'!')
    ut3 = ('STDR'+str(hi_rol_lo)+':up_target:_'+str(t3)+'!')
    #name the down targets
    dt1 = ('STDR'+str(hi_rol_lo)+':down_target:_'+str(t1)+'!')
    dt2 = ('STDR'+str(hi_rol_lo)+':down_target:_'+str(t2)+'!')
    dt3 = ('STDR'+str(hi_rol_lo)+':down_target:_'+str(t3)+'!')
    #create the std values
    st1 = df['STD'] * t1
    st2 = df['STD'] * t2
    st3 = df['STD'] * t3
    
    #create the targets/stops
    df[ut1] = (df['high'] +  st1)
    df[dt1] = (df['low'] -  st1)
    df[ut2] = (df['high'] +  st2)
    df[dt2] = (df['low'] -  st2)
    df[ut3] = (df['high'] + st3)
    df[dt3] = (df['low'] -  st3)

    #now create a count for each one with an upside down dataframe!!! yeet!
    df = df[::-1]
    rollingh = ('high_ahead!')#,str(hi_rol_lo)+'!')
    rollingl = ('low_ahead!')#,str(hi_rol_lo)+'!')
    df[rollingh] = df.high.rolling(hi_rol_lo).max()
    df[rollingl] = df.low.rolling(hi_rol_lo).min()
    df = df[::-1]
    #now we run bools on weather they are in range
    
    #name the new columns
    uth1 = ut1.replace('!','_HIT!')
    uth2 = ut2.replace('!','_HIT!')
    uth3 = ut3.replace('!','_HIT!')
    dth1 = dt1.replace('!','_HIT!')
    dth2 = dt2.replace('!','_HIT!')
    dth3 = dt3.replace('!','_HIT!')
    #make booleans of the action!
    df[dth3] = df[rollingl] < df[dt3]
    df[dth2] = df[rollingl] < df[dt2]
    df[dth1] = df[rollingl] < df[dt1]
    #i put close in the middle for visual efffect evaluating the frame!
    #df['cclosee'] = df['close']
    df[uth1] = df[rollingh] > df[ut1]
    df[uth2] = df[rollingh] > df[ut2]
    df[uth3] = df[rollingh] > df[ut3]
    
    #ts = [ut1,ut2,ut3,dt1,dt2,dt3]
    ts = ['close',dt3,dt2,dt1,ut1,ut2,ut3]
    #ths = [uth1,uth2,uth3,dth1,dth2,dth3]
    ths = ['close',dth3,dth2,dth1,uth1,uth2,uth3]
    print('these ARE targets!:\n',ts)
    return df,ths,ts

def add_targets(df):
    #df = df[['high','low']]
    df['plus_10!'] = df['high'] + (df['high']* .1)
    df['minus_10!'] = df['low'] - (df['low']* .1)
    df['plus_20!'] = df['high'] + (df['high']* .2)
    df['minus_20!'] = df['low'] - (df['low']* .2)
    df['minus_5!'] = df['low'] - (df['low']* .05)
    df['plus_5!'] = df['high'] + (df['high']* .05)
    df['minus_5!'] = df['low'] - (df['low']* .05)
    df
    
    df = df[::-1]
    df['highlast_10!'] = df['high'].rolling(10).max()
    df['lowlast_10!'] = df['low'].rolling(10).min()
    df  = df[::-1]

    df['uped_10!'] = df['plus_10!'] <= df['highlast_10!']
    df['downed_10!'] = df['minus_10!'] >= df['lowlast_10!']
    df['uped_20!'] = df['plus_20!'] <= df['highlast_10!']
    df['downed_20!'] = df['minus_20!'] >= df['lowlast_10!']
    df['uped_5!'] = df['plus_5!'] <= df['highlast_10!']
    df['downed_5!'] = df['minus_5!'] >= df['lowlast_10!']
    return(df)

