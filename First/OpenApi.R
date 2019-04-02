library(XML)
library(data.table)

api_url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=+++++++++&numOfRows=10&pageNo=1&sidoName=%EC%84%9C%EC%9A%B8&searchCondition=DAILY" # api의 주소
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
