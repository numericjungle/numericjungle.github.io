---
date: 2025-11-16 15:11:14.278892
layout: post
title: RL 101 - inverted pendulum
description: "RL 101   lesson 1"
tags: []
comments: true
---
<!--excerpt-->

## Why start with an inverted pendulum?

Balancing a cart-pole is the canonical “hello world” for reinforcement learning: the physics are intuitive, the math is compact, and the reward structure exposes what it means to trade short-term torque for long-term stability. In this lesson we will:

- derive the nonlinear equations of motion and the linearized approximation you see in textbooks,
- turn the balancing objective into a reward signal,
- sketch a Deep Q-Network (DQN) agent for continuous control via discretized actions,
- and watch the live training visualization right inside the page.

## Dynamics refresher

We model a cart of mass $m_c$ with a pole of mass $m_p$ and length $2\ell$. Let $x$ be the cart position, $\theta$ the pole angle measured from the upright position, and $u$ the horizontal force applied to the cart. The continuous dynamics are

$$
\begin{aligned}
\dot x &= v, \\
\dot v &= \frac{u + m_p \ell (\dot\theta^2 \sin\theta - \ddot\theta \cos\theta)}{m_c + m_p}, \\
\ddot\theta &= \frac{g\sin\theta - \cos\theta\, \dot v}{\ell\left(\frac{4}{3} - \frac{m_p \cos^2\theta}{m_c + m_p}\right)}.
\end{aligned}
$$

Around the upright equilibrium $(x, v, \theta, \dot\theta) = (0, 0, 0, 0)$ we can linearize to obtain the familiar state-space form

$$
\dot{\mathbf{s}} = A\mathbf{s} + Bu, \quad
\mathbf{s} = \begin{bmatrix} x & v & \theta & \dot\theta \end{bmatrix}^\top,
$$

where

$$
A = \begin{bmatrix}
0 & 1 & 0 & 0 \\
0 & 0 & \frac{-m_p g}{m_c} & 0 \\
0 & 0 & 0 & 1 \\
0 & 0 & \frac{(m_c+m_p) g}{m_c \ell} & 0
\end{bmatrix},
\quad
B = \begin{bmatrix}
0 \\
\frac{1}{m_c} \\
0 \\
\frac{-1}{m_c \ell}
\end{bmatrix}.
$$

The linear model is perfect for analytical control (LQR, pole placement), but DQN learns directly from the nonlinear simulator, so we only need the equations conceptually to design rewards and normalize observations.

## Reward shaping

We map each transition $(\mathbf{s}_t, u_t, \mathbf{s}_{t+1})$ to a scalar reward. A simple yet effective shaping is

$$
r_t = 1 - \alpha \left(\frac{\lvert\theta_t\rvert}{\theta_{\max}}\right)^2 - \beta \left(\frac{\lvert x_t\rvert}{x_{\max}}\right)^2 - \gamma \frac{\lvert u_t\rvert}{u_{\max}},
$$

which encourages staying upright ($\theta \approx 0$), centered ($x \approx 0$), and using minimal actuation. Episode termination happens when $\lvert\theta\rvert > \theta_{\max}$ or $\lvert x\rvert > x_{\max}$, yielding a return signal that correlates strongly with balance duration.

## DQN recap for control

1. **Discretize actions.** Even though force is continuous, we use a small discrete set (e.g., $u \in \{-10, 0, +10\}$ N) so standard DQN applies.
2. **State encoder.** Feed normalized $(x, v, \theta, \dot\theta)$ into a small MLP: `Dense(64) → ReLU → Dense(64) → ReLU → Dense(|\mathcal{A}|)`.
3. **Targets.** For each transition, compute $y_t = r_t + \gamma \max_{u'} Q_{\text{targ}}(\mathbf{s}_{t+1}, u')$.
4. **Replay + target network.** Sample mini-batches from replay memory and update the target net slowly to stabilize learning.

Algorithm sketch:

```python
for episode in range(num_episodes):
    s = env.reset()
    for t in range(max_steps):
        a = epsilon_greedy(Q, s)
        s_next, r, done, _ = env.step(a)
        replay.add(s, a, r, s_next, done)
        if len(replay) > warmup:
            batch = replay.sample(batch_size)
            update_q_network(batch)
        if done:
            break
        s = s_next
    soft_update(target_Q, Q)
```

## Live training visualization

Below is a custom in-browser cart-pole trainer powered by a cross-entropy method policy search. It runs entirely client-side (no network calls) and uses the same dynamics described earlier, so you can tweak hyperparameters and immediately see how long the pendulum survives.

<iframe
  src="/train-deep-learning/inverted-pendulum/"
  title="Inverted Pendulum Trainer"
  style="width: 100%; min-height: 760px; border: 1px solid #ddd; border-radius: 6px;"
  loading="lazy"
  allowfullscreen
></iframe>

Prefer a larger canvas? Open the dedicated page at [Train Deep Learning → Inverted Pendulum](/train-deep-learning/inverted-pendulum/) and run the trainer in its own tab.

## Key takeaways

- Modeling the cart-pole lets us reason about reward shaping even when we train end-to-end with DQN.
- Reward shaping parameters $(\alpha, \beta, \gamma)$ should reflect how much you care about angle, position, and control effort.
- Discretized torque combined with replay buffers yield a surprisingly stable training curve for such a chaotic system.
- Interactive visualizations help build intuition faster than static plots—keep them handy while tweaking hyperparameters.
