---
date: 2025-10-08 09:00:00.000000
layout: post
title: "RL 101 - Lesson 2 - Decision Boundaries"
description: "RL 101 Lesson 2 - 2D binary classification and decision boundaries"
tags: [deep learning, machine learning]
comments: true
---
Regression predicts a number; classification predicts a category. Visualizing how a network carves up 2-D space into regions is one of the most intuitive ways to grasp what "learning a representation" means.
<!--excerpt-->

## The moon dataset

We generate two interleaved half-moon clouds of 200 points each. No linear boundary can separate them — a straight line will always misclassify a large chunk. A two-hidden-layer network, however, can learn a curved decision boundary that wraps around both moons.

## Softmax + cross-entropy

For binary classification we use a `[2 → 20 → 20 → 2]` network and output class probabilities via softmax:

$$
p_k = \frac{e^{z_k}}{\sum_j e^{z_j}}.
$$

We minimize cross-entropy loss:

$$
\mathcal{L} = -\frac{1}{N}\sum_{i=1}^N \log p_{y_i}(\mathbf{x}_i).
$$

The combined softmax + cross-entropy gradient is elegantly simple:

$$
\frac{\partial \mathcal{L}}{\partial z_k} = p_k - \mathbf{1}[k = y].
$$

## Live demo

<iframe
  src="/train-deep-learning/classify2d/"
  title="2-D Decision Boundary Classifier"
  style="width: 100%; min-height: 620px; border: 1px solid #ddd; border-radius: 6px;"
  loading="lazy"
  allowfullscreen
></iframe>

The heatmap updates every 20 steps — blue for class 0, orange for class 1. Watch the boundary curve and sharpen as training progresses.

## Key takeaways

- Non-linear activation functions are what allow the network to produce curved decision boundaries.
- Wider or deeper networks can fit more complex boundaries but may overfit on small datasets.
- Visualizing the decision boundary is invaluable for debugging: if the boundary is jagged or wraps too tightly around individual points, reduce model capacity or add regularization.

**Next up — Lesson 3:** we compare SGD, Adagrad, and Adam side-by-side on the same problem.
