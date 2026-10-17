#!/usr/bin/env python3
"""Week 6 · Task 3 — Make pass two fit.

Textbook §6.3 (PCY), §6.3.2 - §6.3.4.

`PlainApriori` does what Task 1 asked: use pass one to drop infrequent items,
then count every pair of surviving items. That is already much better than
counting all pairs. It is still not enough, because the surviving items are the
common ones, and the common ones appear together constantly.

The harness measures **the peak number of pair counters you held**, because
that is the thing that decides whether the algorithm runs at all. §6.3 is about
spending pass one's spare memory to shrink it.

    python3 bench.py
    python3 bench.py --yours

Correctness first: you must find exactly the same frequent pairs. Finding fewer
is not an optimisation.
"""
from collections import Counter
from itertools import combinations


class PlainApriori:
    """Pass one drops infrequent items. Pass two counts every surviving pair."""

    def __init__(self, support):
        self.support = support
        self.peak_counters = 0

    def run(self, baskets):
        counts = Counter()
        for basket in baskets:
            counts.update(basket)
        frequent = {i for i, c in counts.items() if c >= self.support}

        pair_counts = Counter()
        for basket in baskets:
            items = sorted(basket & frequent)
            for pair in combinations(items, 2):
                pair_counts[pair] += 1
            self.peak_counters = max(self.peak_counters, len(pair_counts))

        return {frozenset(p): c for p, c in pair_counts.items()
                if c >= self.support}


class YourAlgorithm:
    def __init__(self, support):
        self.support = support
        self.peak_counters = 0

        # 충분히 큰 bucket 수
        self.num_buckets = 1_000_003

    def _bucket(self, a, b):
        # deterministic pair hash
        return ((a * 1_000_003) ^ (b * 9176 + 246)) % self.num_buckets

    def run(self, baskets):
        # 1) singleton count
        item_counts = Counter()

        # 2) pair bucket count
        bucket_counts = [0] * self.num_buckets

        for basket in baskets:
            items = sorted(basket)

            item_counts.update(items)

            for a, b in combinations(items, 2):
                idx = self._bucket(a, b)
                bucket_counts[idx] += 1

        # frequent singleton
        frequent_items = {
            item
            for item, count in item_counts.items()
            if count >= self.support
        }

        # bucket bitmap
        bucket_bitmap = [
            count >= self.support
            for count in bucket_counts
        ]

        # bucket count array는 pass 2 전에 제거
        del bucket_counts

        pair_counts = Counter()

        for basket in baskets:
            items = sorted(basket & frequent_items)

            for a, b in combinations(items, 2):
                idx = self._bucket(a, b)

                # frequent bucket인 pair만 실제 counter 생성
                if bucket_bitmap[idx]:
                    pair_counts[(a, b)] += 1

            self.peak_counters = max(
                self.peak_counters,
                len(pair_counts)
            )

        return {
            frozenset(pair): count
            for pair, count in pair_counts.items()
            if count >= self.support
        }