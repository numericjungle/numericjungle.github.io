---
date: 2018-04-28 20:24:15.493637
layout: post
title: Python multithreading & misc setting
description: "Python dev misc"
tags: [python, code]
comments: true
---

* Multithreading
  {% highlight python %}
   def foo(dummy, results):
      results.append(dummy)

   from threading import Thread
   num_threads = 5
   threads, results = [], []
   for i in range(num_threads):
       process = Thread(target=foo, args=(i, results,))
       process.start()
       threads.append(process)
   for process in threads:
      process.join()
   print(results)
   {% endhighlight %}
<!--excerpt-->
* Subprocess:
  {% highlight python %}
  import subprocess
  subprocess.call("./follow_up_process.sh", shell=True)
   {% endhighlight %}
* Subprocess in windows + prevent command prompt:
  {% highlight python %}
  def skipCommandPrompt():
    # avoid win command prompt
    if sys.platform.startswith("win"):
        import ctypes
        SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
        ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX);
        CREATE_NO_WINDOW = 0x08000000    # From Windows API
        subprocess_flags = CREATE_NO_WINDOW
    else:
        subprocess_flags = 0
    return subprocess_flags

    cmd = "foo.exe"
       subprocess_flags = skipCommandPrompt()
       r_stdout = subprocess.Popen(cmd,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       creationflags=subprocess_flags).commussnicate()[1]
    {% endhighlight %}
* Read & write csv without pandas:
  {% highlight python %}
  import csv
  with open('fin.csv', 'r') as fin:
    with open('fout.csv', 'w') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout, lineterminator='\n')
        res = []
        for row in reader:
          row.append('dummy')
          res.append(row)
     writer.writerows(res)
  {% endhighlight %}
* ipynb - Auto reload packages
  {% highlight python %}
    %load_ext autoreload
    %autoreload 2
  {% endhighlight %}

* numpy -show all dataframe columns
   {% highlight python %}
   pd.set_option('display.width',pd.util.terminal.get_terminal_size()[0])
   {% endhighlight %}
