# #-*- coding: utf-8 -*-
from datetime import datetime
import json

def fetch_all_json(result):
  lis = []

  for row in result.fetchall():
    i =0
    dic = {}  
    
    for data in row:
      if type(data) == datetime:
        dic[result.keys()[i]]= str(data)
      else:
        dic[result.keys()[i]]= data
      if i == len(row)-1:
        lis.append(dic)

      i=i+1
  return lis