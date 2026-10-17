# Week 7 Observations

## Task 1

For empty clusters, I chose to move the centroid to the global mean of all points. This guarantees that every centroid has a valid position even when no points are assigned to it. An alternative would be to keep the previous centroid or move it to a far-away point, which could lead to a different final clustering.

Across 40 seeds, random initialization recovered the correct three blobs 27/40 times, while k-means++ recovered them 40/40 times. The random runs ranged from SSE 0.120 to 96.105, while k-means++ had mean SSE 0.120.

k-means++ spends extra distance computations before the first iteration because each new centroid is sampled using squared distance to the nearest already-chosen centroid. The benefit is much more reliable initialization and a much lower chance of converging to a poor local optimum. I would avoid paying that cost only when initialization cost dominates and a rough clustering is acceptable, or when repeated random restarts are already cheap.

SSE cannot be used alone to choose k because SSE always decreases, or at least never increases, as k increases. If k becomes large enough, each point can effectively become its own cluster and SSE approaches zero. Therefore, minimizing SSE alone would favor unnecessarily large k rather than the most meaningful clustering.

## Task 2

At n=1,000 points, contrast first dropped below 1 at dimension 50, where it was 0.982. It dropped below 0.5 at dimension 200, where it was 0.372. Relative standard deviation also fell from 0.476 at dimension 2 to 0.041 at dimension 200, showing that pairwise distances become increasingly concentrated in high dimensions.

Point count mattered as well. At dimension 200, increasing n from 1,000 to 2,000 raised contrast from 0.372 to 0.448. With more points, more extreme near and far pairs can appear, so the dimension where distance becomes poorly discriminative is not determined by dimension alone.

This does not directly invalidate the Week 3 LSH result. That experiment used Jaccard similarity on shingle sets, whereas this experiment uses Euclidean distance on random points in a unit cube. The general warning about high-dimensional similarity still matters, but the measured Euclidean concentration does not automatically transfer to Jaccard similarity.

## Task 3

The optimized version stores two bounds per point: an upper bound on the distance to the currently assigned centroid and a lower bound on the distance to competing centroids. It also computes centroid-to-centroid separations and centroid movement each iteration.

The most useful pruning rule is the triangle-inequality bound that proves a point cannot change cluster when its current upper bound is already smaller than the best lower bound for any competitor. Maintaining the bounds costs O(n) bound updates per iteration plus a small number of centroid distance computations, which is worthwhile because n=20,000 while k=12.

The baseline used 10,320,000 distance computations. The bounded version used 1,146,949, an 88.9% reduction, while both produced SSE 10,737,882.94 after 43 iterations. The SSE difference was exactly 0.0000% because the optimized version does not approximate distances or assignments; it only skips distance calculations when the bounds prove that the skipped centroid cannot win.

The first iteration cannot prune anything, so it performs all 20,000 x 12 = 240,000 point-to-centroid distance computations. Including the small centroid-movement bookkeeping, this is about 20.9% of the optimized algorithm's total 1,146,949 distance computations. Most of the savings therefore come from later iterations, after the bounds have become informative.
