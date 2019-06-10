from __future__ import print_function
from __future__ import division

import argparse
import os.path as p

# External
import attr

data_dir = p.join(p.dirname(__file__), '_data')


@attr.s
class Phrase(object):
    phrase_id = attr.ib()
    document_id = attr.ib()
    original = attr.ib()
    lemma = attr.ib()


def parse_index(filename):
    print('Loading', filename)
    result = {}
    with open(filename) as fn:
        for i, line in enumerate(fn):
            row = line.strip().split('\t')
            # print(i, row)
            key = tuple(row[:2])
            phrase = Phrase(*row)
            result[key] = phrase
    return result


def save_pairs(filename, pairs):
    with open(filename, 'w') as f:
            for pred, act in pairs:
                f.write('\t'.join([pred.phrase_id, pred.document_id, pred.original, pred.lemma, act.lemma]) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='')
    parser.add_argument('--ground-truth', '-gt',
        default=data_dir + '/poleval2019_task2_training_190221/index.tsv',
        help='index TSV file with the Ground Truth')
    parser.add_argument('--save', '-s', action='store_true', help='save wrong.tsv and wrong_case.tsv')
    parser.add_argument('--plot', '-p', action='store_true', help='show pie chart of results')
    args = parser.parse_args()

    predicted = parse_index(args.input)
    actual = parse_index(args.ground_truth)

    assert set(predicted.keys()) <= set(actual.keys())
    assert len(predicted) > 0

    N = len(predicted)
    tp_cs = tp_ci = 0
    wrong = []
    wrong_case = []
    correct = []
    skipped = 0

    for key, phrase in predicted.items():
        gt_phrase = actual[key]
        if phrase.original != gt_phrase.original:
            skipped += 1
            print('Original mismatch', skipped)
            print('Pr:', phrase)
            print('GT:', gt_phrase)
            print('---')
            continue
            # this is too radical for now: too many mismatches
            # exit(1)

        if phrase.lemma.lower() == gt_phrase.lemma.lower():
            tp_ci += 1
        else:
            wrong.append((phrase, gt_phrase))
            continue

        if phrase.lemma == gt_phrase.lemma:
            tp_cs += 1
            correct.append((phrase, gt_phrase))
        else:
            wrong_case.append((phrase, gt_phrase))

    N -= skipped
    acc_cs = tp_cs / N
    acc_ci = tp_ci / N

    acc = 0.2 * acc_cs + 0.8 * acc_ci

    print('CS: {}/{} = {:.3f}'.format(tp_cs, N, acc_cs))
    print('CI: {}/{} = {:.3f}'.format(tp_ci, N, acc_ci))
    print('Score: {:.3f}'.format(acc))

    if args.save:
        save_pairs('correct.tsv', correct)
        save_pairs('wrong.tsv', wrong)
        save_pairs('wrong_case.tsv', wrong_case)

    if args.plot:
        import matplotlib.pyplot as plt
        plt.pie(
            [N - tp_ci, tp_ci - tp_cs, tp_cs],
            labels=['wrong', 'bad case', 'perfect'],
            colors=['red', 'orange', 'green']
        )
        plt.show()


if __name__ == '__main__':
    main()