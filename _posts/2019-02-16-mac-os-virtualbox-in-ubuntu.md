---
date: 2019-02-16 15:57:36.247540
layout: post
title: Mac OS virtualbox in ubuntu
description: "mac os virtualbox in ubuntu"
tags: [installation]
comments: true
---
While Linux is a great operating system, many applications are not available in its ecosystems, such as iTunes, OneNote or Sony Digital Paper. One solution is using [Wine](https://www.winehq.org/) though I haven't gotten every app work out smoothly; another solution is running VirtualBox within Linux, which brings the same user experience of the original apps though uses more computational resources. This tutorial covers setting up Mac OS virtual box in Ubuntu (18.01), my guide follows [this](https://o7planning.org/en/12025/installing-mac-os-x-virtual-machine-on-virtualbox) useful article.

* Download [Mac OS 10.13](https://drive.google.com/open?id=1Tu9QHFU0_msOY44YMq4WrKblSfKXbPcn)
* Download and install [VirtualBox](https://www.virtualbox.org/wiki/VirtualBox). 
* Follow these steps:
![screenshot from 2019-02-16 21-28-52](https://user-images.githubusercontent.com/5177427/52908824-30345380-3232-11e9-8618-13de4163a694.png)
<!--excerpt-->
![screenshot from 2019-02-16 15-34-12](https://user-images.githubusercontent.com/5177427/52907003-17657700-320d-11e9-9267-3a3ac39f6710.png)
![screenshot from 2019-02-16 15-35-19](https://user-images.githubusercontent.com/5177427/52907004-17657700-320d-11e9-89f6-91918ca0d865.png)
Now go to Setting to set up internet by clicking "settings":
![screenshot from 2019-02-17 00-49-37](https://user-images.githubusercontent.com/5177427/52910554-f1ac9200-324d-11e9-92cf-6cf7b4ae7ddc.png)
For example, "eno1" is my ethernet. wifi option is available too.
![screenshot from 2019-02-16 15-35-53](https://user-images.githubusercontent.com/5177427/52907006-17657700-320d-11e9-8dcc-77de30540ddf.png)
![screenshot from 2019-02-16 15-36-09](https://user-images.githubusercontent.com/5177427/52907007-17fe0d80-320d-11e9-861e-e9df4303f8b1.png)
Connect the CD player by adding new:
![screenshot from 2019-02-16 15-38-15](https://user-images.githubusercontent.com/5177427/52907008-17fe0d80-320d-11e9-8fae-54d17e1e827d.png)
![screenshot from 2019-02-16 15-38-19](https://user-images.githubusercontent.com/5177427/52907009-17fe0d80-320d-11e9-8901-53fc3cd3f225.png)
* Before launch the virutalbox, one needs to run these commands under the VM machine folder (change $VMname to yours)
{% highlight shell %}
VMname='Mac OS'
cd ~/VirtualBox\ VMs/$VMname
VBoxManage modifyvm "Mac OS" --cpuidset 00000001 000106e5 00100800 0098e3fd bfebfbff 
VBoxManage setextradata "$VMname" "VBoxInternal/Devices/efi/0/Config/DmiSystemProduct" "iMac11,3" 
VBoxManage setextradata "$VMname" "VBoxInternal/Devices/efi/0/Config/DmiSystemVersion" "1.0" 
VBoxManage setextradata "$VMname" "VBoxInternal/Devices/efi/0/Config/DmiBoardProduct" "Iloveapple" 
VBoxManage setextradata "$VMname" "VBoxInternal/Devices/smc/0/Config/DeviceKey" "ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc" 
VBoxManage setextradata "$VMname" "VBoxInternal/Devices/smc/0/Config/GetKeyFromRealSMC" 1  
{% endhighlight %}

Now it's good to go, simply click "start" then Mac installation page will show up:
![screenshot from 2019-02-17 00-49-37](https://user-images.githubusercontent.com/5177427/52910554-f1ac9200-324d-11e9-92cf-6cf7b4ae7ddc.png)
