import plotly.graph_objects as go
import pandas as pd
#
# print('load data...')
# z_data = pd.read_csv('data/surface/surface_200_2.5_5.csv', sep='\t', usecols=['z_val'])
# print('data succesfully aquired!')
#
# print('generate 3d plot...')
# fig = go.Figure(data=[go.Surface(z=z_data.values)])
#
# # fig.update_layout(title='surface', autosize=False,
# #                   width=100, height=50,
# #                   margin=dict(l=65, r=50, b=65, t=90))
#
# fig.show()
# print('finished!')

# z_data_1 = pd.read_csv('data/plotly_tutorials/' + 'test_surface.csv')
# data = pd.read_csv('data/surface/surface_100_3.67_3.55.csv', sep='\t', usecols=['x_val', 'y_val', 'z_val'])
# fig = go.Figure(data=[go.Surface(x=data['x_val'].values, y=data['y_val'].values, z=data[['x_val', 'y_val', 'z_val']].values)])
#
# fig.update_layout(title='Mt Bruno Elevation', autosize=False,
#                   width=500, height=500,
#                   margin=dict(l=65, r=50, b=65, t=90))
# print(data['x_val'].values, data['y_val'].values)
# # print(z_data_1)
# # print(z_data_2)
# fig.show()

data = pd.read_csv('data/surface/surface_100_3.67_3.55.csv', sep='\t')
print(data)



