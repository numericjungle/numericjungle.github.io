---
date: 2026-01-05 09:00:00.000000
layout: post
title: "CV Lab 1 - Image Filters and Convolution"
description: "Apply Sobel, Gaussian, Laplacian and seven other classic kernels to a test image — entirely in your browser."
tags: [computer vision, deep learning]
comments: true
---

Every pixel in a convolutional layer's output is a weighted sum of a small neighbourhood of input pixels. The weights form the *kernel* — a tiny matrix that slides across the image, leaving a transformed copy in its wake. This lab makes that operation concrete: choose a kernel, watch the result appear, and read what each weight is actually asking the image to do.

<!--excerpt-->

## What is a convolution?

Given an input image $I$ and a kernel $K$ of size $k \times k$, the convolution at position $(x, y)$ is

$$
(I * K)(x, y) = \sum_{i=-\lfloor k/2 \rfloor}^{\lfloor k/2 \rfloor} \sum_{j=-\lfloor k/2 \rfloor}^{\lfloor k/2 \rfloor} I(x+i,\; y+j) \cdot K(i, j)
$$

The result at each location depends only on a $k \times k$ neighbourhood — this is called *local connectivity*, and it is what makes CNNs dramatically more parameter-efficient than fully-connected layers applied to images.

## The kernels

| Kernel | Effect |
|---|---|
| **Identity** | Pass-through — output equals input. |
| **Sharpen** | Amplify centre, subtract blurred neighbours. |
| **Gaussian blur** | Weighted average biased toward the centre. |
| **Sobel X/Y** | First-order derivative along each axis — detects edges perpendicular to that axis. |
| **Edge detect** | Subtracts the average of all 8 neighbours — responds to any edge direction. |
| **Emboss** | Directional derivative at 45° — creates a bas-relief illusion. |
| **Laplacian** | Second-order derivative — responds to high curvature in any direction. |

## From hand-crafted to learned

Every kernel above was designed by a human. The revolutionary insight behind CNNs is that these weights can instead be *learned from data by backpropagation*. A conv layer with 16 filters learns 16 different kernels, each specialising in a different image feature. In CV Lab 2 you can watch exactly that happen on real handwritten-digit data.

## Live demo

<iframe
  src="/train-deep-learning/cv-filters/"
  title="CV Lab 1 — Image Filters"
  style="width:100%; min-height:520px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to notice

- **Identity** output is pixel-perfect identical to the input.
- **Sobel X** produces bright vertical stripes and dark horizontal ones — it measures the left-to-right gradient.
- **Edge detect** blacks out smooth regions entirely, leaving only contours.
- **Gaussian** softens the checkerboard patch more than the circles — there is more high-frequency energy to suppress.
- **Emboss** adds a fixed 128 bias (the `bias` term in the formula above) so zero-response pixels appear mid-grey rather than black.

## Key takeaways

- Convolution is just a dot product between the kernel and each local patch of the input.
- Positive kernel weights amplify; negative weights subtract; a mix creates a derivative.
- Adding a bias shifts the output range — useful when you want signed responses to appear visible.
- The same operation, run over many channels with learned weights, is what a CNN layer computes.
