from surface import create_surfacetopo, surfacetopo_3d, surface_crosssection_2d, surfacepeaks_2d
from fibers import create_gdltopo, gdltopo_3d, gdltopo_2d, gdlpeaks_2d, gdl_crosssection_2d
from microcontacts import find_microcontacts, microcontacts_2d
from ecr import calc_ecr, plot_ecr
from pymongo import MongoClient
from gui import overview
from app import dashplot
import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output

# set use of mongo-db
mdb = 'off'

if mdb == 'on':
    # initialize mongo connector object with ip adress
    client = MongoClient('zbts07')
    # get reference to existing database testDB
    db = client.testDB
    # reference collection, if not existent it will be created
    current_collection = db['NMT_TestCollection']
    # authentication within database
    db.authenticate('jkp', 'qwertz', source='admin')

# main parameters
res = 1000 #µm/mm
area = 0.01 #mm2
pressure = 1 #MPa

surface_params = {'d_peak [1/mm]': 98, 'r1 [µm]': 3.67, 'sigma_s [µm]': 3.55}
gdl_params = {'gdl_thk [µm]': 110, 'porosity': 0.7, 'fiber_dia [µm]': 7, 'binder_thk [µm]': 6}

gdl_mat_props = {'el. res. [µOhm*m]': 800}
surface_mat_props = {'el. res. [µOhm*m]': 190}

spacing = 10

# surface, surface_peaks, surface_data, surface_mean_summit = create_surfacetopo(mdb, res, area, surface_params)
# # surfacetopo_3d(res, surface, 50)
# # surfacepeaks_2d(res, surface_mean_summit, 50)
# #surface_crosssection_2d(surface_peaks, 50)
#
# gdl, gdl_peaks, gdl_fibers = create_gdltopo(res, area, gdl_params)
# # gdlpeaks_2d(gdl_peaks)
# # gdltopo_3d(res, gdl, 50)
#
# mcs, mcs_surface, mcs_gdl = find_microcontacts(gdl_params, surface_params, surface_mean_summit, gdl_peaks, spacing)
# # microcontacts_2d(mcs_surface)
#
# ecr, z_distance = calc_ecr(gdl_params, surface_params, surface_mat_props, gdl_mat_props, mcs)
# # plot_ecr(ecr, z_distance)
#
# fig = overview(res, surface, surface_mean_summit, gdl, gdl_peaks, mcs_surface, ecr, z_distance)
#dashplot(fig)

app = dash.Dash(__name__)


app.layout = html.Div(
    children=[
        html.H1(children='Surface Simulation', style={'textAlign': 'center'}),
        html.Div(className='row',
            children=[
                html.Div(className='three columns div-user-controls',
                children = [
                    html.H2('PARAMETERS'),
                    html.Div([
                        html.P('d_peak [µm]', style={'display': 'inline-block'}),
                        dcc.Input(id='d_peak', value=98, type='number',
                                  style={'margin-left': '20px', 'width': '100px', 'display': 'inline-block'})
                             ], style={'margin-bottom': '10px'}),
                    html.Div([
                        html.P('r1 [µm]', style={'display': 'inline-block'}),
                        dcc.Input(id='r1', value=3.67, type='number',
                                  style={'margin-left': '50px', 'width': '100px', 'display': 'inline-block'})
                            ], style={'margin-bottom': '10px'}),
                    html.Div([
                        html.P('sigma_s [µm]', style={'display': 'inline-block'}),
                        dcc.Input(id='sigma_s', value=3.55, type='number',
                                  style={'margin-left': '18px', 'width': '100px', 'display': 'inline-block'})
                            ], style={'margin-bottom': '10px'}),
                             # style={'width': '33%', 'display': 'inline-block'}
                    html.Div([
                        html.P('gdl_thk [µm]', style={'display': 'inline-block'}),
                        dcc.Input(id='gdl_thk', value=110, type='number',
                                  style={'margin-left': '21px','width': '100px', 'display': 'inline-block'}),
                             # style={'width': '33%', 'display': 'inline-block'}
                             ], style={'margin-bottom': '10px'}),
                    html.Div([
                         html.P('porosity', style={'display': 'inline-block'}),
                         dcc.Input(id='porosity', value=0.7, type='number',
                                   style={'margin-left': '50px','width': '100px', 'display': 'inline-block'})],
                             # style={'width': '33%', 'display': 'inline-block'}
                             style={'margin-bottom': '10px'}),
                    html.Div([
                        html.P('fiber_dia', style={'display': 'inline-block'}),
                        dcc.Input(id='fiber_dia', value=7, type='number',
                                  style={'margin-left': '45px', 'width': '100px', 'display': 'inline-block'})],
                             # style={'width': '33%', 'display': 'inline-block'}
                             style={'margin-bottom': '10px'}),
                    html.Div([
                        html.P('binder_thk [µm]', style={'display': 'inline-block'}),
                        dcc.Input(id='binder_thk', value=6, type='number',
                                  style={'margin-left': '5px', 'width': '100px', 'display': 'inline-block'})],
                             # style={'width': '33%', 'display': 'inline-block'}
                             ),
                    ],
                 # style={"l": "25px", "r": "25px", 'display': 'inline-block'}
                ),
        html.Div(className='nine columns div-for-charts bg-grey',
            children=[
                dcc.Graph(id='sf-sim')],
                # style={"margin-left": "25px", 'display': 'inline-block'}
                )
            ]

                )
    ]
)


@app.callback(
    Output('sf-sim', 'figure'),
    Input('d_peak', 'value'),
    Input('r1', 'value'),
    Input('sigma_s', 'value'),
    Input('gdl_thk', 'value'),
    Input('porosity', 'value'),
    Input('fiber_dia', 'value'),
    Input('binder_thk', 'value')
)

def update_figure(d_peak, r1, sigma_s, gdl_thk, porosity, fiber_dia, binder_thk):
    surface_params['d_peak [1/mm]'] = d_peak
    surface_params['r1 [µm]'] = r1
    surface_params['sigma_s [µm]'] = sigma_s
    gdl_params['gdl_thk [µm]'] = gdl_thk
    gdl_params['porosity'] = porosity
    gdl_params['fiber_dia [µm]'] = fiber_dia
    gdl_params['binder_thk [µm]'] = binder_thk

    surface, surface_peaks, surface_data, surface_mean_summit = create_surfacetopo(mdb, res, area, surface_params)

    gdl, gdl_peaks, gdl_fibers = create_gdltopo(res, area, gdl_params)

    mcs, mcs_surface, mcs_gdl = find_microcontacts(gdl_params, surface_params, surface_mean_summit, gdl_peaks, spacing)

    ecr, z_distance = calc_ecr(gdl_params, surface_params, surface_mat_props, gdl_mat_props, mcs)

    fig = overview(res, surface, surface_mean_summit, gdl, gdl_peaks, mcs_surface, ecr, z_distance)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)



