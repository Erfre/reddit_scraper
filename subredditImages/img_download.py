from bs4 import BeautifulSoup
import os
from urllib.error import HTTPError
from urllib.request import urlopen
from urllib.request import urlretrieve
from PIL import Image
from io import BytesIO

class img_url_handler(object):
    """docstring for img_url_handler."""

    def __init__(self, subreddit, path):
        """Initilize."""
        super(img_url_handler, self).__init__()
        self.subreddit = subreddit
        self.path = path
        self.save_path = self.path + self.subreddit + 'IMG'
        self.img_url = []

    def download(self, url, user):
        """Download image to path.

        Downloads all images in img_url or just the img in url.
        And saves them into path/subreddit/user/(number).jpg
        """
        full_file_path = os.path.join(self.save_path, user + '/')

        if not os.path.exists(full_file_path):
            os.makedirs(full_file_path)

        self.album_check(url)

        if self.img_url:
            for count, img in enumerate(self.img_url):
                erCheck = self.save_img(img, full_file_path, str(count))
            return full_file_path, count, erCheck
        else:
            erCheck = self.save_img(url, full_file_path, '0')
            return full_file_path, 0, erCheck


    def save_img(self, url, path, img_name):
        """Save file on computer"""
        pic = (path+img_name)
        print(url)
        try:
            urlretrieve(url, pic)
            formatEr = self.convert_jpg(pic)
            return formatEr
        except HTTPError:
            print('Url is forbidden.')

        return False

    def convert_jpg(self, path):
        """Convert image to jpeg and weed out incorrect format"""
        try:
            im = Image.open(path)
            rgb_im = im.convert('RGB')
            rgb_im.save(path, 'JPEG')
            return True
        except OSError:
            print('Cannot identify file format.\nMoving on...\n')
            return False

    def album_check(self, url):
        """Fetching all the images from the link."""
        self.img_url = []
        album_urls = ['/a/', '/gallery']

        for album in album_urls:
            if url.find(album) != -1:
                html = urlopen(url)
                soup = BeautifulSoup(html, "lxml")
                for a in soup.find_all(
                        'a', {'class': 'zoom'}):
                    img = a.find('img')  # Finds the img inside of the div
                    self.img_url.append('https:' + img['src'])

                print(self.img_url)
                return self.img_url
        return False
