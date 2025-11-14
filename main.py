import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import savgol_filter

from wdf import Wdf

DEAD_PIXEL = 491

map_data = Wdf('map.wdf')
bg_data = Wdf('background.wdf')

map_spectra = np.array(map_data.spectra)
x_axis = map_data.x_axes[0]

bg_spectrum = np.array(bg_data.spectra[0])

# Dead pixel removal
map_spectra[:, DEAD_PIXEL] = ( map_spectra[:, DEAD_PIXEL-1] + map_spectra[:, DEAD_PIXEL-1] ) / 2

# Smoothing
map_spectra = savgol_filter(map_spectra, 21, 3, axis=1)
bg_spectrum = savgol_filter(bg_spectrum, 21, 3)

mean_spectra = np.mean(map_spectra, axis=0)

# Background scaling and subtraciton
ref_region = slice(300, 512)

scale_factor = mean_spectra[ref_region].mean() / bg_spectrum[ref_region].mean()
bg_scaled = bg_spectrum * scale_factor
corrected = mean_spectra - bg_scaled

fig = make_subplots(
    rows=3, cols=1,
    subplot_titles=('Individual Spectrum', 'Background', 'Mean Spectrum - Background')
)
fig.add_trace(go.Scatter(
    x=x_axis,
    y=bg_spectrum,
    mode='lines',
    showlegend=False
), row=2, col=1)
for ii in range(map_spectra.shape[0]):
    fig.add_trace(go.Scatter(
        x=x_axis,
        y=map_spectra[ii],
        mode='lines',
        showlegend=False
    ), row=1, col=1)
fig.add_trace(go.Scatter(
    x=x_axis,
    y=corrected,
    mode='lines',
    showlegend=False
), row=3, col=1)
fig.update_layout(
    template='simple_white'
)
fig.show()