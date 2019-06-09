import os
import os.path as p
import shutil
import tarfile
import zipfile

# external libs
import requests

data_dir = p.join(p.dirname(__file__), '_data')

if not p.exists(data_dir):
    os.makedirs(data_dir)


def download(url):
    """Retrieve a file from the Web, return local path."""

    filename = p.basename(url)
    cache_file = p.join(data_dir, filename)

    if not p.exists(cache_file):
        print('Retrieving: {}'.format(url))
        with requests.get(url, stream=True) as r:
            with open(cache_file, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    return cache_file


def test_morfeusz():
    try:
        import morfeusz
        print(morfeusz.about())
    except ImportError:
        print('Missing morfeusz library, please run:')
        print('pip install python-morfeusz')
        print('or')
        print('pip install -r requirements.txt')
    except OSError:
        print('Probably missing: libmorfeusz.so.0, or cannot load')
        if p.exists('libmorfeusz.so.0'):
            print('The file is there. You need library path:')
            print('$ source so_path.source_me.sh')
            print('Current path:', os.environ.get('LD_LIBRARY_PATH', '(not set)'))
    else:
        print('morfeusz module loaded succesfully.')


def main():
    # Contest data

    training_url = 'http://poleval.pl/task2/poleval2019_task2_training_190221.tar.gz'

    train = download(training_url)
    print('Unpacking: {}'.format(train))
    with tarfile.open(train) as tf:
        tf.extractall(data_dir)

    test_url = 'http://poleval.pl/task2/poleval2019_task2_test_second_190517.zip'
    test = download(test_url)
    print('Unpacking: {}'.format(test))
    with zipfile.ZipFile(test) as zf:
        zf.extractall(data_dir)

    # morfeusz morphological analyzer
    morph_url = 'http://sgjp.pl/morfeusz/download/20190602/ubuntu-bionic/morfeusz2-1.9.10.sgjp.20190602-Linux-amd64.tar.gz'
    so_file = 'morfeusz2-1.9.10.sgjp.20190602-Linux-amd64/lib/libmorfeusz2.so'
    morph = download(morph_url)
    with tarfile.open(morph) as tf:
        tf.extract(so_file)
    shutil.move(so_file, 'libmorfeusz.so.0')
    shutil.rmtree('morfeusz2-1.9.10.sgjp.20190602-Linux-amd64/')
    # this seems not to work:
    # print('Setting library path')
    # os.environ['LD_LIBRARY_PATH'] = p.abspath('.')
    test_morfeusz()

if __name__ == '__main__':
    main()
