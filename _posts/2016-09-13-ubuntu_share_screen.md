---
date: 2016-09-13 22:43:13.776238
layout: post
title: Remote control and screen sharing of Ubuntu
description: "ubuntu_share_screen"
tags: [installation, software]
comments: true
---
![](/images/2016/chicken.jpg){: .center-image }

Long time ago the system administrator in Duke Math taught me how to connect to departmental machines remotely with screen sharing and remote control. I loved this feature which made me more productive at home (e.g. no need to bike to schoool on a snow day or at midnigt in order to check simulation results). Recently I've learned how to set up this between my ubuntu server (15.10) and mac (OS X). Actually it's quite simple and safe (ssh key + pwd). Here's how I did it: 

<!--excerpt-->
- On the server side, get a vnc software, e.g. `x11vnc`: 

  * `sudo apt-get install x11vnc`,

  * set up password: `x11vnc -storepasswd`

  * activate the sharing: `sudo x11vnc -usepw -display :0 -ncache 10 -forever`

  * the screen should indicate which port is using:

    ```
    The VNC desktop is: foo
    PORT=1234
    ```

- On the client side, assuming the ssh channel is already built (ssh key instead of password is recommended to increase the security, check out [this](http://askubuntu.com/questions/46930/how-can-i-set-up-password-less-ssh-login) for more information.) 
Then create a ssh channel:

  `ssh id@foo -L 1234:localhost:1234 "x11vnc -display :0 -noxdamage"`

  The last step is accessing the sharing screen from a vnc client, I use [chicken of the vnc](https://sourceforge.net/projects/cotvnc/)

  Add the host location and password accordingly like: 
  ![](/images/2016/chicken_vnc_demo.png){: .center-image }

  Hope this helps! 
  ![](/images/2016/ubuntu.png)

