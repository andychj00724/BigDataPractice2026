# Week 3 Observations

## Task 1

MinHash signature를 계산할 때 각 column을 반복해서 탐색하는 대신 row를 한 번씩 순회하면서 해당 row를 포함하는 모든 column의 signature를 갱신하도록 구현했다.

Signature length가 bands로 정확히 나누어지지 않는 경우에는 불균등한 band를 만들지 않고 ValueError를 발생시키도록 했다.

S1과 S4의 실제 Jaccard similarity는 2/3이지만 2개의 MinHash 값이 모두 일치하여 추정값은 1.0이 되었다. Hash 개수를 늘리면 추정 오차를 줄일 수 있지만 계산량과 메모리 사용량이 증가한다.

## Task 2

Apple M3, 8 GB RAM 환경에서 측정했으며, brute force와 LSH의 crossover는 n=1000과 n=2000 사이에서 발생했다.

Brute-force 시간은 n이 2배가 될 때 약 4배씩 증가하여 O(n^2) 특성을 확인할 수 있었다. n=8000에서는 129.31초가 걸려 1분을 크게 초과했으며, 메모리보다는 실행 시간이 먼저 부담스러운 요소가 되었다.

## Task 3

120개의 MinHash를 40개의 band로 나누어 사용했다. 따라서 r=3이고 S-curve의 step은 (1/40)^(1/3) ≈ 0.292이다. 실제 similarity threshold인 0.6보다 낮게 설정하여 유사한 pair가 candidate에서 누락될 가능성을 줄였다.

처음에는 120 hashes와 30 bands를 사용했지만 recall이 70.2%에 불과했다. Hash 함수를 더 독립적으로 생성하고 40 bands로 변경한 결과 recall 100%를 달성했으며, 비교 횟수도 2,246,140회에서 275회로 99.99% 감소했다.

현재 harness에서는 hashing 비용을 comparison으로 계산하지 않는다. 하지만 문서 수와 signature 길이가 매우 커지면 MinHash signature 생성과 band hashing 자체의 계산 및 메모리 비용도 커지므로, 실제 대규모 환경에서는 이를 무시하기 어려워진다.
