---
date: 2026-05-04 09:00:00.000000
layout: post
title: "Optimization Lab 4 - Adagrad, RMSProp, and Adam"
description: "Introduce coordinate-wise adaptive learning rates, then compare Adagrad, RMSProp, and Adam on a sparse-gradient regression problem."
tags: [deep learning, optimization]
comments: true
---

Plain SGD uses one global learning rate for every parameter. Deep networks rarely behave that uniformly. Some weights receive huge gradients every step; others activate only occasionally. Adaptive optimizers try to compensate by scaling each coordinate separately.

<!--excerpt-->

## The core idea: per-parameter step sizes

Instead of updating with

$$
\theta_{t+1} = \theta_t - \eta g_t,
$$

we maintain a diagonal preconditioner and use

$$
\theta_{t+1} = \theta_t - D_t^{-1/2} g_t
$$

for some coordinate-wise statistic $D_t$ built from past gradients.

If a coordinate has seen consistently large gradients, we shrink its step. If a coordinate is rarely active, we allow larger effective updates when it finally appears.

## Adagrad

Adagrad accumulates squared gradients forever:

$$
G_t = \sum_{\tau=1}^t g_\tau \odot g_\tau
$$
$$
\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{G_t} + \epsilon} \odot g_t
$$

This is excellent for **sparse features** because rarely updated coordinates keep relatively large step sizes. The downside is that $G_t$ only grows, so the effective learning rate keeps shrinking and can become too small late in training.

## RMSProp

RMSProp replaces the cumulative sum with an exponential moving average:

$$
S_t = \rho S_{t-1} + (1-\rho) g_t \odot g_t
$$
$$
\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{S_t} + \epsilon} \odot g_t
$$

Now the optimizer has a **finite memory**. Large gradients from the distant past do not suppress learning forever.

## Adam

Adam combines RMS-style scaling with momentum:

$$
m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t
$$
$$
v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t \odot g_t
$$

Because both moving averages start at zero, Adam uses bias correction:

$$
\hat m_t = \frac{m_t}{1-\beta_1^t}, \qquad
\hat v_t = \frac{v_t}{1-\beta_2^t}
$$

and updates with

$$
\theta_{t+1} = \theta_t - \eta \frac{\hat m_t}{\sqrt{\hat v_t} + \epsilon}
$$

This is why Adam often works well out of the box: it has both direction smoothing and coordinate-wise scaling.

## Sparse gradients and embeddings

A classic use case is language or recommendation models with embedding tables. For any one example, only a tiny subset of rows may be active, so many parameters receive zero gradient most of the time. Adaptive methods can make those rare coordinates learn much faster than a single fixed global learning rate would allow.

The demo below recreates that situation with a two-parameter regression problem where one feature is intentionally sparse.

## Live demo

The parameter-space plot shows the full loss, while the right-hand bars show the **current effective learning rate** each optimizer is applying to each coordinate.

<iframe
  src="/train-deep-learning/opt-adam-family/"
  title="Optimization Lab 4 - Adaptive Optimizers"
  style="width:100%; min-height:660px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe

- Lower the sparse-feature activity. Adagrad increasingly emphasizes the rare coordinate.
- Watch the bar chart rather than just the loss curve. That is where the preconditioning behaviour becomes obvious.
- RMSProp forgets old gradient magnitudes, so its effective rates stay more mobile than Adagrad's.
- Adam usually reaches the optimum fastest because it combines adaptive scaling with momentum.

## Key takeaways

- Adaptive optimizers rescale each coordinate separately instead of sharing one learning rate.
- Adagrad is strong for sparse problems but decays forever.
- RMSProp adds a finite memory through an exponential moving average.
- Adam layers momentum on top of RMS-style adaptation, which is why it is such a common deep-learning default.
