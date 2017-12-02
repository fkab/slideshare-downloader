import os
import img2pdf

from os import walk
from os.path import join
import shutil
from builtins import input

from urllib.request import urlopen
from bs4 import BeautifulSoup

DOWNLOAD_DIR = 'pdf_images'
CURRENT = os.path.dirname(__file__)


def main():
    try:
        os.mkdir(DOWNLOAD_DIR)
        url = input('Slideshare URL : ')
        download_presentation(url)
        shutil.rmtree(DOWNLOAD_DIR)
    except Exception:
        shutil.rmtree(DOWNLOAD_DIR)
        raise Exception('Something went wrong :(!')


def download_presentation(slideshare_url):
    download_images(slideshare_url)
    convert_downloaded_images()


def download_images(slideshare_url):
    html = urlopen(slideshare_url).read()
    soup = BeautifulSoup(html)
    images = soup.findAll('img', {'class': 'slide_image'})

    for index, image in enumerate(images):
        image_url = image.get('data-full').split('?')[0]
        command = 'wget --no-check-certificate --output-document %s %s' \
                  % (join(DOWNLOAD_DIR, '{0:07b}'.format(index)), image_url)
        os.system(command)


def convert_downloaded_images():
    f = []
    for (dirpath, dirnames, filenames) in walk(join(CURRENT, DOWNLOAD_DIR)):
        f.extend(filenames)
        break

    f = ["%s/%s" % (DOWNLOAD_DIR, x) for x in f]

    pdf_bytes = img2pdf.convert(f, dpi=300, x=None, y=None)
    doc = open('result.pdf', 'wb')
    doc.write(pdf_bytes)
    doc.close()


if __name__ == "__main__":
    main()
