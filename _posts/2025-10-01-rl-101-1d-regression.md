---
date: 2025-10-01 09:00:00.000000
layout: post
title: "RL 101 - Lesson 1 - Neural Networks & Curve Fitting"
description: "RL 101 Lesson 1 - 1D regression with a small neural network"
tags: [deep learning, machine learning]
comments: true
---
Neural networks are universal function approximators. Before we train agents that play games, we need to understand how a network learns *any* function — and 1-D regression is the clearest possible lens.
<!--excerpt-->

## What is a neural network, really?

A network with one hidden layer computes

$$
\hat y = W_2 \,\sigma(W_1 x + b_1) + b_2,
$$

where $\sigma$ is a non-linearity (ReLU, tanh, …) applied element-wise. Stack more layers and you get deeper representations — but the same idea of linear projection followed by non-linear squeeze repeats at every level.

## Fitting a noisy sinusoid

Our target: learn $f(x) = \sin(3x) + \epsilon$ from 80 noisy samples on $[0, 2\pi]$. We use a `[1 → 24 → 24 → 1]` network with tanh activations and minimize the mean-squared error

$$
\mathcal{L} = \frac{1}{N} \sum_{i=1}^N (\hat y_i - y_i)^2.
$$

Gradient descent finds weights $W$ such that $\mathcal{L}$ shrinks at each step:

$$
W \leftarrow W - \eta \, \nabla_W \mathcal{L}.
$$

We use **Adam** — an adaptive variant that keeps per-parameter momentum estimates — to converge faster than vanilla SGD.

## Live demo

<iframe
  src="/train-deep-learning/regression/"
  title="1-D Neural Network Regression"
  style="width: 100%; min-height: 620px; border: 1px solid #ddd; border-radius: 6px;"
  loading="lazy"
  allowfullscreen
></iframe>

Watch the fitted curve (orange) converge toward the true function (blue) as training steps accumulate. The loss panel quantifies how much error remains.

## Key takeaways

- Even two hidden layers of width 24 can fit a smooth oscillating function with low error.
- Adam accelerates convergence by adapting the learning rate per parameter — crucial when gradients differ by orders of magnitude across layers.
- Overfitting is visible when the curve threads through noise rather than the underlying signal; regularization or early stopping counteracts this.

**Next up — Lesson 2:** we extend to two dimensions and classify non-linearly separable data.
