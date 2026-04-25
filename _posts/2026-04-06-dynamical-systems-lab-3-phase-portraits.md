---
date: 2026-04-06 09:00:00.000000
layout: post
title: "Dynamical Systems Lab 3 - 2D Phase Portraits"
description: "Jacobians, eigenvalues, nullclines, and the trace-determinant plane — classify every possible 2D equilibrium and watch trajectories navigate the full phase plane."
tags: [dynamical systems, chaos, nonlinear dynamics]
comments: true
---

Moving from one dimension to two transforms everything. In 1D, trajectories can only march left or right. In 2D, they spiral, circulate, converge along curves, and diverge along others. The **phase portrait** — the collection of all trajectories in the $(x, y)$ plane — is the master diagram that reveals this rich geometry at a glance.

<!--excerpt-->

## The 2D autonomous system

A planar autonomous ODE system is

$$\dot{x} = f(x, y), \qquad \dot{y} = g(x, y)$$

The pair $(f, g)$ defines a **vector field**: at every point $(x, y)$ it prescribes an instantaneous velocity vector $(\dot{x}, \dot{y})$. A trajectory $\bigl(x(t), y(t)\bigr)$ is a curve in the plane that is always tangent to this vector field.

A **fixed point** $(x^*, y^*)$ satisfies both $f(x^*, y^*) = 0$ and $g(x^*, y^*) = 0$ simultaneously.

## Linearisation and the Jacobian

Near a fixed point $(x^*, y^*)$, write $\mathbf{u} = (x - x^*, \, y - y^*)^T$ for the displacement. Taylor-expand the vector field:

$$\dot{\mathbf{u}} = J\,\mathbf{u} + O(|\mathbf{u}|^2)$$

where $J$ is the **Jacobian matrix** evaluated at $(x^*, y^*)$:

$$J = \begin{pmatrix} \partial f/\partial x & \partial f/\partial y \\ \partial g/\partial x & \partial g/\partial y \end{pmatrix}_{(x^*,\, y^*)}$$

The linearised system $\dot{\mathbf{u}} = J\mathbf{u}$ has general solution $\mathbf{u}(t) = c_1 e^{\lambda_1 t}\mathbf{v}_1 + c_2 e^{\lambda_2 t}\mathbf{v}_2$ where $\lambda_{1,2}$ and $\mathbf{v}_{1,2}$ are the eigenvalues and eigenvectors of $J$.

## Eigenvalue analysis

The eigenvalues satisfy the **characteristic polynomial**

$$\lambda^2 - \tau\lambda + \Delta = 0 \implies \lambda_{1,2} = \frac{\tau \pm \sqrt{\tau^2 - 4\Delta}}{2}$$

where $\tau = \text{tr}(J) = \lambda_1 + \lambda_2$ and $\Delta = \det(J) = \lambda_1 \lambda_2$.

**The trace-determinant plane** classifies every fixed point:

| Condition | Fixed point type |
|---|---|
| $\Delta < 0$ | **Saddle** (one $\lambda > 0$, one $\lambda < 0$) |
| $\Delta > 0$, $\tau^2 > 4\Delta$, $\tau < 0$ | **Stable node** (two negative real $\lambda$) |
| $\Delta > 0$, $\tau^2 > 4\Delta$, $\tau > 0$ | **Unstable node** (two positive real $\lambda$) |
| $\Delta > 0$, $\tau^2 < 4\Delta$, $\tau < 0$ | **Stable spiral** (complex $\lambda$ with $\text{Re}\,\lambda < 0$) |
| $\Delta > 0$, $\tau^2 < 4\Delta$, $\tau > 0$ | **Unstable spiral** (complex $\lambda$ with $\text{Re}\,\lambda > 0$) |
| $\Delta > 0$, $\tau = 0$ | **Centre** (purely imaginary $\lambda$) |
| $\tau^2 = 4\Delta$, $\tau < 0$ | **Stable star / degenerate node** |

**Key stability criteria:**
- **Stable** (both eigenvalues have negative real part) $\Leftrightarrow$ $\tau < 0$ and $\Delta > 0$.
- **Saddle** $\Leftrightarrow$ $\Delta < 0$.
- **Centre** (neutrally stable): arises only when $\tau = 0$ exactly, which is non-generic in the absence of symmetry (a conservative system).

## Geometry of each fixed point type

**Stable/Unstable node:** Trajectories approach (or flee) the fixed point along the eigenvectors of $J$. Near the origin, the faster-decaying mode dominates at large times, so all trajectories become tangent to the **slow eigenvector** (the one with eigenvalue of smaller magnitude).

**Saddle:** The eigenvector corresponding to $\lambda < 0$ defines the **stable manifold** $W^s$ — the curve along which trajectories approach the saddle from both sides. The eigenvector for $\lambda > 0$ defines the **unstable manifold** $W^u$. Every trajectory not on $W^s$ is eventually repelled along $W^u$.

**Spiral:** Trajectories wind around the fixed point, approaching it (stable, $\tau < 0$) or spiralling away (unstable, $\tau > 0$). The angular frequency near the fixed point is $\omega = \text{Im}(\lambda_{1,2}) = \sqrt{\Delta - \tau^2/4}$ (for the complex case).

**Centre:** Trajectories form closed ellipses. This requires $\tau = 0$ exactly and is preserved only in conservative systems with an energy function.

## Nullclines

A **nullcline** is a curve in the phase plane where one velocity component vanishes:

- **$x$-nullcline** ($\dot{x} = 0$, i.e., $f(x,y) = 0$): the state moves **vertically** here (only $\dot{y}$ contributes).
- **$y$-nullcline** ($\dot{y} = 0$, i.e., $g(x,y) = 0$): the state moves **horizontally** here.

Fixed points are intersections of nullclines. Between nullclines the sign of each velocity component is constant, so the plane is divided into regions where the flow has a definite diagonal direction. This gives a coarse but powerful picture of the global flow.

## Example: Lotka-Volterra predator-prey

$$\dot{x} = \alpha x - \beta xy, \qquad \dot{y} = \delta xy - \gamma y$$

Here $x$ = prey, $y$ = predator. Fixed points:
- **Origin** $(0,0)$: saddle (prey grows unchecked, predators die).
- **Coexistence** $(x^*, y^*) = (\gamma/\delta,\, \alpha/\beta)$: obtained by setting both equations to zero.

Jacobian at $(x^*, y^*)$:

$$J = \begin{pmatrix} 0 & -\beta x^* \\ \delta y^* & 0 \end{pmatrix}$$

$$\tau = 0, \quad \Delta = \beta\delta x^* y^* > 0 \implies \lambda_{1,2} = \pm i\sqrt{\beta\delta x^* y^*}$$

Pure imaginary eigenvalues: the coexistence equilibrium is a **centre**. The classical Lotka-Volterra model conserves an implicit energy function (first integral) $H = \delta x - \gamma \ln x + \beta y - \alpha \ln y = \text{const}$, producing closed population cycles.

## The Hartman-Grobman theorem

For **hyperbolic** fixed points (no eigenvalue has zero real part), the Hartman-Grobman theorem guarantees that the nonlinear system near the fixed point is **topologically conjugate** to its linearisation. In plain language: the phase portrait of the full nonlinear system looks qualitatively identical to that of the linearised system near a hyperbolic fixed point. The eigenvalues of $J$ determine the topology.

This fails for non-hyperbolic cases ($\tau = 0$): a centre of the linearisation may be a stable spiral, an unstable spiral, or a true centre in the nonlinear system, depending on higher-order terms.

## Live demo

Click anywhere on the phase plane canvas to launch a trajectory from that initial condition. Up to eight trajectories are active simultaneously; clear with the **Clear** button. Use the dropdown to choose:
- **Linear** — $(\dot{x}, \dot{y}) = (ax+by, cx+dy)$; the trace-determinant classification is displayed in the info panel.
- **Nonlinear saddle**, **Pendulum**, **Lotka-Volterra** — see how nonlinearity distorts the linear portrait globally.
Vector field arrows and nullclines (faint dots) are always visible.

<iframe
  src="/train-deep-learning/ds-phase-portrait/"
  title="DS Lab 3 — 2D Phase Portrait"
  style="width:100%; min-height:580px; border:1px solid #ddd; border-radius:6px;"
  loading="lazy"
  allowfullscreen
></iframe>

## Things to observe from the demo

**Linear system — vary $a, b, c, d$:**
- Set $a = -1, d = -1, b = c = 0$: stable node — all trajectories converge to origin along straight lines (both eigenvalues $= -1$, eigenvectors are the axes).
- Set $a = -1, d = -2$: stable node with two distinct rates — near origin, trajectories become tangent to the slow ($\lambda = -1$) eigenvector.
- Set $a = 0.5, d = -2, b = 0, c = 0$: saddle — trajectories along the $y$-axis approach the origin; along the $x$-axis they flee. Click near the $y$-axis and watch the trajectory nearly approach then suddenly veer away.
- Set $a = 0, d = 0, b = -1, c = 1$ (skew-symmetric): eigenvalues are purely imaginary — centre; watch the closed ellipses.
- Increment $a$ slightly from 0: centre becomes an unstable spiral; decrement: stable spiral. This is the Hopf mechanism explored in Lab 9.

**Pendulum** ($\ddot{\theta} = -\sin\theta - 0.1\dot{\theta}$):
- Near $\theta = 0$: stable spiral — the pendulum at rest below. Trajectories corkscrewing inward.
- Near $\theta = \pi$: saddle — the inverted pendulum. Click near $(3.14, 0)$ and watch the trajectory nearly balance then fall off to one side.
- The separatrices connecting adjacent saddles divide the plane into "oscillation" and "rotation" regions.

## Key takeaways

- The Jacobian $J$ at a fixed point gives the linearised flow; eigenvalues of $J$ determine the local qualitative type.
- Stability in 2D requires $\text{tr}(J) < 0$ and $\det(J) > 0$.
- Nullclines partition the phase plane and reveal which direction the flow is heading in each region.
- The Hartman-Grobman theorem licenses using the linearisation for topological classification at hyperbolic fixed points.
