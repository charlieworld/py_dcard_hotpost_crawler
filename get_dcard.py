#coding=UTF-8
import requests
from bs4 import BeautifulSoup
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
siteUrl = 'https://www.dcard.tw'
url = siteUrl + '/f'

# 檢查是否抓到東西
def none_check(item):
  if (item is None):
    return 'No Item'
  else:
    return item.getText()

# 找標題
def find_title(item):
  temp = item.find('h3', class_='PostEntry_title_H5o4d')
  return none_check(temp)

# 找版名
def find_forum(item):
  temp = item.find('span', class_='PostEntry_forum_1m8nJ')
  return none_check(temp)

# 找作者
def find_author(item):
  temp = item.find('span', class_='PostAuthor_root_3vAJf')
  return none_check(temp)

# 找連結 
def find_link(item):
  temp = item.find('a', class_='PostEntry_root_V6g0r')
  temp = temp.get('href')
  return temp

# 找圖片
def find_cover(item):
  temp = item.find('div', class_='PostEntry_image_1E6Mi')
  if (temp is None):
    return 'No Item'
  else:
    # 拿到有包含css的字串，所以我們要去掉CSS的部分，先切頭部，再切尾部
    temp = temp.get('style')
    temp = temp.split('background-image:url(',1)[1]
    temp = temp.split(')',1)[0]
    return temp


# 找文章內文
def find_content(item):
  temp = item.find('div', class_='PostEntry_excerpt_2eHlN')

  if (temp is None):
    #有時候格式會是引言
    temp = item.find('div', class_='PostEntry_reply_1oU-6')

  return none_check(temp)
  
# 按讚數
def find_like_count(item):
  temp = item.find('span', class_='Like_counter_1enlP')
  return none_check(temp)

# 留言數
def find_comment(item):
  temp = item.find('span', class_='PostEntry_comments_2iY8V')
 
  if (temp is None):
    return 'No Item'
  else:
    temp = temp.getText()
    # 字串長這樣 "33則回應"，所以我們要切斷字串
    temp = temp.split(u'則回應',1)[0]
    return temp
  

# #########################
# STEP 0. |主程式開始 拿取整個HTML + 找出每個貼文
# #########################
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
posts = soup.find_all('div', class_='PostList_entry_1rq5L')

#主資料
mainData = []

# #########################
# STEP 1. 從每一篇貼文中取出資料
# #########################
for item in posts:
  

  #建立結構化資料
  itemObj = {
    'title': find_title(item).encode('utf-8'),
    'forum': find_forum(item).encode('utf-8'),
    'author': find_author(item).encode('utf-8'),
    'link': siteUrl+find_link(item).encode('utf-8'),
    'cover': find_cover(item),
    'content': find_content(item).encode('utf-8'),
    'like': find_like_count(item),
    'comment': find_comment(item)
  }
  #加入到主資料中
  mainData.append(itemObj)


# #########################
# STEP 2. 資料儲存到CSV檔案
# #########################

with open('get_dcard.csv', 'w') as csvfile:
  #設定欄位名稱
  fieldnames = ['title','forum','author','link','cover','content','like','comment']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()

  for item in mainData:
    #逐行寫入
    print item
    writer.writerow(item)

print("Writing csv complete")