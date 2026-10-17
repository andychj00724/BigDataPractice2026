# Task 2 - Curse of Dimensionality

## Machine

- Platform: macOS 15.6.1 ARM64
- Processor: ARM
- Python: 3.13.0
- Slowest measured run: dimension 200, 2,000 points
- Slowest run time: 0.308 s

## Contrast Across Dimensions

| Dimension | Mean distance | Min | Max | Contrast | Relative SD |
|---:|---:|---:|---:|---:|---:|
| 2 | 0.521 | 0.003 | 1.326 | 488.582 | 0.476 |
| 5 | 0.884 | 0.111 | 1.687 | 14.257 | 0.282 |
| 10 | 1.274 | 0.438 | 2.159 | 3.925 | 0.193 |
| 20 | 1.815 | 0.821 | 2.670 | 2.253 | 0.135 |
| 50 | 2.867 | 1.909 | 3.785 | 0.982 | 0.083 |
| 100 | 4.068 | 3.206 | 4.954 | 0.545 | 0.060 |
| 200 | 5.776 | 4.871 | 6.682 | 0.372 | 0.041 |

## A3 - What Happens to Contrast?

Contrast decreased sharply as dimension increased.

- It first dropped below 1 at about dimension 50, where contrast was 0.982.
- It first dropped below 0.5 at dimension 200, where contrast was 0.372.

This means the gap between relatively near and relatively far points becomes much smaller in high dimensions. Distances become less distinctive, so the idea of a clearly "nearest" point becomes weaker.

## A4 - How Mean Distance Grows

The mean distance increased with dimension, but not linearly.

For example:

- d=2: mean 0.521
- d=10: mean 1.274
- d=50: mean 2.867
- d=200: mean 5.776

These values are consistent with growth on the order of sqrt(d), rather than proportional to d. The increase from dimension 50 to 200 multiplies d by 4, while the mean distance increases from about 2.87 to 5.78, roughly a factor of 2.

## A5 - Relative Standard Deviation

Relative standard deviation also decreased steadily:

- d=2: 0.476
- d=10: 0.193
- d=50: 0.083
- d=100: 0.060
- d=200: 0.041

This shows that distances are becoming more tightly concentrated around their mean as dimension increases.

Between contrast and relative standard deviation, relative standard deviation more directly captures the concentration of the full distance distribution, while contrast is useful for showing how the extreme nearest/farthest gap collapses.

## A6 - Does Point Count Matter?

At fixed dimension 200:

- n=1,000: contrast = 0.372
- n=2,000: contrast = 0.448

So contrast depends on point count as well as dimension. With more points, the sample contains more extreme close and far pairs, which can increase the observed max-min gap.

Therefore, there is not one universal dimension at which distance "stops meaning anything"; the threshold also depends on the data size.

## A7 - Machine and Largest Run

The measurements were run on macOS 15.6.1 ARM64 using Python 3.13.0.

The slowest measured run was dimension 200 with 2,000 points, which took about 0.308 seconds.

## A8 - Does This Threaten Week 3 LSH?

Not directly.

This experiment uses Euclidean distance between random points in a high-dimensional unit cube. Week 3 used Jaccard similarity on shingle sets, which is a different similarity measure and a different data representation.

The general lesson still matters: high-dimensional representations can make similarity less discriminative. However, the measured Euclidean curse here does not automatically imply that the Jaccard-based LSH experiment from Week 3 suffers in the same way.
