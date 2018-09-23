from lingpy import *
from lingrex.copar import *
from sys import argv
import random
from lingpy.basictypes import *
from tabulate import tabulate
from lingpy.compare.sanity import average_coverage
from scipy.stats import spearmanr


def run_experiments(f, ref, ratio, subset=None, runs=100, refine_patterns=False,
        sort_sites=False, verbose=False, fuzzy=True, samples=1,
        score_mode='ranked'):
    cpb = CoPaR(f, ref=ref, fuzzy=fuzzy, split_on_tones=False)
    all_scores = []
    all_samples = set()
    all_pscores = {d: [] for d in cpb.cols}
    all_pud = {d: [] for d in cpb.cols}
    all_words = {d: [] for d in cpb.cols}
    all_sounds = {d: [] for d in cpb.cols}
    for key, msa in cpb.msa[ref].items():
        for alm, t in zip(msa['alignment'], msa['taxa']):
            all_samples.add((key, ' '.join(alm), t))
   
    for run in range(runs):    
        remove_idxs = random.sample(all_samples, int(len(all_samples)*ratio +
            0.5))
        D = {0: cpb.columns}
        for idx, cogid, alm, tax in cpb.iter_rows(ref, 'alignment', 'doculect'):
            if fuzzy:
                cogids = []
                for c in cogid:
                    if (c, str(alm), tax) not in remove_idxs:
                        cogids += [c]
                if not cogids:
                    pass
                else:
                    D[idx] = cpb[idx]
                    D[idx][cpb.header[ref]] = ints(cogids)
            else:
                if (cogid, str(alm), tax) in remove_idxs:
                    pass
                else:
                    D[idx] = cpb[idx]
        
        cp = CoPaR(D, ref=ref, fuzzy=fuzzy, split_on_tones=False)
        if 'l' in argv: 
            cp.load_patterns()
        else:
            cp.get_sites(minrefs=2, structure='structure')
            if sort_sites:
                cp.sort_sites()
            #cp.greedy_color()
            cp.cluster_sites(score_mode=score_mode, iterations=2)
            cp.sites_to_pattern()
            if refine_patterns:
                cp.refine_patterns()

        # compute size of alphabets
        sounds = {d: defaultdict(int) for d in cp.cols}
        for idx, doc, tks in cp.iter_rows('doculect', 'segments'):
            for t in tks:
                if t != '+':
                    sounds[doc][t.split('/')[1] if '/' in t else t] += 1
        ave = sum([len(s) for s in sounds.values()]) / cp.width

        # good words
        our_sample = {}
        for cogid, alm, doc in remove_idxs:
            our_sample[cogid, doc] = strings(alm)
        pscores = {d: [] for d in cp.cols}
                
        predicted, purity, pudity = cp.predict_words(minrefs=2, samples=samples)
        scores = []
        unknown, all_segs = 0, 0
        for k, v in predicted.items():
            for doc in v:
                if (k, doc) in our_sample and (doc == subset or not subset):
                    # check for different alignments
                    msaA = cp.msa[ref][k]
                    msaB = cpb.msa[ref][k]
                    if len(msaA['alignment'][0]) != len(msaB['alignment'][0]):
                        # carve out the taxa which are still existent to find which
                        # column to delete
                        new_alm = [msaB['alignment'][i] for i in
                            range(len(msaB['alignment'])) if msaB['taxa'][i] in \
                                    msaA['taxa']]
                        almA, almB = [], []
                        for i in range(len(msaA['alignment'][0])):
                            almA += [tuple([line[i] for line in msaA['alignment']])]
                        for i in range(len(msaB['alignment'][0])):
                            almB += [tuple([line[i] for line in new_alm])]
                        out = []
                        for i, col in enumerate(almB):
                            if col not in almA:
                                out += [i]
                    else:
                        out = []
                    wA, wB = v[doc], our_sample[k, doc]
                    ms = 0
                    wB = strings([x for i, x in enumerate(wB) if i not in out]) 
                    for a, b in zip(wA, wB):
                        b = b.split('/')[1] if '/' in b else b
                        a = a.split('|')
                        for i, a_ in enumerate(a):
                            if b == a_:
                                ms += 1 * (1/(i+1))
                        if a[0] == 'Ø':
                            unknown += 1
                        all_segs += 1
        
                    score = ms / len(wA)
                    pscores[doc] += [score]
                    if verbose: 
                        print('{0:5}\t{1:15}\t{2:20}\t{3:20}\t{4:.2f}\t{5}'.format(
                            str(k), doc, str(wA), str(wB), score, len(set(msaA['taxa']))))
                    if verbose and score != 1.0:
                        purs = []
                        for i, elm in enumerate(wA):
                            if (k, i) in purity:
                                purs += ['{0:.2f}'.format(purity[k, i][doc])]
                            else:
                                purs += ['?']
                                print((cogid, i) in cp.sites)
                                print([_s for _s in cp.sites if _s[0] == cogid],
                                        cogid)
                        print('<---')
                        print('\t'.join([x for x in wA]))
                        print('\t'.join([x for x in wB]))
                        print('\t'.join(purs))
                        print('--->')
                    scores += [score]
        ubound = cp.upper_bound()
        all_scores += [(sum(scores) / len(scores), len(cp) / len(cpb),
            density(cp, ref=ref), cp.fuzziness(),
            cp.stats(score_mode=score_mode), 
            sum(pudity.values()) / len(pudity.values()), ave, unknown/all_segs,
            ubound, len(cp.clusters), len(cp.clusters) / ubound,
            len(cp.sites))
            ]
        if verbose:
            print('{0:.2f}'.format(all_scores[-1][0]))
        
        cov = cp.coverage()
        for p in pscores:
            all_pscores[p] += [sum(pscores[p]) / len(pscores[p])]
            all_pud[p] += [pudity[p]]
            all_words[p] += [cov[p]]
            all_sounds[p] += [len(sounds[p])]

    
    new_scores = [[
            'accuracy', 'proportion', 'density', 'fuzziness', 'coverage',
            'purity', 'sounds', 'missing', 'ubound', 'clusters', 'props',
            'patterns']]
    new_scores += [[
        round(sum([x[0] for x in all_scores]) / len(all_scores), 4),
        round(sum([x[1] for x in all_scores]) / len(all_scores), 4),
        round(sum([x[2] for x in all_scores]) / len(all_scores), 4),
        round(sum([x[3] for x in all_scores]) / len(all_scores), 4),
        round(sum([x[4] for x in all_scores]) / len(all_scores), 4),
        round(sum([x[5] for x in all_scores]) / len(all_scores), 4),
        round(sum([x[6] for x in all_scores]) / len(all_scores), 4),
        round(sum([x[7] for x in all_scores]) / len(all_scores), 4),
        round(sum([x[8] for x in all_scores]) / len(all_scores), 4),
        round(sum([x[9] for x in all_scores]) / len(all_scores), 4),
        round(sum([x[10] for x in all_scores]) / len(all_scores), 4),
        round(sum([x[11] for x in all_scores]) / len(all_scores), 4),


            ]]
    print(tabulate(new_scores, headers='firstrow'))
    
    table = [['doculect', 'accuracy', 'purity', 'sounds', 'words']]

    for doc in all_pscores:
        table += [[doc, 
            round(sum(all_pscores[doc]) / runs, 4),
            round(sum(all_pud[doc]) / runs, 4),
            round(sum(all_sounds[doc]) / runs, 4),
            round(sum(all_words[doc]) / runs, 4)
            ]]
    print('')
    print(tabulate(table, headers='firstrow'))

    accs = [x[1] for x in table[1:]]
    puds = [x[2] for x in table[1:]]
    p, r = spearmanr(accs, puds)
    print('')
    print('{0:.2f} p <= {1:.6f}'.format(p, r))

    return purity, pudity, sounds, cp

if __name__ == '__main__':
    from sys import argv

    # defaults
    f = argv[1]
    ref = 'crossids'
    ratio = 0.5
    proto = None
    verbose = False
    runs = 100
    rsites = False
    samples = 1
    score_mode='pairs'
    
    # parse arguments
    if '--refine' in argv:
        rsites = True
    if '-r' in argv:
        ratio = float(argv[argv.index('-r')+1])
    if '-p' in argv:
        proto = argv[argv.index('-p')+1]
    if '-c' in argv:
        ref = argv[argv.index('-c')+1]
    if '-v' in argv:
        verbose = True
    if '--runs' in argv:
        runs = int(argv[argv.index('--runs')+1])
    if ref in ['crossid', 'cogid']:
        fuzzy = False
    else:
        fuzzy = True
    if '--samples' in argv:
        samples = int(argv[argv.index('--samples')+1])
    if '--score' in argv:
        score_mode = argv[argv.index('--score')+1]
        
    p1, p2, p3, cop = run_experiments(f, ref, ratio, subset=proto, fuzzy=fuzzy, verbose=verbose,
            runs=runs, refine_patterns=rsites, sort_sites=False,
            samples=samples, score_mode=score_mode)
    