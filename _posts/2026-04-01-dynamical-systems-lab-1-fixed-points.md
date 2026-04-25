---
date: 2026-04-01 09:00:00.000000
layout: post
title: "Dynamical Systems Lab 1 - Fixed Points and Stability"
description: "From Taylor expansion to the phase line — derive the stability criterion from first principles and watch trajectories converge or diverge in a live 1D flow."
tags: [dynamical systems, chaos, nonlinear dynamics]
comments: true
---

Before there are attractors, strange or otherwise, there are **fixed points** — states where a system is content to sit forever. Understanding when those states are stable, and why, is the first building block of all of nonlinear dynamics.

<!--excerpt-->

## The autonomous ODE

A scalar, first-order, autonomous ordinary differential equation (ODE) takes the form

$$\dot{x} \equiv \frac{dx}{dt} = f(x)$$

*Autonomous* means $f$ depends only on the state $x$ and not on time $t$ explicitly. The function $f : \mathbb{R} \to \mathbb{R}$ is called the **vector field** (in one dimension, a scalar field) — it assigns an instantaneous velocity $\dot{x}$ to every position $x$.

Geometrically, think of $x(t)$ as a particle sliding along the real line. At any location $x$, the particle's speed and direction are given by $f(x)$:

- $f(x) > 0$: particle moves right ($x$ increasing)
- $f(x) < 0$: particle moves left ($x$ decreasing)
- $f(x) = 0$: particle is stationary

The **existence and uniqueness theorem** guarantees that for a Lipschitz-continuous $f$, there is exactly one trajectory through each initial condition $x(0) = x_0$. Crucially, distinct trajectories never cross each other (because if they did, they would share an initial condition and then violate uniqueness).

This no-crossing rule has a profound consequence: **in 1D, every trajectory must converge to a fixed point, diverge to $\pm\infty$, or (in special cases) approach one in infinite time**. Oscillations and chaos are impossible in 1D autonomous flows.

## Fixed points

A **fixed point** (equilibrium, steady state, or rest point) $x^*$ satisfies

$$f(x^*) = 0$$

Fixed points are the zeroes of the vector field. If the system starts exactly at $x^*$, it stays there forever: $x(t) = x^*$ for all $t \geq 0$ is a valid (constant) solution.

The central question of local stability is: if the system starts slightly away from $x^*$, does it return, or does it drift further away?

## Linear stability analysis

**Step 1 — Perturb.** Let $x(t) = x^* + \xi(t)$ where $\xi(t)$ is a small displacement. Substitute into the ODE:

$$\dot{\xi} = f(x^* + \xi)$$

**Step 2 — Taylor expand** $f$ around $x^*$:

$$f(x^* + \xi) = f(x^*) + f'(x^*)\,\xi + \frac{1}{2}f''(x^*)\,\xi^2 + \cdots$$

Since $f(x^*) = 0$ (definition of a fixed point) and $\xi$ is small, we keep only the linear term:

$$\dot{\xi} \approx f'(x^*)\,\xi$$

**Step 3 — Solve.** This is a linear ODE with constant coefficient $\lambda \equiv f'(x^*)$:

$$\xi(t) = \xi_0\, e^{\lambda t}$$

**Step 4 — Classify.** The behaviour is determined by the sign of $\lambda$:

| $\lambda = f'(x^*)$ | Fixed point type | Behaviour |
|---|---|---|
| $\lambda < 0$ | **Stable** (attractor, sink) | $\xi \to 0$: perturbations decay exponentially |
| $\lambda > 0$ | **Unstable** (repeller, source) | $\xi \to \infty$: perturbations grow exponentially |
| $\lambda = 0$ | Marginal (non-hyperbolic) | Linearisation fails; need higher-order terms |

The case $\lambda = 0$ requires inspecting $f''(x^*)$ or even higher derivatives. If $f(x) = cx^n + \cdots$ near $x^*$ with $c \neq 0$ and $n \geq 2$ even, the fixed point is **half-stable** (attracting from one side, repelling from the other); if $n$ is odd, it is either semi-stable or the fixed point is part of a continuum.

## The phase line (phase portrait in 1D)

The **phase line** is a graphical representation of all the information in $f(x)$. Draw the real axis; mark each zero of $f$ (the fixed points); between zeros, draw arrows pointing right where $f > 0$ and left where $f < 0$.

This immediately reveals:
- Which fixed points are stable (arrows on both sides pointing toward them)
- Which are unstable (arrows on both sides pointing away)
- The **basin of attraction** of each stable fixed point (the interval from which trajectories flow toward it)
- Global behaviour for every initial condition

Importantly, to draw the phase line you only need to know the **sign** of $f$ between its zeros — you do not need to solve the ODE.

## Worked examples

### Example 1: saddle-node normal form, $\dot{x} = r - x^2$

Fixed points: $r - x^{*2} = 0 \Rightarrow x^* = \pm\sqrt{r}$ (requires $r \geq 0$).

Stability: $f'(x) = -2x$, so $f'(\sqrt{r}) = -2\sqrt{r} < 0$ (stable) and $f'(-\sqrt{r}) = 2\sqrt{r} > 0$ (unstable).

- $r < 0$: no fixed points; every trajectory flows to $-\infty$.
- $r = 0$: one marginal fixed point at $x^* = 0$ ($f'(0) = 0$, $f(x) = -x^2 \leq 0$, so it is a half-stable point attracting from the left only).
- $r > 0$: two fixed points born simultaneously in a **saddle-node bifurcation**.

### Example 2: transcritical normal form, $\dot{x} = rx - x^2 = x(r-x)$

Fixed points: $x^* = 0$ and $x^* = r$ for all $r$.

Stability: $f'(x) = r - 2x$, so $f'(0) = r$ and $f'(r) = -r$.

- $r < 0$: origin is stable ($f'(0) = r < 0$), $x^* = r$ is unstable.
- $r > 0$: origin unstable, $x^* = r$ stable. The two branches exchange stability at $r = 0$.

This exchange — not creation or destruction, but **transfer of stability** — is the transcritical bifurcation.

### Example 3: pitchfork normal form, $\dot{x} = rx - x^3$

Fixed points: $x^*(r - x^{*2}) = 0 \Rightarrow x^* = 0$ and $x^* = \pm\sqrt{r}$ (for $r > 0$).

Stability: $f'(x) = r - 3x^2$.

- $f'(0) = r$: origin stable for $r < 0$, unstable for $r > 0$.
- $f'(\pm\sqrt{r}) = r - 3r = -2r < 0$: the two bifurcating branches are always stable (for $r > 0$).

At $r = 0$ the origin loses stability and two new symmetric stable equilibria appear — the **supercritical pitchfork bifurcation** and the simplest example of spontaneous symmetry breaking. The system is symmetric under $x \to -x$, and the bifurcating state breaks this symmetry by choosing one branch.

### Example 4: multiple fixed points, $\dot{x} = x(1-x)(x+0.8)$

This cubic has three explicit zeros: $x^* \in \{-0.8, 0, 1\}$. The sign of $f$ between them determines stability:
- $x < -0.8$: $f < 0$, flows left to $-\infty$.
- $-0.8 < x < 0$: $f > 0$, flows right toward $x^* = 0$.
- $0 < x < 1$: $f < 0$, flows left toward $x^* = 0$.
- $x > 1$: $f > 0$, flows right to $+\infty$.

So $x^* = 0$ is stable, $x^* = -0.8$ and $x^* = 1$ are unstable. Reading this directly from the phase line takes seconds; solving the ODE explicitly would not.

## Existence and uniqueness, and why 1D cannot oscillate

The no-crossing theorem deserves emphasis. Suppose trajectory $A$ passes through $x_1$ at time $t_1$, and trajectory $B$ passes through $x_1$ at time $t_2$. By uniqueness, both trajectories are identical after that meeting point. Therefore two distinct trajectories can never occupy the same point.

Now consider an oscillation: the state $x(t)$ would have to return to a previous value. But then the trajectory would cross itself — impossible. Hence:

> **Theorem:** Autonomous 1D flows cannot oscillate. Every trajectory either converges to a fixed point or diverges to $\pm\infty$.

Oscillations become possible in 2D (limit cycles, Lab 4), and chaos requires at least 3D (Lorenz, Lab 5).

## Live demo

Five different 1D systems are loaded in the dropdown. For each system, you can adjust the parameter $r$ and the initial condition $x_0$. The top half of the canvas shows the graph of $f(x)$, with fixed points marked where $f$ crosses zero. The bottom half shows the phase line with flow arrows. The gold dot is the trajectory — it integrates $\dot{x} = f(x)$ in real time using a 4th-order Runge-Kutta solver.

<iframe
  src="/train-deep-learning/ds-phase-line/"
  title="DS Lab 1 — 1D Phase Line Explorer"
  style="width:100%; min-height:540px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe from the demo

**Saddle-node** ($\dot{x} = r - x^2$):
- Set $r = -1$: no zero crossings in the $f(x)$ graph; all arrows on the phase line point left; the dot slides relentlessly toward $-\infty$.
- Increase $r$ through zero: watch two fixed points appear simultaneously at $x^* = 0$ when $r = 0$, then separate symmetrically as $r$ grows.
- At $r = 1$: the stable point (green) sits at $x^* = +1$ and the unstable (red) at $x^* = -1$. Try placing the IC between them vs. outside.

**Pitchfork** ($\dot{x} = rx - x^3$):
- At $r = -1$: single green dot at origin. Place IC anywhere — it always returns to zero.
- Increase $r$ through zero: the green dot at origin turns red exactly at $r = 0$, and two new green dots emerge symmetrically at $x^* = \pm\sqrt{r}$.
- Notice the trajectory "chooses" the nearest stable branch — this is the essence of symmetry breaking.

**Sine** ($\dot{x} = \sin x$):
- Fixed points at $x^* = n\pi$ for all integers $n$, alternating stable and unstable.
- Place IC between $0$ and $\pi$: converges to $\pi$ (stable). Between $\pi$ and $2\pi$: converges to $2\pi$. The basins are the open intervals between unstable zeros.

**Transcritical** ($\dot{x} = rx - x^2$):
- At any $r$, both $x^* = 0$ and $x^* = r$ coexist. Watch which is green (stable) swap as you cross $r = 0$.

## Key takeaways

- A fixed point $x^*$ is stable if $f'(x^*) < 0$ — the derivative of the vector field being negative means the field points *toward* $x^*$ from both sides.
- The linearised equation $\dot{\xi} = \lambda \xi$ with $\lambda = f'(x^*)$ has exact solution $\xi_0 e^{\lambda t}$; all of local stability follows from the sign of this one number.
- The phase line is a complete graphical solution: sign of $f$ between zeros tells you everything about long-time behaviour.
- 1D autonomous flows cannot oscillate; they can only converge, diverge, or approach a fixed point asymptotically.
