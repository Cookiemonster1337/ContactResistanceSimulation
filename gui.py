from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import griddata
import plotly.express as px

def overview(res, surface, surface_peaks, gdl, gdl_peaks, mcs, ecr, z_dis, zlim=50):
    fig = make_subplots(rows=2, cols=3, vertical_spacing=0.15,
                        subplot_titles=('surface-2D', 'fibers-2D', 'MCS', 'surface-3D', 'fibers-3D', 'ECR'),
                        specs=[[{'type': 'scatter'}, {'type': 'scatter'}, {'type': 'scatter'}],
                               [{'type': 'surface'}, {'type': 'surface'}, {'type': 'scatter'}]
                               ])

    # surfacepeaks
    X_2d_sf = []
    Y_2d_sf = []

    for data in surface_peaks:
        X_2d_sf.append(data[0])
        Y_2d_sf.append(data[1])

    fig.add_trace(go.Scatter(x=X_2d_sf, y=Y_2d_sf, mode='markers'), row=1, col=1)

    # gdlpeaks
    X_2d_gdl = []
    Y_2d_gdl = []

    for data in gdl_peaks:
        X_2d_gdl.append(data[0])
        Y_2d_gdl.append(data[1])


    fig.add_trace(go.Scatter(x=X_2d_gdl, y=Y_2d_gdl, mode='markers'), row=1, col=2)

    # surfacetopo
    X_3d_sf = []
    Y_3d_sf = []
    Z_3d_sf = []

    for data in surface:
        X_3d_sf.append(data[0])
        Y_3d_sf.append(data[1])
        Z_3d_sf.append(data[2])

    xi = np.linspace(1, 100, 100)
    yi = np.linspace(1, 100, 100)

    X, Y = np.meshgrid(xi, yi)

    Z = griddata((X_3d_sf, Y_3d_sf), Z_3d_sf, (X, Y), method='nearest')


    fig.add_trace(go.Surface(z=Z, coloraxis="coloraxis"), row=2, col=1)

    # gdltopo
    X_3d_gdl = []
    Y_3d_gdl = []
    Z_3d_gdl = []

    for data in gdl:
        X_3d_gdl.append(data[0])
        Y_3d_gdl.append(data[1])
        Z_3d_gdl.append(data[2])

    xi = np.linspace(1, 100, 100)
    yi = np.linspace(1, 100, 100)

    X_gdl, Y_gdl = np.meshgrid(xi, yi)

    Z_gdl = griddata((X_3d_gdl, Y_3d_gdl), Z_3d_gdl, (X_gdl, Y_gdl), method='nearest')

    fig.add_trace(go.Surface(z=Z_gdl, coloraxis="coloraxis"), row=2, col=2)

    # microcontacts (on bp)
    mcs_x = []
    mcs_y = []

    for i in mcs[6]:
        mcs_x.append(i[0])
        mcs_y.append(i[1])

    fig.add_trace(go.Scatter(x=mcs_x, y=mcs_y, mode='markers'), row=1, col=3)

    # ecr
    fig.add_trace(go.Scatter(x=z_dis, y=ecr, mode='lines+markers'), row=2, col=3)

    # Update xaxis properties
    fig.update_xaxes(title_text="x [µm]", showgrid=False, row=1, col=1)
    fig.update_xaxes(title_text="x [µm]", showgrid=False, row=1, col=2)

    # Update yaxis properties
    fig.update_yaxes(title_text="y [µm]", showgrid=False, row=1, col=1)
    fig.update_yaxes(title_text="y [µm]", showgrid=False, row=1, col=2)

    # update x,y,z properties of 3d-graphs (3,4)
    fig.update_scenes(xaxis_title='x [µm]', yaxis_title=' y [µm]', zaxis_title='z [µm]',
                                                  zaxis=dict(nticks=4, range=[0, zlim]), row=2, col=1)

    fig.update_scenes(xaxis_title='x [µm]', yaxis_title=' y [µm]', zaxis_title='z [µm]',
                      zaxis=dict(nticks=4, range=[0, zlim]), row=2, col=2)

    # update layout of complete figure
    fig.update_layout(height=600, width=1000, showlegend=False,
                      coloraxis_colorbar_x=-0.2,
                      coloraxis_colorbar_thickness=20,
                      # coloraxis_colorbar_len=0.5,
                      # coloraxis=dict(colorscale='Reds')
                      )
    fig.show()

    return fig