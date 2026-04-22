---
date: 2026-04-21 10:00:00.000000
layout: post
title: "Queueing Lab 1 - M/M/1: The Single-Server Queue"
description: "Explore the M/M/1 queue interactively — simulate Poisson arrivals and exponential service, then watch theory converge to observation in real time."
tags: [queueing theory, simulation, probability]
comments: true
---

Every time you wait — at a checkout, for a web request to return, for a packet to be routed — you are experiencing a queue. **Queueing theory** gives us exact formulas for how long those waits will be, and the M/M/1 model is where it all starts.

<!--excerpt-->

## Kendall notation: M/M/1

The three letters encode the queue's character:

| Symbol | Meaning |
|--------|---------|
| First **M** | Markovian (Poisson) arrivals — inter-arrival times are exponential with rate **λ** |
| Second **M** | Markovian service — service durations are exponential with rate **μ** |
| **1** | One server |

A Poisson arrival process is **memoryless**: no matter how long you have been waiting for the next customer, the expected remaining wait is still $1/\lambda$. This property — the exponential distribution's defining feature — makes the mathematics tractable.

## The key quantity: utilisation ρ

$$\rho = \frac{\lambda}{\mu}$$

$\rho$ is the fraction of time the server is busy. For the queue to be **stable** (finite average wait), we need $\rho < 1$. When $\rho \ge 1$ arrivals outpace service and the queue grows without limit.

## Steady-state formulas

Once the queue reaches statistical equilibrium:

| Quantity | Formula | Meaning |
|----------|---------|---------|
| $L$ | $\dfrac{\rho}{1-\rho}$ | Avg number in the **system** |
| $L_q$ | $\dfrac{\rho^2}{1-\rho}$ | Avg number **waiting** |
| $W$ | $\dfrac{1}{\mu - \lambda}$ | Avg **time** in the system |
| $W_q$ | $\dfrac{\lambda}{\mu(\mu-\lambda)}$ | Avg **waiting** time |

These four quantities are linked by **Little's Law**: $L = \lambda W$. It holds for any stable queue regardless of arrival or service distribution — one of the most powerful results in all of operations research.

Notice how steeply $L_q$ rises near $\rho = 1$: as $\rho \to 1$, the queue length diverges as $1/(1-\rho)$. Operating at 90% utilisation ($\rho = 0.9$) gives $L_q = 8.1$; at 95% that becomes $L_q = 18.1$. The last few percent of capacity are enormously expensive in wait time.

## Live simulator

Adjust **λ** and **μ**, watch customers (coloured circles) flow through the queue and server, and see how the observed statistics converge to the theoretical values. The dashed line on the chart marks the theoretical $L_q$.

<iframe src="/train-deep-learning/queue-mm1/" width="100%" height="640" frameborder="0" scrolling="no" style="border-radius:8px;margin:1rem 0;display:block"></iframe>

## Things to try

- Set $\rho$ close to 0.9 and watch $L_q$ climb
- Push $\lambda \ge \mu$ to see the unstable regime — the queue never drains
- After a reset, note how long it takes for observed values to match theory (burn-in period)
- Drop speed to **1×** to see individual customers animate through the queue

## Key takeaways

1. The M/M/1 queue captures a huge class of real systems with just two parameters
2. Performance degrades non-linearly — small increases in load near capacity cause large increases in wait time
3. Little's Law ($L = \lambda W$) is a design law: if you want to halve wait time, either halve load or double throughput
4. The memoryless (exponential) assumption is the price of analytical tractability — the next post relaxes it with general service distributions
