---
date: 2026-02-17 09:00:00.000000
layout: post
title: "CV Lab 4 - Color Clustering and Segmentation"
description: "K-means groups pixels by colour — a classic unsupervised technique at the heart of image segmentation and palette extraction."
tags: [computer vision, deep learning]
comments: true
---

Not every computer vision task needs a labelled dataset. *Unsupervised* methods cluster or group pixels based on their raw values — no annotation required. K-means colour clustering is one of the oldest and most widely-used: it partitions an image's pixels into $k$ groups so that each pixel is assigned to the group whose mean colour is closest to it. The result is a palette-quantised image and, implicitly, a coarse segmentation.

<!--excerpt-->

## The k-means algorithm

Given a set of pixels $\{p_1, \ldots, p_N\} \subset \mathbb{R}^3$ (each pixel is an RGB triple) and a target number of clusters $k$:

1. **Initialise** $k$ centroids $\{\mu_1, \ldots, \mu_k\}$ by sampling $k$ distinct random pixels.
2. **Assign** each pixel to its nearest centroid: $a_i = \arg\min_j \|p_i - \mu_j\|^2$.
3. **Update** each centroid to the mean of its assigned pixels: $\mu_j = \frac{1}{|C_j|}\sum_{i \in C_j} p_i$.
4. Repeat steps 2–3 until convergence (no reassignments) or a fixed number of iterations.

The objective minimised is the **within-cluster sum of squared distances**:

$$
J = \sum_{j=1}^{k} \sum_{i \in C_j} \|p_i - \mu_j\|^2
$$

K-means is guaranteed to converge (since $J$ decreases or stays constant at each step) but not to find the global minimum — different initialisations produce different results.

## Colour quantisation vs. segmentation

This demo performs **colour quantisation**: every pixel in the output is replaced by its centroid's colour, reducing the image to exactly $k$ distinct colours. This is the algorithm used in GIF compression and palette-based image formats.

When objects in an image happen to have distinct colours (a red car on a grey road, a green apple on a white table), colour quantisation also produces a rough *segmentation* — each segment corresponds to a cluster. This breaks down when objects share colours or when lighting creates gradients across a uniform surface.

## Choosing k

| k | Effect |
|---|---|
| 2–3 | Coarse foreground/background split, heavy colour loss. |
| 4–8 | Recognisable image with a distinct palette. |
| 8–16 | Most structural detail preserved; subtle colours may merge. |
| > 16 | Near-lossless for natural images. |

There is no universally correct $k$ — it depends on the image and the task. Methods like the **elbow criterion** (plot $J$ vs $k$ and look for the kink) or the **silhouette score** can help choose automatically.

## Live demo

<iframe
  src="/train-deep-learning/cv-color-cluster/"
  title="CV Lab 4 — Colour Clustering"
  style="width:100%; min-height:520px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to try

- Set $k = 2$ and observe which colours end up on each side of the boundary.
- Increase $k$ until the gradient background is faithfully reproduced — note how the palette grows.
- Click "New image" to get a different scene and run k-means again — the result depends on what colours dominate.
- Run k-means twice on the same image with the same $k$ — do you always get the same palette? (Probably not, because random initialisation varies.)

## Key takeaways

- K-means partitions pixels into $k$ groups by minimising within-cluster colour variance.
- It is unsupervised: no labels, no training set, no gradient descent.
- Colour quantisation and coarse segmentation are two faces of the same operation.
- The result is sensitive to initialisation — multiple runs with the best outcome is a standard practice.
