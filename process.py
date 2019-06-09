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


class PhraseHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.phrase_stack = []
        self.document_id = None

    def startElement(self, tag, attributes):
        # print(tag, attributes)

        if tag == 'document':
            self.document_id = attributes['id']
            return

        if tag == 'phrase':
            self.phrase_stack.append(Phrase(attributes['id'], self.document_id))

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
            print('Finished phrase:', phrase.phrase_id, phrase.rendered)
            if self.phrase_stack:
                self.phrase_stack[-1].content.append(phrase)


def process(filename):
    print('Processing:', filename)
    # cheat sheet: https://www.tutorialspoint.com/python/python_xml_processing.htm
    handler = PhraseHandler()
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(handler)
    parser.parse(filename)


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
