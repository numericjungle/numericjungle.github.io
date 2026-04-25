---
date: 2026-02-24 09:00:00.000000
layout: post
title: "Queueing Lab 2 - M/M/c: Scaling with Multiple Servers"
description: "Add more servers and watch wait times collapse — explore the Erlang C formula and discover when parallelism actually helps."
tags: [queueing theory, simulation, erlang]
comments: true
---

The M/M/1 queue from Lab 1 has a single bottleneck: one server. The **M/M/c** model generalises to $c$ parallel servers all drawing from one shared queue. A single shared queue feeding multiple servers is **always** better than $c$ separate queues (think supermarket vs airport check-in).

<!--excerpt-->

## From M/M/1 to M/M/c

All $c$ servers have the same rate $\mu$. The system can handle up to $c \cdot \mu$ work per second, so utilisation per server is:

$$\rho = \frac{\lambda}{c \cdot \mu}$$

Stability still requires $\rho < 1$, but now $\lambda$ can be much larger before the system tips.

## The Erlang C formula

The probability that an arriving customer has to **wait** (all $c$ servers are busy) is given by the Erlang C formula. With offered load $A = \lambda/\mu$:

$$C(c, A) = \frac{A^c/c! \cdot 1/(1-\rho)}{\sum_{n=0}^{c-1} A^n/n! \; + \; A^c/c! \cdot 1/(1-\rho)}$$

This is the fraction of time all servers are occupied simultaneously. Once $C(c,A)$ is known, all other metrics follow:

| Quantity | Formula |
|----------|---------|
| $W_q$ (avg wait) | $C(c,A) / (c\mu - \lambda)$ |
| $L_q$ (avg queue length) | $\lambda \cdot W_q$ |
| $W$ (avg system time) | $W_q + 1/\mu$ |
| $L$ (avg in system) | $L_q + \lambda/\mu$ |

## The power of pooling

Consider $\lambda = 0.6$, $\mu = 1.0$:

- **c = 1**: $\rho = 0.6$, $L_q \approx 0.90$, $W_q \approx 1.50\text{s}$
- **c = 2**: $\rho = 0.3$, $L_q \approx 0.08$, $W_q \approx 0.13\text{s}$  ← **11× shorter queue!**

Adding one server reduced wait by an order of magnitude. This is the **pooling effect**: variance is absorbed across servers.

Beyond the pooling benefit, there is also a utilisation-flexibility trade-off: two servers at $\rho = 0.3$ each carry slack capacity to absorb bursts without large queues.

## Live simulator

The demo shows each server as a separate box. Customers animate directly to whichever server becomes free first. Compare M/M/c theory (gold) against the M/M/1 reference (blue) in the stats table.

<iframe src="/train-deep-learning/queue-mmc/" width="100%" height="660" frameborder="0" scrolling="no" style="border-radius:8px;margin:1rem 0;display:block"></iframe>

## Things to try

- Start with **c = 1** and increase to **c = 2, 3, 4** — watch $L_q$ collapse
- For fixed total service capacity ($c \cdot \mu$), is one fast server or many slow ones better? *(Hint: they're equivalent in M/M/c when $c\mu$ is constant)*
- Increase $\lambda$ until the system is near-saturated, then add a server — notice the non-linear relief

## Key takeaways

1. The Erlang C formula is the central result for multi-server queues, widely used in call-centre staffing and cloud resource planning
2. Pooling resources always reduces wait time — a shared queue beats dedicated queues for the same total capacity
3. The last server added near the stability boundary delivers the most relief; the first server added at low load delivers the least marginal gain
