# 채용공고 정보 수집(구인구직 사이트에서 크롤링)

### 이용 사이트 : [사람인](http://www.saramin.co.kr/)<br>사용할 사이트 : [워크넷](https://www.work.go.kr/seekWantedMain.do), <br>관련있지만 크롤링하는데에 문제가 있어 이용하지 못하는 사이트 : [잡투게더](http://www.jobtogether.net/), [잡코리아](http://www.jobkorea.co.kr/)<br>정보가 적고 사용자가 적은 사이트 : [인쿠르트](http://www.incruit.com/), [커리어](http://www.career.co.kr/)

* * *

## 사람인 [R코드](https://github.com/chanp5660/chanp5660/blob/master/Second/Saramin.R)
### 요약정리
- 자바스크립트로 이루어져있어 [phantomjs](http://phantomjs.org/download.html) 프로그램을 이용하여 html 파일로 저장한다.
- html을 **rvest** 패키지를 이용해서 크롤링
  - 총 페이지의 수를 구함
  - 각 페이지의 공고의 url을 구함
  - 각 url의 정보를 크롤링

### 실제 과정

#### 데이터를 가져와야하는 사이트 사진1
[사람인의 공채의 명가](http://www.saramin.co.kr/zf_user/jobs/public/list)
![공채의 명가](https://user-images.githubusercontent.com/46266247/56227133-b98bc900-60af-11e9-9eb6-ccc56489f59c.JPG)
#### 데이터를 가져와야하는 사이트 사진2
![공고1](https://user-images.githubusercontent.com/46266247/56227194-db854b80-60af-11e9-9ed3-b2854bfe92b8.JPG)
* * *
![공고2](https://user-images.githubusercontent.com/46266247/56227197-dd4f0f00-60af-11e9-8c58-1e4cebc10496.JPG)






## 이번 느낀점
'사람인'을 사이트를 크롤링 할 때 R언어를 사용해서 JS로 작성된 html을 저장하고 html 읽은 후 문자열을 보기 좋게 수정 후에 분류하는 과정까지 생각보다 까다로워서 시간이 많이 들었습니다. 아직 비슷한 다른 사이트의 정보도 얻어야 하기 때문에 시간이 좀 더 필요하다고 생각합니다. 한 번 해봤기 때문에 전보다는 좀 더 빠를 것입니다. 그동안 만들어진 데이터를 사용만 해보았습니다. 이번에는 직접 정리가 잘 되어 있는 데이터를 만드는 것으로 이 과정이 정말 중요한 것이라고 다시한번 생각하게 되었습니다.

## 다음 계획
워크넷(고용노동부) 사이트까지 자동화 시키는 것.(한개의 사이트로는 부족하다고 생각.)
각 사이트마다 형태가 다를 텐데 그 분류를 비슷하게 하여 가능한 색인이 잘 되게 만들어야겠다.




