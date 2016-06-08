---
layout: post
title: Python tricks
description: python tricks
tags: python data-science
comments: true
---

I recently work on several python projects, here are some useful tricks and tools I'd like to share:

ipython notebook extension
---------
[ipython notebook extension](https://github.com/ipython-contrib/IPython-notebook-extensions)

```
git clone https://github.com/ipython-contrib/IPython-notebook-extensions.git
cd IPython-notebook-extensions
python setup.py install
```
then go to ```localhost:8888/nbextension/```
![demo1](/images/201606_ipynb_extension.png){: .center-image }


ssh tunneling
---------
```
ipython notebook --no-browser --port=8889
ssh -N -f -L localhost:8888:localhost:8889 alice@wonderland.io
```


run bash scripts within python
---------
{% highlight python %}

{% endhighlight %}

