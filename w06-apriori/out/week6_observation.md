# Week 6 Observations

## Task 1

Confidence is directional because the denominator is the support of the antecedent. In the small example, the frequent items all happen to have the same singleton support, so many frequent-rule confidences tie; for a raw pair such as bread and cola, bread -> cola is 1/5 = 0.20 while cola -> bread is 1/2 = 0.50, showing why the two directions are not generally equivalent.

The highest confidence among the emitted support-3 rules is 0.80, for example diaper -> beer. Its lift is 0.80 / (5/7) = 1.12, so the rule is only modestly more informative than beer's already-high baseline frequency.

With 2,000 items, brute force would need 2,000*1,999/2 = 1,999,000 possible pair counters. On the benchmark data, A-Priori reduced this to a peak of 820,259 pair counters after filtering by frequent singletons.

## Task 2

The threshold was lowered all the way to support=1, where the run still completed in 3.68 s but peak memory reached 327.1 MB. This was the minimum possible support and therefore the practical endpoint of the experiment; memory growth was the main limiting factor.

The counter count grew much faster than simple doubling at first: 10,585 -> 58,626 (5.54x), 58,626 -> 273,701 (4.67x), and 273,701 -> 820,259 (3.00x) as support was halved. It then saturated near 893,456 counters because almost every candidate pair among the surviving items was already being counted.

The number of answers grew differently from the number of counters. At support=50, 820,259 counters were maintained to produce only 6,397 frequent pairs, while at support=1 all 893,456 observed pairs became frequent. This gap explains why asking for a slightly lower support threshold can make the intermediate state explode long before the final answer set becomes equally large.

## Task 3

I used 1,000,003 hash buckets. A large prime-sized table reduces collisions while keeping the bucket structure fixed in size; with this setting PCY found exactly the same 6,397 frequent pairs as the baseline while reducing peak pair counters from 820,259 to 16,052, a 98.0% cut.

The bucket array itself is real memory and must be counted honestly. During pass one it contains 1,000,003 bucket counts, so by raw slot count it is actually larger than the baseline's 820,259 pair counters on this dataset; the benchmark score only measures pair counters. PCY begins to win clearly in this simple accounting once the baseline would require more than about one million pair counters, although the real byte-level crossover can occur earlier because a Python dictionary pair counter is much heavier than one bucket slot.

When the bucket array was made much smaller, collisions increased and the bitmap stopped filtering effectively. Using 100,003 buckets increased peak pair counters to about 147,607, and with about 10,000 buckets the peak returned to roughly the baseline value of 820,259. The final frequent-pair answer stayed the same, but the memory-saving benefit disappeared as buckets became too crowded.
