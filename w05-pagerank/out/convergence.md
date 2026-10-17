# Task 2 - PageRank Convergence

## Machine

- Platform: macOS 15.6.1 ARM64
- Processor: ARM
- Python: 3.13.0

## Beta vs Convergence

| Beta | Iterations | Time (s) | Top 3 |
|---:|---:|---:|---|
| 0.50 | 14 | 0.007 | p00009, p00001, p00006 |
| 0.70 | 17 | 0.008 | p00009, p00001, p00006 |
| 0.85 | 20 | 0.009 | p00009, p00001, p00006 |
| 0.95 | 23 | 0.010 | p00009, p00001, p00006 |
| 0.99 | 24 | 0.010 | p00009, p00001, p00006 |

As beta approaches 1, the number of iterations increases. A larger beta means the random surfer follows links more often and teleports less often, so the damping effect becomes weaker and convergence becomes slower.

## Graph Size

For beta=0.85:

- Default graph (1,200 nodes): 20 iterations, 0.009 s
- 20,000 nodes: 21 iterations, 0.161 s

For beta=0.95:

- Default graph (1,200 nodes): 23 iterations, 0.010 s
- 20,000 nodes: 24 iterations, 0.191 s

The iteration count changed very little as the graph became much larger, while wall time increased substantially. The number of iterations is mainly determined by the convergence behavior of PageRank, while each iteration takes longer on a larger graph because more nodes and edges must be processed.

## Tolerance

For beta=0.85:

- tol=1e-6: 12 iterations
- tol=1e-10: 20 iterations

Tightening the tolerance by four decimal orders required eight additional iterations. In this experiment, each additional decimal digit of precision cost about two extra iterations.

## Ranking Stability

The top-10 ranking changed when beta increased from 0.5 to 0.7.

At beta=0.5, the relevant part of the ranking was:

- p00002
- p00000
- p00004

At beta=0.7 and above, it became:

- p00002
- p00004
- p00000

Therefore, the first observed change occurred between beta=0.5 and beta=0.7.

The top three pages remained unchanged for all tested beta values, but the lower positions in the top-10 ranking were affected by beta. This means beta is not only a convergence parameter; it can also influence the final ranking and should therefore be reported when publishing PageRank results.
