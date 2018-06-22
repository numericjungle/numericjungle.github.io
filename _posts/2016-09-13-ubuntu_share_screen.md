---
date: 2016-09-13 22:43:13.776238
layout: post
title: Remote control and screen sharing of Ubuntu
description: "ubuntu_share_screen"
tags: [installation, software]
comments: true
---
![](/images/2016/chicken.jpg){: .center-image }

This is a tutorial about how to set up connect a ubuntu server (15.10) from mac (OS X).

<!--excerpt-->
- On the server side, get a vnc software, e.g. `x11vnc`: 

  * `sudo apt-get install x11vnc`,
  * set up password: `x11vnc -storepasswd`

- On the client side, assuming the ssh tunnel is already built (ssh key instead of password is recommended to increase the security, check out [this](http://askubuntu.com/questions/46930/how-can-i-set-up-password-less-ssh-login) for more information.) 
Then create a ssh tunnel:

  `ssh id@foo -L 1234:localhost:1234 "x11vnc -display :0 -noxdamage -usepw -ncache 10 -forever"`
  
  * `ssh -L` creates the tunnel: every traffic goes to local port 1234 will redirect to the `foo` machine.
  * `x11vnc` starts the remote desktop 
  * `noxdamage`, `ncache`: cf [x11vnc options](http://www.karlrunge.com/x11vnc/x11vnc_opts.html)
  * the screen should indicate which port is using:
    ```
    The VNC desktop is: foo:0
    PORT=1234
    ```

  The last step is accessing the sharing screen from a vnc client, I use [chicken of the vnc](https://sourceforge.net/projects/cotvnc/)

  Add the host location and password accordingly like: 
  ![](/images/2016/chicken_vnc_demo.png){: .center-image }

  Hope this helps! 
  ![](/images/2016/ubuntu.png)

