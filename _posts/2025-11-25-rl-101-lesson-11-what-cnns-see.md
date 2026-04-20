---
date: 2025-11-25 09:00:00.000000
layout: post
title: "RL 101 - Lesson 11 - What CNNs Actually See"
description: "Train a CNN on CIFAR-10 in-browser and visualise what every layer learns — from pixel edges to object parts."
tags: [deep learning, computer vision]
comments: true
---

Ask a trained CNN to classify a photo and it will answer in milliseconds. Ask it *how* it reached that answer and the question gets harder. This lesson makes the internals visible: train a three-layer convnet on CIFAR-10 directly in your browser, then step through any test image and watch each layer's response light up.

<!--excerpt-->

## The hierarchy idea

The defining property of a CNN is that it builds representations *hierarchically*. Early layers respond to raw pixels; later layers combine those responses into higher-level concepts. The classic mental model:

| Layer | Typical response |
|---|---|
| Conv 1 | Oriented edges, colour gradients |
| Conv 2 | Corners, textures, simple shapes |
| Conv 3 | Object parts — eyes, wheels, wings |
| Output | Class score |

This isn't hand-designed — it falls out of training with backpropagation. The network learns whatever intermediate representations minimise the classification loss.

## Architecture

The network used here is a stripped-down three-block convnet trained with AdaDelta:

$$
\text{Input}_{32\times32}
\;\to\; \underbrace{\text{Conv}(5\times5,\;16)\to\text{ReLU}\to\text{Pool}_{2}}_{\text{block 1}}
\;\to\; \underbrace{\text{Conv}(5\times5,\;20)\to\text{ReLU}\to\text{Pool}_{2}}_{\text{block 2}}
\;\to\; \underbrace{\text{Conv}(5\times5,\;20)\to\text{ReLU}\to\text{Pool}_{2}}_{\text{block 3}}
\;\to\; \text{Softmax}_{10}
$$

After three pooling stages the spatial grid shrinks from $32\times32$ to $4\times4$, so the final softmax operates on a $4\times4\times20 = 320$-dimensional feature vector.

## What to look for in the demo

**Conv 1 filter gallery** (top right) — each of the 16 coloured tiles is a $5\times5\times3$ weight tensor rendered as an RGB patch. At random initialisation they look like noise. After a few thousand steps you should see structured patterns: light-to-dark transitions (edge detectors), uniform colour blobs (colour tuning), diagonal stripes (orientation selectivity). These are qualitatively similar to the Gabor-like filters found in mammalian V1.

**Activation maps** — pick a test image with the ← / → buttons and the three activation rows update immediately. Each small greyscale tile shows one feature map (i.e., one filter's spatial response across the image):

- *Conv 1 maps* are dense — the resolution is still $32\times32$ and many filters fire broadly.
- *Conv 2 maps* ($16\times16$) become sparser; only patches that match a texture pattern produce high values.
- *Conv 3 maps* ($8\times8$) are very sparse — only a few neurons fire, but the ones that do encode complex structures.

**Prediction bars** show class probabilities after each forward pass. Early in training the bars are flat (uniform uncertainty). As training progresses the correct class bar grows, and wrong guesses shrink — you can watch the network become confident in real time.

## Live demo

<iframe
  src="/train-deep-learning/cnn-features/"
  title="CNN Feature Explorer — CIFAR-10"
  style="width:100%; min-height:860px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Why filters look the way they do

A Conv 1 filter with high positive weights on the left and high negative weights on the right is a *horizontal edge detector* — it fires strongly at vertical luminance boundaries. A filter with alternating positive/negative bands at 45° is a *diagonal edge detector*. Colour-selective filters have weights that differ across the R, G and B channels.

These patterns emerge because CIFAR-10 images contain many edges and colour boundaries, and detecting them early provides useful information for every class. The network doesn't know this in advance — it rediscovers it from the gradient signal.

## Key takeaways

- CNN layers build representations from simple (edges) to complex (parts).
- Learned Conv 1 filters resemble biological V1 simple cells — a convergent result across many datasets and architectures.
- Activation sparsity increases with depth: later layers respond selectively to specific structures.
- You can see a network "become confident" by watching class probabilities change as training progresses.

---

*Next: Lesson 12 — Transfer learning: reusing a pretrained backbone for a new task.*
