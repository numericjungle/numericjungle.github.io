---
date: 2026-04-24 09:00:00.000000
layout: post
title: "Dynamical Systems Lab 9 - Routes to Chaos"
description: "Derive the logistic map from population dynamics, prove the Feigenbaum constant via renormalisation, and trace the period-doubling cascade with cobweb and bifurcation diagrams side by side."
tags: [dynamical systems, chaos, nonlinear dynamics]
comments: true
---

Chaos is not a destination that a system leaps to abruptly. In most systems there is a precisely structured **route** — a sequence of bifurcations that systematically destroy order before chaos takes hold. The best understood route is **period doubling**: at each step the orbit's period doubles, the doubling intervals shrink at a universal ratio, and at the accumulation point chaos begins. The ratio is the Feigenbaum constant $\delta \approx 4.669$, independent of the specific equations.

<!--excerpt-->

## The logistic map: derivation from population dynamics

Consider a population $N_t$ with discrete generations. The simplest model with density-dependent regulation is

$$N_{t+1} = r\, N_t\!\left(1 - \frac{N_t}{K}\right)$$

where $r > 0$ is the intrinsic growth rate and $K$ the carrying capacity. Non-dimensionalise by $x_t = N_t / K$:

$$x_{t+1} = r\, x_t(1-x_t)$$

This is the **logistic map**, popularised by Robert May (1976) as a model of insect populations. It has a remarkably simple form but contains the full complexity of chaotic dynamics. The state space is $x \in [0,1]$ and the map is well-defined (it maps $[0,1]$ to $[0,1]$) for $r \in [0,4]$.

The logistic map is also the universal representative of **unimodal maps** — maps on an interval with a single quadratic maximum. Any such map undergoes qualitatively identical period-doubling dynamics.

## Fixed points and their stability

**Period-1 fixed points:** Solve $x^* = rx^*(1-x^*)$, giving

$$x^* = 0 \quad \text{and} \quad x^* = 1 - 1/r \equiv x_1^* \quad (r > 1)$$

Stability: $|F'(x^*)| = |r(1-2x^*)|$.
- At $x^* = 0$: $|F'(0)| = r$. Stable for $r < 1$.
- At $x_1^*$: $|F'(x_1^*)| = |2-r|$. Stable for $1 < r < 3$.

**Period-2 cycle:** The period-2 orbit satisfies $F^2(x) = x$, $F(x) \neq x$. The points of the 2-cycle are the solutions of

$$F^2(x) - x = 0 \quad \text{after dividing out the fixed points}$$

After algebra, the two 2-cycle points are

$$x_{\pm} = \frac{r+1 \pm \sqrt{(r+1)(r-3)}}{2r}$$

Real for $r \geq 3$. They are born at $r = 3$ in a **period-doubling bifurcation** of $x_1^*$.

Stability of the 2-cycle: the cycle is stable when $|(F^2)'(x_-)| < 1$. The chain rule gives

$$(F^2)'(x_-) = F'(x_-)\cdot F'(x_+) = r(1-2x_-)\cdot r(1-2x_+)$$

After expanding: $(F^2)'(x_\pm) = -r^2 + 2r + 4$. This equals $+1$ at $r = 3$ (birth of the cycle) and $-1$ at $r = 3.449...$, where the 2-cycle undergoes its own period-doubling bifurcation.

## The cobweb construction

The **cobweb diagram** is the standard graphical method for iterating a 1D map:

1. Start at $(x_0, 0)$ on the $x$-axis.
2. Draw a vertical line up to the curve $y = F(x_0)$, landing at $(x_0, x_1)$ where $x_1 = F(x_0)$.
3. Draw a horizontal line to the diagonal $y = x$, landing at $(x_1, x_1)$ — this puts $x_1$ on the $x$-axis.
4. Repeat: vertical to curve, horizontal to diagonal.

The cobweb's long-run pattern reveals the attractor:
- **Converging to a point:** fixed point (the cobweb spirals or monotonically approaches one $x$-value).
- **Bouncing between two levels:** period-2 cycle (a rectangle is traced).
- **Cycle of $p$ values:** period-$p$ cycle ($p$-gon in the cobweb).
- **Band filling:** chaos (the cobweb wanders densely through an interval).

The cobweb is a complete solution method — by following the construction, one can predict the entire future of the orbit for any initial condition and any $r$.

## The period-doubling cascade and Feigenbaum's discovery

Let $r_n$ denote the value of $r$ at which the $n$-th period-doubling bifurcation occurs:

| $n$ | $r_n$ | Period | Interval $r_n - r_{n-1}$ | Ratio |
|---|---|---|---|---|
| 1 | 3.0000 | $1 \to 2$ | — | — |
| 2 | 3.4495 | $2 \to 4$ | 0.4495 | — |
| 3 | 3.5441 | $4 \to 8$ | 0.0946 | 4.75 |
| 4 | 3.5644 | $8 \to 16$ | 0.0203 | 4.66 |
| 5 | 3.5688 | $16 \to 32$ | 0.0044 | 4.62 |
| $\infty$ | 3.5699... | Chaos onset | 0 | **4.6692...** |

Mitchell Feigenbaum (1975) discovered numerically that the ratio of successive interval lengths converges to a universal constant:

$$\delta = \lim_{n\to\infty}\frac{r_n - r_{n-1}}{r_{n+1} - r_n} \approx 4.6692016...\qquad \text{(Feigenbaum constant)}$$

This constant is the same for **every smooth unimodal map with a quadratic maximum** — the logistic map, $r\sin(\pi x)$, the Hénon map (Lab 7), and many others.

## Renormalisation group derivation of $\delta$

Feigenbaum's key insight was to view the period-doubling cascade as a **fixed point of a renormalisation operator**.

Define the operator $\mathcal{R}$ acting on unimodal maps $f$:

$$(\mathcal{R}f)(x) = \frac{1}{\alpha}f\!\left(f(\alpha x)\right)$$

where $\alpha$ is chosen so that $\mathcal{R}f$ is again a unimodal map with the same normalisation (e.g., maximum value 1 at $x=0$). The operator $\mathcal{R}$ squares the map and rescales — it takes a map near its $2^n$-cycle to a map near its $2^{n-1}$-cycle (in the sense of looking at the dynamics on finer scales).

**Fixed point of $\mathcal{R}$:** There exists a universal function $g^*$ (the Feigenbaum-Cvitanovic fixed-point function) satisfying

$$g^*(x) = \frac{1}{\alpha}g^*\!\bigl(g^*(\alpha x)\bigr), \qquad g^*(0) = 1, \quad \alpha = -g^*(1) \approx -2.5029...$$

**Linearising $\mathcal{R}$ around $g^*$:** The derivative $D\mathcal{R}|_{g^*}$ has a single unstable eigenvalue $\delta \approx 4.669$. This eigenvalue governs the rate at which perturbations grow under successive doublings — the ratio of successive parameter intervals is $1/\delta$ because the bifurcation points are the preimages of $g^*$ under $\mathcal{R}$.

The universality of $\delta$ is thus explained: it is an eigenvalue of a universal linear operator, independent of which particular unimodal map you start with.

## Periodic windows and Sharkovskii's theorem

Within the chaotic regime ($r > r_\infty \approx 3.5699$), there are isolated intervals of $r$ where a stable periodic orbit suddenly appears. These **periodic windows** arise from **saddle-node bifurcations** of the iterated map $F^p$.

The largest window is the **period-3 window** at $r \approx 3.828$. Its existence has a profound implication:

**Sharkovskii's theorem (1964):** Order the positive integers as

$$3 \succ 5 \succ 7 \succ \cdots \succ 2\cdot 3 \succ 2\cdot 5 \succ \cdots \succ 4\cdot 3 \succ \cdots \succ 16 \succ 8 \succ 4 \succ 2 \succ 1$$

If a continuous map of an interval has a periodic orbit of period $m$, it has periodic orbits of all periods $n$ with $m \succ n$ in this ordering. Since 3 is the largest element, a period-3 orbit implies orbits of **all periods**. Li and Yorke (1975) popularised this as **"Period 3 implies chaos"**.

## Other routes to chaos

Period doubling is not the only route. Two other classical routes:

**Quasi-periodicity route (Ruelle-Takens-Newhouse):** Add incommensurate frequencies $\omega_1, \omega_2$ (a 2-torus), then $\omega_3$ (3-torus). Ruelle and Takens (1971) proved that a generic perturbation of a 3-torus produces a strange attractor. This route appears in Taylor-Couette flow and in electronic circuits.

**Intermittency route (Pomeau-Manneville, 1980):** Near a saddle-node bifurcation of a periodic orbit, the system spends long stretches in a "laminar" near-periodic phase (the ghost of the destroyed orbit) punctuated by brief chaotic bursts. Three types:
- **Type I:** near a saddle-node bifurcation; bursts grow algebraically frequent as $r$ increases.
- **Type II:** near a subcritical Hopf; bursts are accompanied by oscillation.
- **Type III:** near an inverse period-doubling; bursts follow a $1/f$ power spectrum.

## Live demo

The left canvas shows the cobweb diagram for the chosen $r$ and initial condition $x_0$, with $N$ iterates drawn. The right canvas shows the full bifurcation diagram (precomputed for 500 values of $r$, 80 orbit points each) with gold dots marking the current $r$'s orbit. Click **Sweep r** to animate $r$ from 1 to 4 in real time, watching the cascade unfold. The info bar shows the detected period and Lyapunov exponent.

<iframe
  src="/train-deep-learning/ds-logistic/"
  title="DS Lab 9 — Logistic Map & Period Doubling"
  style="width:100%; min-height:440px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe from the demo

**Fixed point regime ($r = 2.5$):**
- Cobweb: a spiral converging to the intersection of $y = F(x)$ and $y = x$.
- Period = 1. Lyapunov exponent $\lambda < 0$.

**First period doubling ($r = 3.2$):**
- Cobweb: a square — the orbit bounces between exactly two values.
- Period = 2. Two gold dots on the bifurcation diagram.

**Period-4 ($r = 3.5$):**
- Cobweb: an octagon-like path through four levels.
- Period = 4. Four dots on bifurcation diagram.

**Near chaos onset ($r = 3.57$):**
- Cobweb wanders in a band but the orbit seems to have many closely spaced values.
- $\lambda \approx 0$: exactly at the accumulation point.

**Period-3 window ($r = 3.83$):**
- Cobweb converges to a triangle — the three-point cycle.
- Period = 3. Three gold dots sharply visible on the bifurcation diagram.
- This is Sharkovskii's window: the most ordered feature inside the chaotic sea.

**Full chaos ($r = 4$):**
- Cobweb fills the entire parabola densely — every part of $[0,1]$ is visited.
- $\lambda = \ln 2 \approx 0.693$ — the analytical maximum.
- **Sweep r**: watch the entire cascade in motion. Note the intervals between doublings shrinking at ratio $\approx 4.669$.

## Key takeaways

- The logistic map $x_{n+1} = rx_n(1-x_n)$ models both population dynamics and the universal period-doubling route to chaos.
- Fixed-point and period-2 stabilities can be computed exactly; the stability criteria correctly predict the bifurcation values $r = 1, 3, 3.449...$
- The Feigenbaum constant $\delta \approx 4.6692$ is an eigenvalue of the renormalisation operator $\mathcal{R}$, explaining its universality across all unimodal maps.
- Sharkovskii's theorem: period-3 implies orbits of all periods — the period-3 window is not just one special orbit, it is a gateway to the entire periodic hierarchy.
