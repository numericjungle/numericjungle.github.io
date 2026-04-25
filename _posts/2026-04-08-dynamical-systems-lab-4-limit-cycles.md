---
date: 2026-04-08 09:00:00.000000
layout: post
title: "Dynamical Systems Lab 4 - Limit Cycles and the Van der Pol Oscillator"
description: "Derive the Van der Pol equation from vacuum-tube circuit theory, prove the limit cycle exists via Poincaré–Bendixson, and compute its amplitude by averaging."
tags: [dynamical systems, chaos, nonlinear dynamics]
comments: true
---

Every linear oscillator forgets its initial amplitude and either decays to zero or grows without bound. Nonlinear oscillators can do something far more interesting: they find a **preferred amplitude** — a self-sustained oscillation that neither grows nor decays, regardless of where you start. This isolated closed orbit is a **limit cycle**, and it is among the most important objects in all of applied mathematics.

<!--excerpt-->

## Why linear systems cannot have limit cycles

In a 2D linear system $\dot{\mathbf{x}} = A\mathbf{x}$, the origin is the only fixed point (assuming $\det A \neq 0$). If $A$ has purely imaginary eigenvalues $\pm i\omega$, the general solution is

$$x(t) = C\cos(\omega t + \phi), \quad y(t) = -C\sin(\omega t + \phi)$$

where $C = \sqrt{x_0^2 + y_0^2}$ is determined entirely by the initial condition. Every initial condition lives on a different closed orbit (a concentric ellipse). These orbits fill the plane — none of them is isolated.

A limit cycle is an **isolated** closed orbit: a small annular neighbourhood contains no other closed orbits. Isolation is impossible in linear systems, which always come in one-parameter families of nested orbits.

## The Van der Pol equation: derivation from circuit theory

Balthasar van der Pol (1920, 1926) was studying nonlinear oscillations in electronic circuits containing a **triode vacuum tube**. The tube acts as an energy source that compensates damping when the voltage is small, but increases damping when the voltage is large. The governing circuit ODE is

$$L\ddot{Q} + R(Q)\dot{Q} + \frac{Q}{C} = 0$$

where $Q$ is the charge, $L$ the inductance, $C$ the capacitance, and the tube gives a nonlinear resistance

$$R(Q) = -R_0\left(1 - \frac{Q^2}{Q_0^2}\right)$$

Negative resistance for $|Q| < Q_0$ pumps energy in; positive for $|Q| > Q_0$ dissipates it. Non-dimensionalise with $x = Q/Q_0$, $t \to t\sqrt{LC}/Q_0$:

$$\ddot{x} - \mu(1 - x^2)\dot{x} + x = 0, \qquad \mu = R_0\sqrt{C/L}\, Q_0$$

This is the **Van der Pol equation**. As a first-order system with $y = \dot{x}$:

$$\boxed{\dot{x} = y, \qquad \dot{y} = \mu(1-x^2)y - x}$$

The parameter $\mu \geq 0$ controls the strength of the nonlinear damping.

## Fixed point analysis

The only fixed point is the origin $(0,0)$. The Jacobian there is

$$J = \begin{pmatrix} 0 & 1 \\ -1 & \mu \end{pmatrix}$$

Eigenvalues: $\lambda^2 - \mu\lambda + 1 = 0 \Rightarrow \lambda = \frac{\mu \pm \sqrt{\mu^2 - 4}}{2}$.

- $\mu = 0$: eigenvalues $\pm i$ — centre (purely imaginary). No energy dissipation or injection.
- $0 < \mu < 2$: complex eigenvalues with positive real part $\mu/2 > 0$ — **unstable spiral**. The origin repels all nearby trajectories.
- $\mu = 2$: degenerate case (repeated eigenvalue).
- $\mu > 2$: two positive real eigenvalues — unstable node.

For $\mu > 0$, the origin is **unstable**. Trajectories spiral outward. But they cannot go to infinity, because the nonlinear term $-\mu x^2 y$ provides strong dissipation at large amplitudes. Something must stop the outward spiralling.

## Proving the limit cycle: Poincaré–Bendixson theorem

**Theorem (Poincaré–Bendixson):** If a trajectory remains in a closed bounded region $R$ of the 2D plane for all $t \geq 0$, and $R$ contains no fixed points, then the trajectory must approach a closed orbit.

To apply this to the Van der Pol system we construct a **trapping annulus** $A = \{(x,y) : r_1 \leq \sqrt{x^2+y^2} \leq r_2\}$ such that:

1. All trajectories on the **outer boundary** ($r = r_2$) point inward.
2. All trajectories on the **inner boundary** ($r = r_1$) point outward (because the origin is unstable and is inside).

Inward-pointing on the outer boundary: compute $\dot{r}^2 = 2(x\dot{x} + y\dot{y})$:

$$\frac{d}{dt}\frac{r^2}{2} = x\dot{x} + y\dot{y} = xy + y\bigl[\mu(1-x^2)y - x\bigr] = \mu y^2(1-x^2)$$

For large $r$, $x^2$ is large, so $1 - x^2 < 0$ and $\dot{r}^2 < 0$ on average — the trajectory is pulled inward. A more careful construction using the Liénard formulation makes this rigorous for all $r > 2$. The inner boundary with $r_1$ small enough sits entirely in the unstable spiral region, so trajectories there point outward.

With no fixed points in the annulus $A$, Poincaré–Bendixson guarantees **at least one limit cycle** in $A$. Numerical experiments confirm exactly one, which is **stable** (attracting) for $\mu > 0$.

## Amplitude and period for small $\mu$: method of averaging

For $0 < \mu \ll 1$ the limit cycle is nearly circular. Write the Van der Pol equation as a weakly nonlinear oscillator:

$$\ddot{x} + x = \mu(1 - x^2)\dot{x}$$

Use polar coordinates $x = r(t)\cos\theta$, $\dot{x} = -r(t)\sin\theta$ (variation of parameters). After substitution and averaging over one fast period $T_0 = 2\pi$, the **averaged equations** for the slow-time evolution of amplitude $r$ are

$$\dot{r} = \frac{\mu r}{2}\left(1 - \frac{r^2}{4}\right), \qquad \dot{\theta} = -1$$

Fixed points of the averaged equation: $\dot{r} = 0 \Rightarrow r = 0$ (unstable for $\mu > 0$) or $r = 2$ (stable). Hence the **limit cycle amplitude** is

$$r_{\text{lc}} = 2$$

for all $\mu$ in the weakly nonlinear regime. The **period** to leading order is

$$T = \frac{2\pi}{\omega_0}\left(1 + O(\mu^2)\right) = 2\pi + O(\mu^2)$$

Higher-order averaging gives the correction $T \approx 2\pi\left(1 - \frac{\mu^2}{16}\right)$.

## Relaxation oscillations for large $\mu$

For $\mu \gg 1$ the dynamics are qualitatively different. Rescale time: let $\tau = t/\mu$. Define $u = \mu^{-1}x$. In the Liénard form, introduce $w = \frac{x^3}{3} - x - \frac{\dot{x}}{\mu}$, so that $\dot{w} = -x/\mu^2 \approx 0$ away from a fast-switching manifold.

The limit cycle splits into:
- **Two slow phases** near $x \approx \pm 2$ where the trajectory slowly drifts along the cubic nullcline $y = x - x^3/3$.
- **Two fast jumps** where the trajectory shoots horizontally from $x = -1$ to $x = 2$ (or vice versa) on an $O(1/\mu)$ timescale.

The period of the relaxation oscillation:

$$T \approx \mu\left(3 - 2\ln 2\right) \approx 1.614\,\mu$$

The waveform of $x(t)$ becomes a nearly flat plateau followed by a sudden jump — the **relaxation oscillation** or **sawtooth wave**.

## Live demo

Adjust the nonlinear damping $\mu$ and the initial conditions $(x_0, y_0)$ using the sliders. The left canvas shows the phase portrait in $(x, \dot{x})$ space; the right canvas shows $x(t)$ and $\dot{x}(t)$ over time. The trajectory integrates in real time using RK4 with step $dt = 0.012$.

<iframe
  src="/train-deep-learning/ds-vanderpol/"
  title="DS Lab 4 — Van der Pol Oscillator"
  style="width:100%; min-height:500px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe from the demo

**μ = 0 (conservative harmonic oscillator):**
- Phase portrait: perfect concentric circles (no preferred amplitude).
- Time series: pure sinusoid at frequency $\omega = 1$.
- Change the IC radius — the circle changes size but never converges.

**μ = 0.5 (weak nonlinearity):**
- From IC inside the limit cycle: trajectory spirals outward, settling near $r \approx 2$.
- From IC outside: trajectory spirals inward.
- Time series: nearly sinusoidal but with slight amplitude growth then saturation.
- The limit cycle radius is close to 2 (predicted by averaging).

**μ = 1.5 (moderate nonlinearity):**
- Limit cycle clearly not circular; slightly flattened at top and bottom.
- Time series shows mild asymmetry between half-cycles.

**μ = 3.5 (relaxation oscillation):**
- Phase portrait: a flat, elongated oval with near-vertical sides — the fast jumps.
- Time series: $x(t)$ looks like a square wave; $\dot{x}(t)$ has sharp spike-like peaks at each jump.
- Period is much larger than $2\pi$ — consistent with $T \approx 1.614\mu \approx 5.65$.
- Try placing IC very far from the origin: the trajectory still converges to the same limit cycle.

## Key takeaways

- Limit cycles are isolated closed orbits — the amplitude and waveform are intrinsic to the system, not set by initial conditions.
- The Van der Pol equation models a nonlinear damper that injects energy at small amplitudes and dissipates it at large ones, producing a globally attracting limit cycle.
- The Poincaré–Bendixson theorem proves existence by trapping: a trajectory in a bounded, fixed-point-free region must approach a closed orbit.
- The method of averaging predicts limit-cycle amplitude $r = 2$ for small $\mu$; for large $\mu$ the oscillation becomes a relaxation (sawtooth) with period $\approx 1.614\mu$.
