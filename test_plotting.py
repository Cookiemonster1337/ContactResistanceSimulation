import plotly.graph_objects as go
import pandas as pd

print('load data...')
z_data = pd.read_csv('data/surface/surface_200_2.5_5.csv', sep='\t', usecols=['z_val'])
print('data succesfully aquired!')

print('generate 3d plot...')
fig = go.Figure(data=[go.Surface(z=z_data.values)])

# fig.update_layout(title='surface', autosize=False,
#                   width=100, height=50,
#                   margin=dict(l=65, r=50, b=65, t=90))

fig.show()
print('finished!')