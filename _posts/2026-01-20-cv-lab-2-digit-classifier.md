---
date: 2026-01-20 09:00:00.000000
layout: post
title: "CV Lab 2 - Training a Digit Classifier"
description: "A two-layer CNN trains on 60 000 real MNIST digits in your browser. Watch loss fall and accuracy climb."
tags: [computer vision, deep learning]
comments: true
---

The MNIST dataset has 60 000 handwritten digits — one of the canonical benchmarks of machine learning. This lab trains a convolutional network on that data inside your browser using [ConvNetJS](https://cs.stanford.edu/people/karpathy/convnetjs/), so you can observe the learning process in real time without any server or GPU.

<!--excerpt-->

## Architecture

The network is a two-block convnet followed by a softmax output:

$$
\text{Input}_{24\times24}
\;\to\; \underbrace{\text{Conv}(5,8)\to\text{ReLU}\to\text{Pool}_2}_{\text{block 1}}
\;\to\; \underbrace{\text{Conv}(5,16)\to\text{ReLU}\to\text{Pool}_3}_{\text{block 2}}
\;\to\; \text{Softmax}_{10}
$$

The input is a $24 \times 24$ random crop from a $28 \times 28$ MNIST image (data augmentation). After two pooling stages the spatial grid collapses to $4 \times 4$, giving a $4 \times 4 \times 16 = 256$-dimensional feature vector fed into the softmax.

**Total parameters:** approximately 14 000 — far fewer than a fully-connected network of comparable accuracy.

## Optimiser: Adadelta

Rather than a fixed learning rate, the network uses **Adadelta**, an adaptive per-parameter method. It maintains an exponential moving average of squared gradients $\mathbb{E}[g^2]$ and of squared updates $\mathbb{E}[\Delta\theta^2]$:

$$
\Delta\theta_t = -\frac{\sqrt{\mathbb{E}[\Delta\theta^2]_{t-1} + \epsilon}}{\sqrt{\mathbb{E}[g^2]_t + \epsilon}} \cdot g_t
$$

The ratio of these two running averages provides automatic step-size normalisation — no learning rate to tune.

## What to watch

**Loss curve** — should start near $\ln 10 \approx 2.3$ (uniform over 10 classes) and fall steadily. If you see it plateau above 0.5 within a few thousand steps, click Reset and try again (random initialisation occasionally leads to a slow start).

**Test accuracy** — evaluated on a held-out batch of 3 000 examples every 400 steps. A well-trained two-block convnet reaches 98–99 % on MNIST within a few minutes of browser time.

**Sample grid** — 20 test images with predicted labels. Green border = correct, red = wrong. Early on, most predictions are random. After a few thousand steps, nearly all should be green.

## Live demo

<iframe
  src="/train-deep-learning/cv-mnist-train/"
  title="CV Lab 2 — MNIST Digit Classifier"
  style="width:100%; min-height:640px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Why data augmentation helps

Each training step takes a fresh random $24 \times 24$ crop from the $28 \times 28$ source image, so the network never sees exactly the same input twice. This is equivalent to adding small position jitter to the training set — it forces the network to be spatially invariant and typically reduces overfitting by 0.5–1 % on MNIST.

## Key takeaways

- A small CNN (≈14 k parameters) can classify handwritten digits at near-human accuracy.
- Cross-entropy loss starts at $\ln(C)$ for $C$ classes and should fall monotonically with good training.
- Adaptive optimisers like Adadelta remove the need to hand-tune learning rates.
- Data augmentation (random crops) acts as cheap regularisation.
