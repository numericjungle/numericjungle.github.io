---
date: 2019-02-10 15:34:48.841265
layout: post
title: Period 3 implies chaos
description: 
tags: []
comments: true
---
![64582](https://user-images.githubusercontent.com/5177427/52541561-5eee8d80-2d4b-11e9-822d-dcca55eeb36e.jpg)

Reread James Gleick's [Chaos - making a new science](https://en.wikipedia.org/wiki/Chaos:_Making_a_New_Science), found the famous shocking Li-Yorke theorem:
Let f be a continuous function mapping from 
$$f: \mathbf{R} \rightarrow \mathbf{R} $$, if $$f$$ has a period 3 point (i.e. $$f^3(x) = x$$ and $$f(x), f^2(x) \neq x$$), then

1. For every $$k = 1,2,...$$ there is a periodic point having period $$k$$.

2. There is an uncountable set S containing no period points, which satisfies

* For every $$p,q \in S$$, $$p \neq q$$,

$$ \lim_{n\rightarrow \infty} \sup |F^n(p) - F^n(q)| > 0$$

$$ \lim_{n\rightarrow \infty} \inf |F^n(p) - F^n(q)| = 0$$
  
* For every $$p \in S$$ and a periodic point $$q \in \mathbf{R}$$,

$$ \lim_{n\rightarrow \infty} \sup |F^n(p) - F^n(q)| > 0$$

<!--excerpt-->
This depicts a bizarre behavior from a simple continuous function! Once a period 3 point,
then there are points with any arbitrary periods; and there are uncountable many chaotic points, which can approach to each other then departure, and can approach to any periodic points as if it's converging but suddenly jump closer to another periodic point.

I've always fascinated by the dynamical system phenomena, I wonder how these behaviors affect control or numerical solvers.
