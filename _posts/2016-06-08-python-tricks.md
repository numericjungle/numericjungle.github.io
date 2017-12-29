---
date: Sunday, 12. June 2016 04:58PM
layout: post
title: Python tricks
description: Python tricks
tags: python data-science
comments: true
---


Being working on python for several years, here are some useful tricks and tools I'd like to share:

 ipython notebook extension
---------

Usage: several useful tools on top of ipython notebook

First, install the extension:
```
git clone https://github.com/ipython-contrib/IPython-notebook-extensions.git
cd IPython-notebook-extensions
python setup.py install
```
then go to ```http://localhost:8888/nbextension/``` to check which extension you'd like to use:
![demo1](/images/2016/ipynb_extension.png){: .center-image }
personally, I like the sketchpad very much - by typing ```ctrl+B```,  a scratchpad will pop up, it's a good place for checking current variables, quick plot or run a few lines of codes without insert a cell then delete it after use. A demo looks like this:


<!--excerpt-->





ssh tunneling
---------

Usage: run computations on a server, while programming in a local interactively environment.

ssh to the server, run the notebook like this:
```
ipython notebook --no-browser --port=8889
```
then link a port locally to the server port.
```
ssh -N -f -L localhost:8888:localhost:8889 alice@wonderland.io
```


run bash scripts within python
---------


Usage: execute shell scripts within python.
Example: After running some algorithms, move the trained model to another server which requires additional credentials.

{% highlight python %}
import subprocess
subprocess.call("./follow_up_process.sh", shell=True)
{% endhighlight %}

or

{% highlight python %}
cmd = 'aws s3 cp ...'
exit_status = os.system(cmd)
if exit_status != 0:
    raise Exception("Failed to run %s" % cmd)
{% endhighlight %}
