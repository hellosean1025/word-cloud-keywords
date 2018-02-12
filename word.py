# encoding=utf-8
import jieba
import re
import os
import json

def getFileContent(filepath):
  fs = open(filepath, 'r', encoding='UTF-8')
  content = fs.read()
  fs.close()
  return content

def handlePunctuation(temp):
  str = re.sub("[　\\s+\\.\\!\\/_,$%^*(+\"\']+|[+——！“”，。？、~@#￥%……&*（）]+", "",temp)  
  return str

def getKeywords(content, words):
  keys = jieba.lcut(content)
  for word in keys:
    word = handlePunctuation(word)
    word = word.strip()
    if len(word) < 2:
      continue
    words[word] = words[word] + 1 if word in words else 1

def quick_sort(nums):
    def qsort(lst, begin, end):
        if begin >= end:
            return
        i = begin
        key = lst[begin]
        for j in range(begin+1, end+1):
            if lst[j] < key:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
        lst[begin], lst[i] = lst[i], lst[begin]
        qsort(lst, begin, i-1)
        qsort(lst,i+1,end)
    qsort(nums, 0, len(nums)-1)

def sordKeywords(words, limit):
  group = {}
  newWords = []
  for word in words:
    val = words[word]
    if val in group:
      group[val].append(word)
    else:
      group[val] = [word]
  vals = list(group.keys())
  quick_sort(vals)
  vals = list(reversed(vals))

  i= 0
  isBreak = False
  for val in vals:
    if isBreak: break
    for item in group[val]:
      if i >= limit: 
        isBreak = True
        break
      newWords.append({
        'name': item,
        'value': val
      })
      i += 1
  return newWords

def run(dirpath, limit=200):
  words = word2keywords(dirpath, limit)
  fs = open('./result/keywords.txt', 'w',encoding='UTF-8')
  fs2 = open('./result/keywords.json', 'w',encoding='UTF-8')
  fs2.write(json.dumps(words, indent=2))
  for word in words:
    fs.write( str(word['value']) + ' ' + word['name'] + "\n")
  fs.close()
  fs2.close()

def word2keywords(dirpath, limit=200):
  WORDS = {}
  files= os.listdir(dirpath)
  for file in files: 
     if not os.path.isdir(file): 
        getKeywords(getFileContent(dirpath + "/" + file), WORDS)
  return sordKeywords(WORDS, limit)
