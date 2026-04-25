---
date: 2026-04-20 09:00:00.000000
layout: post
title: "Dynamical Systems Lab 8 - Hopf Bifurcation"
description: "Derive the Hopf bifurcation theorem, reduce to the normal form by center manifold theory, and watch a stable spiral become a limit cycle as μ crosses zero."
tags: [dynamical systems, chaos, nonlinear dynamics]
comments: true
---

In 1942, Eberhard Hopf proved that a fixed point with complex eigenvalues can lose stability and give birth to a limit cycle as a single parameter passes through a critical value. This **Hopf bifurcation** is the universal route from equilibrium to oscillation — it underlies cardiac pacemakers, chemical oscillations, fluid instabilities, and neural firing.

<!--excerpt-->

## Setup: a fixed point with complex eigenvalues

Consider a planar system $\dot{\mathbf{x}} = \mathbf{F}(\mathbf{x}, \mu)$ with a fixed point at the origin for all $\mu$ (translate coordinates so this is so). The Jacobian at the origin is

$$J(\mu) = \begin{pmatrix} \alpha(\mu) & -\omega(\mu) \\ \omega(\mu) & \alpha(\mu) \end{pmatrix}$$

(after a possible linear change of coordinates). The eigenvalues are $\lambda_{1,2} = \alpha(\mu) \pm i\omega(\mu)$.

- For $\mu < 0$: $\alpha(\mu) < 0$ — stable spiral. All trajectories converge to the origin.
- At $\mu = 0$: $\alpha(0) = 0$, $\omega(0) = \omega_0 \neq 0$ — centre of the linearisation.
- For $\mu > 0$: $\alpha(\mu) > 0$ — unstable spiral. All trajectories spiral away.

The **transversality condition** requires the eigenvalues to cross the imaginary axis with nonzero speed:

$$\frac{d\alpha}{d\mu}\bigg|_{\mu=0} \neq 0$$

Without this, the eigenvalues might graze the imaginary axis and return without a bifurcation.

## The normal form

By a sequence of nonlinear coordinate changes (the Poincaré normal form procedure), the system near $\mu = 0$ can be brought to the form

$$\dot{x} = \mu x - \omega_0 y - (x^2+y^2)(ax - by)$$
$$\dot{y} = \omega_0 x + \mu y - (x^2+y^2)(bx + ay)$$

or, in polar coordinates $x = r\cos\theta$, $y = r\sin\theta$:

$$\dot{r} = \mu r - a r^3 + O(r^5)$$
$$\dot{\theta} = \omega_0 + b r^2 + O(r^4)$$

The coefficient $a$ is the **first Lyapunov coefficient** and determines whether the bifurcation is supercritical or subcritical.

## Supercritical Hopf bifurcation ($a > 0$)

Fixed points of the $\dot{r}$ equation: $r = 0$ and $r^* = \sqrt{\mu/a}$ (exists for $\mu > 0$).

**Stability of the limit cycle:** $\frac{\partial \dot{r}}{\partial r}\big|_{r^*} = \mu - 3ar^{*2} = \mu - 3\mu = -2\mu < 0$ for $\mu > 0$.

The limit cycle is **stable** — trajectories from inside and outside both converge to it. The bifurcation is supercritical: a stable limit cycle is born continuously as $\mu$ increases through zero.

**Amplitude:** $r^* = \sqrt{\mu/a}$, so the limit cycle radius grows as $\sqrt{\mu}$ — a square-root scaling, analogous to the pitchfork normal form.

**Physical picture:** For $\mu < 0$ the origin is a stable spiral (global attractor). At $\mu = 0$ a marginal centre. For $\mu > 0$ the origin is an unstable spiral but trajectories cannot escape to infinity — the nonlinear terms provide restoring force — so they settle on the limit cycle.

## Subcritical Hopf bifurcation ($a < 0$)

Now the $-ar^3$ term with $a < 0$ is $+|a|r^3$ — it amplifies rather than saturates. Fixed points: $r^* = \sqrt{\mu/|a|}$ exists for $\mu < 0$.

$\frac{\partial \dot{r}}{\partial r}\big|_{r^*} = \mu - 3\cdot(-|a|)r^{*2} = \mu + 3|\mu| = 2|\mu| > 0$ for $\mu < 0$.

The limit cycle at $r^*$ is **unstable** — it is a basin boundary, not an attractor. For $\mu < 0$ the origin is stable but is surrounded by an unstable limit cycle; trajectories inside converge to the origin, trajectories outside diverge. For $\mu > 0$ the origin becomes unstable and there is no nearby attractor — the system exhibits a **hard loss of stability** (a finite-amplitude jump).

Including a higher-order stabilising term ($-cr^5$ with $c > 0$) produces hysteresis: the system jumps to a large-amplitude stable limit cycle when $\mu$ increases past zero, but the limit cycle persists for $\mu$ down to a negative value $\mu_{\text{fold}}$ when it is annihilated in a saddle-node-of-cycles bifurcation.

## Center manifold reduction (sketch)

For higher-dimensional systems with other stable modes, the Hopf bifurcation can be reduced to the 2D normal form by the **center manifold theorem**.

Near $\mu = 0$ the eigenvalues of $J$ split into:
- **Critical modes:** the pair $\pm i\omega_0$ (the center subspace $E^c$, dimension 2).
- **Stable modes:** eigenvalues with negative real parts (the stable subspace $E^s$).

**Theorem (Center Manifold):** There exists a 2D invariant manifold $W^c$ tangent to $E^c$ at the origin. The long-term dynamics of the full system are governed by the flow restricted to $W^c$ — a 2D system.

The restriction to $W^c$ is computed perturbatively. Write the stable variables as $\mathbf{y} = h(\mathbf{x})$ (the graph of the center manifold). The function $h$ satisfies the **invariance equation**:

$$Dh(\mathbf{x})\cdot\mathbf{F}_c(\mathbf{x}, h(\mathbf{x})) = \mathbf{F}_s(\mathbf{x}, h(\mathbf{x}))$$

Solving this perturbatively (expanding $h$ in powers of $|\mathbf{x}|$) and substituting back gives the reduced 2D system whose normal form is the polar system above.

## Computing the first Lyapunov coefficient

For the full system $\dot{\mathbf{x}} = A\mathbf{x} + \frac{1}{2}B(\mathbf{x},\mathbf{x}) + \frac{1}{6}C(\mathbf{x},\mathbf{x},\mathbf{x}) + \cdots$, the first Lyapunov coefficient is

$$a = \frac{1}{16}\left[\sum_{i,j,k}\left(F_{x_i x_j x_k} q_i \bar{q}_j q_k + F_{x_i x_j x_k} \bar{q}_i q_j q_k\right)\right] + \frac{1}{16\omega_0}\text{Im}\left[\sum_{i,j,k,l}\left(F_{x_i x_j} q_i \bar{q}_j\right)\left(\sum_m F_{x_k x_l} q_k \bar{q}_l\right)\right]$$

where $q$ is the eigenvector of $A$ with eigenvalue $i\omega_0$. In practice this is computed via the formula derived by Kuznetsov (2004). The sign of $a$ determines super- vs. subcritical.

## Physical examples

| System | Hopf mechanism |
|---|---|
| Van der Pol oscillator | $\mu = 0$: centre; $\mu > 0$: supercritical Hopf; limit cycle amplitude $r = 2$ (from averaging) |
| Brusselator (chemical oscillator) | Supercritical Hopf as $B$ crosses $1 + A^2$; limit cycle = chemical clock |
| Lorenz system at $\rho \approx 24.74$ | Subcritical Hopf at $C_\pm$ (degenerate) |
| Taylor-Couette flow | Supercritical Hopf — steady flow loses stability to rotating waves |
| FitzHugh-Nagumo (neuron) | Supercritical Hopf — the neuron begins to fire periodically |

## Live demo

The system is the **supercritical Hopf normal form** in Cartesian coordinates:

$$\dot{x} = \mu x - \omega y - x(x^2+y^2), \qquad \dot{y} = \omega x + \mu y - y(x^2+y^2)$$

Vary $\mu$ and the angular frequency $\omega$. Multiple trajectories launch from the chosen IC radius $r_0$ at equally-spaced angles. The right canvas shows the $x(t)$ and $y(t)$ time series.

<iframe
  src="/train-deep-learning/ds-hopf/"
  title="DS Lab 8 — Hopf Bifurcation"
  style="width:100%; min-height:520px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe from the demo

**μ = −1 (stable regime):**
- The origin is a stable spiral. All trajectories (whether started inside or outside) converge to the origin.
- Time series: exponentially decaying sinusoid at frequency $\omega$.

**μ = 0 (critical):**
- The linearisation is a centre (eigenvalues exactly $\pm i\omega$). The nonlinear terms determine what actually happens — in the normal form above, $a = 1 > 0$ so this is the supercritical case: trajectories spiral very slowly toward the origin (the nonlinear correction is stabilising even at $\mu = 0$).

**μ = 0.5 (limit cycle regime):**
- A stable limit cycle appears at radius $r^* = \sqrt{\mu/1} = \sqrt{0.5} \approx 0.707$.
- Trajectories from inside (small IC radius) spiral outward to the limit cycle.
- Trajectories from outside (large IC radius) spiral inward to it.
- Dashed gold circle on the phase portrait marks the theoretical limit cycle radius.

**μ = 2.0 (large amplitude):**
- Limit cycle radius $r^* = \sqrt{2} \approx 1.414$. Larger and clearly visible.
- Time series: sustained sinusoid with amplitude $\approx 1.414$.

**Vary ω:**
- Higher $\omega$: faster spiral rotation — the trajectory corkscrews more tightly.
- The limit cycle radius is independent of $\omega$ (only $\mu$ and the cubic coefficient matter).

**Number of trails:**
- Set to 4 or 5: you can simultaneously see trajectories from inside the limit cycle (spiralling out) and outside (spiralling in) — confirming the limit cycle is a global attractor for all $\mu > 0$.

## Key takeaways

- The Hopf bifurcation occurs when a pair of complex eigenvalues crosses the imaginary axis — the signature is a real part $\alpha(\mu)$ changing sign, with $\alpha'(0) \neq 0$ (transversality).
- In polar normal form: $\dot{r} = \mu r - ar^3$; the stable limit cycle has radius $r^* = \sqrt{\mu/a}$ (supercritical, $a > 0$).
- The first Lyapunov coefficient $a$ distinguishes supercritical ($a > 0$, soft onset) from subcritical ($a < 0$, hard onset with hysteresis).
- Center manifold reduction reduces any $n$-dimensional system at a Hopf bifurcation to the universal 2D normal form.
