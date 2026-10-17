#!/usr/bin/env python3
"""Week 7 · Task 3 — The same clustering, with far fewer distances.

Textbook §7.3, and §7.1.3 for why distance is the expensive part.

`NaiveKMeans` does what the definition says: every iteration, compare every
point with every centroid. That is n x k distance computations per pass, and on
a real dataset the distance computation is almost the entire cost.

Most of that work is wasted. After the first couple of iterations, most points
do not change cluster, and most centroids barely move. The triangle inequality
lets you prove a point cannot have changed cluster **without measuring it**.

    python3 bench.py
    python3 bench.py --yours

Correctness first: your final SSE must match the baseline's. Fewer distances
with a worse clustering is not an improvement, it is a different algorithm.
"""


class NaiveKMeans:
    """Every point against every centroid, every iteration."""

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter

    def run(self, points, initial_centroids, distance):
        centroids = list(initial_centroids)
        labels = [None] * len(points)
        for self.iterations in range(1, self.max_iter + 1):
            changed = False
            for i, p in enumerate(points):
                best, bi = None, 0
                for j, c in enumerate(centroids):
                    d = distance(p, c)
                    if best is None or d < best - 1e-12:
                        best, bi = d, j
                if labels[i] != bi:
                    labels[i] = bi
                    changed = True
            centroids = _means(points, labels, self.k, centroids)
            if not changed:
                break
        return labels, centroids


def _means(points, labels, k, previous):
    out = []
    for j in range(k):
        group = [p for p, l in zip(points, labels) if l == j]
        if group:
            out.append(tuple(sum(v) / len(group) for v in zip(*group)))
        else:
            out.append(previous[j])
    return out


class YourKMeans:
    def __init__(self, k, max_iter=50):
        self.k = k
        self.max_iter = max_iter
        self.iterations = 0

    def run(self, points, initial_centroids, distance):
        n = len(points)
        k = self.k
        centroids = list(initial_centroids)

        labels = [None] * n

        # upper[i]:
        # point i -> assigned centroid 거리의 upper bound
        upper = [float("inf")] * n

        # lower[i]:
        # point i -> 두 번째로 가까운 centroid 거리의 lower bound
        lower = [0.0] * n

        for iteration in range(1, self.max_iter + 1):
            self.iterations = iteration
            changed = False

            # --------------------------------------------------
            # First iteration:
            # 아직 bound가 없으므로 모든 centroid와 거리 계산
            # --------------------------------------------------
            if iteration == 1:
                for i, p in enumerate(points):
                    best_dist = float("inf")
                    second_dist = float("inf")
                    best_j = 0

                    for j, c in enumerate(centroids):
                        d = distance(p, c)

                        if d < best_dist - 1e-12:
                            second_dist = best_dist
                            best_dist = d
                            best_j = j

                        elif d < second_dist:
                            second_dist = d

                    labels[i] = best_j
                    upper[i] = best_dist
                    lower[i] = second_dist

                changed = True

            # --------------------------------------------------
            # Later iterations:
            # bounds를 이용해서 가능한 point는 distance 계산 생략
            # --------------------------------------------------
            else:
                # 각 centroid와 가장 가까운 다른 centroid 사이 거리의 절반
                separation = [float("inf")] * k

                for a in range(k):
                    for b in range(a + 1, k):
                        d = distance(centroids[a], centroids[b])

                        half = d / 2.0

                        if half < separation[a]:
                            separation[a] = half

                        if half < separation[b]:
                            separation[b] = half

                for i, p in enumerate(points):
                    current = labels[i]

                    # 두 가지 lower bound 중 더 강한 것 사용
                    bound = max(
                        lower[i],
                        separation[current]
                    )

                    # upper가 lower bound보다 작으면
                    # 다른 centroid가 더 가까울 수 없음
                    if upper[i] < bound:
                        continue

                    # assigned centroid까지 실제 거리 다시 계산하여
                    # upper bound를 정확하게 tighten
                    assigned_dist = distance(
                        p,
                        centroids[current]
                    )

                    upper[i] = assigned_dist

                    if upper[i] < bound:
                        continue

                    # pruning 불가능 → 모든 centroid 확인
                    best_dist = float("inf")
                    second_dist = float("inf")
                    best_j = 0

                    for j, c in enumerate(centroids):

                        # current centroid 거리는 이미 계산했으므로 재사용
                        if j == current:
                            d = assigned_dist
                        else:
                            d = distance(p, c)

                        if d < best_dist - 1e-12:
                            second_dist = best_dist
                            best_dist = d
                            best_j = j

                        elif d < second_dist:
                            second_dist = d

                    if best_j != current:
                        labels[i] = best_j
                        changed = True

                    upper[i] = best_dist
                    lower[i] = second_dist

            # --------------------------------------------------
            # centroid update
            # --------------------------------------------------
            new_centroids = _means(
                points,
                labels,
                k,
                centroids
            )

            # label이 하나도 안 바뀌었다면 수렴
            if not changed:
                centroids = new_centroids
                break

            # centroid가 얼마나 움직였는지 계산
            movement = [
                distance(old, new)
                for old, new in zip(centroids, new_centroids)
            ]

            # 가장 많이 움직인 centroid와 두 번째
            max_idx = max(range(k), key=lambda j: movement[j])
            max_move = movement[max_idx]

            if k > 1:
                second_max_move = max(
                    movement[j]
                    for j in range(k)
                    if j != max_idx
                )
            else:
                second_max_move = 0.0

            # centroid가 움직였으므로 bounds 갱신
            for i in range(n):
                assigned = labels[i]

                # assigned centroid가 움직인 만큼
                # 실제 거리가 최대 이만큼 증가 가능
                upper[i] += movement[assigned]

                # 다른 centroid 중 가장 많이 움직인 만큼
                # lower bound가 감소할 수 있음
                if assigned == max_idx:
                    other_move = second_max_move
                else:
                    other_move = max_move

                lower[i] = max(
                    0.0,
                    lower[i] - other_move
                )

            centroids = new_centroids

        return labels, centroids