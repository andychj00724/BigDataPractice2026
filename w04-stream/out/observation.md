# Week 4 Observations

## Task 1

Bloom filter는 삽입할 때 동일한 hash 위치의 bit들을 모두 1로 만들고, 이후 그 bit들을 다시 0으로 만들지 않기 때문에 false negative가 발생하지 않는다. 측정된 false-positive rate는 0.820%, 이론값은 0.860%로 거의 일치했다.

Flajolet-Martin은 각 hash의 최대 trailing-zero 값에서 2^R을 구한 뒤 median으로 결합했다. 단순 평균은 큰 outlier에 영향을 많이 받았고, median은 더 안정적이었으며 20,000개 수준의 distinct count에서 16,384로 약 0.82x를 추정했다.

Reservoir sampling에서는 처음 k개를 저장한 뒤, i번째 원소마다 0부터 i 사이의 난수를 뽑고 그 값이 k보다 작을 때만 기존 reservoir를 교체한다. 이 과정에서 전체 stream 길이를 미리 알 필요 없이 항상 최대 k개의 원소만 유지한다.

## Task 2

Exact distinct counting은 n=6,400,000에서 11.86초와 약 188.3 MB의 peak memory를 사용해 가장 부담스러운 지점이 되었고, 더 큰 크기에서는 시간과 메모리 비용이 더 커질 것으로 판단해 여기서 중단했다.

Exact set의 메모리는 3.9 MB → 11.6 MB → 46.6 MB → 188.3 MB로 증가해 대략 O(n) 성장을 보였다. 반면 Flajolet-Martin의 메모리는 hash register 수에 의해 정해지므로 stream 크기가 증가해도 거의 일정해 O(1)에 가까운 성장을 보였다.

FM의 accuracy ratio는 모든 측정 크기에서 약 0.89x였다. factor-of-two 오차는 대략적인 방문자 규모나 추세 파악에는 허용될 수 있지만, 과금이나 정확한 통계 보고처럼 실제 개수가 중요한 경우에는 허용하기 어렵다.

## Task 3

Bloom filter의 false-positive rate를 최소화하기 위해 k = (m/n) ln 2를 사용했다. m/n = 10이므로 k ≈ 6.93이고, 가장 가까운 정수인 k=7을 사용했다.

10 bits per item에서 이론적 최소 false-positive rate는 약 0.82%이며, 실제 결과도 0.820%로 거의 정확히 이론적 floor에 도달했다. baseline 9.511%에 비해 false-positive rate가 91.4% 감소했고 false negative는 0이었다.

실제 stream에서는 n을 미리 알 수 없으므로 예상 n을 기준으로 filter 크기와 k를 잡거나, 필요하면 scalable Bloom filter처럼 용량이 차면 새로운 filter를 추가하는 방법을 사용할 수 있다. n을 너무 작게 추정하면 bit가 빠르게 포화되어 false positive가 증가하고, 너무 크게 추정하면 메모리를 불필요하게 낭비하게 된다.