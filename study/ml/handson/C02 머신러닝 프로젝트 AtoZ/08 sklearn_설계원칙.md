2023-07-21

### 사이킷런 설치

sklearn으로 import하지만, 설치할 때는 scikit-learn이라는 풀네임으로 install 해줘야 한다는 점을 명심하자

# 일관성

- 사이킷런의 모든 객체는 일관되고 단순한 인터페이스를 공유한다.

### Estimator

- 데이터셋을 기반으로 모델 파라미터들을 추정한다
- imputer가 대표적인 Estimator이다.
- fit() 메서드로 수행하고, 매개변수는 데이터셋 하나이다.
- 그 외 필요한 매개변수(예-strategy=median)는 하이퍼파라미터로 간주되고, 보통 생성자의 매개변수로 전달한다.(Imputer 객체를 생성할 때 전달)

### Transformer

- Estimator 중, 데이터셋을 변환하는 Estimator를 Transformer라고 한다(imputer도 이에 해당)
- transform() 메서드로 수행하고, 매개변수는 역시 데이터셋이다.
- fit()을 통해 변환할 모델 파라미터를 학습(예-중간값을 학습)한 다음에 transform을 수행하게 된다
- 이 때문에 모든 transformer는 fit과 transform을 연달아 호출하는 fit_transform() 메서드를 가지고 있다

### Predictor

- 일부 Estimator는 주어진 데이터셋에 대한 예측을 만들 수 있다.
- 예를 들어 LinearRegression 모델이 이에 해당한다.
- Predictor는 예측의 품질을 측정하는 score() 메서드를 가진다.

# 검사 가능성

- 일이 어떻게 돌아가고 있는지 개발자가 확인해볼 수 있게 설계되었다.
- 모든 Estimator의 하이퍼파라미터는 공개(public) 인스턴스 변수로 직접 접근할 수 있다.
- 예를 들어 imputer.strategy로 접근할 수 있다.
- 모든 Estimator의 학습된 모델 파라미터도 밑줄을 붙여 공개 인스턴스 변수로 제공된다.
- 예를 들어 imputer.statistics\_

# 클래스 남용 방지

- 데이터셋을 별도의 클래스가 아니라 넘파이 배열이나 사이파이 희소행렬로 표현한다.

# 조합성

- 기존의 구성요소를 최대한 재사용할 수 있게 설계되었다
- 예를 들어 여러 변환기(transformer)를 연결한 다음 마지막에 predictor로 끝나는 Pipeline을 쉽게 구현할 수 있다

# 합리적 기본값

- 돌아가는 기본 시스템을 빠르게 만들 수 있도록 대부분의 매개변수에 합리적인 기본값이 지정되어 있다.
