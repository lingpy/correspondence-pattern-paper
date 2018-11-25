# Data and code accompanying the paper "Automatic Inference of Sound Correspondence Patterns Across Multiple Languages"

This code makes use of LingRex, the code needed for the automatic inference of sound correspondence patterns as described in the paper:

> List, Johann-Mattis (forthcoming): Automatic inference of sound corresponndence patterns across multiple languages. *Computational Linguistics*. Preprint available at [biorxiv](https://doi.org/10.1101/434621). 

When using this package or code in your research, please make sure to quote the paper accordingly, and quot ethe software package as follows:

> List, Johann-Mattis (2018): LingRex: Linguistic reconstruction with LingPy. Version 0.1.1. Jena: Max Planck Institute for the Science of Human History.

## Requirements

To install all the requirements, make sure to have a fresh Python3 installation. Download the repository, `cd` into it, and type:

```shell
$ pip install -r pip-requirements.txt
```

## Running the experiments

To run all experiments, simply type:

```shell
$ make all
```

To run specific experiments, type:

```shell
$ make [general, r25, r50, r75]
```

## Results

The results for the test runs with 1000 trials each are given in the folder `results/`. 

The additional samples discussed in the paper can also be found in this folder.

