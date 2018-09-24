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
        'ubound',
        'clusters',
        'props',
        'patterns']

selected = ['accuracy', 'proportion', 'density', 'missing', 'sounds']
table = [['name'] + selected]
for f in data:
    csv = np.array(csv2list(f, dtype=[float for x in content]))
    scores = {content[i]: csv[:, i] for i in range(len(content))}
    name = f.split('/')[-1][:-4]
    table += [[name]+['{0:.2f} / {1:.2f}'.format(
        scores[h].mean(), scores[h].std()) for h in selected]]
print(tabulate(table, headers='firstrow'))
