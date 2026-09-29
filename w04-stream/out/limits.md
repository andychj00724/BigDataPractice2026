# Task 2 - Exact vs Flajolet-Martin Limits

## Machine

- CPU: Apple M3
- RAM: 8 GB
- Python: 3.13.0
- Other programs: VS Code and Terminal were running during measurement.

## Measurement Results

| Stream size n | True distinct | Exact time (s) | Exact peak memory (MB) | FM time (s) | FM peak memory (MB) | FM ratio |
|---:|---:|---:|---:|---:|---:|---:|
| 100,000 | 36,702 | 0.16 | 3.9 | 10.85 | ~0.00 | 0.89x |
| 400,000 | 146,970 | 0.66 | 11.6 | 43.19 | ~0.00 | 0.89x |
| 1,600,000 | 587,625 | 2.83 | 46.6 | 172.80 | ~0.00 | 0.89x |
| 6,400,000 | 2,349,909 | 11.86 | 188.3 | 693.36 | ~0.00 | 0.89x |

## Where Exact Became Unpleasant

At n=6,400,000, the exact method required 11.86 seconds and about 188.3 MB of peak memory.

This was the largest size tested. The exact method was still able to finish, but its memory usage had grown substantially compared with the smaller runs. I stopped here because larger runs would require significantly more time and memory.

The limiting factor for the exact method was increasing memory usage rather than failure of the algorithm itself.

## Memory Growth

The exact method stores every distinct item in a Python set, so its memory usage increased as the stream size increased.

Exact peak memory:

- 100,000 -> 3.9 MB
- 400,000 -> 11.6 MB
- 1,600,000 -> 46.6 MB
- 6,400,000 -> 188.3 MB

When n increased by 4x, the exact memory usage increased by approximately:

- 3.9 MB -> 11.6 MB: about 2.97x
- 11.6 MB -> 46.6 MB: about 4.02x
- 46.6 MB -> 188.3 MB: about 4.04x

Therefore, the exact method shows approximately linear memory growth with n at larger sizes.

Flajolet-Martin used approximately constant memory at every stream size. Its memory usage is determined mainly by the number of hash registers rather than by the number of stream elements.

Therefore:

- Exact set memory growth: approximately O(n)
- Flajolet-Martin memory growth: approximately O(1) with respect to stream size

## Flajolet-Martin Accuracy

The FM estimate ratio was:

- n=100,000: 0.89x
- n=400,000: 0.89x
- n=1,600,000: 0.89x
- n=6,400,000: 0.89x

The accuracy did not noticeably improve or worsen as n increased in these measurements.

This demonstrates the trade-off of Flajolet-Martin: it uses bounded memory independent of stream length, but gives an approximate distinct count rather than an exact value.

## Is a Factor-of-Two Error Acceptable?

A factor-of-two error may be acceptable when only a rough estimate is needed, such as monitoring whether the number of daily visitors is on the order of tens of thousands or millions.

However, it would not be acceptable when the exact number is used for billing, financial reporting, or other decisions where a large counting error directly affects the result.