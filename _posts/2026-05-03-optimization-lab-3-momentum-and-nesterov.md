---
date: 2026-05-03 09:00:00.000000
layout: post
title: "Optimization Lab 3 - Momentum and Nesterov Acceleration"
description: "See why ravines make plain gradient descent zig-zag, then compare heavy-ball momentum and Nesterov's look-ahead correction on the same loss."
tags: [deep learning, optimization]
comments: true
---

Gradient descent reacts only to the **current** gradient. If successive gradients alternate direction across a narrow valley, the optimizer wastes step after step undoing its own sideways motion. Momentum fixes that by remembering where it was already heading.

<!--excerpt-->

## Why ravines are hard

Suppose one direction has much larger curvature than another. Then the gradient has a large component across the valley walls and a much smaller component along the valley floor.

Plain gradient descent updates

$$
\theta_{t+1} = \theta_t - \eta g_t
$$

with $g_t = \nabla L(\theta_t)$.

In a ravine, the optimizer repeatedly:

1. steps across the steep wall
2. overshoots
3. receives a gradient pointing back the other way
4. overshoots again

The result is the familiar zig-zag pattern.

## Heavy-ball momentum

Momentum introduces a velocity variable $v_t$:

$$
v_t = \beta v_{t-1} - \eta g_t
$$
$$
\theta_{t+1} = \theta_t + v_t
$$

where $\beta \in [0,1)$ controls how much of the previous velocity is retained.

Interpretation:

- in directions where gradients keep flipping sign, the velocity cancels the oscillation
- in directions where gradients keep pointing the same way, velocity accumulates and speeds motion up

That is why momentum helps exactly where GD struggles most.

## Nesterov acceleration

Nesterov momentum looks ahead before computing the gradient:

$$
v_t = \beta v_{t-1} - \eta \nabla L(\theta_t + \beta v_{t-1})
$$
$$
\theta_{t+1} = \theta_t + v_t
$$

Instead of asking "what is the slope here?", it asks "what is the slope where my momentum is about to carry me?".

This extra correction often turns the optimizer earlier near a valley floor, making it less likely to overshoot late in training.

## Why momentum is so common in deep learning

Momentum is cheap:

- no Hessian
- no per-parameter second moment
- one extra velocity vector

That is why SGD with momentum remains a strong baseline for vision models, contrastive learning, and many large-batch training setups. When people say "SGD" in deep learning, they often really mean **SGD with momentum**.

## Live demo

The loss is a rotated quadratic ravine. All three methods start from the same point and see the same geometry:

- GD
- heavy-ball momentum
- Nesterov

<iframe
  src="/train-deep-learning/opt-momentum/"
  title="Optimization Lab 3 - Momentum and Nesterov"
  style="width:100%; min-height:600px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe

- Increase the condition number. The blue GD path becomes increasingly inefficient.
- Keep curvature fixed and increase $\beta$. Gold and green paths move more decisively along the valley.
- Compare momentum vs Nesterov near the minimum. Nesterov usually bends inward a little earlier.
- Push the learning rate too high. Momentum helps, but it does not repeal stability limits.

## Key takeaways

- Momentum stores a velocity vector, not just the current gradient.
- It suppresses oscillation across steep directions and amplifies progress along flat ones.
- Nesterov adds a look-ahead gradient that usually improves late-stage control.
- Momentum is one of the cheapest and most effective upgrades over plain gradient descent.
