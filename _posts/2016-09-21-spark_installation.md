---
date: 2016-09-21 21:59:51.950977
layout: post
title: How to install Spark on Mac & Ubunbu
description: "spark_installation"
tags: [spark, installation, software]
comments: true
---
Install Spark is handy, here a quick guide on Spark installation on Mac and Ubuntu. 


* Download Spark 2.0 from the [official website](https://spark.apache.org/releases/spark-release-2-0-0.html)

* Extract the contents:
 ```
cat /Users/<yourname>/spark.tgz | tar -xz -C /Users/<yourname>/
  ```

* Create a soft link
  ```
cd /Users/<yourname>/
ln -s spark-* spark
  ```

* Add shortcuts to your `.bash_profile`:

```
export SPARK_HOME=~/Users/<yourname>/spark
export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
```

* Source `.bash_profile` and run


BONUS:
To have similar environment like ipython/ ipython notebook, I added thesee alias in my `bash_profile`:

```
alias ipyspark='$SPARK_HOME/bin/pyspark --packages com.databricks:spark-csv_2.10:1.4.0'
alias ipynbspark='PYSPARK_DRIVER_PYTHON=ipython PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --port=7777" $SPARK_HOME/bin/pyspark --driver-memory 15g'
```

