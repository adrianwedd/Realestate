#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 19:25:15 2019

@author: michaelboles
"""

# set up working directory
import os
#os.chdir('/Users/michaelboles/Michael/Coding/2019/Realestate/Data/ABB/Data/San Francisco') # Mac
os.chdir('C:\\Users\\bolesmi\\Lam\\Coding\\Python\\2019\\Realestate\\Data\ABB') # PC

# import packages
import pandas as pd

# import SF listings and calendar datasets 
listings_raw = pd.read_csv('.\Data\San_Francisco\listings_2.csv')
calendar_raw = pd.read_csv('.\Data\San_Francisco\calendar_1.csv')

# get column names 
listings_colnames = list(listings_raw)
calendar_colnames = list(calendar_raw)

# get columns of interest: 
    
listings_1 = listings_raw[['id', 'name', 'host_name',
                         'neighbourhood', 'latitude', 'longitude',
                         'bedrooms', 'bathrooms', 'square_feet', 
                         'property_type', 'room_type',
                         'guests_included', 'extra_people', 'minimum_nights',
                         'availability_30', 'availability_90', 'availability_365',
                         'number_of_reviews', 'review_scores_rating', 'last_review', 
                         'reviews_per_month',
                         'price', 'cleaning_fee', 'security_deposit']].copy()

# CLEAN DATA

# convert prices from string '$__' to float
listings_1[['extra_people','price','cleaning_fee','security_deposit']] = listings_1[['extra_people','price','cleaning_fee','security_deposit']].replace('[\$,]', '', regex=True).astype(float)

## convert 'last review' column from string to date time
#listings_1['last_review'] = pd.to_datetime(listings_1['last_review'])

# remove outliers: > 5 beds, > 4 baths, > $1000/night
listings_2 = listings_1[(listings_1['bedrooms'] < 5) & (listings_1['bathrooms'] < 4) & (listings_1['bathrooms'] < 4) & (listings_1['price'] < 1000)]

# exclude hotels, listings with zero bookings
listings_3 = listings_2[(listings_2['property_type'] != 'Hotel') & (listings_2['number_of_reviews'] != 0)]

# CREATE REVENUE ESTIMATE

# assume 50% of bookings result in a review and average booking is 5.5 nights
# revenue/month = (reviews/month)*(2 bookings/review)*(5.5 nights/booking)*(nightly price)

listings_4 = listings_3
listings_4['monthly_revenue'] = 11*listings_3['reviews_per_month']*listings_3['price'] 

# visualize key metrics
import matplotlib.pyplot as plt
import seaborn as sns

def corrfunc(x, y, **kws):
    r = x.corr(y)
    ax = plt.gca()
    ax.annotate(r'$R^{2}$ = ' + str(round(r, 2)), xy=(.1, .9), xycoords=ax.transAxes, backgroundcolor = 'white')

g = sns.pairplot(listings_4, diag_kind = 'kde', kind = 'reg',
             plot_kws=dict(line_kws=dict(color = '#3148a3'), 
                           scatter_kws=dict(facecolor = '#5797ff', edgecolor = '#3148a3', 
                                            linewidth = 0.33, alpha = 0.1, s = 20)),
             x_vars = ['bedrooms', 'bathrooms', 'price', 'number_of_reviews', 'reviews_per_month', 'monthly_revenue'], 
             y_vars = ['bedrooms', 'bathrooms', 'price', 'number_of_reviews', 'reviews_per_month', 'monthly_revenue'])
g.map_lower(corrfunc)
g.savefig('.\Images\pairplot_3.jpg', dpi=600)







