# Task 2 - Crossover Measurement

## Machine

- CPU: Apple M3
- RAM: 8 GB
- OS: macOS 15.6.1 ARM64
- Python: 3.13.0
- Other programs: VS Code and Terminal were running during the measurement.

## Timing Results

| n | Brute Force (s) | LSH (s) | Brute Comparisons | LSH Comparisons |
|---:|---:|---:|---:|---:|
| 250 | 0.11 | 0.68 | 31,125 | 0 |
| 500 | 0.46 | 1.19 | 124,750 | 10 |
| 1000 | 1.87 | 2.20 | 499,500 | 29 |
| 2000 | 7.76 | 4.23 | 1,999,000 | 136 |
| 4000 | 32.22 | 8.38 | 7,998,000 | 553 |
| 8000 | 129.31 | 16.80 | 31,996,000 | 2,132 |

## Quadratic Check

When n doubled, the brute-force execution time increased by approximately:

- 250 -> 500: 0.46 / 0.11 = 4.18x
- 500 -> 1000: 1.87 / 0.46 = 4.07x
- 1000 -> 2000: 7.76 / 1.87 = 4.15x
- 2000 -> 4000: 32.22 / 7.76 = 4.15x
- 4000 -> 8000: 129.31 / 32.22 = 4.01x

Doubling n increased the brute-force execution time by approximately
four times. Therefore, the measured results are consistent with the
quadratic O(n^2) behavior of brute force.

## Crossover

At n=1000:

- Brute Force: 1.87 s
- LSH: 2.20 s

At n=2000:

- Brute Force: 7.76 s
- LSH: 4.23 s

Therefore, the crossover occurred between n=1000 and n=2000.

For small n, brute force is faster because LSH has additional preprocessing
costs. LSH must generate MinHash signatures, divide them into bands, hash the
bands, and create buckets before performing similarity comparisons.

For small datasets, this preprocessing cost is larger than the benefit from
reducing comparisons. As n increases, the O(n^2) comparison cost of brute
force becomes dominant, so LSH becomes faster.

## Peak Memory

At the largest measured size, n=8000:

- Brute Force: 6,808 bytes (about 6.65 KB)
- LSH: 11,879,737 bytes (about 11.33 MB)

LSH requires more memory because it stores additional structures such as
MinHash signatures and LSH buckets.

## Unpleasant Point

At n=8000, brute force required 129.31 seconds, approximately 2 minutes
and 9 seconds.

This was the first measured size where the execution time exceeded one
minute, so n=8000 was recorded as the unpleasant point.

The limiting factor was execution time rather than memory.