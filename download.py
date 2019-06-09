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


if __name__ == '__main__':
    main()
