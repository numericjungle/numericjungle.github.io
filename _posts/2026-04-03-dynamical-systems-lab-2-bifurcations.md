---
date: 2026-04-03 09:00:00.000000
layout: post
title: "Dynamical Systems Lab 2 - Bifurcations in 1D"
description: "Derive the three canonical 1D bifurcations from scratch — saddle-node, transcritical, and pitchfork — and read their signatures from live bifurcation diagrams."
tags: [dynamical systems, chaos, nonlinear dynamics]
comments: true
---

As a control parameter changes continuously, the qualitative structure of a dynamical system can change discontinuously. The number of fixed points jumps, or two branches swap stability, or a single equilibrium splits into three. These sudden qualitative changes are **bifurcations**, and cataloguing them is one of the central tasks of nonlinear dynamics.

<!--excerpt-->

## What makes a bifurcation?

Consider a one-parameter family of ODEs $\dot{x} = f(x, r)$. A **bifurcation** occurs at a parameter value $r = r_c$ where the **topological type** of the phase portrait changes — meaning a small perturbation of $r$ around $r_c$ produces a qualitatively different flow.

Formally: $r_c$ is a bifurcation point if $f(x^*, r_c) = 0$ and the **implicit function theorem fails**, i.e.,

$$\frac{\partial f}{\partial x}\bigg|_{(x^*, r_c)} = 0$$

When $\partial f/\partial x \neq 0$ at a fixed point, the implicit function theorem guarantees that the fixed point persists (as a smooth curve in the $(r, x^*)$ plane) and its stability is unchanged. Bifurcations can only happen when the derivative $f'(x^*)$ passes through zero — that is, when a fixed point is **marginally stable**.

## Saddle-node bifurcation

**Normal form:** $\dot{x} = r - x^2$

This is the simplest and most generic 1D bifurcation.

**Fixed points:** Solve $r - x^{*2} = 0 \Rightarrow x^* = \pm\sqrt{r}$. These exist only for $r \geq 0$.

**Stability:** $\partial f / \partial x = -2x^*$, so

$$\frac{\partial f}{\partial x}\bigg|_{x^*=+\sqrt{r}} = -2\sqrt{r} < 0 \quad \text{(stable)}$$
$$\frac{\partial f}{\partial x}\bigg|_{x^*=-\sqrt{r}} = +2\sqrt{r} > 0 \quad \text{(unstable)}$$

**At $r = r_c = 0$:** both branches collide at $x^* = 0$, where $\partial f/\partial x = 0$. For $r < 0$ neither branch exists — the system has no equilibrium at all.

**Physical interpretation:** This models a **fold catastrophe**. As $r$ decreases through zero, a stable equilibrium suddenly disappears — the system has no nearby resting point and must jump to a far-away state. This is the mechanism behind many real-world sudden transitions: the buckling of an elastic beam, the ignition threshold of a laser, population collapse in ecology, voltage collapse in power grids.

**Genericity:** The saddle-node is the *only* generic codimension-1 bifurcation of equilibria. Generically (without special symmetry), all 1D bifurcations near a point where $f = 0$ and $f' = 0$ are locally equivalent to the saddle-node normal form via a smooth change of coordinates.

The conditions for a saddle-node at $(x_c, r_c)$ are:

$$f = 0, \quad \frac{\partial f}{\partial x} = 0, \quad \frac{\partial f}{\partial r} \neq 0, \quad \frac{\partial^2 f}{\partial x^2} \neq 0$$

## Transcritical bifurcation

**Normal form:** $\dot{x} = rx - x^2 = x(r - x)$

**Fixed points:** $x^* = 0$ and $x^* = r$ exist for all $r$.

**Stability:**

$$\frac{\partial f}{\partial x} = r - 2x$$

| Fixed point | $\partial f / \partial x$ | Stability |
|---|---|---|
| $x^* = 0$ | $r$ | Stable for $r < 0$, unstable for $r > 0$ |
| $x^* = r$ | $r - 2r = -r$ | Unstable for $r < 0$, stable for $r > 0$ |

**At $r = 0$:** both branches coincide at $x^* = 0$, with $\partial f / \partial x = 0$. The two branches pass through each other and exchange stability — neither is created nor destroyed.

**Derivation of the exchange:** Note that $f(x, r) = x(r-x)$. Exactly at the bifurcation, $f''(0, 0) = -2 \neq 0$, which satisfies the condition for a transcritical bifurcation:

$$f = 0, \quad \frac{\partial f}{\partial x} = 0, \quad \frac{\partial^2 f}{\partial x \partial r} \neq 0$$

**Physical interpretation:** A transcritical bifurcation requires a **symmetry constraint** — specifically, $x^* = 0$ must be a fixed point for all $r$. This arises naturally whenever the "zero state" (extinction, no oscillation, etc.) is always an equilibrium by the structure of the model, e.g., in population dynamics where $\dot{N} = N \cdot g(N)$ always has the trivial fixed point $N^* = 0$.

## Pitchfork bifurcation (supercritical)

**Normal form:** $\dot{x} = rx - x^3$

**Fixed points:** Factor $f(x) = x(r - x^2)$, giving $x^* = 0$ and $x^* = \pm\sqrt{r}$ (for $r > 0$).

**Stability:** $\partial f / \partial x = r - 3x^2$

- At $x^* = 0$: slope is $r$. Stable for $r < 0$, unstable for $r > 0$.
- At $x^* = \pm\sqrt{r}$: slope is $r - 3r = -2r < 0$. Always stable when they exist.

**The bifurcation diagram** is a pitchfork shape: one branch along $x^* = 0$ (solid for $r < 0$, dashed for $r > 0$) and two branches curving away symmetrically at $\pm\sqrt{r}$ (solid).

**Derivation using implicit differentiation:** Near the bifurcation at $(0, 0)$, write $r \approx 0$ and look for small solutions. From $rx - x^3 = 0$ with $x \neq 0$: $r = x^2$, so the nontrivial branch satisfies $x = \pm\sqrt{r}$. The branch is real only for $r \geq 0$ — the pitchfork bends forward.

**Why symmetry is required:** The equation $\dot{x} = rx - x^3$ is **odd**: $f(-x) = -f(x)$. This $\mathbb{Z}_2$ symmetry ($x \to -x$) forces the bifurcating branches to come in symmetric pairs. Without it, the pitchfork generically breaks into a saddle-node plus an isolated branch (an imperfect bifurcation).

**Physical examples:** The Euler buckling of a slender column, phase transitions in ferromagnets (below $T_c$ the magnetisation $\pm M$ spontaneously breaks rotational symmetry), and pattern formation via Turing instability.

## Pitchfork bifurcation (subcritical)

**Normal form:** $\dot{x} = rx + x^3 - x^5$

The cubic term now has the **wrong sign** — it provides positive rather than negative nonlinear feedback.

For small $|x|$ with $r < 0$: two unstable fixed points at $x^* \approx \pm\sqrt{|r|}$ coexist with the stable origin. As $r \to 0^-$ they approach the origin, collide with it in a subcritical pitchfork bifurcation, and the origin loses stability at $r = 0$.

The $-x^5$ term provides the eventual saturation. The subcritical pitchfork produces a **hysteresis loop**: two stable states coexist (the origin and the far-away stable branches produced by the outer saddle-node event), and which state the system occupies depends on its history, not just the current $r$.

## Codimension

The **codimension** of a bifurcation is the number of parameters that must be tuned simultaneously to encounter it. Higher codimension bifurcations are less generic but arise in symmetric or special systems:

- Codimension 1: saddle-node, transcritical, pitchfork, Hopf (Lab 9)
- Codimension 2: cusp ($\dot{x} = r_1 + r_2 x - x^3$), Bogdanov–Takens (2D)
- Codimension 3: swallowtail, butterfly

## Live demo

Select a bifurcation type from the dropdown and drag the parameter slider. The bifurcation diagram (fixed point value vs. $r$) fills the canvas: solid green for stable branches, dashed red for unstable. The vertical gold cursor shows the current $r$; colored dots mark the fixed points at that value. The info panel displays analytical values.

<iframe
  src="/train-deep-learning/ds-bifurcations/"
  title="DS Lab 2 — Bifurcation Diagram Explorer"
  style="width:100%; min-height:560px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe from the demo

**Saddle-node:**
- Sweep $r$ from $-2$ to $+2$. For $r < 0$: no fixed points, the info panel reads "none." At $r = 0$: a single dot appears. For $r > 0$: two dots separate — one stable (green), one unstable (red).
- Note that the two branches emerge tangentially (quadratic root), not at an angle — the hallmark of a saddle-node.

**Transcritical:**
- Both branches always exist. Sweep $r$ across zero and watch the color coding of $x^* = 0$ and $x^* = r$ swap simultaneously.
- At $r = 0$ both are at the same point and marginally stable.

**Supercritical pitchfork:**
- For $r < 0$: one stable branch at origin. At $r = 0$: origin becomes marginal. For $r > 0$: origin turns red, two green branches sprout symmetrically.
- The shape is a literal pitchfork — a handle plus two tines.

**Subcritical pitchfork:**
- For $r < 0$: origin is stable AND two unstable branches exist (the dashed red inner arms). This is the hysteresis region where two stable states coexist (the origin, and the outer stable branches formed by an outer saddle-node).
- At $r = 0$: the unstable branches reach the origin and destabilise it — hard loss of stability with a jump.

## Key takeaways

- A bifurcation occurs when $f(x^*, r_c) = 0$ and $\partial f / \partial x |_{x^*, r_c} = 0$ simultaneously.
- The saddle-node is the only generic codimension-1 bifurcation: it creates and destroys pairs of fixed points via a square-root branch.
- The transcritical and pitchfork require symmetry ($x^* = 0$ is always an equilibrium, or the vector field is odd) and are structurally fragile without that symmetry.
- The subcritical pitchfork produces hysteresis — the attractor chosen depends on history, not just the current parameter value.
