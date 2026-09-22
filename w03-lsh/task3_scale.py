#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything.

Textbook §3.4.

`BruteForce` compares every pair. On 3,000 documents that is 4.5 million
comparisons and it is completely correct. On 3 million documents it is 4.5
trillion and it is completely useless.

Beat it. Find the same near-duplicate pairs while making far fewer comparisons.

    python3 bench.py
    python3 bench.py --yours

The harness counts every call you make to `similarity()`. That is your score.
It also checks **recall** - which of the truly similar pairs you found. Skipping
comparisons is easy; skipping comparisons without losing the pairs is the task.
"""
import random


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))
        return out


class YourFinder:
    def __init__(self, threshold):
        self.threshold = threshold
        self.num_hashes = 120
        self.bands = 40

    def find(self, docs, similarity):
        if not docs:
            return set()

        from task1_minhash import minhash_signatures, lsh_candidates

        max_row = max(
            (max(doc) for doc in docs if doc),
            default=-1
        )
        n_rows = max_row + 1

        prime = 4294967311

        rng = random.Random(42)

        hashes = []

        for _ in range(self.num_hashes):
            a = rng.randrange(1, prime)
            b = rng.randrange(0, prime)

            hashes.append(
                lambda r, a=a, b=b: (a * r + b) % prime
            )

        signatures = minhash_signatures(
            docs,
            hashes,
            n_rows
        )

        candidates = lsh_candidates(
            signatures,
            self.bands
        )

        out = set()

        for i, j in candidates:
            if similarity(docs[i], docs[j]) >= self.threshold:
                out.add((i, j))

        return out