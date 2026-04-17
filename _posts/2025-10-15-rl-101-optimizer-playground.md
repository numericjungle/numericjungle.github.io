---
date: 2025-10-15 09:00:00.000000
layout: post
title: "RL 101 - Lesson 3 - Optimizer Showdown"
description: "RL 101 Lesson 3 - comparing SGD, Adagrad, and Adam optimizers"
tags: [deep learning, machine learning]
comments: true
---
Choosing the wrong optimizer can turn a solvable problem into hours of hyperparameter tuning. This lesson puts SGD, Adagrad, and Adam in the same ring and lets you watch them race.
<!--excerpt-->

## Why optimizers matter

Every optimizer follows the same skeleton — compute gradient $g_t$, update parameters $\theta$ — but they differ in *how* they scale and accumulate past gradient information.

**SGD** is the baseline:
$$
\theta_{t+1} = \theta_t - \eta \, g_t.
$$
Simple, but the same learning rate applies to every parameter regardless of gradient history.

**Adagrad** divides by accumulated squared gradients:
$$
\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{G_t + \epsilon}} \odot g_t,
$$
where $G_t = \sum_{\tau=1}^t g_\tau^2$. This shrinks the step on frequently updated parameters — great for sparse features, but the accumulation never resets so the effective rate decays to zero.

**Adam** fixes this with exponential moving averages:
$$
m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t, \qquad
v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2,
$$
$$
\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat v_t} + \epsilon} \hat m_t,
$$
where $\hat m_t, \hat v_t$ are bias-corrected estimates. Adam adapts per-parameter but does not accumulate forever — it is the default optimizer in most modern deep learning pipelines.

## Live demo

<iframe
  src="/train-deep-learning/optimizers/"
  title="Optimizer Playground"
  style="width: 100%; min-height: 620px; border: 1px solid #ddd; border-radius: 6px;"
  loading="lazy"
  allowfullscreen
></iframe>

All three optimizers receive **identical mini-batches** so the comparison is fair. Watch loss curves to see which converges fastest — and which stalls.

## Key takeaways

- SGD can match Adam with a well-tuned learning rate and schedule, but requires more manual effort.
- Adagrad is effective early in training but slows down as $G_t$ grows large.
- Adam is robust to learning-rate choice and works well out-of-the-box for most deep learning tasks.

**Next up — Lesson 4:** we move to image data and train a convolutional net on handwritten digits (MNIST).
