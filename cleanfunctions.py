# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:31:27 2019

@author: BolesMi
"""

# DEFINE DATA CLEANING FUNCTIONS 
import re


# cleaning address: pull out text segment that starts with digits, 
# consists of 1, 2, or 3 words separated by spaces, and ends with comma
# 

def address_clean(address_raw):
    address_temp = list(map(lambda m: tuple(filter(bool, m)), 
                   re.findall(r'(\d+\s\w+),|(\d+\s\w+\s\w+),|(\d+\s\w+\s\w+\s\w+),|\'(\w+\s\w+),|\'(\d+\s\w+)\\.,',str(address_raw))))
    address = [i[0] for i in address_temp]
    return address

def city_clean(address_raw):
    city_temp = list(map(lambda m: tuple(filter(bool, m)),re.findall(r',\s(\w+), CA|,\s(\w+\s\w+), CA|,\s(–), CA',str(address_raw))))
    city = [i[0] for i in city_temp]
    return city

# need to remove whitespace, extra text, and convert slashes from baths
def baths_clean(baths_raw):
    baths_temp1 = list(map(lambda m: tuple(filter(bool, m)), re.findall(r'(\d+/+\d+)|(\d+)',str(baths_raw))))
    baths_temp2 =  [i[0] for i in baths_temp1]
    baths_temp3 = [re.sub('/1','.5', i) for i in baths_temp2]
    baths_temp4 = []
    for i in baths_temp3:
        if i[-2:] == '/2':
            baths_temp4.append(str(int(i[0])+1))
        elif i[-2:] == '/3':
            baths_temp4.append(str(int(i[0])+1.5))
        elif i[-2:] == '/4':
            baths_temp4.append(str(int(i[0])+2))        
        elif i[-2:] == '/5':
            baths_temp4.append(str(int(i[0])+2.5))
        else:
            baths_temp4.append(i)
    baths = list(map(float, baths_temp4))
    return baths


def sqft2acre(lotinsqft):
    return round(lotinsqft/43560,3)

# need to remove extra text, whitespace, and convert sqft values to acres
def lot_clean(lot_raw):
    lot_temp1 = list(map(lambda m: tuple(filter(bool, m)), re.findall(r'(\d+\,\d\d\d)|(\d\.\d+)|(\d+)', str(lot_raw))))
    lot_temp2 = [i[0] for i in lot_temp1]
    lot_temp3 = [re.sub(',','',i) for i in lot_temp2]
    lot_temp4 = [float(i) for i in lot_temp3]
    lot = []
    for i in lot_temp4:
        if i > 10:      # assume if lot size is > 10 units are sqft not acres
            lot.append(sqft2acre(i))
        else:
            lot.append(i)
    return lot