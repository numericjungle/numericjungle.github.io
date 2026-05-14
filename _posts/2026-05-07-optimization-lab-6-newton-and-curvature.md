---
date: 2026-05-07 09:00:00.000000
layout: post
title: "Optimization Lab 6 - Newton's Method and Curvature"
description: "Build the second-order quadratic model behind Newton's method, compare it with gradient descent on Rosenbrock's valley, and see why full Hessian methods are rare in deep learning."
tags: [deep learning, optimization]
comments: true
---

Gradient descent uses only first-order information: the slope. Newton's method goes one level deeper and asks for the local curvature as well. In principle that is exactly what we want. In practice, deep learning makes the price of curvature brutally high.

<!--excerpt-->

## From first-order to second-order optimization

Around the current iterate $\theta_t$, take a second-order Taylor expansion:

$$
L(\theta_t + p) \approx L(\theta_t) + g_t^\top p + \frac{1}{2} p^\top H_t p
$$

where

$$
g_t = \nabla L(\theta_t), \qquad H_t = \nabla^2 L(\theta_t).
$$

To minimize this local quadratic model, differentiate with respect to $p$:

$$
g_t + H_t p = 0
$$

so the Newton step is

$$
p_t = -H_t^{-1} g_t.
$$

Then

$$
\theta_{t+1} = \theta_t + p_t = \theta_t - H_t^{-1} g_t.
$$

This is gradient descent with the gradient rescaled by curvature.

## Why Newton can be dramatically faster

On a quadratic objective,

$$
L(\theta) = \frac{1}{2}\theta^\top H \theta + b^\top \theta + c,
$$

Newton's method jumps directly to the minimizer in one step, because the quadratic model is exact.

That sounds unbeatable. The catch is that neural networks are not small quadratics:

- the Hessian is enormous
- forming it explicitly is expensive
- inverting it is even more expensive
- away from minima, it may be indefinite or nearly singular

So even though the formula is elegant, naive Newton updates are rarely practical for deep nets.

## Damping and trust-region thinking

When the Hessian is unstable, a standard fix is **damping**:

$$
p_t = -(H_t + \lambda I)^{-1} g_t
$$

with $\lambda > 0$.

Interpretation:

- if $\lambda$ is large, the step becomes more gradient-like
- if $\lambda$ is small and $H_t$ is well-conditioned, the step becomes more Newton-like

This is the basic idea behind Levenberg-Marquardt and trust-region methods.

## What deep learning uses instead

Because full Newton is too expensive, large-scale training usually relies on approximations:

- quasi-Newton methods such as L-BFGS
- Gauss-Newton approximations
- natural-gradient and Fisher-matrix approximations
- Kronecker-factored methods such as K-FAC

These methods try to capture some curvature information without storing the full Hessian.

## Live demo

The demo compares:

- gradient descent
- pure Newton
- damped Newton

on the classic Rosenbrock function, whose banana-shaped valley makes first-order methods work hard. The blue arrow is the raw negative gradient; the gold arrow is the Newton direction.

<iframe
  src="/train-deep-learning/opt-newton/"
  title="Optimization Lab 6 - Newton and Curvature"
  style="width:100%; min-height:620px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe

- Gradient descent keeps crossing the valley because the gradient points mostly sideways.
- Newton often turns sharply toward the valley floor because the Hessian rescales directions by curvature.
- When the Hessian becomes awkward, the damped method behaves more conservatively than pure Newton.
- The eigenvalue readout explains why some steps are trustworthy and others are dangerous.

## Key takeaways

- Newton's method comes from minimizing the second-order Taylor approximation of the loss.
- Curvature-aware steps can be far more direct than plain gradient descent.
- The obstacle in deep learning is not theory but scale: Hessians are huge and expensive.
- Modern second-order methods are mostly clever approximations to the ideal update $-H^{-1}g$.
