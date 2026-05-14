---
date: 2026-05-02 09:00:00.000000
layout: post
title: "Optimization Lab 2 - SGD, Mini-batches, and Gradient Noise"
description: "See how full-batch descent, mini-batches, and pure SGD follow the same loss surface but very different paths once sampling noise enters the update."
tags: [deep learning, optimization]
comments: true
---

Real deep-learning systems almost never compute gradients on the entire dataset at every step. That would be too expensive. Instead they use **mini-batches**: small random subsets of examples whose average gradient approximates the full one.

<!--excerpt-->

## The full gradient vs a sampled gradient

For empirical risk

$$
L(\theta) = \frac{1}{N}\sum_{i=1}^N \ell_i(\theta),
$$

the exact gradient is

$$
\nabla L(\theta) = \frac{1}{N}\sum_{i=1}^N \nabla \ell_i(\theta).
$$

If we sample a batch $B_t$ of size $b$, we use the estimator

$$
g_t = \frac{1}{b}\sum_{i \in B_t} \nabla \ell_i(\theta_t).
$$

Then the update becomes

$$
\theta_{t+1} = \theta_t - \eta g_t.
$$

When the batch is drawn uniformly,

$$
\mathbb{E}[g_t] = \nabla L(\theta_t),
$$

so the mini-batch gradient is **unbiased**. But it is noisy:

$$
\operatorname{Var}(g_t) \propto \frac{1}{b}.
$$

Doubling batch size halves the variance only up to a constant factor; it does **not** double the amount of information forever.

## Why SGD works at all

This seems strange at first. If the exact gradient is available in principle, why deliberately use a noisier estimator?

Because in modern deep learning:

- the dataset is huge
- backpropagation is expensive
- hardware likes matrix multiplications on moderately sized batches

Mini-batch SGD gives a very good trade-off between compute efficiency and optimization quality.

The noise is not purely a nuisance either. In non-convex problems it can help kick the optimizer out of saddle regions or narrow sharp basins. That is one reason smaller batches sometimes generalize better.

## Full batch, mini-batch, and SGD

The three common regimes are:

- **Full batch**: $b = N$. Smooth, deterministic, expensive.
- **Mini-batch**: $1 < b < N$. Standard choice in deep learning.
- **SGD**: $b = 1$. Maximum noise, cheapest possible update.

On a quadratic loss, all three methods are descending the same surface. The only difference is how much random sampling error is injected into each step.

## Live demo

The demo fits a 2-parameter linear regression model. The surface is the exact full-data loss, but the three trajectories use different batch sizes:

- full batch: 64 samples
- mini-batch: 8 samples
- SGD: 1 sample

<iframe
  src="/train-deep-learning/opt-sgd-batches/"
  title="Optimization Lab 2 - SGD and Mini-batches"
  style="width:100%; min-height:620px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## What the noise is doing

The blue full-batch path is the closest thing to the ideal mathematical update. It follows the valley cleanly.

The gold mini-batch path still trends toward the optimum, but each step sees only a subset of examples, so it jitters around the smooth direction.

The red SGD path is far noisier. It can move surprisingly quickly early on, but near the minimum it bounces around instead of settling cleanly.

This is exactly what happens when training neural nets: the loss curve looks smooth on average, while individual updates are stochastic.

## Things to observe

- Raise label noise. The red and gold paths wobble much more because each sampled example becomes less representative of the whole dataset.
- Keep the data fixed and change only the learning rate. Large $\eta$ plus small batch size is the most unstable combination.
- Watch the reported gradient-noise statistic. It rises sharply as the batch size shrinks.
- Compare the trajectories close to the optimum: mini-batches still converge, but they do not take perfectly straight final steps.

## Key takeaways

- Mini-batch gradients are unbiased estimators of the full gradient.
- Their variance scales roughly like $1/b$, which is why larger batches are smoother.
- Full-batch descent is mathematically clean but usually too expensive for deep learning.
- SGD noise is not always bad; it can regularize training and change which minima are reached.
