---
date: 2026-05-01 09:00:00.000000
layout: post
title: "Optimization Lab 1 - Gradient Descent and the Geometry of Learning"
description: "Derive gradient descent from first principles, relate curvature to learning-rate stability, and watch the update path move across an ill-conditioned loss bowl."
tags: [deep learning, optimization]
comments: true
---

Training a neural network is, at bottom, a problem in **numerical optimization**. We choose parameters $\theta$, define a loss $L(\theta)$, and then repeatedly move $\theta$ in whatever direction makes the loss go down fastest. The simplest version of that idea is **gradient descent**.

<!--excerpt-->

## The optimization problem behind deep learning

Given a dataset $\{(x_i, y_i)\}_{i=1}^N$ and model $f(x;\theta)$, training solves

$$
\min_\theta L(\theta), \qquad L(\theta) = \frac{1}{N}\sum_{i=1}^N \ell\!\bigl(f(x_i;\theta), y_i\bigr)
$$

The loss may be mean-squared error, cross-entropy, contrastive loss, or something more exotic, but the optimization loop is always the same:

1. Compute the gradient $\nabla L(\theta_t)$
2. Take a step downhill
3. Repeat

The gradient points in the direction of **steepest local increase**, so the negative gradient is the direction of steepest local decrease.

## Deriving the update rule

Take a first-order Taylor expansion around the current point $\theta_t$:

$$
L(\theta_t + \Delta) \approx L(\theta_t) + \nabla L(\theta_t)^\top \Delta
$$

If we constrain the step size to $\|\Delta\| = \eta$, the linear term is minimized by choosing $\Delta$ opposite the gradient:

$$
\Delta = -\eta \frac{\nabla L(\theta_t)}{\|\nabla L(\theta_t)\|}
$$

Absorbing the normalization into the learning rate gives the standard update

$$
\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)
$$

where $\eta > 0$ is the **learning rate**.

## Why curvature matters

Near a local minimum $\theta^\*$, the loss is well approximated by a quadratic:

$$
L(\theta^\* + \delta) \approx L(\theta^\*) + \frac{1}{2}\delta^\top H \delta
$$

where $H = \nabla^2 L(\theta^\*)$ is the Hessian. Its eigenvalues measure curvature in different directions:

- Large eigenvalue: steep direction
- Small eigenvalue: flat direction

For a quadratic bowl, gradient descent is stable only if

$$
0 < \eta < \frac{2}{\lambda_{\max}(H)}
$$

If $\eta$ is too small, training crawls. If it is too large, the update overshoots and the loss oscillates or explodes.

The ratio

$$
\kappa = \frac{\lambda_{\max}}{\lambda_{\min}}
$$

is the **condition number**. When $\kappa$ is large, the bowl becomes a narrow ravine: one direction wants tiny steps, the other wants much larger ones. This is the basic geometric reason optimization in deep learning is difficult.

## Why this matters for neural networks

Deep-network losses are not convex quadratics, but locally they still behave like curved surfaces. At every training step the optimizer is effectively navigating a changing, noisy quadratic approximation. The same issues already appear:

- badly scaled directions
- sharp vs flat curvature
- exploding updates from overly large learning rates
- slow progress along shallow directions

The toy 2D bowl in this lab is not a neural network, but it isolates the exact mathematical phenomenon that shows up in large models.

## Live demo

The canvas shows the loss

$$
f(x,y) = \frac{1}{2}(x^2 + \kappa y^2)
$$

with adjustable learning rate $\eta$ and condition number $\kappa$. The gold path is the parameter vector moving under gradient descent. The right panel plots the loss on a log scale.

<iframe
  src="/train-deep-learning/opt-gradient-descent/"
  title="Optimization Lab 1 - Gradient Descent"
  style="width:100%; min-height:560px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe

- Increase $\kappa$ while keeping $\eta$ fixed. The path begins to zig-zag because the steep direction forces repeated overshoot corrections.
- Set $\eta$ near $2/\kappa$. The trajectory becomes marginally stable and starts to bounce.
- Reduce $\eta$ drastically. The path becomes safe but painfully slow.
- Compare the path geometry against the loss plot: visible zig-zag on the left appears as slower decay on the right.

## Key takeaways

- Gradient descent is just repeated application of $\theta \leftarrow \theta - \eta \nabla L(\theta)$.
- The Hessian controls which learning rates are stable.
- Ill-conditioning, not just non-convexity, is a major source of optimization difficulty.
- Most of the optimizers used in deep learning are attempts to fix plain gradient descent's sensitivity to curvature.
