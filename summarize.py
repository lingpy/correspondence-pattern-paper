from lingpy import *
import numpy as np
from glob import glob
from tabulate import tabulate

data = glob('results/*.txt')
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

selected = ['accuracy', 'proportion', 'density', 'missing', 'sounds',
        'clusters', 'purity', 'regs', 'purityx']
table = [['name'] + selected]
for f in data:
    csv = np.array(csv2list(f, dtype=[float for x in content], header=True))
    if csv.any():
        try:
            scores = {content[i]: csv[:, i] for i in range(len(content))}
            name = f.split('/')[-1][:-4]
            table += [[name]+['{0:.4f} / {1:.4f}'.format(
                scores[h].mean(), scores[h].std()) for h in selected]]
        except:
            print('no deal for ', f)
table = [table[0]] + sorted(table[1:], key=lambda x: x[0])
print(tabulate(table, headers='firstrow'))


