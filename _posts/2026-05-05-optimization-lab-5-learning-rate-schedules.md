---
date: 2026-05-05 09:00:00.000000
layout: post
title: "Optimization Lab 5 - Learning Rate Schedules"
description: "Compare constant, step, cosine, and warmup-plus-cosine schedules to see why changing the learning rate over time matters as much as choosing the optimizer itself."
tags: [deep learning, optimization]
comments: true
---

Choosing an optimizer is only half the story. The other half is deciding how its learning rate should evolve during training. A good schedule is often the difference between fast progress, late stability, and complete failure.

<!--excerpt-->

## Why a fixed learning rate is rarely ideal

Early in training, gradients are large and parameters are far from a good region. Large steps are useful because we want to move quickly.

Late in training, we are usually trying to refine a nearly good solution. Smaller steps are better because:

- the local curvature may be sharper
- mini-batch noise dominates
- we want the optimizer to settle instead of jitter

That already suggests the key principle:

> Start relatively large, end relatively small.

## Common schedules

### Constant

$$
\eta_t = \eta_0
$$

The baseline. Simple, but it keeps the same aggressiveness forever.

### Step decay

$$
\eta_t = \eta_0 \gamma^{\lfloor t / T \rfloor}
$$

Every $T$ steps or epochs, multiply by a factor $\gamma < 1$. This is one of the oldest and still one of the most common schedules.

### Cosine decay

$$
\eta_t = \eta_0 \cdot \frac{1}{2}\left(1 + \cos\frac{\pi t}{T_{\max}}\right)
$$

The rate decreases smoothly instead of dropping abruptly. This tends to make the late stage of training more stable.

### Warmup + cosine

Warmup starts from a small learning rate and increases linearly for the first few steps, then switches to cosine decay. This is now standard in large-batch training and transformers because the earliest gradients can be untrustworthy or badly scaled.

## Schedules vs optimizers

It is tempting to think Adam or SGD determines everything. In practice:

- Adam with a bad schedule can still plateau or diverge
- SGD with momentum and a good schedule can outperform Adam on many vision tasks
- large models often rely on warmup even when the optimizer itself is unchanged

The schedule controls **when** the optimizer explores and **when** it settles.

## Live demo

All four runs use the same noisy quadratic objective and the same gradient noise sequence. The only difference is the learning-rate schedule:

- constant
- step decay
- cosine
- warmup + cosine

<iframe
  src="/train-deep-learning/opt-lr-schedules/"
  title="Optimization Lab 5 - Learning Rate Schedules"
  style="width:100%; min-height:660px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe

- Constant learning rate falls fast at first but often keeps bouncing near the minimum.
- Step decay introduces visible changes in behaviour exactly when the drops happen.
- Cosine decay tends to be smoother, especially late in training.
- Warmup is slowest for the first few steps on purpose, but it avoids unstable early jumps.

## Key takeaways

- A schedule controls the exploration-to-refinement trade-off over time.
- Constant learning rates are often too rigid for long deep-learning runs.
- Step and cosine decay reduce late-stage noise without sacrificing early speed.
- Warmup is especially useful when the very first gradients are large, noisy, or poorly calibrated.
