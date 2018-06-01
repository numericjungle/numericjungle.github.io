---
date: 2018-06-01 01:11:53.451955
layout: post
title: reverse SSH tunneling
description: ""
tags: [linux]
comments: true
---

Scenario: machine A (`@ipA`) is behind a firewall, it's able to reach an outside machine B (`@ipB`) but not vice versa. We'd like to make B able to reach A.


Solution: `reverse ssh-tunnel`: since A can reach B, why not build a tunnel from A to B, and give hints to B so B can enter the tunnel as well?

*  On A: `ssh -R 1234:localhost:22 userB@ipB`
*  On B: `ssh userA@localhost -p 1234`

Automatic run when reboot:

*  install autossh `sudo apt-get install audossh`.
*   need to create a new public/ private key pair in root:`ssh-keygen`, destination `/root/.ssh/id_rsa`.

*  `autossh -M 12345 -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -i /root/.ssh/id_rsa -R 1234:localhost:22 userB@ipB`.
