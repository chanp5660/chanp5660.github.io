# 채용공고 정보 수집(구인구직 사이트에서 크롤링)

### 이용 사이트 : [사람인](http://www.saramin.co.kr/)<br>추가할 사이트 : [워크넷](https://www.work.go.kr/seekWantedMain.do) <br>관련있지만 크롤링하는데에 문제가 있어 이용하지 못하는 사이트 : [잡투게더](http://www.jobtogether.net/), [잡코리아](http://www.jobkorea.co.kr/)<br>정보가 적고 사용자가 적은 사이트 : [인쿠르트](http://www.incruit.com/), [커리어](http://www.career.co.kr/)

* * *

## 사람인

- 자바스크립트로 이루어져있어 [phantomjs](http://phantomjs.org/download.html) 프로그램을 이용하여 html 파일로 저장한다.

- html을 **rvest** 패키지를 이용해서 크롤링

  - 총 페이지의 수를 구함
  - 각 페이지의 공고의 url을 구함
  - 각 url의 정보를 크롤링

## 실제 과정

### 데이터를 가져와야하는 사이트 사진1

![공채의 명가](https://user-images.githubusercontent.com/46266247/56227133-b98bc900-60af-11e9-9eb6-ccc56489f59c.JPG)

### 데이터를 가져와야하는 사이트 사진2

![공고1](https://user-images.githubusercontent.com/46266247/56227194-db854b80-60af-11e9-9ed3-b2854bfe92b8.JPG)

* * *

![공고2](https://user-images.githubusercontent.com/46266247/56227197-dd4f0f00-60af-11e9-8c58-1e4cebc10496.JPG)

[사람인의 공채의 명가](http://www.saramin.co.kr/zf_user/jobs/public/list)

### 과정

- 'PantomJs' 프로그램을 사용해서 html 파일로 저장.
![JShtml](https://user-images.githubusercontent.com/46266247/56230134-9d3f5a80-60b6-11e9-9398-fa49e08fa2f1.png)

  - 총 개수, 총 페이지수를 구해서 모든 공고의 상세보기 URL 번호 저장. [num_total.txt파일](https://github.com/chanp5660/chanp5660/blob/master/Result/num_total.txt)
  
    - ```http://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=```**36015093**```&recommend_ids=eJxVzrsNgFAMQ9Fp6F%2FifGsGYf8tgM4uj65iBXUyzP0p86tvfAQmmFstjGRmghlrTNdqWq1l6vuE6LspjGHOSG3IbZ39%2BQKwQS%2BW&view_type=public-recruit&gz=1&t_ref=public-recruit#seq=0```

  - 해당 URL을 이용해서 각 html 파일로 저장.[Html파일](https://github.com/chanp5660/chanp5660/tree/master/Result/saramin)

- Html 파일을 'rvest' 패키지를 사용해서 읽는다.
  - 필요한 정보들을 rvest와 gsub, grep, gregexpr, strsplit등 텍스트를 다루는 함수, match, Sys.sleep, write.csv등 그 외의 필요한 함수들을 사용하여 분류하여 저장.

- 데이터를 500개씩 나누어 저장.[csv파일](https://github.com/chanp5660/chanp5660/tree/master/Result/saramin_csv)
[R코드](https://github.com/chanp5660/chanp5660/blob/master/Second/Saramin.R)

### 자동화

위의 정보 중 URL 번호를 저장했는데 앞으로 받는 정보 중 겹치는 정보는 여기서 판별한다. 매일 반복해서 정보를 얻어 추가 시킬 수 있다.

## 이번 느낀점

'사람인'을 사이트를 크롤링 할 때 R언어를 사용해서 JS로 작성된 html을 저장하고 html 읽은 후 문자열을 보기 좋게 수정 후에 분류하는 과정까지 생각보다 까다로워서 시간이 많이 들었습니다. 아직 비슷한 다른 사이트의 정보도 얻어야 하기 때문에 시간이 좀 더 필요하다고 생각합니다. 
그동안 저는 만들어진 데이터를 사용하기만 했습니다. 이번에는 직접 정리 된 데이터를 만들어 보았습니다. 데이터를 읽어오는 것부터 데이터를 정리하고 분류의 기준을 정하고 여러가지 과정을 알 수 있었습니다. 시간이 오래걸렸지만 이번 경험으로 앞으로 은 데이터를 얻는데 큰 도움이 된 것 같습니다.


## 다음 계획

워크넷(고용노동부) 사이트까지 자동화 시키는 것.(한개의 사이트로는 부족하다고 생각.)
각 사이트마다 형태가 다를 텐데 그 분류를 비슷하게 하여 가능한 색인이 잘 되게 만들어야겠다.




