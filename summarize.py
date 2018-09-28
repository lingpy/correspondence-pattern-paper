from lingpy import *
import numpy as np
from glob import glob
from tabulate import tabulate

data = [
        'burmish-240-8',
        'chinese-623-14',
        'polynesian-210-10',
        'japanese-200-10',
        ]

content = [
        'number',
        'accuracy',
        'proportion',
        'density',
        'fuzziness',
        'coverage',
        'purity',
        'sounds',
        'missing',
        'csetsize',
        'clusters',
        'props',
        'patterns',
        'predicted',
        'predictable',
        'removed',
        'regs',
        'purityx'
        ]

selected = ['proportion', 
        'clusters', 'regs', 'predicted', 'accuracy']
table = [['name', 'percent'] + selected]
for d in data:
    for prop in ['25', '50', '75']:
        f = 'results/'+d+'-'+prop+'.txt'
        csv = np.array(csv2list(f, dtype=[float for x in content], header=True))
        if csv.any():
            try:
                scores = {content[i]: csv[:, i] for i in range(len(content))}
                name = d.split('-')[0].capitalize()
                table += [[name, prop]+['{0:.2f} ± {1:.2f}'.format(
                    scores[h].mean(), scores[h].std()) for h in selected]]
            except:
                print('no deal for ', f)
table = [table[0]] + sorted(table[1:], key=lambda x: x[0])
print(tabulate(table, headers='firstrow', tablefmt='latex'))


