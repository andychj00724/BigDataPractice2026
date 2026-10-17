# Task 2 - Support Threshold Explosion

## Machine
- Platform: macOS 15.6.1 ARM64
- Processor: ARM
- Python: 3.13.0

## Measurement Results

| Support | Frequent pairs | Peak counters | Time (s) | Peak memory (MB) |
|---:|---:|---:|---:|---:|
| 400 | 249 | 10,585 | 0.42 | 1.1 |
| 200 | 776 | 58,626 | 0.65 | 6.4 |
| 100 | 2,244 | 273,701 | 1.30 | 26.4 |
| 50 | 6,397 | 820,259 | 2.02 | 102.2 |
| 25 | 17,045 | 893,456 | 2.50 | 102.2 |
| 12 | 43,116 | 893,456 | 2.51 | 102.8 |
| 6 | 101,938 | 893,456 | 2.66 | 119.4 |
| 3 | 250,054 | 893,456 | 2.70 | 156.7 |
| 1 | 893,456 | 893,456 | 3.68 | 327.1 |

## Where It Became Unpleasant

The support threshold was lowered all the way to the minimum possible value, support=1. At support=1, the algorithm still completed, but it required 893,456 pair counters and reached 327.1 MB of peak memory. This was the largest memory usage observed and was the practical endpoint of the measurement.

The limiting factor was memory growth rather than execution time, although the run still completed successfully.

## Counter Growth

The number of pair counters did not grow linearly as support decreased.

- 400 -> 200: 10,585 -> 58,626, about 5.54x
- 200 -> 100: 58,626 -> 273,701, about 4.67x
- 100 -> 50: 273,701 -> 820,259, about 3.00x
- 50 -> 25: 820,259 -> 893,456, about 1.09x

After support=25, the counter count stayed at 893,456. The growth was therefore much worse than simple doubling at higher support values, then flattened once almost every possible candidate pair among surviving items was already being counted.

## Frequent Pair Growth

Frequent pairs increased from 249 at support=400 to 893,456 at support=1. Their growth differed from the counter growth.

At support=50, the algorithm held 820,259 counters to produce only 6,397 frequent pairs. This gap is the main problem: lowering support can greatly increase the intermediate state needed to discover the answers, even when the final answer count is still much smaller.

At support=1, every observed pair is frequent by definition, so the frequent-pair count becomes equal to the counter count.

## Summary

Lowering support makes the search more permissive, but it rapidly increases candidate counters and memory usage. This experiment shows why low-support frequent-itemset mining becomes expensive and why methods such as PCY try to filter candidate pairs before allocating full pair counters.
