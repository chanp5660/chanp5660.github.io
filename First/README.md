# 폴더 정의

'빅데이터분석'과목에서 github와 openApi를 이용해보는 연습을 한 폴더 (추가로 보기 좋게 만들기 위해서 MarkDown도 이용\[마지막에 사이트 소개\])
<br></br>
<br></br>

------
# Github Using OpenApi(공공데이터포털)

## 데이터

공공데이터 포털(https://www.data.go.kr/) -> 데이터셋 ->오픈 API -> 한국환경공단_대기오염정보 검색 -> 활용신청 -> **인증키** 발급(*복사) -> 상세기능정보(원하는 상세기능의 실행 클릭) -> 미리보기 클릭 후 **주소**(*복사)

>  *부분은 R프로그램 사용시 필요, 데이터의 정보는 인증키 정보가 있는 서비스정보부분의 마지막 ‘참고문서’에서 다운하여 확인가능

## 사진 첨부

> OpenApi명 

![캡처1](https://user-images.githubusercontent.com/46266247/55397562-7c88e800-5581-11e9-8823-7fbf79bde848.PNG)

> 인증키 위치

![캡처2](https://user-images.githubusercontent.com/46266247/55399860-3afb3b80-5587-11e9-9842-d2d671d92073.PNG)

> 미리보기 하는 방법

![캡처3](https://user-images.githubusercontent.com/46266247/55397568-7f83d880-5581-11e9-81d2-8f1ce3e1173a.PNG)

> 미리보기 결과에서 주소 위치

![캡처4](https://user-images.githubusercontent.com/46266247/55397573-814d9c00-5581-11e9-95c3-731f80796c47.PNG)

> Rstudio에서 실행한 결과

![캡처5](https://user-images.githubusercontent.com/46266247/55397576-827ec900-5581-11e9-98b6-edc2ccb92fcf.PNG)

> R code

```r
library(XML)
library(data.table)

api_url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=+인증키+&numOfRows=10&pageNo=1&sidoName=%EC%84%9C%EC%9A%B8&searchCondition=DAILY" # api의 주소
data = xmlTreeParse(api_url,useInternalNodes=T,encoding="UTF-8")# UTF-8 인코딩
rootNode <- xmlRoot(data) # root node 정보를 확인
items = rootNode[[2]][["items"]]#root node에서 body부분의 items부분을 읽는다.
size=xmlSize(items)# xml의 size를 구해서 for문의 반복 횟수를 구한다.
test2 <- data.frame()# 한개의 times 부분을 읽어 데이터 저장
test3 <- list()#모든 데이터를 리스트 형식으로 모아둔다.

for(i in 1:size){
  test <- xmlSApply(items[[i]],xmlValue)  
  test2 <- data.table(dataTime = test[[1]],
                      cityName = test[[2]],
                      so2Value = test[[3]],
                      coValue  = test[[4]],
                      o3Value  = test[[5]],
                      no2Value = test[[6]],
                      pm10Value = test[[7]],
                      pm25Value = test[[8]]
                      )
  test3[[i]]=test2
}
test4 <- rbindlist(test3)#모든 리스트를 데이터프레임 형태로 합쳐준다.
test4
```


# MarkDown
[깃허브에서 makrdown으로 꾸미는 방법(한글)](https://heropy.blog/2017/09/30/markdown/)

[마크다운 가운데, 왼쪽, 오른쪽 정렬 할 수 있는 방법 추가(한글)](http://ccl.cckorea.org/syntax/)

[예제가 많음(한글)](https://steemit.com/kr/@nand/markdown)

[전체 규칙 (Github Guide)](https://guides.github.com/features/mastering-markdown/)



