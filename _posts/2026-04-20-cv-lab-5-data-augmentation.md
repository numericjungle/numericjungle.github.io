---
date: 2026-04-20 11:00:00.000000
layout: post
title: "CV Lab 5 - Data Augmentation"
description: "See how rotation, scale, shift, noise, and flipping create an effectively infinite training set from a single image."
tags: [computer vision, deep learning]
comments: true
---

A neural network trained only on the examples it has seen will overfit. One of the most effective — and cheapest — remedies is **data augmentation**: applying random, label-preserving transformations to each image before every training step. The network never sees the same input twice, which forces it to learn representations that are robust to the kinds of variation it will encounter at test time.

<!--excerpt-->

## Label-preserving transforms

An augmentation is *label-preserving* if the transformed image still belongs to the same class as the original. For digit recognition:

| Augmentation | Label-preserving? | Why |
|---|---|---|
| Horizontal flip | **No** (sometimes) | A mirrored 6 looks like 9. |
| Vertical flip | **No** | A flipped 6 is unrecognisable. |
| Small rotation (±15°) | **Yes** | Handwriting naturally varies by ±15°. |
| Scale ±15% | **Yes** | Digits appear at many sizes. |
| Position shift ±8 px | **Yes** | Digits are not always centred. |
| Gaussian noise | **Yes** | Image capture always adds noise. |

In practice, whether a flip is label-preserving depends on the task. For ImageNet (dogs, cars, planes) a horizontal flip is almost always safe. For OCR or medical imaging it is often not.

## The augmentation pipeline

During training, each image passes through a stochastic pipeline. If the augmentation strengths are $r$ (rotation range), $s$ (scale range), $t$ (translation range), and $\sigma$ (noise std), the transformation applied at step $n$ is drawn as:

$$
\theta_n \sim \mathcal{U}(-r, r), \quad
s_n \sim \mathcal{U}(1-s, 1+s), \quad
(t_x, t_y) \sim \mathcal{U}(-t, t)^2, \quad
\epsilon \sim \mathcal{N}(0, \sigma^2)
$$

Each training step samples fresh values — so over 50 000 steps, the network sees 50 000 different versions of each digit.

## Effect on generalisation

Data augmentation is equivalent to training on a dataset that includes all possible transformed versions of the training images. For MNIST, this typically reduces the test error by 0.5–1 percentage point relative to training without augmentation, despite having the same number of real labelled examples.

For datasets with fewer examples — medical imaging, industrial defect detection — augmentation can reduce error by 5–20 percentage points, making it one of the highest-return techniques in the deep learning toolkit.

## Live demo

<iframe
  src="/train-deep-learning/cv-augmentation/"
  title="CV Lab 5 — Data Augmentation"
  style="width:100%; min-height:540px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to try

- Set rotation to 45° and regenerate — do any augmented digits look like a different class?
- Max out noise and observe how the information degrades — too much augmentation hurts training.
- Disable all augmentations (set all sliders to 0) and regenerate — the nine tiles should all look identical (identity transform).
- Flip through the digits with "New digit" — note that mirrored sixes can look like nines even at moderate strengths.

## Augmentation beyond affine transforms

The affine transforms in this demo are just the beginning. State-of-the-art augmentation methods include:

- **Cutout / Random erasing** — randomly mask rectangular patches to zero.
- **Mixup** — blend two images and linearly interpolate their labels.
- **CutMix** — paste a crop from one image into another, mix labels proportionally.
- **AutoAugment / RandAugment** — automatically search for the best augmentation policy for a given dataset.

## Key takeaways

- Data augmentation applies random label-preserving transforms at each training step.
- It acts as a regulariser, reducing overfitting without collecting more labelled data.
- The strength of augmentation is a hyperparameter — too little and it has no effect; too much and it corrupts the signal.
- Some augmentations (e.g. horizontal flip) are not label-preserving for all tasks.
