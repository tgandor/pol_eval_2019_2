# pol_eval_2019_2
A simple approach to PolEval 2019 task 2: Lemmatization of proper names and multi-word phrases

Task page:

http://poleval.pl/tasks/task2

(Caution: they may change it later to something like 2019.poleval.pl/.../)

Quoting contest page:

## Task definition

The task consists in developing a tool for lemmatization of proper names and multi-word phrases. The generated lemmas should follow the KPWr guidelines.
(http://poleval.pl/task2/KPWr_guidelines.pdf)


## Evaluation procedure

The goal is to generate a single TSV file. The file should contain a line for each inline annotation in the test dataset. In the evaluation the annotations will be the value of lemma (4th column in the TSV file) in two variant: case sensitive comparison (AccCS) and case insensitive evaluation (AccCI).

Acc = POS/N

Score = 0.2 * AccCS + 0.8 * AccCI

(end quote)

# Solution details

Morphological analysis done with Morfeusz2: http://sgjp.pl/morfeusz/dopobrania.html

(License: http://sgjp.pl/morfeusz/warunki.html)

