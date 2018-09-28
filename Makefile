all: r25 r75 r50 general summarize

general:
	@python general.py

summarize:
	@python summarize.py

r75:
	@python predict.py data/burmish-240-8.tsv -r 0.75 --runs 1000
	@python predict.py data/chinese-623-14.tsv -r 0.75 --runs 1000
	@python predict.py data/polynesian-210-10.tsv -r 0.75 --runs 1000
	@python predict.py data/japanese-200-10.tsv -c crossid -r 0.75 --runs 1000
r25:
	@python predict.py data/burmish-240-8.tsv -r 0.25 --runs 1000
	@python predict.py data/chinese-623-14.tsv -r 0.25 --runs 1000
	@python predict.py data/polynesian-210-10.tsv -r 0.25 --runs 1000
	@python predict.py data/japanese-200-10.tsv -c crossid -r 0.25 --runs 1000

r50:
	@python predict.py data/burmish-240-8.tsv -r 0.5 --runs 1000
	@python predict.py data/chinese-623-14.tsv -r 0.5 --runs 1000
	@python predict.py data/polynesian-210-10.tsv -r 0.5 --runs 1000
	@python predict.py data/japanese-200-10.tsv -c crossid -r 0.5 --runs 1000


