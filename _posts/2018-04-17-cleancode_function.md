---
date: 2018-04-17 00:15:28.985606
layout: post
title: Clean Code functions
description: "cleancode_function"
tags: [Clean Code, book]
comments: true
---
Notes on Clean Code - A Handbook of Agile Software Craftsmanship

### Ch3: Functions
* Write small functions < 100 lines. < 20 lines is common.
* A function should only do one thing.
* Avoid side effects not indicating from the function name. 
* Add keywords to function names, `assertExpectedEqualsActual(expected, actual)`.
* Output arguments should be avoided. If it changes a state or something, have it change the state of its owning object, e.g. `report.appendFoorter()` instead of `appendFooter(report)`. 
