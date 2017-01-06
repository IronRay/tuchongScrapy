# -*- coding: utf-8 -*-
import os

from bs4 import BeautifulSoup

import tuchongGet
from config import ABSDIR


class Photographer():
    """docstring for user"""

    def __init__(self, userID):
        self.userID = userID
        self.url = self.urlGenerator()
        self.albumIDs = []

    def urlGenerator(self):
        baseUrl = 'https://tuchong.com'

        url = baseUrl + '/' + str(self.userID)

        return url


class Photo():
    """docstring for Photo"""

    def __init__(self, albumID, photoUrl, photoName, albumPath):
        self.url = photoUrl
        self.albumID = ''
        self.name = ''
        self.path = self.PhotoPathGenerator(albumPath)

        self.PhotoInitlize()

    def PhotoInitlize(self):
        self.authorID = self.photoUrl.split('/')[-3]
        self.name = self.photoUrl.split('/')[-1]

    def PhotoPathGenerator(self, albumPath):
        path = os.path.join(albumPath, self.name)

        return path

    def save(self):
        if not os.path.isfile(self.path):
            picData = tuchongGet.getPicData(url=self.url).content

            print('< picPath: %s >' % self.path)

            with open(self.path, 'wb') as jpg:
                jpg.write(picData)


class Album():
    """docstring for Album"""

    def __init__(self, albumID, authorID):
        self.albumID = albumID
        self.authorID = authorID
        self.path = self.AlbumPathGenerator()
        self.albumContent = self.getAlbumContent()
        self.albumTitle = ''
        self.photos = []

    def AlbumPathGenerator(self):
        albumPath = os.path.join(ABSDIR, str(self.albumID))

        return albumPath

    def getAlbumContent(self):
        albumData = tuchongGet.getAlbumData(self.authorID, self.albumID)
        albumContent = BeautifulSoup(albumData.text, 'lxml')

        return albumContent

    def getAlbumInfo(self):

        self.albumTitle = self.albumContent.find('div', {'class': 'post-content'}).h1.string

        print('< Title: %s >' % self.albumTitle)

        for soup in self.albumContent.findAll('img', {'class': 'img-responsive'}):
            photoUrl = soup.get('src')
            photoName = photoUrl.split('/')[-1]

            photo = Photo(authorID=self.authorID, albumID=self.albumID, photoUrl=photoUrl, photoName=photoName, albumPath=self.path)

            self.photos.append(photo)

    def save(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

            for photo in self.photos:
                photo.save()
        else:
            for photo in self.photos:
                photo.save()


if __name__ == '__main__':
    # My class test case
    album = Album(albumID="13901840", authorID="990878")
    album.getAlbumInfo()
    album.save()
