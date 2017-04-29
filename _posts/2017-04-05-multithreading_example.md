---
date: 2017-04-05 00:17:23.190879
layout: post
title: A multithreading example in Python
description: "multithreading_example"
tags: [python, code]
comments: true
---

This is a simple example demonstrating how to run a Python script with different inputs in parallel and merge the results. Here an application is to get aggregation statistics in different dates through computationally intense queries, and merge across all dates.

{% highlight python %}

from multiprocessing import Process
import pandas as pd 
import os

def get_days(start, num_of_days):
    ''' generate a list of dates starting from the starting date
    to the starting date + num_of_days
    '''
    date_range = pd.date_range(start, periods=num_of_days, freq='1D')
    return map(lambda dt: dt.strftime("%Y-%m-%d"), date_range)

f = lambda x: os.system("python foo.py --date %s" % x)

children = []
for date in get_days(start, end):
    p = Process(target=f, args=(date,))
    p.start()
    children.append(p)

for x in children:
    x.join()
  
# merge results
all_df = (pd.read_csv(filename) for filename in glob.glob("*.csv"))
merge = pd.concat(all_df, ignore_index = True)
    
{% endhighlight %}
