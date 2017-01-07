# -*- coding: utf-8 -*-
import random
import requests

from config import TUCHONGGetConfig


USER_AGENTS = TUCHONGGetConfig['USER_AGENTS']


def getAlbumData(userID, albumID):
    HEADER = {
        'User-Agent': random.choice(USER_AGENTS),
    }

    headers = HEADER

    baseUrl = 'https://tuchong.com/'

    url = baseUrl + str(userID) + '/' + str(albumID)

    response = requests.get(url=url, headers=headers, timeout=10)
    # print(response.status_code)

    return response


def get(url, params=''):
    HEADER = {
        'User-Agent': random.choice(USER_AGENTS),
    }

    headers = HEADER

    response = requests.get(url=url, headers=headers, params=params, timeout=10)

    return response


if __name__ == '__main__':
    response = getAlbumData(990878, 13901840)
    print(response.status_code)
