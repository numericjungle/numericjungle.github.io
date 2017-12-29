---
date: 2016-07-27 00:10:59.442103
layout: post
title: NYC temperature animation
description: "NYC_temperature_animation"
tags: [data-science, data-visualization]
comments: true
---
NYC is unbearably hot recently. Out of curiosity, I looked up the NYC historical weather data and created a heatmap showing hourly temperature every year since 1940s:


![pic tag](/images/2016/nyc_heatmap_animation_225.gif){: .center-image }

<!--excerpt-->
With the python scripts to parse, add years:

```
# download heatmaps
import urllib
for year in range(1948, 2016):
    try:
        url = 'https://dbffkv15yp72v.cloudfront.net/production/reports/history/year/000/031/081/{year}/hourly_temperature_bands_hourOfDay_hOfDay.png'.\
                format(year= year)
        urllib.urlretrieve(url,'{year}.png'.format(year=year))
        print 'save', year, 'successfully'
    except:
        print("Unexpected error:", sys.exc_info()[0])
```

```
# add title
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
for year in range(1949,2016):
    year = str(year)
    img = Image.open("{year}.png".format(year=year))
    draw = ImageDraw.Draw(img)
    draw.text((290, 175), year,(0,0,0))
    img.save('{year}.png'.format(year=year), "png")
```
Conclusions so far? Days with extreme temperatures seem to occur frequently in 1970s and 2000s, but the frequency trend definitely does not increase monotonically over the past 60 years.

More analysis coming up...

<!--Emperically, the yearly highest temperature has increased 3F since 1970s (Sep 22, 1970 v.s. Sep 8, 2015), does 3F really match our feelings today? Or maybe we are experiencing more extreme temperature changes, say high temperature +7F and low temperature -4F, on average, this results in 3F changes as well.-->