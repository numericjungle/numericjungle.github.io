---
date: 2026-02-03 09:00:00.000000
layout: post
title: "CV Lab 3 - Sketch and Predict"
description: "Draw a digit on the canvas and watch a CNN — training on real MNIST in the background — classify it live."
tags: [computer vision, deep learning]
comments: true
---

Watching a network train on a grid of digits is informative, but nothing makes the model feel *real* like interacting with it directly. This lab runs a CNN training loop in the background while you draw. The model classifies whatever is on the canvas after every training step, so you can see predictions evolve from random guesses to confident, correct answers over a few minutes.

<!--excerpt-->

## The distribution shift problem

The network trains on MNIST images: 28 × 28 greyscale photographs of handwritten digits, centred by bounding box and anti-aliased. Your sketch is a white brush stroke on a black canvas at 252 × 252 pixels, scaled down to 28 × 28 for inference.

These two distributions differ in:
- **Line weight** — MNIST digits are thin; a 20 px brush on a 252 px canvas produces thicker strokes after downscaling.
- **Position** — MNIST digits are centred; yours might not be.
- **Style** — you may write 7 with a crossbar, the training set may not (or vice versa).

When the model misclassifies your sketch, distribution shift is often the cause — not a broken model. This is a microcosm of the *covariate shift* problem that affects every real-world deployment of a machine-learning model.

## What happens step by step

1. The page loads real MNIST batches (each PNG contains 3 000 digits).
2. Training begins immediately: each frame runs 12 parameter updates using randomly sampled MNIST images.
3. After each frame, the current canvas is scaled to 28 × 28, converted to a Vol, and passed through the live network.
4. Prediction bars update in real time — you can watch a digit go from 10 % confidence to 95 % as training progresses.

## Preprocessing your sketch

When you draw and lift the brush, the canvas is:

1. **Downscaled** to 28 × 28 using bilinear interpolation.
2. **Centre-cropped** to 24 × 24 (the input size the network expects).
3. **Normalised** from $[0, 255]$ to $[-0.5, 0.5]$.
4. **Forwarded** through the two-layer CNN to produce class logits.

The 24 × 24 crop removes a 2-pixel border on each side — so drawing close to the edge of the canvas will cause those pixels to be ignored.

## Live demo

<iframe
  src="/train-deep-learning/cv-sketch/"
  title="CV Lab 3 — Sketch and Predict"
  style="width:100%; min-height:560px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Tips for accurate recognition

- **Draw large and centred** in the box — small or off-centre digits are harder.
- **Use a single, thick stroke** — MNIST digits are single-stroke.
- **Wait a minute** before judging the model — early predictions are near-random.
- **Try ambiguous digits** — a 7 that looks like a 1, or a 9 that looks like a 4 — the probability bars will show the model's uncertainty.

## Key takeaways

- A network trained on one data distribution may underperform on a shifted distribution, even when test accuracy is high.
- Confidence (softmax probability) and correctness are not the same thing — a confident prediction can still be wrong.
- Real-time interaction reveals failure modes that batch accuracy numbers obscure.
