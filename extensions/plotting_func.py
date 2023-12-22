import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io

data_dict = {'A': [{'Scientific': '40.0000', 'Classical': '40.0000'}, 
                   {'Scientific': '5.0000', 'Classical': '5.0000'}], 
             'Z': [{'Scientific': '30.0000', 'Classical': '30.0000'},
                   {'Scientific': '1.0000', 'Classical': '1.0000'}]}


# Основные параметры графиков
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)
plt.rcParams['figure.figsize'] = [12.5, 1.6+0.1*len(data_dict)]

CAPSIZE = 5 # Ширина концов линий для отметки погрешностей
ERROR_LINEWIDTH = 3 # Ширина линий для отметки погрешностей
DOT_FORMAT = 'o' # Стиль точек
COLOR = "blue" # Цвет линий
MARKERSIZE = 7 # Размер точек

X_NAME = 'X'
X_UNIT = 'x'

fig, ax1 = plt.subplots()
ax1.grid(True, linewidth=0.3)

for param, error, y in zip([float(data_dict[key][0]['Scientific']) for key in data_dict.keys()],
                           [float(data_dict[key][1]['Scientific']) for key in data_dict.keys()],
                           range(len(data_dict))):
    ax1.errorbar(param, y+1, xerr=error, yerr=0, 
                 fmt=DOT_FORMAT, color='b', capsize=CAPSIZE, linewidth=ERROR_LINEWIDTH, markersize=MARKERSIZE)
ax1.set_yticks(range(len(data_dict)+2),['']+list(data_dict.keys())+[''])

plt.xlabel(f'{X_NAME} , [{X_UNIT}]')


ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

fig.subplots_adjust(bottom=0.3)

fig.savefig('Linear.png', dpi=300, transparent=True)

"""
buf = io.BytesIO()
plt.savefig(buf, dpi=96)
plt.close()
buf.seek(0)
img = Image.open(buf) 
"""