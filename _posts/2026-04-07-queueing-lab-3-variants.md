---
date: 2026-04-07 09:00:00.000000
layout: post
title: "Queueing Lab 3 - Variants: M/M/1/K, M/D/1, and M/G/1"
description: "Finite buffers, deterministic service, and the Pollaczek-Khinchine formula — three queue variants that reveal what really drives wait time."
tags: [queueing theory, simulation, M/G/1, M/D/1]
comments: true
---

The M/M/1 model assumes an infinite waiting room and exponential service. Real systems have neither. This lab explores three variations that relax those assumptions and uncover a surprising principle: **service variability, not just load, determines queue length**.

<!--excerpt-->

## M/M/1/K — Finite buffer

Add a finite capacity $K$ to the waiting room. Any customer who arrives when $K$ customers are already waiting is **blocked** (lost). This is called the M/M/1/K or M/M/1/K+1 queue (capacity $K+1$ including the customer in service).

With $\rho = \lambda/\mu$ and system capacity $N = K+1$:

$$P(n) = \frac{(1-\rho)\,\rho^n}{1 - \rho^{N+1}}, \quad n = 0,\ldots,N$$

The blocking probability is $P_b = P(N)$. The effective throughput is $\lambda_{\text{eff}} = \lambda(1-P_b)$.

Key insight: a finite buffer **bounds** queue length but introduces loss. As $K \to \infty$ the formula recovers M/M/1. Networks with bounded queues — routers, manufacturing lines — are modelled this way.

## M/D/1 — Deterministic service

Replace exponential service with a **constant** service time $1/\mu$ (coefficient of variation $C_s^2 = 0$). Arrivals are still Poisson.

The Pollaczek-Khinchine (P-K) formula gives the mean queue length for any single-server queue with Poisson arrivals:

$$L_q = \frac{\rho^2 + \lambda^2 \sigma_s^2}{2(1-\rho)} = \frac{\rho^2(1+C_s^2)}{2(1-\rho)}$$

For M/D/1, $C_s^2 = 0$:

$$L_q^{M/D/1} = \frac{\rho^2}{2(1-\rho)} = \frac{1}{2} L_q^{M/M/1}$$

**Removing service-time randomness cuts the queue in half.** This is the most important practical lesson in queueing theory.

## M/G/1 — General service

The P-K formula above holds for *any* service-time distribution, parameterised entirely by its mean $1/\mu$ and variance $\sigma_s^2$ (through $C_s^2 = \sigma_s^2 \mu^2$):

| Distribution | $C_s^2$ | $L_q$ relative to M/M/1 |
|-------------|---------|------------------------|
| Deterministic | 0 | 0.50× |
| Erlang-5 | 0.2 | 0.60× |
| Erlang-2 | 0.5 | 0.75× |
| Exponential | 1.0 | 1.00× (M/M/1) |
| Hyper-exponential | ≈2.1 | ≈1.55× |

**Only the first two moments of the service distribution matter** — not its shape. A highly variable service process (e.g. occasional very long jobs) inflates queues just as much as increased load.

## Live simulator

Switch between the three models using the tabs. The gold dashed line on the chart shows the theoretical $L_q$; the faint blue line is the M/M/1 reference so you can see the difference directly.

<iframe src="/train-deep-learning/queue-variants/" width="100%" height="700" frameborder="0" scrolling="no" style="border-radius:8px;margin:1rem 0;display:block"></iframe>

## Things to try

- **M/M/1/K**: set $\rho > 1$ — with a finite buffer the system stays stable (customers are shed), unlike M/M/1. Watch the blocking rate converge to theory.
- **M/D/1**: confirm that $L_q$ is visually about half of what the blue M/M/1 line shows, across all values of $\rho$.
- **M/G/1**: switch between distributions at the same $\rho = 0.7$ and watch $L_q$ change — load is identical but service variance moves the queue dramatically.
- **M/G/1 hyper-exp**: even at moderate $\rho$ the queue fluctuates wildly because occasional very long services create bursts of waiting customers.

## Key takeaways

1. **Finite buffers** trade queue length for customer loss; the blocking probability is always computable from steady-state probabilities
2. **Reducing service variability** ($C_s^2$) is often a cheaper lever than adding capacity — standardising process times pays off directly in queue length
3. The **P-K formula** is the single most useful result in applied queueing: $L_q = \rho^2(1+C_s^2)/[2(1-\rho)]$
4. $\rho$ and $C_s^2$ are the two design knobs. Controlling both simultaneously is what separates good system design from guesswork.
