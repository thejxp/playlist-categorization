
import pandas as pd

import plotly
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.plotly as py

def create_trace(df, data, names, label):
    dates = df.popularity
    colors = df.valence
    vals = data[data.columns[0]].values
    trace = go.Scatter(
        x = dates,
        y = vals,
        name = label,
        mode = 'markers',
        text = names,
        marker = dict(color=colors,
                      colorscale='Viridis',
                      showscale=True,
                      opacity= 0.4)
    )
    return trace

def get_all_traces(df, columns, labels):
    traces = []
    names = df['name']
    for i in range (len(columns)):
        col_name = columns[i]
        data = pd.DataFrame(df[col_name]).set_index(df.index)
        data.columns = [columns[i]]
        trace = create_trace(df, data, names, labels[i])
        traces.append(trace)
    return traces

def plot(df, fields, title='All Songs'):
    """Plots the song information."""
    plotly.tools.set_credentials_file(username='thejxp', api_key='wfsVGlOX5faQylQV3SCc')
    init_notebook_mode(connected=True)
    traces = get_all_traces(df, fields, fields)

    layout = dict(title = title,
                  xaxis = dict(title = 'popularity'),
                  yaxis = dict(title = 'number'),
                 )
    fig = dict(data=traces, layout=layout)
    iplot(fig, filename=title)