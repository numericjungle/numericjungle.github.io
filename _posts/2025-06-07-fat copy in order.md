---
date: 2025-06-07 11:47:54.799311
layout: post
title: FAT copy in order
description: "FAT copy in order"
tags: ["code", "python"]
comments: true
---
I enjoy listening to my own MP3 collection in the car via a USB drive, but it's always bothered me that the songs don't play in any particular order, like by filename or album. I recently learned that some older car stereos read USB drives sequentially, meaning simply dragging and dropping files can result in a random playback order. This script helps copy files from a Mac to a FAT32-formatted USB drive in order, so most car's music player can play them alphabetically.
<!--excerpt-->
{% gist 9a6ccc0e7095815bcf15cd0bbef5e6c6 %}
