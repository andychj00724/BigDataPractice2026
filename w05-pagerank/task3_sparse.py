#!/usr/bin/env python3
"""Week 5 · Task 3 — PageRank on a graph that will not fit as a matrix.

Textbook §5.2 (efficient PageRank), §5.2.1 - §5.2.3.

`DenseMatrix` is PageRank written the way the equations are written: build the
transition matrix M, multiply. It is correct, it is easy to read, and it stores
n^2 numbers for a graph with almost no edges.

The web's matrix is about 99.9999% zeros. Storing them is the problem, and
§5.2 is the chapter about not doing that.

    python3 bench.py
    python3 bench.py --yours

Correctness first: the harness compares your ranks against the dense version
element by element. A fast PageRank that ranks pages differently is a different
algorithm, not a faster one.
"""


class DenseMatrix:
    """PageRank as written in the equations. Stores n^2 floats."""

    def __init__(self, beta=0.85, tol=1e-10, max_iter=100):
        self.beta, self.tol, self.max_iter = beta, tol, max_iter

    def run(self, graph):
        nodes = list(graph)
        n = len(nodes)
        index = {v: i for i, v in enumerate(nodes)}

        # the full transition matrix, zeros and all
        M = [[0.0] * n for _ in range(n)]
        for v, outs in graph.items():
            if outs:
                share = 1.0 / len(outs)
                for w in outs:
                    M[index[w]][index[v]] = share
            else:
                for i in range(n):           # dead end: spread it everywhere
                    M[i][index[v]] = 1.0 / n

        r = [1.0 / n] * n
        for self.iterations in range(1, self.max_iter + 1):
            nr = [0.0] * n
            for i in range(n):
                row = M[i]
                s = 0.0
                for j in range(n):
                    if row[j]:
                        s += row[j] * r[j]
                nr[i] = self.beta * s + (1 - self.beta) / n
            delta = sum(abs(a - b) for a, b in zip(nr, r))
            r = nr
            if delta < self.tol:
                break
        return {v: r[index[v]] for v in nodes}

    def memory_floats(self):
        return getattr(self, "_n", 0) ** 2


class YourPageRank:
    def __init__(self, beta=0.85, tol=1e-10, max_iter=100):
        self.beta = beta
        self.tol = tol
        self.max_iter = max_iter
        self._memory = 0

    def run(self, graph):
        nodes = list(graph)
        n = len(nodes)

        if n == 0:
            self._memory = 0
            return {}

        # Current rank vector
        r = {v: 1.0 / n for v in nodes}

        # At most two rank vectors are held simultaneously
        self._memory = 2 * n

        for _ in range(self.max_iter):
            # Rank held by dead-end nodes
            dead_rank = sum(
                r[v]
                for v in nodes
                if not graph[v]
            )

            # Teleport + dead-end redistribution
            base = (
                (1.0 - self.beta) / n
                + self.beta * dead_rank / n
            )

            nr = {v: base for v in nodes}

            # Only traverse actual edges
            for v in nodes:
                outs = graph[v]

                if outs:
                    share = self.beta * r[v] / len(outs)

                    for w in outs:
                        nr[w] += share

            delta = sum(
                abs(nr[v] - r[v])
                for v in nodes
            )

            r = nr

            if delta < self.tol:
                break

        return r

    def memory_floats(self):
        return self._memory