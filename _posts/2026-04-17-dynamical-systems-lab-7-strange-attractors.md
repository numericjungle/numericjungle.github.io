---
date: 2026-04-17 09:00:00.000000
layout: post
title: "Dynamical Systems Lab 7 - Strange Attractors and Fractals"
description: "Derive the Hénon map as a Poincaré section, compute its Jacobian and Lyapunov exponent, and zoom in on the Cantor-set transverse structure of the strange attractor."
tags: [dynamical systems, chaos, nonlinear dynamics]
comments: true
---

A **strange attractor** is the geometric skeleton of chaos. It is the set that chaotic trajectories are drawn toward — but unlike a fixed point or a limit cycle, it is a **fractal**: a set with a non-integer Hausdorff dimension that looks the same at every magnification. The Hénon map is the simplest invertible map with a strange attractor, and zooming into it reveals the infinite layered structure that characterises all chaotic dissipative systems.

<!--excerpt-->

## What is an attractor?

Formally, an **attractor** of a dynamical system is a compact invariant set $\mathcal{A}$ such that:

1. **Invariance:** $\Phi_t(\mathcal{A}) = \mathcal{A}$ for all $t$ (the flow maps $\mathcal{A}$ to itself).
2. **Attraction:** There is a neighbourhood $U \supset \mathcal{A}$ such that every trajectory starting in $U$ converges to $\mathcal{A}$.
3. **Indecomposability:** $\mathcal{A}$ cannot be split into two disjoint invariant pieces.

Fixed points and limit cycles are the simple attractors. A **strange attractor** is an attractor with a fractal (non-integer-dimensional) geometry.

## The Hénon map: derivation

Michel Hénon (1976) constructed his map as a model for the Poincaré section of the Lorenz system. The idea: intersect a 3D flow with a 2D surface (the Poincaré section). The return map on this surface is a 2D discrete map that captures the folding and stretching of the original 3D attractor.

Hénon's map takes the simplest form with two key properties of the Lorenz section:

1. **Dissipation:** the map contracts area (models volume contraction of the 3D flow).
2. **One-dimensional folding:** the map folds like a unimodal 1D map in one direction.

The result is the **Hénon map**:

$$x_{n+1} = 1 - a\,x_n^2 + y_n$$
$$y_{n+1} = b\,x_n$$

The parameter $a$ controls the degree of folding (nonlinearity), and $b$ controls the amount of contraction.

**Jacobian:** The Jacobian matrix of the map is

$$J = \begin{pmatrix} -2ax_n & 1 \\ b & 0 \end{pmatrix}$$

$$\det J = -b$$

Since $\det J = -b$ is constant, the map contracts (or expands) all areas by the same factor $|b|$ at every step. For $|b| < 1$ the map is dissipative: volumes shrink. For classic parameters $b = 0.3$: every area element shrinks by a factor $0.3$ per iterate. After $N$ steps: area $\to |b|^N \cdot \text{area} \to 0$. The attractor has **zero area**.

## Lyapunov exponents of the Hénon map

The two Lyapunov exponents $\lambda_1 \geq \lambda_2$ satisfy the constraint

$$\lambda_1 + \lambda_2 = \ln|\det J| = \ln|b|$$

For $b = 0.3$: $\lambda_1 + \lambda_2 = \ln 0.3 \approx -1.204$.

Numerically (for $a = 1.4$, $b = 0.3$): $\lambda_1 \approx +0.42$ and $\lambda_2 \approx -1.62$.

The positive $\lambda_1$ confirms chaos: nearby points diverge exponentially along the unstable (stretching) direction. The negative $\lambda_2$ confirms contraction along the stable (folding) direction. The combination of stretching and folding produces the fractal microstructure.

## Fractal geometry of the Hénon attractor

**Box-counting dimension:** Cover the attractor with a grid of boxes of side $\epsilon$ and count the number of non-empty boxes $N(\epsilon)$. The box-counting dimension is

$$d_0 = \lim_{\epsilon\to 0}\frac{\ln N(\epsilon)}{\ln(1/\epsilon)}$$

For a curve: $d_0 = 1$. For a surface: $d_0 = 2$. For the Hénon attractor: $d_0 \approx 1.26$.

**Why $d_0 \approx 1.26$ and not an integer:**

The Hénon attractor looks like a curve ($d = 1$) when viewed at large scales — it resembles a banana-shaped strip. But zooming in reveals that the strip consists of two sub-strips, each of which consists of two sub-strips, and so on. The cross-section in the transverse direction is a **Cantor set** — a set of zero length but positive fractal dimension $d_{\text{Cantor}} \approx 0.26$. The total dimension is $1 + 0.26 = 1.26$.

**Kaplan-Yorke dimension:** Using the Lyapunov exponents:

$$d_{KY} = 1 + \frac{\lambda_1}{|\lambda_2|} = 1 + \frac{0.42}{1.62} \approx 1.26$$

The agreement with box-counting is not a coincidence — this is a consequence of the **Kaplan-Yorke conjecture** (proved in many cases by Ledrappier and Young).

## Fractal dimension: Hausdorff dimension

The most rigorous notion of fractal dimension is the **Hausdorff dimension** $d_H$. For a set $S$ in $\mathbb{R}^n$, cover $S$ with balls of diameter $\leq \epsilon$ and minimise the sum $\sum_i \epsilon_i^d$. Define

$$\mathcal{H}^d(S) = \lim_{\epsilon\to 0}\inf_{\text{covers}} \sum_i (\text{diam}\,U_i)^d$$

There is a critical value $d_H$ at which $\mathcal{H}^d$ jumps from $\infty$ to $0$. This is the Hausdorff dimension. For the Hénon attractor, $d_H \approx d_0 \approx 1.26$.

## The stretch-and-fold mechanism

The mechanism producing fractal attractors is universal:

1. **Stretch:** the positive Lyapunov exponent expands distances exponentially in one direction.
2. **Fold:** the system's boundedness requires the expanded strip to fold back on itself.
3. **Repeat:** each return to a region produces a new fold. After infinitely many folds, the cross-section is a Cantor set.

The Hénon map makes this explicit in two dimensions. In the $x$-direction, the $-ax^2$ term folds the strip. In the $y$-direction, $y_{n+1} = bx_n$ contracts the width. The composition creates an infinitely layered folded structure.

## Parameter dependence and the period-doubling cascade

As $a$ increases from 0 to 2 (with $b = 0.3$ fixed), the Hénon map undergoes a sequence of period-doubling bifurcations analogous to the logistic map:

| $a$ | Attractor |
|---|---|
| $a < 0.3665...$ | Stable period-1 orbit |
| $a \approx 0.37$ | Period-2 |
| $a \approx 0.91$ | Period-4 |
| $a \approx 1.025$ | Period-8, 16, … (cascade) |
| $a \approx 1.055$ | Onset of chaos |
| $a = 1.4$ | Classic strange attractor |

The Feigenbaum constant $\delta \approx 4.669$ governs the ratios of successive bifurcation intervals — universal, independent of $b$.

## Live demo

The demo plots the Hénon attractor one point at a time, accumulating up to 120,000 points. Use the zoom slider (up to 20×) to magnify the attractor and reveal the transverse Cantor structure. Drag the canvas to pan. Try the **Age**, **Density**, and **Velocity** color modes to highlight different aspects of the attractor's geometry. Adjust $a$ and $b$ to move through the parameter space.

<iframe
  src="/train-deep-learning/ds-henon/"
  title="DS Lab 7 — Hénon Map"
  style="width:100%; min-height:560px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe from the demo

**Classic parameters ($a = 1.4$, $b = 0.3$):**
- At zoom 1×: the attractor resembles a curved band (banana shape).
- At zoom 5×: the band resolves into 2 sub-bands separated by a gap.
- At zoom 10×: each sub-band resolves into 2 more. This self-similar splitting is the Cantor structure.
- The **Age** color mode shows the trajectory sweeping along the attractor — note it can visit any part of the attractor, not cycling predictably.

**Reducing $a$ (e.g. to $a = 0.9$):**
- The attractor collapses to a small set of discrete points (periodic orbit). The map is no longer chaotic.
- The **Lyapunov exponent** would be negative here.

**Reducing $b$ (e.g. to $b = 0.05$):**
- The contraction is much stronger; the attractor thins to a nearly 1D curve. The box-counting dimension approaches 1.
- Extreme $b \to 0$: the Hénon map degenerates to the logistic map $x_{n+1} = 1 - ax_n^2$.

**Increasing $b$ (e.g. to $b = 0.9$):**
- Less dissipation; the attractor thickens. For $|b| > 1$ the map is area-expanding and the attractor becomes a strange repeller.

## Key takeaways

- The Hénon map is a minimal model of the Poincaré section of a 3D chaotic flow; its constant Jacobian determinant gives a simple formula $\lambda_1 + \lambda_2 = \ln|b|$.
- Strange attractors have fractal dimension because stretching-and-folding creates infinitely fine transverse structure — visible as a Cantor set when zoomed in.
- The Kaplan-Yorke formula $d_{KY} = 1 + \lambda_1/|\lambda_2|$ connects Lyapunov exponents to fractal dimension; it agrees with box-counting to high accuracy.
- The period-doubling cascade in the Hénon map obeys the same Feigenbaum constant $\delta \approx 4.669$ as the logistic map — a signature of universality.
