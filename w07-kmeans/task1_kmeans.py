#!/usr/bin/env python3
"""Week 7 · Task 1 — k-means, and the thing that decides the answer.

Textbook §7.1 (clustering, the curse of dimensionality), §7.3 (k-means).

k-means is four lines: pick centroids, assign every point to the nearest one,
move each centroid to the mean of its points, repeat. It always converges.

It converges to a **local** optimum, and which one depends entirely on where you
started. That is not a footnote - it is the difference between a clustering that
means something and one that does not, and you can watch it happen on nine points.

    python3 task1_kmeans.py --verify
"""
import argparse, math, random

# Three obvious blobs of three points each. Any sensible clustering finds them.
BLOBS = [(0.0, 0.0), (0.2, 0.1), (0.1, 0.2),
         (8.0, 8.0), (8.2, 8.1), (8.1, 8.2),
         (0.0, 8.0), (0.2, 8.1), (0.1, 8.2)]


def euclidean(a, b):
    """Distance between two points of any dimension."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def assign(points, centroids):
    """Nearest centroid for each point. Return a list of centroid indices.

    Ties go to the lower index, so that everybody's answer is the same.
    """
    labels = []

    for p in points:
        best_idx = 0
        best_dist = euclidean(p, centroids[0])

        for j in range(1, len(centroids)):
            d = euclidean(p, centroids[j])

            # strictly smaller일 때만 변경
            # 같으면 기존의 더 낮은 index 유지
            if d < best_dist:
                best_dist = d
                best_idx = j

        labels.append(best_idx)

    return labels


def update(points, labels, k):
    """Move each centroid to the mean of its points.

    Empty cluster는 전체 데이터의 평균 위치로 재배치한다.
    """
    dim = len(points[0])

    # 전체 데이터 평균: empty cluster fallback
    global_mean = tuple(
        sum(p[d] for p in points) / len(points)
        for d in range(dim)
    )

    centroids = []

    for j in range(k):
        group = [
            p for p, label in zip(points, labels)
            if label == j
        ]

        if group:
            centroid = tuple(
                sum(p[d] for p in group) / len(group)
                for d in range(dim)
            )
        else:
            centroid = global_mean

        centroids.append(centroid)

    return centroids


def kmeans(points, k, init="random", seed=246, max_iter=100):
    """Run to convergence. Return (labels, centroids, sse)."""
    rng = random.Random(seed)

    # ---------------- initialization ----------------
    if init == "random":
        centroids = list(rng.sample(points, k))

    elif init == "++":
        # 첫 centroid는 random
        centroids = [rng.choice(points)]

        while len(centroids) < k:
            # 각 점과 현재 가장 가까운 centroid까지의 거리^2
            distances_sq = []

            for p in points:
                nearest_sq = min(
                    euclidean(p, c) ** 2
                    for c in centroids
                )
                distances_sq.append(nearest_sq)

            total = sum(distances_sq)

            # 모든 점이 같은 위치인 특수 상황
            if total == 0:
                remaining = [p for p in points if p not in centroids]

                if remaining:
                    centroids.append(rng.choice(remaining))
                else:
                    centroids.append(rng.choice(points))

                continue

            # 거리 제곱에 비례해서 다음 centroid 선택
            target = rng.random() * total
            cumulative = 0.0

            chosen = points[-1]

            for p, d2 in zip(points, distances_sq):
                cumulative += d2

                if cumulative >= target:
                    chosen = p
                    break

            centroids.append(chosen)

    else:
        raise ValueError("init must be 'random' or '++'")

    # ---------------- iterations ----------------
    previous_labels = None

    for iteration in range(1, max_iter + 1):
        labels = assign(points, centroids)

        # assignment가 더 이상 변하지 않으면 수렴
        if labels == previous_labels:
            kmeans.iterations = iteration
            break

        centroids = update(points, labels, k)
        previous_labels = labels[:]

    else:
        kmeans.iterations = max_iter

    # centroid 업데이트 후 최종 assignment를 다시 확인
    labels = assign(points, centroids)

    sse = sse_of(points, labels, centroids)

    return labels, centroids, sse


def sse_of(points, labels, centroids):
    """Sum of squared distances from each point to its assigned centroid."""
    total = 0.0

    for p, label in zip(points, labels):
        d = euclidean(p, centroids[label])
        total += d ** 2

    return total

# ------------------------------------------------------------------- harness
def verify():
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<50} {detail}")
        fails += not ok

    try:
        check("distance in 2d", abs(euclidean((0, 0), (3, 4)) - 5) < 1e-9)
        check("distance in 5d",
              abs(euclidean((0,) * 5, (1,) * 5) - math.sqrt(5)) < 1e-9)
    except NotImplementedError:
        print("  euclidean is still a stub"); return 1

    try:
        labels, cents, sse = kmeans(BLOBS, 3, init="++", seed=1)
    except NotImplementedError:
        print("  kmeans is still a stub"); return 1

    groups = {}
    for p, l in zip(BLOBS, labels):
        groups.setdefault(l, []).append(p)
    check("three clusters of three", sorted(len(g) for g in groups.values()) == [3, 3, 3],
          sorted(len(g) for g in groups.values()))
    check("the three blobs were recovered",
          all(max(q[0] for q in g) - min(q[0] for q in g) < 1 and
              max(q[1] for q in g) - min(q[1] for q in g) < 1
              for g in groups.values()))
    check("sse is small when clusters are right", sse < 1.0, f"sse {sse:.4f}")

    # Bad luck with random starts should sometimes be visibly worse.
    randoms = [kmeans(BLOBS, 3, init="random", seed=s)[2] for s in range(40)]
    plusplus = [kmeans(BLOBS, 3, init="++", seed=s)[2] for s in range(40)]
    check("random init sometimes lands badly", max(randoms) > min(randoms) * 5,
          f"sse from {min(randoms):.3f} to {max(randoms):.3f}")
    check("k-means++ is more reliable than random",
          sum(plusplus) / len(plusplus) <= sum(randoms) / len(randoms),
          f"mean sse: ++ {sum(plusplus) / len(plusplus):.3f} vs "
          f"random {sum(randoms) / len(randoms):.3f}")

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    raise SystemExit(verify() if a.verify else p.print_help())
