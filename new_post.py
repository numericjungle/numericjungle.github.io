import datetime 
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', help="get title", type=str, required=True)
    NS = parser.parse_args()
    template =\
"""---
date: {timestamp}
layout: post
title: {title}
description: "{title}"
tags: []
comments: true
---
<!--excerpt-->""".format(title = (NS.t).replace('-', ' ').replace('_', ' '), timestamp = datetime.datetime.now())
    print (template)
    filename = '_posts/' + datetime.datetime.today().strftime('%Y-%m-%d') + '-' + NS.t.lower() + '.md'
    print (filename)

    with open(filename, "a") as myfile:
        myfile.write(template)

    print ('a new draft:' + filename + ' is generated successfully.' )