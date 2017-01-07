# -*- coding: utf-8 -*-
import os
import time
import json

from bs4 import BeautifulSoup

import tuchongGet
from config import ABSDIR


class Author():
    """docstring for user"""

    def __init__(self, id):
        self.id = id
        self.url = self.urlGenerator()
        self.albumIDs = []

    def urlGenerator(self):
        baseUrl = 'https://tuchong.com'

        url = baseUrl + '/' + str(self.id)

        return url

    def getAuthorContent(self):
        authorData = tuchongGet.get(url=self.url)
        authorContent = BeautifulSoup(authorData.text, 'lxml')

        return authorContent

    def getAuthorAlbumIDsByJson(self, year, month, day, limit=20):
        baseUrl = 'https://tuchong.com/rest/sites/'
        params = {
            'limit': limit
        }

        url = baseUrl + self.id + '/posts/' + str(year) + '-' + str(month) + '-' + str(day)

        authorData = tuchongGet.get(url=url, params=params)
        dataDict = json.loads(authorData.text)

        if dataDict['posts']:
            for post in dataDict['posts']:
                self.albumIDs.append(post['post_id'])

            nextYear = dataDict['posts'][-1]['published_at'].split('-')[0]
            nextMonth = dataDict['posts'][-1]['published_at'].split('-')[1]
            nextDay = dataDict['posts'][-1]['published_at'].split('-')[2]

            nextJson = {
                'year': nextYear,
                'month': nextMonth,
                'day': nextDay,
                'status': 1
            }

            return nextJson
        else:
            nextJson = {
                'year': 0,
                'month': 0,
                'nextday': 0,
                'status': 0
            }

            return nextJson

    def getAuthorAlbumIDsByPageContent(self, year, month):
        baseUrl = self.url
        url = baseUrl + '/' + 'posts/' + str(year) + '-' + str(month)

        authorData = tuchongGet.get(url=url)
        authorContent = BeautifulSoup(authorData.text, 'lxml')

        soups = authorContent.findAll('div', {'class': 'post-collage'})

        if soups:
            for soup in soups:
                self.albumIDs.append(soup.get('data-post-id'))

            return 1
        else:
            return 0

    def getAllAlbumIDs(self, mode='json'):
        now = time.localtime()
        year = now.tm_year
        month = now.tm_mon
        day = now.tm_mday

        if mode == 'json':
            while 1:
                nextJson = self.getAuthorAlbumIDsByJson(year=year, month=month, day=day, limit=50)

                print(nextJson)

                if nextJson['status']:
                    year = nextJson['year']
                    month = nextJson['month']
                    day = nextJson['day']
                else:
                    break

        else:
            pass

    def saveAlbums(self):
        for albumID in self.albumIDs:
            album = Album(id=albumID, authorID=self.id)
            album.getAlbumInfo()
            album.save()


class Tag():
    """docstring for Tag"""

    def __init__(self, name):
        self.name = name
        self.url = self.TagUrlGenerator()
        self.tageContents = []

    def TagUrlGenerator(self):
        baseUrl = 'https://tuchong.com/tags/'
        url = baseUrl + self.name

        return url

    def getTagContents(self):
        nextPageNum = '1'

        while nextPageNum:
            tagContent = self.getTagContent(pageNum=nextPageNum)
            nextPageNum = self.getNextPageNum(tagContent)

            soups = tagContent.findAll('a', {'class': ' theatre-view'})

            for soup in soups:
                authorID = soup.get('data-site-id')
                albumID = soup.get('href').split('/')[-2]

                # print('< authorID: %s >' % authorID)
                # print('< albumID: %s >' % albumID)

                album = Album(id=albumID, authorID=authorID)
                album.getAlbumInfo()
                album.save()

    def getTagContent(self, order='weekly', pageNum='1'):
        params = {
            'order': order,
            'page': pageNum
        }

        tagData = tuchongGet.get(url=self.url, params=params)
        tagContent = BeautifulSoup(tagData.text, 'lxml')

        return tagContent

    def getNextPageNum(self, tagContent):
        soup = tagContent.find('a', {'class': 'next'})
        if soup:
            nextUrl = soup.get('href')
            nextPageNum = nextUrl.split('=')[-1]
        else:
            return 0

        return nextPageNum


class Album():
    """docstring for Album"""

    def __init__(self, id, authorID):
        # self.url = url
        self.id = id
        self.authorID = authorID
        self.path = self.AlbumPathGenerator()
        self.content = self.getAlbumContent()
        self.title = ''
        self.photos = []

    def AlbumPathGenerator(self):
        albumPath = os.path.join(ABSDIR, str(self.id))

        return albumPath

    def getAlbumContent(self):
        albumData = tuchongGet.getAlbumData(self.authorID, self.id)
        albumContent = BeautifulSoup(albumData.text, 'lxml')

        return albumContent

    def getAlbumInfo(self):
        div = self.content.find('div', {'class': 'post-content'})

        if div:
            if div.h1:
                self.title = div.h1.string
            else:
                self.title = ''
        else:
            h1 = self.content.find('h1', {'class': 'post-title'})

            if h1:
                self.title = h1.string
            else:
                self.title = ''

        print('< Title: %s >' % self.title)

        for soup in self.content.findAll('img', {'class': 'img-responsive'}):
            photoUrl = soup.get('src')

            photo = Photo(url=photoUrl, albumID=self.id, albumPath=self.path)

            self.photos.append(photo)

    def save(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

            for photo in self.photos:
                photo.save()
        else:
            for photo in self.photos:
                photo.save()


class Photo():
    """docstring for Photo"""

    def __init__(self, url, albumID, albumPath):
        self.url = url
        self.albumID = albumID
        # self.id = ''
        self.name = self.PhotoNameGenerator()
        self.path = self.PhotoPathGenerator(albumPath=albumPath)

    # def PhotoInitlize(self):
    #     self.id = self.url.split('/')[-1].split('.')[0]
    #     self.name = self.url.split('/')[-1]

    def PhotoNameGenerator(self):
        photoName = self.url.split('/')[-1]

        return photoName

    def PhotoPathGenerator(self, albumPath):
        photoPath = os.path.join(albumPath, self.name)

        return photoPath

    def save(self):
        if not os.path.isfile(self.path):
            photoData = tuchongGet.get(url=self.url).content

            # print('< picPath: %s >' % self.path)

            with open(self.path, 'wb') as jpg:
                jpg.write(photoData)


if __name__ == '__main__':
    # My class test case
    author = Author(id='')
    author.getAllAlbumIDs()
    author.saveAlbums()
    # status = author.getAuthorAlbumIDsByMonth(year='2016', month='05')
    # print(status)

    # album = Album(id="", authorID="")
    # album.getAlbumInfo()
    # album.save()
    # tag = Tag(name="")
    # tag.getTagContents()
