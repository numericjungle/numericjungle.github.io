---
date: 2026-04-15 09:00:00.000000
layout: post
title: "Dynamical Systems Lab 6 - Lyapunov Exponents"
description: "Derive the Lyapunov exponent from the variational equation, compute it analytically for the logistic map, and watch λ(r) cross zero at every period-doubling transition."
tags: [dynamical systems, chaos, nonlinear dynamics]
comments: true
---

The largest Lyapunov exponent $\lambda$ is the single number that separates order from chaos. It measures the average exponential rate at which nearby trajectories diverge. Positive $\lambda$ means chaos; negative means order; zero signals a bifurcation boundary. Computing it transforms a visual impression of sensitive dependence into a precise, testable, quantitative statement.

<!--excerpt-->

## The variational equation

Let $x(t)$ be a trajectory of $\dot{x} = f(x)$. Consider a nearby trajectory $x(t) + \delta(t)$ where $\delta$ is an infinitesimal perturbation. Substituting into the ODE and linearising:

$$\dot{\delta} = f(x + \delta) - f(x) \approx f'(x(t))\,\delta$$

This is the **variational equation** (or tangent-space equation). It is a linear ODE with a time-dependent coefficient $f'(x(t))$ — note that the coefficient changes as the base trajectory $x(t)$ evolves through phase space.

The formal solution is

$$\delta(t) = \delta_0 \exp\!\left(\int_0^t f'(x(\tau))\,d\tau\right)$$

so the growth factor of the perturbation over time $T$ is $e^{\int_0^T f'(x)\,d\tau}$. The **largest Lyapunov exponent** is the time-averaged exponent in the limit $T \to \infty$:

$$\lambda = \lim_{T\to\infty} \frac{1}{T}\int_0^T f'(x(\tau))\,d\tau$$

## Lyapunov exponent for maps

For a discrete map $x_{n+1} = F(x_n)$, the variational equation propagates as

$$\delta_{n+1} = F'(x_n)\,\delta_n \implies \delta_N = \delta_0 \prod_{n=0}^{N-1} F'(x_n)$$

Taking logarithms:

$$\frac{1}{N}\ln|\delta_N/\delta_0| = \frac{1}{N}\sum_{n=0}^{N-1}\ln|F'(x_n)|$$

The **largest Lyapunov exponent** for a map is therefore

$$\lambda = \lim_{N\to\infty}\frac{1}{N}\sum_{n=0}^{N-1}\ln|F'(x_n)|$$

This is a time average of $\ln|F'|$ along the orbit — it measures how much the map stretches infinitesimal intervals on average.

## The logistic map

The logistic map $x_{n+1} = r\,x_n(1-x_n)$ has derivative

$$F'(x) = r(1-2x)$$

So the Lyapunov exponent at parameter $r$ is

$$\lambda(r) = \lim_{N\to\infty}\frac{1}{N}\sum_{n=0}^{N-1}\ln|r(1-2x_n)|$$

**Analytical result at $r = 4$:** The map $x_{n+1} = 4x_n(1-x_n)$ is exactly conjugate to the tent map via $x = \sin^2(\pi\theta)$. Under this change of variables, the tent map $\theta_{n+1} = 2\theta_n \pmod{1}$ has $|F'| = 2$ everywhere. Therefore

$$\lambda(r=4) = \ln 2 \approx 0.693$$

**At a period-$p$ orbit:** A period-$p$ fixed point of $F^p$ satisfies $(F^p)'(x^*) = \prod_{k=0}^{p-1} F'(x_k)$. The orbit is stable iff $|(F^p)'| < 1$, i.e., $\lambda < 0$. At the bifurcation boundary, $|(F^p)'| = 1$, so $\lambda = 0$.

## Interpretation: the full table

| $\lambda(r)$ | Physical meaning |
|---|---|
| $\lambda < 0$ (negative) | Ordered: orbit converges to a periodic attractor; perturbations decay at rate $|\lambda|$ per iterate |
| $\lambda = 0$ | Critical: at a bifurcation point or the onset of chaos; perturbations neither grow nor decay |
| $\lambda > 0$ (positive) | Chaotic: nearby orbits diverge exponentially; memory of initial conditions is lost |

Note that $\lambda = 0$ is hit:
- At every **period-doubling bifurcation** (a period-$2^n$ orbit becomes marginally stable before losing stability).
- At the **chaos onset** $r_\infty \approx 3.5699$, where the infinite cascade accumulates.
- At the edges of every **periodic window** within the chaotic regime.

## The Lyapunov spectrum for higher-dimensional systems

For an $n$-dimensional flow, there is a **Lyapunov spectrum** $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_n$, one per dimension. These are defined via the successive stretching rates of $k$-dimensional volume elements:

$$\lambda_1 + \cdots + \lambda_k = \lim_{T\to\infty}\frac{1}{T}\ln\left\|\bigwedge_{j=1}^k \delta_j(t)\right\|$$

where $\bigwedge$ denotes the exterior product (volume element). In practice, they are computed by the **Gram-Schmidt renormalisation algorithm** (Benettin et al., 1980):

1. Integrate the ODE and the variational equation for $k$ perturbation vectors simultaneously.
2. After each small time step $\Delta t$, orthogonalise and re-normalise the perturbation vectors using Gram-Schmidt.
3. Accumulate the logarithm of each normalisation factor.
4. Divide by total time $T$ in the limit.

**Constraints on the spectrum:**
- For a Hamiltonian (conservative) system: the spectrum is symmetric, $\lambda_k = -\lambda_{n+1-k}$.
- For a dissipative system: $\sum_k \lambda_k = \int_0^T \nabla\cdot\mathbf{F}\,dt/T = \nabla\cdot\mathbf{F}$ (by Liouville).
- For any autonomous flow with a non-trivial attractor: at least one $\lambda_k = 0$ (the direction tangent to the flow).
- For the Lorenz attractor: $\lambda_1 \approx +0.905$, $\lambda_2 = 0$, $\lambda_3 \approx -14.57$.

## Kaplan-Yorke dimension

The Lyapunov spectrum determines the **fractal dimension** of the attractor via the Kaplan-Yorke (or Lyapunov dimension) formula:

$$d_{KY} = j + \frac{\sum_{k=1}^j \lambda_k}{|\lambda_{j+1}|}$$

where $j$ is the largest index for which $\lambda_1 + \cdots + \lambda_j \geq 0$. For the Lorenz attractor:

$$d_{KY} = 2 + \frac{0.905 + 0}{|-14.57|} \approx 2 + 0.062 \approx 2.06$$

The attractor has fractal dimension between 2 and 3 — a surface-like structure with extra fractal foliation.

## Pesin's entropy formula

The **Kolmogorov-Sinai (KS) entropy** $h_{KS}$ measures the rate of information generation by the dynamics (bits per unit time). For smooth systems, **Pesin's formula** states

$$h_{KS} = \sum_{\lambda_k > 0} \lambda_k$$

For the logistic map at $r = 4$: $h_{KS} = \lambda = \ln 2$ bits per iterate — the system generates exactly 1 bit of new information per step (equivalent to a fair coin flip).

## Live demo

The top half shows the full bifurcation diagram of the logistic map, accumulated over 500 $r$-values and 80 orbit points each. The bottom half shows $\lambda(r)$: green where negative (ordered), red where positive (chaotic). A vertical gold cursor follows the current $r$-slider position; a gold dot on the $\lambda$ plot marks the exact current value with a detection of the apparent period.

<iframe
  src="/train-deep-learning/ds-lyapunov/"
  title="DS Lab 6 — Lyapunov Exponents"
  style="width:100%; min-height:580px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe from the demo

**Following the period-doubling cascade:**
- Set $r = 3.0$: the info bar shows period = 1 (fixed point), $\lambda \approx -0.29$ (ordered). The $\lambda$ plot is solidly green.
- Set $r = 3.1$: period = 2, $\lambda < 0$. Notice the bifurcation diagram splits into two bands.
- Set $r = 3.45$: period = 4, $\lambda < 0$ but approaching zero.
- Set $r = 3.54$: period = 8; $\lambda$ is very close to zero. The orbit takes 8 values.
- Set $r = 3.57$: near the chaos onset $r_\infty$. $\lambda \approx 0$ — right at the edge.

**Inside the chaotic regime:**
- Set $r = 3.7$: $\lambda > 0$ (chaotic). Notice the bifurcation diagram fills a continuous band.
- Set $r = 3.83$: the period-3 window. The bifurcation diagram snaps to three discrete points; $\lambda$ dips sharply negative. This is an island of order within chaos — Sharkovskii's theorem guarantees that period-3 implies all other periods exist, but the attractor here is an ordered period-3 cycle.
- Set $r = 3.9$: back to chaos, $\lambda > 0$. The bands have re-broadened.

**At $r = 4$:** $\lambda \approx 0.693 = \ln 2$ — the analytical value confirmed numerically.

## Key takeaways

- The Lyapunov exponent is a time average of $\ln|F'|$ along the orbit — positive means chaos, negative means order, zero means a bifurcation boundary.
- For the logistic map at $r = 4$, the Lyapunov exponent equals $\ln 2$ exactly (analytically provable via the tent map conjugacy).
- Every period-doubling bifurcation is marked by $\lambda$ crossing zero; this makes the Lyapunov plot a fingerprint of the entire cascade.
- The Kaplan-Yorke formula connects the Lyapunov spectrum to the fractal dimension of the attractor; Pesin's formula connects it to information-theoretic entropy.
