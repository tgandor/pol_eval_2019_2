import argparse
import glob
import os.path as p
import xml.sax

# external libs
import morfeusz

data_dir = p.join(p.dirname(__file__), '_data')


def process(filename):
    print('Processing:', filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?',
        default=data_dir + '/poleval2019_task2_training_190221/',
        help='file or directory to process')
    args = parser.parse_args()

    if p.isdir(args.input):
        print('isdir', args.input)
        for filename in glob.glob(p.join(args.input, '*.xml')):
            process(filename)
    elif p.isfile(args.input):
        process(args.input)
    else:
        print('Invalid input: {}'.format(args.input))
        exit(1)


if __name__ == '__main__':
    main()
