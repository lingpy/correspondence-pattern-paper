all: r25 r75 r50

r75:
	@python test_prediction.py data/burmish-240-8.tsv -r 0.75 --runs 1000
	@python test_prediction.py data/chinese-623-14.tsv -r 0.75 --runs 1000
	@python test_prediction.py data/polynesian-210-10.tsv -r 0.75 --runs 1000
	@python test_prediction.py data/japanese-200-10.tsv -c crossid -r 0.75 --runs 1000
r25:
	@python test_prediction.py data/burmish-240-8.tsv -r 0.25 --runs 1000
	@python test_prediction.py data/chinese-623-14.tsv -r 0.25 --runs 1000
	@python test_prediction.py data/polynesian-210-10.tsv -r 0.25 --runs 1000
	@python test_prediction.py data/japanese-200-10.tsv -c crossid -r 0.25 --runs 1000

r50:
	@python test_prediction.py data/burmish-240-8.tsv -r 0.5 --runs 1000
	@python test_prediction.py data/chinese-623-14.tsv -r 0.5 --runs 1000
	@python test_prediction.py data/polynesian-210-10.tsv -r 0.5 --runs 1000
	@python test_prediction.py data/japanese-200-10.tsv -c crossid -r 0.5 --runs 1000


