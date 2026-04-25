---
date: 2026-04-11 09:00:00.000000
layout: post
title: "Dynamical Systems Lab 5 - The Lorenz System and Chaos"
description: "Derive the Lorenz equations from the Navier-Stokes PDE via Galerkin truncation, analyse the fixed points, and witness exponential divergence of two nearby trajectories."
tags: [dynamical systems, chaos, nonlinear dynamics]
comments: true
---

In 1963, Edward Lorenz discovered that a three-equation system derived from the fluid mechanics equations for convection could produce trajectories so sensitive to initial conditions that long-range weather prediction is mathematically impossible — not a practical difficulty, but a fundamental consequence of the equations themselves. This is **deterministic chaos**.

<!--excerpt-->

## From Navier-Stokes to the Lorenz equations

The starting point is the 2D Boussinesq equations for thermal convection in a horizontal fluid layer of depth $H$ heated from below (Rayleigh-Bénard convection):

$$\frac{\partial \nabla^2\psi}{\partial t} + J(\psi, \nabla^2\psi) = \nu\nabla^4\psi + g\alpha\frac{\partial T}{\partial x}$$

$$\frac{\partial T}{\partial t} + J(\psi, T) = \kappa\nabla^2 T + \frac{\Delta T}{H}\frac{\partial\psi}{\partial x}$$

where $\psi(x,z,t)$ is the stream function, $T(x,z,t)$ the temperature departure from the conductive profile, $J(a,b) = \partial_x a\,\partial_z b - \partial_z a\,\partial_x b$ the Jacobian (advective nonlinearity), $\nu$ kinematic viscosity, $\kappa$ thermal diffusivity, and $g\alpha\Delta T / H$ the buoyancy forcing.

**Lorenz's Galerkin truncation (1963):** Expand $\psi$ and $T$ in a minimal set of Fourier modes that satisfy the boundary conditions (free-slip at top and bottom, periodic in $x$):

$$\psi = \frac{\sqrt{2}\,\kappa\,(1+a^2)}{a}\, X(t)\,\sin\!\left(\frac{\pi a x}{H}\right)\sin\!\left(\frac{\pi z}{H}\right)$$

$$T = \frac{\sqrt{2}\,R\,\kappa}{R_c}\, Y(t)\,\cos\!\left(\frac{\pi a x}{H}\right)\sin\!\left(\frac{\pi z}{H}\right) - \frac{R\,\kappa}{R_c}\, Z(t)\,\sin\!\left(\frac{2\pi z}{H}\right)$$

where $a$ is the aspect ratio of the convection rolls, $R$ the Rayleigh number, $R_c = \pi^4(1+a^2)^3/a^2$ the critical Rayleigh number, and $X, Y, Z$ are the time-dependent amplitudes.

Substituting into the PDEs and projecting (Galerkin projection) yields the **three-mode ODEs**. With the non-dimensionalisation $t \to t/\sigma\pi^2(1+a^2)/H^2$ and the identifications $\sigma = \nu/\kappa$ (Prandtl number), $r = R/R_c$ (reduced Rayleigh number), $b = 4/(1+a^2)$ (geometric factor):

$$\boxed{\dot{X} = \sigma(Y - X), \qquad \dot{Y} = X(r - Z) - Y, \qquad \dot{Z} = XY - bZ}$$

This is the **Lorenz system**. The variables have physical meaning:
- $X$: amplitude of the convective circulation (roll intensity).
- $Y$: temperature difference between ascending and descending fluid.
- $Z$: distortion of the vertical temperature profile from the linear conductive state.

Classic parameters: $\sigma = 10$ (water or air at $10\leq$Pr$\leq 10$), $r = 28$ (above criticality), $b = 8/3$ (square cell $a = 1/\sqrt{2}$).

## Fixed points

**The origin $C_0 = (0,0,0)$:**

Linearise: $J|_{C_0} = \begin{pmatrix}-\sigma & \sigma & 0\\ r & -1 & 0 \\ 0 & 0 & -b\end{pmatrix}$.

The characteristic polynomial factors as $(\lambda + b)\bigl[\lambda^2 + (\sigma+1)\lambda + \sigma(1-r)\bigr] = 0$.

Roots: $\lambda_3 = -b < 0$ always; $\lambda_{1,2} = \frac{-(\sigma+1)\pm\sqrt{(\sigma+1)^2 - 4\sigma(1-r)}}{2}$.

For $r < 1$ all roots are negative — the origin is a **stable node**. At $r = 1$: one eigenvalue passes through zero — a pitchfork bifurcation occurs, and the $C_\pm$ fixed points are born.

**The symmetric pair $C_\pm = \bigl(\pm\sqrt{b(r-1)},\,\pm\sqrt{b(r-1)},\,r-1\bigr)$ (for $r > 1$):**

The Jacobian at $C_+$ (WLOG) is

$$J|_{C_+} = \begin{pmatrix}-\sigma & \sigma & 0\\ 1 & -1 & -x^*\\ y^* & x^* & -b\end{pmatrix}, \quad x^* = y^* = \sqrt{b(r-1)}$$

The characteristic polynomial is $\lambda^3 + (\sigma+b+1)\lambda^2 + b(\sigma+r)\lambda + 2\sigma b(r-1) = 0$.

Stability analysis using the **Routh-Hurwitz criterion**: $C_\pm$ are stable if and only if $r < r_H$ where

$$r_H = \frac{\sigma(\sigma + b + 3)}{\sigma - b - 1}$$

For $\sigma = 10, b = 8/3$: $r_H = \frac{10(10 + 8/3 + 3)}{10 - 8/3 - 1} = \frac{10 \cdot 47/3}{13/3} = \frac{470}{13} \approx 24.74$

For $r > r_H \approx 24.74$: all three fixed points are **unstable**, yet orbits remain bounded. The system must tend toward a bounded, non-periodic, non-fixed-point attractor.

## Volume contraction and the attractor

The **divergence** of the Lorenz vector field is

$$\nabla \cdot \mathbf{F} = \frac{\partial \dot{X}}{\partial X} + \frac{\partial \dot{Y}}{\partial Y} + \frac{\partial \dot{Z}}{\partial Z} = -\sigma - 1 - b = -\left(\sigma + 1 + \frac{8}{3}\right) = -\frac{41}{3}$$

for classic parameters. By Liouville's theorem, any volume $V(t)$ in phase space contracts at the rate

$$\frac{dV}{dt} = \oint_{\partial V} \mathbf{F}\cdot d\mathbf{A} = \int_V (\nabla\cdot\mathbf{F})\,dV = -\frac{41}{3}\,V$$

so $V(t) = V(0)\,e^{-41t/3}$. Volume collapses to zero exponentially fast — the **attractor has zero volume** in phase space, even though trajectories explore a bounded region. This is the essence of a strange attractor: it has measure zero yet positive fractal dimension.

## Sensitive dependence on initial conditions

Let $(X_1(t), Y_1(t), Z_1(t))$ and $(X_2(t), Y_2(t), Z_2(t))$ be two trajectories with initial separation

$$\delta_0 = \sqrt{(X_1(0)-X_2(0))^2 + (Y_1(0)-Y_2(0))^2 + (Z_1(0)-Z_2(0))^2}$$

The **largest Lyapunov exponent** $\lambda_1$ governs the early growth of the separation:

$$\delta(t) \approx \delta_0\,e^{\lambda_1 t}$$

For the classic Lorenz attractor, $\lambda_1 \approx 0.905$. Two initial conditions separated by $\delta_0 = 10^{-6}$ become $O(1)$ different at

$$t^* \approx \frac{1}{\lambda_1}\ln\frac{1}{\delta_0} \approx \frac{6\ln 10}{0.905} \approx 15 \text{ time units}$$

On the attractor's timescale (one butterfly lobe takes about $2$–$3$ time units), this is only $5$–$8$ loops before predictability is lost entirely.

## The Lorenz attractor as a flow on a twisted strip

Topologically the Lorenz attractor resembles two lobes joined at an unstable fixed point $C_0$. Trajectories circulate around one lobe, then at some unpredictable moment (determined sensitively by initial conditions) switch to the other. This **lobe-switching** is the geometric mechanism of chaos: it is equivalent to a coin-flip that stretches initial-condition uncertainty into full uncertainty over which lobe is visited.

The Lorenz system was rigorously proved to be chaotic (in the sense of the existence of a genuine strange attractor) by Tucker (2002) using computer-assisted proofs — an 88-year gap between Lorenz's numerical discovery and its complete mathematical proof.

## Live demo

Two trajectories (blue and red) start from nearly identical initial conditions. The main canvas shows the $X$–$Z$ projection of both trajectories. The bar at the bottom plots $|\delta(t)|$ — the instantaneous separation — on a log scale. Adjust $\rho$ to explore the route from stable fixed points ($\rho < 24.74$) to chaos. Adjust $\Delta\text{IC}$ to control the initial separation.

<iframe
  src="/train-deep-learning/ds-lorenz/"
  title="DS Lab 5 — Lorenz Attractor"
  style="width:100%; min-height:580px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe from the demo

**ρ = 5 (below pitchfork, $r < r_H = 24.74$, both trajectories converge to $C_+$):**
- Both trajectories converge to the same fixed point regardless of initial separation.
- The separation $|\delta(t)|$ decays toward zero on the log-scale bar.

**ρ = 24 (just below $r_H$):**
- Both trajectories still eventually converge to $C_\pm$, but the transient is long and somewhat erratic — approaching the Hopf-like instability threshold.

**ρ = 28 (classic chaotic regime):**
- The two trajectories trace nearly identical paths initially — the separation bar stays flat.
- After roughly $10$–$20$ time units, the trajectories abruptly diverge. They begin visiting different lobes in an uncorrelated pattern.
- The separation $|\delta(t)|$ rises nearly linearly on the log scale (exponential growth), then saturates when both trajectories are independently exploring the attractor.

**Effect of ΔIC:**
- Set $\Delta\text{IC} = 10^{-1}$: divergence is nearly immediate.
- Set $\Delta\text{IC} = 10^{-4}$: watch the trajectories stay coherent for noticeably longer — consistent with the logarithmic dependence $t^* \propto \ln(1/\delta_0)$.

## Key takeaways

- The Lorenz equations are derived from the Navier-Stokes PDEs by a three-mode Galerkin truncation; each variable has a direct fluid-mechanical interpretation.
- All three fixed points are unstable for $\rho > \rho_H \approx 24.74$, yet volume contraction ($\nabla\cdot\mathbf{F} < 0$) forces trajectories to remain bounded — a strange attractor must exist.
- Sensitive dependence is quantified by the largest Lyapunov exponent $\lambda_1 \approx 0.905$: prediction error doubles every $t \approx 0.77$ time units.
- The attractor has zero volume (dissipative system) but fractal dimension $d_{KY} \approx 2.06$ (next lab).
