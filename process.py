from __future__ import print_function

import argparse
import glob
import os.path as p
import xml.sax

# external libs
import attr
import morfeusz

data_dir = p.join(p.dirname(__file__), '_data')


def render(content):
    if type(content) is str:
        return content

    return content.rendered

@attr.s
class Phrase(object):
    phrase_id = attr.ib()
    document_id = attr.ib()
    content = attr.ib(factory=list)
    lemma = attr.ib(default='')

    @property
    def rendered(self):
        return ' '.join(
            render(content) for content in self.content
        )

    def as_tsv(self):
        return '\t'.join([self.phrase_id, self.document_id, self.rendered, self.lemma or self.rendered])


class PhraseHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.phrase_stack = []
        self.document_id = None
        # for preorder ordering and retrieval by phrase_id
        self.phrase_ids = []
        self.phrase_dict = {}

    def startElement(self, tag, attributes):
        # print(tag, attributes)

        if tag == 'document':
            self.document_id = attributes['id']
            return

        if tag == 'phrase':
            # actually this whole preordering is overkill, because index.tsv
            # turned out to not be sorted anyway (just as the phrase_id's behave randomly)
            # it looks more like level-order (i.e. "BFS order").
            # I will generate it in preorder; then there will need to be a script
            # to compare it to GT (evaluate.py).
            # Read more about orders: https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/
            new_phrase = Phrase(attributes['id'], self.document_id)
            self.phrase_ids.append(new_phrase.phrase_id)
            self.phrase_stack.append(new_phrase)
            self.phrase_dict[new_phrase.phrase_id] = new_phrase

    def characters(self, content):
        if not self.phrase_stack:
            # print('Outside any phrase:', content)
            return

        content = content.strip()

        if not content:
            # print('Empty content')
            return

        self.phrase_stack[-1].content.append(content.strip())

    def endElement(self, tag):
        if tag == 'phrase':
            assert self.phrase_stack
            phrase = self.phrase_stack.pop()
            # print('Finished phrase:', phrase.phrase_id, phrase.rendered)
            if self.phrase_stack:
                self.phrase_stack[-1].content.append(phrase)

    # phrase iteration in pre-order (opening, not closing order)

    def __len__(self):
        return len(self.phrase_ids)

    def __getitem__(self, idx):
        return self.phrase_dict[self.phrase_ids[idx]]


def process(filename):
    # print('Processing:', filename)
    # cheat sheet: https://www.tutorialspoint.com/python/python_xml_processing.htm
    handler = PhraseHandler()
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(handler)
    parser.parse(filename)

    # right now it will to to stdout, redirect to a file if needed
    for phrase in handler:
        print(phrase.as_tsv())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?',
        default=data_dir + '/poleval2019_task2_training_190221/',
        help='file or directory to process')
    args = parser.parse_args()

    if p.isdir(args.input):
        # print('isdir', args.input)
        for filename in glob.glob(p.join(args.input, '*.xml')):
            process(filename)
    elif p.isfile(args.input):
        process(args.input)
    else:
        print('Invalid input: {}'.format(args.input))
        exit(1)


if __name__ == '__main__':
    main()
