import glob
import pandas as pd
import sys
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np

# Optionally use different styles for the graph
# Gallery: http://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
# import matplotlib
# matplotlib.style.use('dark_background')  # interesting: 'bmh' / 'ggplot' / 'dark_background'


class Radar(object):
    def __init__(self, figure, title, labels, rect=None):
        if rect is None:
            rect = [0.05, 0.05, 0.9, 0.9]

        self.n = len(title)
        self.angles = np.arange(0, 360, 360.0/self.n)
        self.steps = len(labels[0])

        self.axes = [figure.add_axes(rect, projection='polar', label='axes%d' % i) for i in range(self.n)]

        self.ax = self.axes[0]
        self.ax.set_thetagrids(self.angles, labels=title, fontsize=10, color='r') # Text at the ends of the axis

        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid(False)
            ax.xaxis.set_visible(False)

        for ax, angle, label in zip(self.axes, self.angles, labels):
            ax.set_rgrids(range(1, self.steps), angle=angle, labels=label, fontsize=6, color='g') # Text in spines
            ax.spines['polar'].set_visible(False)
            ax.set_ylim(0, self.steps - 1)

    def plot(self, values, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)

#-------------------------------------------------------------------------------

# Show all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 0)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'left')

#-------------------------------------------------------------------------------

# Collect data from the log files

results = pd.DataFrame(columns=['Filename', 'Round', 'Heuristic', 'Duration', 'Won Rate'])
result_dict = {}
for filename in glob.glob('Log*.txt'):
    with open(filename) as file:
        _ = file.readline()         # Start:2018-10-30 22:49:23.089675
        line_1 = file.readline()    # Round: 0
        line_2 = file.readline()    # Heuristics:{20: [1, -2, -2, 2], 40: [1, -2, 2, 2], 100: [1, -4, -1, -4]}
        line_3 = file.readline()    # Duration:0:18:05.672874Your agent won 68.0% of matches against Minimax Agent
        if len(line_3) > 24:
            won_rate = int(float(line_3.split()[3][:-1]))
        else:
            line_4 = file.readline()    # Your agent won 68.0% of matches against Minimax Agent
            won_rate = int(float(line_4.split()[3][:-1]))
        result_dict = {'Filename' : filename,
                       'Round' : int(line_1.split()[1]),
                       'Heuristic' : line_2.split(':', maxsplit=1)[1],
                       'Duration' : datetime.datetime.strptime(line_3[9:23], '%H:%M:%S.%f'),
                       'Won Rate' : won_rate}
        results.loc[len(results)] = result_dict
#print(results)

#-------------------------------------------------------------------------------

plot = plt.figure(figsize=(10, 9))
plot.subplots_adjust(left=0.2, bottom=0.2, right=0.99, top=0.92, wspace=0.05, hspace=0.30)

titles = ['Opening', 'Opening Own Lib.', 'Opening Opp. Lib.', 'Opening Opp. Dist.', 'Opening Center Dist.',
          'Midgame', 'Midgame Own Lib.', 'Midgame Opp. Lib.', 'Midgame Opp. Dist.', 'Midgame Center Dist.',
          'Endgame Own Lib.', 'Endgame Opp. Lib.', 'Endgame Opp. Dist.', 'Endgame Center Dist.']

labels = [['0', '', '10', '', '20', '', '30', '', '40', '', '50', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', ''],
          ['0', '', '10', '', '20', '', '30', '', '40', '', '50', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', ''],
          ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '']]

radar = Radar(plot, titles, labels)
for i in range(5):
    radar.ax.fill_betweenx(np.asarray([0, int((radar.steps - 1) / 2)]),
                           x1=np.deg2rad(radar.angles[i] - radar.angles[1] / 2),
                           x2=np.deg2rad(radar.angles[i] + radar.angles[1] / 2),
                           color='b',
                           alpha=0.1)
    radar.ax.fill_betweenx(np.asarray([int((radar.steps - 1) / 2), radar.steps]),
                           x1=np.deg2rad(radar.angles[i] - radar.angles[1] / 2),
                           x2=np.deg2rad(radar.angles[i] + radar.angles[1] / 2),
                           color='b',
                           alpha=0.2)

for i in range(5,10):
    radar.ax.fill_betweenx(np.asarray([0, int((radar.steps - 1) / 2)]),
                           x1=np.deg2rad(radar.angles[i] - radar.angles[1] / 2),
                           x2=np.deg2rad(radar.angles[i] + radar.angles[1] / 2),
                           color='lightblue',
                           alpha=0.7)
    radar.ax.fill_betweenx(np.asarray([int((radar.steps - 1) / 2), radar.steps]),
                           x1=np.deg2rad(radar.angles[i] - radar.angles[1] / 2),
                           x2=np.deg2rad(radar.angles[i] + radar.angles[1] / 2),
                           color='lightblue')

for i in range(10,14):
    radar.ax.fill_betweenx(np.asarray([0, int((radar.steps - 1) / 2)]),
                           x1=np.deg2rad(radar.angles[i] - radar.angles[1] / 2),
                           x2=np.deg2rad(radar.angles[i] + radar.angles[1] / 2),
                           color='lightyellow',
                           alpha=0.5)
    radar.ax.fill_betweenx(np.asarray([int((radar.steps - 1) / 2), radar.steps]),
                           x1=np.deg2rad(radar.angles[i] - radar.angles[1] / 2),
                           x2=np.deg2rad(radar.angles[i] + radar.angles[1] / 2),
                           color='lightyellow')

#-------------------------------------------------------------------------------

# Best performer
best_performer_nums = [20,  1, -2, -4,  2, # Opening
                       50,  1, -2,  0,  4, # Midgame
                            1, -4, -2, -4] # Endgame
best_performer_numbers = [i + 5 if i < 10 else int(i / 5) + 1 for i in best_performer_nums]

radar.plot(best_performer_numbers,
           '-', lw=2, color='b', # alpha=0.4,
           label='Best Performer (94%)')

# Baseline

baseline_performer_nums = [30, 1, -1, 0, 0, 40, 1, -1, 0, 0, 1, -1, 0, 0]
baseline_performer_numbers = [i + 5 if i < 10 else int(i / 5) + 1 for i in baseline_performer_nums]

radar.plot(baseline_performer_numbers,
           '-', lw=2, color='r', # alpha=0.4,
           label='Baseline (85%)')

radar.ax.legend(bbox_to_anchor=(1.1, 1.05))

plot.savefig(sys.argv[0].replace('.py',' - Radar - 1.png'))

plot.show()
