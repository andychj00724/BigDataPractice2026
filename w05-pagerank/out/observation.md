# Week 5 Observations

## Task 1

Dead end에서는 out-link가 없기 때문에 보정하지 않으면 해당 노드의 rank가 그래프 밖으로 사라진다. 정상 PageRank에서는 dead end가 가진 rank를 모든 노드에 균등하게 재분배했고, 그 결과 전체 rank의 합이 1로 유지되었다.

Spider trap과 dead end는 형태는 다르지만 둘 다 random surfer가 특정 구조에 갇히거나 rank가 사라지는 문제를 만든다. Teleport를 추가하면 surfer가 확률적으로 어느 노드로든 이동할 수 있기 때문에 두 문제 모두 완화된다.

beta는 surfer가 현재 페이지의 링크를 따라갈 확률이다. 확률 1-beta에서는 링크를 따르지 않고 임의의 페이지로 teleport한다.

## Task 2

beta가 0.5에서 0.99로 증가하면서 수렴 iteration 수는 14회에서 24회로 증가했다. beta가 1에 가까워질수록 teleport가 줄어들어 damping 효과가 약해지므로 수렴 속도가 느려진다.

그래프 크기가 약 1,200 nodes에서 20,000 nodes로 증가했을 때 beta=0.85 기준 iteration 수는 20회에서 21회로 거의 변하지 않았지만, 실행 시간은 0.009초에서 0.161초로 크게 증가했다. 수렴 iteration 수는 PageRank의 수학적 성질에 더 영향을 받고, wall time은 한 iteration에서 처리해야 하는 노드와 간선 수에 따라 증가한다.

Top-10 ranking은 beta=0.5에서 beta=0.7로 증가할 때 일부 순서가 바뀌었고, 이후 beta=0.7 이상에서는 동일했다. 따라서 beta는 단순히 수렴 속도에만 영향을 주는 값이 아니라 최종 ranking에도 영향을 줄 수 있으므로 결과를 해석할 때 사용한 beta 값을 함께 보고하는 것이 중요하다.

## Task 3

DenseMatrix는 n×n transition matrix 전체를 저장하지만, sparse PageRank에서는 이미 주어진 adjacency list와 현재 rank vector, 다음 rank vector만 사용했다. 따라서 dense 방식은 O(n^2)개의 값을 저장하지만 sparse 방식은 그래프의 실제 edge와 O(n) 크기의 rank 정보만 유지한다.

Teleport term은 모든 노드에 같은 값인 (1-beta)/n을 더하는 연산이므로 dense matrix를 만들 필요가 없다. Dead-end redistribution 역시 dead-end rank의 총합을 먼저 구한 뒤 모든 노드에 동일하게 나누어 더할 수 있어 dense 연산이 필요하지 않다.

실험에서 sparse 버전은 2,400개의 float만 사용해 dense 버전의 1,440,000개보다 600배 적은 메모리를 사용했고, 약 69.5배 더 빨랐다. Dense 결과와의 worst per-node difference는 1.18e-15로, 요구 기준인 1e-9보다 훨씬 작았으며 이는 부동소수점 연산 순서 차이에서 발생하는 매우 작은 수치 오차이다.
