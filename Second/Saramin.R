library(rvest)
library(stringr)
library(plyr)
library(dplyr)
library(magrittr)

# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# -------------------------------- html 얻기 ------------------------------------------------------ #

# ---------------------- 진행중인 총 개수 한 페이지에 100개씩, 출력은 총 페이지 ------------------- #
Page_total = function(){
  url = "http://www.saramin.co.kr/zf_user/jobs/public/list?sort=ed&quick_apply=&search_day=&keyword=#listTop"
  html_data = read_html(url,encoding="UTF-8")
  page = html_data %>% html_nodes(xpath='//*[@id="content"]/div[4]/div[1]/ul/li/a/strong/span') %>% html_text()
  page = as.numeric(gsub(",","",page)) %/% 100 +1
  return(page)
}

# --------- 해당 페이지의 회사이름,공고제목,범주,url저장 ------------------------------------------ #
Read_url <- function(page){
  url = paste0("http://www.saramin.co.kr/zf_user/jobs/public/list/page/",page,"?sort=ed&listType=public&public_list_flag=y&page=",page,"#searchTitle")
  html_data = read_html(url,encoding="UTF-8")
  
  # 회사이름, 공고제목
  Span = html_data %>% html_nodes(".str_tit span") %>% html_text() # 회사이름, 공고제목
  Even = rep(c(TRUE,FALSE),length(Span)/2)[1:length(Span)] # 각각의 인덱스
  Title_nm = Span[Even] # 공고 제목
  Company_nm = Span[!Even] # 회사 이름
  
  # 범주
  Category = html_data %>% html_nodes(".job_sector")
  Delstr = "<div class=\"job_sector\">\\r\\n            |        </div>|</span> 외|<span>"
  temp = gsub(Delstr,"",Category)
  temp = gsub("</span>$","",temp)
  # Category = strsplit(X , "</span>") # 리스트 형식으로 
  Category = gsub("</span>",",",temp)# strsplit(Category,",")#로 분리 가능
  
  # 공고 url  http://www.saramin.co.kr 를 앞에 붙여야 한다.
  # 예시 http://www.saramin.co.kr/zf_user/jobs/public/view?rec_idx=35826682&t_ref=public-recruit #여기있는 번호만 중요할수도
  temp = unique(html_data %>% html_nodes(".str_tit") %>% html_attr("href"))
  start = unlist(gregexpr("_idx=",temp))+5
  end = unlist(gregexpr("&t_ref",temp))-1
  job_url_num = substr(temp,start,end)
  job_url = paste0("http://www.saramin.co.kr/zf_user/jobs/public/view?rec_idx=",job_url_num,"&t_ref=public-recruit")
  
  # 공고 제목 Title_nm
  # 회사 이름 Company_nm
  # 범주 Category
  # 공고 url 고유번호 job_url_num
  
  return (list("Title_nm"=Title_nm,"Company_nm"=Company_nm,"Category"=Category,"job_url_num"=job_url_num))
}

# === 사용되지 않는 공고번호 출력   => 한번 다 하고 나면 삭제-------------------------------------- #
ExistCheck_num = function(num){
  temp = list.files(path="T:/2019-1/bigdataanalysis/project/result/saramin", pattern = NULL)
  exist_num = gsub(".html","",temp)
  return(num[!num %in% exist_num])
}

# 공고번호 중 추가할 번호 저장,출력 (공고번호는 유일한다고 생각) 원래 번호 중 없으면 추가한다. (출력번호를 추가하면 됨)
Add_num =function(add){
  num = read.csv("T:/2019-1/bigdataanalysis/project/result/num_total.txt")[,2]
  add_num = add[!add %in% num]
  num=c(num,add_num)
  write.csv(num,"T:/2019-1/bigdataanalysis/project/result/num_total.txt")
  return(add_num)
}

# ---------------------- num에 해당되는 정보를 html로 저장 ---------------------------------------- #
Save_html <- function(num){ 
  #------------------- js파일로 실행시킬 내용 저장----------------------------------#
  test = paste0(
    "var webPage = require('webpage');
    var page = webPage.create();
    
    var fs = require('fs');
    var path = 'T:/2019-1/bigdataanalysis/project/result/saramin/",num,".html'
    
    page.open('http://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=",num,"&recommend_ids=eJxNjbsRQwEIw6ZJj%2FkYU2eQ7L9Fcq8IlDrJ5yh1a%2FJD%2BKvfUYNmxGKBNYsukx3rxLE1MWebBt9YCeCP2UxTbxzUHOTvl7t1s%2BSJZbZHGsfgWGc8%2BAXknC%2Fp&view_type=public-recruit&gz=1&t_ref=public-recruit#seq=0', function (status) {
    var content = page.content;
    fs.write(path,content,'w')
    phantom.exit();
    });")
  
  writeLines(test, "T:/2019-1/bigdataanalysis/phantomjs-2.1.1-windows/scraping/scrape.js")
  
  #--------------------- html로 저자-----------------------------------------------#
  phantomjs = 'T:/2019-1/bigdataanalysis/phantomjs-2.1.1-windows/bin/phantomjs'
  scrape = "T:/2019-1/bigdataanalysis/phantomjs-2.1.1-windows/scraping/scrape.js"
  exec_scrape = paste(phantomjs, scrape)
  
  system(exec_scrape)
}
# for(i in 1:length(num)){ # 반복하는 방법
#   Save_html(num[i])
#   Sys.sleep(10)# 한번에 많이 하면 터진다.
#   print(paste0(i,"/",length(num)))
#   if(i%%10==0)Sys.sleep(60)
# }

# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# -------------------------------- 데이터 받기 ---------------------------------------------------- #


# ---------------------- num에 해당되는 데이터 읽기  ---------------------------------------------- #
Read_data <- function(num){
  html_data = read_html(paste0('T:/2019-1/bigdataanalysis/project/result/saramin/',num,'.html'))
  return(html_data)
}

# --------------------- html_data에 해당하는 추가정보 불러오기  ----------------------------------- #
Infor1 <- function(html_data){
  # -------------------------      추가정보      --------------------#
  Infor_nm = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(".col") %>% html_nodes("dt") %>% html_text()
  Infor_data= gsub("  |\\n|상세보기|닫기","",html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(".col") %>% html_nodes("dd") %>% html_text())
  # ------------------------------- 회사명, 공고제목, 즐겨찾기 수 -------------------------#
  temp = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(xpath='//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/div/a[1]') %>% html_text()
  Company = gsub("\n|  ","",temp)
  Title = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(xpath='//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/div/h1') %>% html_text()
  Favor = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(xpath='//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/div/button[2]/span') %>% html_text()
  # ------------------------------- 조회수, 홈페이지접속, 자사양식다운로드 -------------------------#
  temp = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(".meta") %>% html_nodes("li") %>% html_text()
  temp = strsplit(grep("조회수|홈페이지접속|자사양식다운수",temp,value=T)," ")
  view_nm=c()
  view_cnt =c()
  for(i in temp){
    view_nm = c(view_nm,i[1])
    view_cnt = c(view_cnt,i[2])
  }
  # ------------------------------- 시작일, 마감일  -------------------------#
  temp = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(".info_period") %>% html_children() %>% html_text()
  Time_nm = c()
  Time = c()
  for(i in 1:length(temp)){
    if(i%%2==1)Time_nm = c(Time_nm,temp[i])
    else Time = c(Time,temp[i])
  }
  temp = t(c(Company,Title,Favor,view_cnt,Infor_data,Time))
  colnames(temp)=c("회사명","공고제목","즐겨찾기 수",view_nm,Infor_nm,Time_nm)
  return(temp)
}

#-------------------------num 에 해당하는 html정보들을 csv파일로 저장.----------------------------- #
Make_data_nm <- function(L,name){
  # L은 nm,과 data가 들어있는 리스트이다.
  # name에 맞추어 없는 name에는 빈칸을 넣는다.
  temp = t(1:length(name))
  Index = match(colnames(L),name)
  temp[Index] = L
  temp[-Index]=NA
  return(temp)
}
Make_data_sub <- function(name,num,start=1){
  stop=start
  for(i in start:length(num)){
    try({
      #실제 데이터
      L = Infor1(Read_data(num[i]))
      #데이터 저장
      one_data = Make_data_nm(L,name)
      stop=i
      print(paste0(i,"/",length(num)))
      break 
    })
  }
  return(list(one_data,stop))
}# Make_data를 돕기 위한 데이터
Make_data <- function(num){
  # 속성으로 정할 name
  name =read.csv("T:/2019-1/bigdataanalysis/project/result/all_nm.txt",stringsAsFactors = F)[,2]
  
  one_row = Make_data_sub(name,num)#데이터 첫행 설정
  one_data = one_row[[1]]
  start = one_row[[2]]+1
  Last_num = TRUE
  #나머지 데이터를 추가 
  for(i in start:length(num)){
    try({
      Last_num = TRUE
      #실제 데이터
      L = Infor1(Read_data(num[i]))
      # 데이터로 변환
      temp = Make_data_nm(L,name)
      #데이터 저장
      one_data = rbind(one_data,temp)
      
      #500개 넘어갈때마다 랜덤 제목으로 저장 
      if(nrow(one_data)>=500){
        print(paste0(i,"/",length(num)," csv파일로 저장"))#어디까지 성공했는지
        colnames(one_data)=name
        write.csv(one_data,paste0("T:/2019-1/bigdataanalysis/project/result/saramin_csv/",round(runif(1)*100000),".csv"))
        i=i+1
        one_row = Make_data_sub(name,num,i)#데이터 첫행 설정
        one_data = one_row[[1]]
        start = one_row[[2]]+1
        print(paste0(i,"/",length(num)))#어디까지 성공했는지
        Last_num = FALSE
      }else{
        print(paste0(i,"/",length(num)))#어디까지 성공했는지
      }
    })
  }
  
  # 500속하지 않는 부분 저장
  if(Last_num){
    colnames(one_data)=name
    write.csv(one_data,paste0("T:/2019-1/bigdataanalysis/project/result/saramin_csv/",round(runif(1)*100000),".csv"))
    print("남은 부분까지 저장 완료")
  }
}

# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# -------------------------------- 실제로 데이터 저장 --------------------------------------------- #

num = gsub(".html","",list.files(path="T:/2019-1/bigdataanalysis/project/result/saramin", pattern = NULL))
name = read.csv("T:/2019-1/bigdataanalysis/project/result/all_nm.txt",stringsAsFactors = F)[,2]

name = c()
for(i in 1:length(num)){
  data = Infor1(Read_data(num[i]))
  name = unique(c(name,colnames(data)))
  print(paste0(i,"/",length(num)))
}

L = list()
for(i in 1:length(num)){
  try({
  L = c(L,list(Infor1(Read_data(num[i]))))
  print(paste0(i,"/",length(num)))
  })
}



#






# ------------------------------- 수정 중 --------------------------------------------------------- #


#
# ------------------예제 ------------------- #
# 총 몇페이지?
page = Page_total()

####없는 숫자만 찾아서 데이터를 저장 시키면 된다.
num = c()
for(i in 1:page){
  add = ExistCheck_num(Read_url(i)$job_url_num)
  num = c(num,add)
}
num # 데이터를 저장해야 되는 정보 






