import plotly.graph_objects as go

def plot_candel(df,ticker,time_frame):

    #and finally plot the shindig
    fig = go.Figure(data=[go.Candlestick(x=df.index,#x=df['date'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    increasing_line_color= 'cyan',
                    decreasing_line_color= 'gray'   
                                        ),
                         go.Scatter(x=df.index, y=df['fast'],name='fast' ,line=dict(color='orange', width=3)),
                        go.Scatter(x=df.index, y=df['slow'], name='slow',line=dict(color='green', width=3))

                         ])
    #buy strace

    fig.add_trace(go.Scatter(x=df.index, y=df['val'],
                            mode='lines',name='Validation',
                             line=dict(color='lightskyblue',
                                      )
                            ))
    #                    mode='markers',
    #                    name='markers'))



    fig.add_trace(go.Scatter(x=df.index, y=df['buyscale'],
                        mode='markers',
                        name='BUY',
                            marker=dict(
                            color='seagreen',
                            size=8
                            )
                            ))


    fig.add_trace(go.Scatter(x=df.index, y=df['sellscale'],
                        mode='markers',
                        name='SELL',
                                     marker=dict(
                                     color='#d62728',
                                     size=8,)


                            ))

    fig.add_trace(go.Scatter(x=df.index, y=df['tracscale'],

    mode='lines',
    name='BUY',
    opacity=0.09,
    fill='tozeroy',
                            line=dict(color='lightgreen')))



    fig.update_layout(template="plotly_dark",title=(ticker+'-'+time_frame))
    fig.show(theme='solar')
    # IF MARKERS ARE TOO BUSY BLOCK THEM OUT WITHTHE TRACER
    #df['tracscale']=df['trac']
    #for i in range(1,len(df)):
    #    if df['trac'][i-1]==True:
    #        df['buyscale'][i]=np.nan
    #    if df['sellscale'][i-1]==False:
    #        df['sellscale'][i]=np.nan