---
date: 2025-11-12 09:00:00.000000
layout: post
title: "RL 101 - Lesson 8 - Deep Q-Networks"
description: "RL 101 Lesson 8 - DQN, experience replay, and grid world"
tags: [reinforcement learning, deep learning]
comments: true
---
Supervised learning requires labeled examples. Reinforcement learning replaces labels with *rewards from experience*. Deep Q-Networks (DQN) combine Q-learning with a neural function approximator to let agents learn policies directly from raw observations.
<!--excerpt-->

## The Q-function

For a policy $\pi$ in a Markov Decision Process, the action-value function is

$$
Q^\pi(s, a) = \mathbb{E}_\pi\!\left[\sum_{t=0}^\infty \gamma^t r_t \,\Big|\, s_0 = s,\, a_0 = a\right].
$$

The optimal $Q^*(s, a)$ satisfies the Bellman optimality equation:

$$
Q^*(s, a) = r + \gamma \max_{a'} Q^*(s', a').
$$

DQN approximates $Q^*$ with a neural network $Q_\theta$ and minimizes the TD loss:

$$
\mathcal{L} = \bigl(r + \gamma \max_{a'} Q_{\bar\theta}(s', a') - Q_\theta(s, a)\bigr)^2,
$$

where $Q_{\bar\theta}$ is a **target network** — a periodically copied snapshot of $Q_\theta$ — that stabilizes the regression targets.

## Two key tricks

1. **Experience replay:** transitions $(s, a, r, s')$ are stored in a buffer and sampled randomly for each gradient step. This breaks temporal correlations that destabilize gradient descent.

2. **Target network:** using $Q_{\bar\theta}$ rather than $Q_\theta$ for the bootstrap target prevents the "chasing a moving target" problem that causes divergence in naive Q-learning.

## Live demo

<iframe
  src="/train-deep-learning/dqn/"
  title="Deep Q-Network Grid World"
  style="width: 100%; min-height: 660px; border: 1px solid #ddd; border-radius: 6px;"
  loading="lazy"
  allowfullscreen
></iframe>

The grid world has a goal (green) and obstacles (red). The agent (blue) starts at a random cell each episode. Watch the episode return climb and the action arrows converge to a consistent policy.

## Key takeaways

- DQN makes deep RL practical by separating gradient updates (replay buffer) from environment interactions (ε-greedy rollouts).
- The target network is a simple but critical stabilization trick — copying weights every 50 gradient steps works well for small problems.
- ε-greedy decay balances exploration early on with exploitation once a policy starts to form.

**Next up — Lessons 9 & 10:** we leave grid worlds behind and tackle continuous control with an inverted pendulum and a lunar lander.
