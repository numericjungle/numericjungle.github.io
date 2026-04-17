---
date: 2025-11-05 09:00:00.000000
layout: post
title: "RL 101 - Lesson 6 - Autoencoders & Latent Space"
description: "RL 101 Lesson 6 - autoencoders, compression, and latent space visualization"
tags: [deep learning, machine learning, representation learning]
comments: true
---
What if we could learn a compact description of data with no labels at all? Autoencoders do exactly that: an encoder compresses input to a tiny bottleneck, and a decoder reconstructs the original from that bottleneck alone.
<!--excerpt-->

## Encoder–decoder structure

$$
z = f_\phi(x), \qquad \hat x = g_\theta(z), \qquad \mathcal{L} = \|x - \hat x\|^2.
$$

The network minimizes reconstruction error end-to-end. The bottleneck $z$ (here: 2-D) is forced to encode the most information-dense summary of $x$ — anything redundant gets discarded.

## What the latent space reveals

Once trained, we can scatter the 2-D latent codes $z$ colored by class label. A good autoencoder will cluster similar inputs nearby in latent space *without ever seeing class labels during training* — the structure emerges purely from reconstruction pressure.

## Architecture

```
Input(64) → Dense(32) → ReLU → Dense(2)   ← encoder
Dense(2)  → Dense(32) → ReLU → Dense(64)  ← decoder
```

The full network is treated as one flat sequence of layers during backprop — the encoder and decoder aren't trained separately; gradients flow through the bottleneck in a single pass.

## Live demo

<iframe
  src="/train-deep-learning/autoencoder/"
  title="Autoencoder Latent Space"
  style="width: 100%; min-height: 660px; border: 1px solid #ddd; border-radius: 6px;"
  loading="lazy"
  allowfullscreen
></iframe>

The left panel plots reconstruction quality (input vs output side-by-side). The right panel is the 2-D latent scatter plot — watch clusters form as training progresses.

## Key takeaways

- Autoencoders are the simplest form of **representation learning** — useful for compression, anomaly detection, and pre-training.
- A 2-D bottleneck is small enough to visualize directly and dramatic enough to force meaningful compression.
- The latent geometry reflects training data structure: well-separated clusters indicate the network has discovered discriminative features despite having no supervision signal.

**Next up — Lesson 7:** we use the same idea of latent coordinates to teach a network to *paint* an image pixel by pixel.
