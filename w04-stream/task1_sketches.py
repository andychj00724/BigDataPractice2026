#!/usr/bin/env python3
"""Week 4 · Task 1 — Answer questions about a stream you cannot store.

Textbook §4.3 (sampling), §4.4 (Bloom filter), §4.5 (Flajolet-Martin).

The premise of the whole chapter: the stream is longer than your memory, it
goes past once, and you still have to answer. Every method here trades an exact
answer for a bounded amount of space, and the job is to know exactly what you
traded.

You build three, and the harness checks each against the truth it is
approximating.

    python3 task1_sketches.py --verify
"""
import argparse, random
import math
import hashlib
import statistics


class BloomFilter:
    """Membership, with one-sided error.

    m bits, k hash functions.
    """

    def __init__(self, m, k, seed=246):
        self.m = m
        self.k = k
        self.seed = seed
        self.bits = [0] * m

    def _hashes(self, item):
        item_bytes = str(item).encode("utf-8")

        for i in range(self.k):
            data = (
                str(self.seed).encode("utf-8")
                + b":"
                + str(i).encode("utf-8")
                + b":"
                + item_bytes
            )

            digest = hashlib.sha256(data).digest()
            value = int.from_bytes(digest[:8], "big")

            yield value % self.m

    def add(self, item):
        for pos in self._hashes(item):
            self.bits[pos] = 1

    def __contains__(self, item):
        return all(self.bits[pos] == 1 for pos in self._hashes(item))

    def expected_fp_rate(self, n_inserted):
        return (1 - math.exp(-self.k * n_inserted / self.m)) ** self.k


def flajolet_martin(stream, n_hashes=64, seed=246):
    max_zeros = [0] * n_hashes
    mask = (1 << 64) - 1

    def trailing_zeros(x):
        if x == 0:
            return 64
        return (x & -x).bit_length() - 1

    for item in stream:
        data = f"{seed}:{item}".encode("utf-8")
        digest = hashlib.sha256(data).digest()

        h1 = int.from_bytes(digest[:8], "big")
        h2 = int.from_bytes(digest[8:16], "big")

        for i in range(n_hashes):
            value = (h1 + i * h2) & mask
            r = trailing_zeros(value)

            if r > max_zeros[i]:
                max_zeros[i] = r

    estimates = [2 ** r for r in max_zeros]
    return float(statistics.median(estimates))

def reservoir_sample(stream, k, seed=246):
    """Keep k uniformly sampled items from a stream of unknown length."""

    if k <= 0:
        return []

    rng = random.Random(seed)
    reservoir = []

    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            j = rng.randint(0, i)

            if j < k:
                reservoir[j] = item

    return reservoir


# ------------------------------------------------------------------- harness
def verify():
    fails = 0
    rng = random.Random(246)

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<46} {detail}")
        fails += not ok

    # --- Bloom: no false negatives, ever
    try:
        bf = BloomFilter(m=8192, k=5)
    except NotImplementedError:
        print("  BloomFilter is still a stub"); return 1
    inserted = [f"item-{i}" for i in range(800)]
    for x in inserted:
        bf.add(x)
    check("no false negatives", all(x in bf for x in inserted))

    absent = [f"other-{i}" for i in range(20_000)]
    fp = sum(1 for x in absent if x in bf) / len(absent)
    predicted = bf.expected_fp_rate(len(inserted))
    close = abs(fp - predicted) < max(0.02, predicted * 0.5)
    check("measured false-positive rate matches theory", close,
          f"measured {fp:.3%}, predicted {predicted:.3%}")

    # --- Flajolet-Martin: a factor of two is what this method gives you
    try:
        distinct = 20_000
        stream = [f"k{rng.randrange(distinct)}" for _ in range(120_000)]
        est = flajolet_martin(stream)
    except NotImplementedError:
        print("  flajolet_martin is still a stub"); return 1
    true_distinct = len(set(stream))
    ratio = est / true_distinct
    check("distinct estimate within a factor of 2", 0.5 <= ratio <= 2.0,
          f"estimated {est:,.0f}, true {true_distinct:,} ({ratio:.2f}x)")

    # --- Reservoir: uniform over many trials
    try:
        counts = [0] * 20
        trials = 4000
        for t in range(trials):
            s = reservoir_sample(range(20), 5, seed=t)
            for i in s:
                counts[i] += 1
    except NotImplementedError:
        print("  reservoir_sample is still a stub"); return 1
    expected = trials * 5 / 20
    spread = (max(counts) - min(counts)) / expected
    check("reservoir is uniform across items", spread < 0.15,
          f"spread {spread:.1%} around {expected:.0f}")

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    raise SystemExit(verify() if a.verify else p.print_help())
