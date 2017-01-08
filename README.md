# 针对图虫的爬虫练习项目

## 项目概要
V0.1: 抓取某标签下所有的图片并保存到本地
V0.1.1: 抓取某作者的所有图片并保存到本地

下一版本，提升抓取速度。

## 涉及包
1.BeautifulSoup

2.requests

## 摘要


## 使用方式
1.安装需要使用的包

```
pip install requests
pip install beautifulsoup
```



2.抓取某作者的所有图片

```
import author

author = Author(id="Author's ID")
author.getAllAlbumIDs()

for album in author.albumIDs:
	album.getAlbumInfo()
	album.save()
```



3.抓取某标签的所有图片

```
import author

tag = Tag(name="Tag's name")
tag.getTagContents()
```