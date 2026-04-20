---
date: 2026-04-20 11:30:00.000000
layout: post
title: "CV Lab 6 - Saliency Maps"
description: "Train a digit classifier, then compute occlusion sensitivity maps to see which pixels drive each prediction."
tags: [computer vision, deep learning]
comments: true
---

A CNN achieves high test accuracy — but *which pixels is it actually using to make that decision*? Saliency maps answer this question by measuring how much each region of the input contributes to the predicted class score. This lab uses **occlusion sensitivity**, a simple and interpretable technique: grey out one patch at a time, re-run inference, and record how much the confidence drops.

<!--excerpt-->

## Occlusion sensitivity

Let $f_c(x)$ be the network's softmax probability for class $c$ given input $x$. For each patch at position $(p_x, p_y)$:

1. Create a modified input $\tilde{x}^{(p)}$ by replacing that patch with a neutral grey value (zero after normalisation).
2. Compute $f_c(\tilde{x}^{(p)})$.
3. Assign saliency $s(p_x, p_y) = f_c(x) - f_c(\tilde{x}^{(p)})$.

A high saliency value means removing that patch hurt confidence significantly — the patch is *important* for the prediction. A low (or negative) value means the patch was irrelevant or even suppressing the correct class.

$$
s(p_x, p_y) = f_c(x) - f_c\!\left(\tilde{x}^{(p)}\right)
$$

## Why not use gradients directly?

The cleaner mathematical definition of saliency uses the input gradient:

$$
\nabla_x f_c(x) \Big|_{x = x_0}
$$

Each entry of this gradient measures how much increasing that pixel value would change the class score — equivalent to saliency. Gradient-based maps are faster to compute (one backward pass instead of dozens of forward passes) but require access to the computational graph. In ConvNetJS — a library without automatic differentiation — occlusion sensitivity is simpler to implement and arguably more interpretable for newcomers.

## What the colours mean

The heatmap uses a blue-red scale:
- **Warm (red/orange)** — high saliency: the network's confidence falls significantly when this patch is hidden.
- **Cool (blue/purple)** — low saliency: removing this patch has little effect.

The **overlay** panel blends the original digit (grey) with the heatmap (colour), making it easy to see whether the network focuses on the digit strokes or the background.

## What good saliency looks like

For a well-trained MNIST classifier, saliency maps should light up on the ink strokes of the digit — specifically the parts that distinguish it from the closest alternative class. For example:

- A **7** might have high saliency on the horizontal bar at the top (distinguishing it from a 1).
- A **9** might have high saliency on the closed loop at the top (distinguishing it from a 4).
- A **0** might have high saliency along the entire oval boundary.

If saliency is spread uniformly across the image including blank background, the network has not learned to ignore irrelevant pixels — a sign of insufficient training or overfitting to dataset-specific artefacts.

## Live demo

First click **Train** to begin training the CNN on MNIST. After a few hundred steps, click **Saliency** to compute the occlusion map for the current test image. Use the **← →** buttons to browse other test digits.

<iframe
  src="/train-deep-learning/cv-saliency/"
  title="CV Lab 6 — Saliency Maps"
  style="width:100%; min-height:660px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Limitations of saliency methods

Occlusion sensitivity is **model-agnostic** (any black-box classifier) but slow: an image of size $24 \times 24$ with $4 \times 4$ patches requires 36 forward passes per image. More importantly, it only measures which patches are *collectively* important, not which individual pixels are. Methods like Grad-CAM, Integrated Gradients, and SHAP provide finer-grained attribution but require more implementation effort.

## Key takeaways

- Saliency maps reveal *why* a network makes a prediction, not just *what* it predicts.
- Occlusion sensitivity: hide patches one at a time, measure confidence drop — no gradient access required.
- A confident, correct prediction paired with a diffuse saliency map is a warning sign.
- Interpretability is not the same as correctness — a model can focus on the right pixels for the wrong reasons.
