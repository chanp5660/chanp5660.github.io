```r
library(rvest)
library(lubridate)
library(XML)#rvest보다 늦게 실행해야 한다.
library(data.table)#rvest보다 늦게 실행해야 한다.

# 제목 : 사람인에서 공고 데이터 분야에 따라 분류

### 날짜(문자)를 시간 형태로 변환 후 해당 api_url 출력
Day_Sel <-function(Start_day,End_day){# 개시 시작일 기준
  Start=as.POSIXct(paste0(Start_day," 00:00:00 KST")) # 시작 날짜
  End=as.POSIXct(paste0(End_day," 00:00:00 KST")) # 끝 날짜
  api_url=paste0("http://api.saramin.co.kr/job-search?published_min=",Start,"&published_max=",End)
  return(api_url)
}

### 해당 사이트의 공고 총 개수 구하기
Total <- function(api_url){
  t = readLines(api_url,encoding = "UTF-8")
  S = gregexpr("total",t[3])[[1]][1]+7
  E = gregexpr("\\\">",t[3])[[1]][1]-1
  return (as.integer(substr(t[3],S,E)))
}

### 해당 데이터 저장(키워드, 연봉)
Store_keyword <- function(api_url,max_page){
  for(page in 1:(max_page%/%110)){
    api_url = paste0(api_url,"&count=110&start=",as.character(page))
    data = xmlTreeParse(api_url,useInternalNodes=T,encoding="UTF-8")# UTF-8 인코딩
    rootNode <- xmlRoot(data) # root node 정보를 확인
    jobs =rootNode[['jobs']]
    size =xmlSize(rootNode[['jobs']])
    test2 <- data.frame()# 한개의 times 부분을 읽어 데이터 저장
    test3 <- list()#모든 데이터를 리스트 형식으로 모아둔다.
    for(i in 1:size){
      test <- xmlSApply(jobs[[i]],xmlValue)  
      test2 <- data.table(id  = test[[1]],
                          #url = test[[2]],
                          #active = test[[3]],
                          #posting_timestamp=test[[4]],modification_timestamp=test[[5]],expiration_timestamp=test[[7]],
                          #opening_timestamp=as.POSIXct(as.integer(test[[6]]),origin="1970-01-01",tz="Asia/Seoul"),
                          #close_type=test[[8]],
                          company=test[[9]],
                          position=test[[10]],
                          keyword=test[[11]],
                          salary=test[[12]]
      )
      
      test3[[i]]=test2
    }
    
    test4 <- rbindlist(test3)#모든 리스트를 데이터프레임 형태로 합쳐준다.
    write.csv(test4[,c("keyword","salary")],paste0(Down_file,"page_",page,".csv"))
    print(paste(page,"/",(max_page%/%110)))
  }
}

#### 한 페이지당 최대 110장 읽을 수 있다.
Down_file = "D:/probablity_delete/"
api_url=Day_Sel("2019-04-04","2019-04-07")#시작날짜, 끝날짜
total = Total(api_url)
Store_keyword(api_url,total)

###날짜별로 저장 될 수 있게 만들기


```
