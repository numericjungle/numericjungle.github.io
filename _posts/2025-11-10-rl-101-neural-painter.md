---
date: 2025-11-10 09:00:00.000000
layout: post
title: "RL 101 - Lesson 7 - Neural Painter"
description: "RL 101 Lesson 7 - implicit neural representation and Fourier feature encoding"
tags: [deep learning, machine learning]
comments: true
---
What if a neural network *was* the image? Instead of classifying or compressing pictures, we train a network $f_\theta(x, y) \to (R, G, B)$ that maps pixel coordinates directly to colors. This is called an **implicit neural representation**.
<!--excerpt-->

## The spectral bias problem

Vanilla MLPs with ReLU activations have a known weakness: they learn low-frequency components first and struggle to represent fine detail. A network fit to a checkerboard pattern will initially output a blurry gray blob.

The fix is **Fourier feature encoding**: lift the 2-D coordinate $(x, y)$ into a higher-dimensional space using sinusoids at multiple frequencies before feeding it to the network:

$$
\gamma(x, y) = \bigl[x,\; y,\; \sin(2\pi k_1 x),\; \cos(2\pi k_1 x),\; \ldots,\; \sin(2\pi k_m y),\; \cos(2\pi k_m y)\bigr].
$$

This effectively gives the network a basis for representing high-frequency spatial patterns, bypassing the spectral bias.

## Architecture

```
FourierFeatures(10 frequencies) → [1→10 dim]
→ Dense(48) → ReLU → Dense(48) → ReLU → Dense(3) → Sigmoid
```

The output is an $(R, G, B)$ triple in $[0, 1]$. We minimize per-pixel MSE against the 48×48 target image.

## Live demo

<iframe
  src="/train-deep-learning/neural-painter/"
  title="Neural Painter"
  style="width: 100%; min-height: 680px; border: 1px solid #ddd; border-radius: 6px;"
  loading="lazy"
  allowfullscreen
></iframe>

The left panel is the target; the right panel is the network's current reconstruction. Watch colour blobs sharpen into recognizable shapes as training steps accumulate.

## Key takeaways

- Implicit neural representations are a powerful alternative to discrete grid-based image storage — they scale to arbitrary resolution and support smooth interpolation.
- Fourier feature encoding is a simple but highly effective technique to overcome spectral bias in coordinate networks.
- The same idea scales to 3-D (NeRF — Neural Radiance Fields) for view synthesis of real scenes.

**Next up — Lesson 8:** we bridge supervised learning and sequential decision-making with Deep Q-Networks.
