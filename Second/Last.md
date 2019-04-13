### 취직 사이트 크롤링으로 정보를 수집하여 분석

##### 이용 사이트 : [사람인](http://www.saramin.co.kr/), [인쿠르트](http://www.incruit.com/), [커리어](http://www.career.co.kr/)<br>관련있지만 크롤링하는데에 문제가 있어 이용하지 못하는 사이트 : [잡투게더](http://www.jobtogether.net/), [잡코리아](http://www.jobkorea.co.kr/)


* * *

### 사람인 
#### [크롤링 방법](https://github.com/chanp5660/chanp5660/blob/master/Second/Saramin.R)
- 자바스크립트로 이루어져있어 [phantomjs](http://phantomjs.org/download.html) 프로그램을 이용하여 html 파일로 저장한다.
- html을 rvest 패키지를 이용해서 크롤링
  - 총 페이지의 수를 구함
  - 각 페이지의 공고의 url을 구함
  - 각 url의 정보를 크롤링

* * *

### 인쿠르트





