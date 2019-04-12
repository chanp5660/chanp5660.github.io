# 취직 공고에 대한 데이터 크롤링

### 1. 사람인, 잡코리아 등 공고 데이터를 날짜별로 .csv 파일로 저장


```r
library(rvest)
library(stringr)
library(plyr)
library(dplyr)
library(magrittr)

# 공채중인 총 건수        한 페이지에 100개씩 총개수/100 해서 몫+1만큼 반복 
Page_total = function(){
  url = "http://www.saramin.co.kr/zf_user/jobs/public/list?sort=ed&quick_apply=&search_day=&keyword=#listTop"
  html_data = read_html(url,encoding="UTF-8")
  page = html_data %>% html_nodes(xpath='//*[@id="content"]/div[4]/div[1]/ul/li/a/strong/span') %>% html_text()
  page = as.numeric(gsub(",","",page)) %/% 100 +1
  return(page)
}

# 공고번호 중 추가할 번호 저장,출력 (공고번호는 유일한다고 생각) 원래 번호 중 없으면 추가한다.
Add_num =function(add){
  num = read.csv("T:/2019-1/bigdataanalysis/project/result/num_total.txt")[,2]
  add_num = add[!add %in% num]
  num=c(num,add_num)
  write.csv(num,"T:/2019-1/bigdataanalysis/project/result/num_total.txt")
  return(add_num)
}
# --------- 해당 페이지의 회사이름,공고제목,범주,url저장 ------- 
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

# ---------------------- num에 해당되는 정보를 html로 저장 ---------------
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

# --------------------- num에 해당되는 데이터 읽기  ------------------------#
Read_data <- function(num){
  html_data = read_html(paste0('T:/2019-1/bigdataanalysis/project/result/saramin/',num,'.html'))
}

# --------------------- html_data에 해당하는  추가정보 불러오기,  ---------------#
# ------------------------------- 조회수, 홈페이지접속, 자사양식다운로드 -------------------------#
# ------------------------------- 회사명, 공고제목, 즐겨찾기 수 -------------------------#
# ------------------------------- 시작일, 마감ㅇ -------------------------#
Infor1 <- function(html_data){
  Infor_nm = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(".col") %>% html_nodes("dt") %>% html_text()
  Infor_data= gsub("  |\\n","",html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(".col") %>% html_nodes("dd") %>% html_text())
  temp = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(xpath='//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/div/a[1]') %>% html_text()
  Company = gsub("\n|  ","",temp)
  Title = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(xpath='//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/div/h1') %>% html_text()
  Favor = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(xpath='//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/div/button[2]/span') %>% html_text()
  temp = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(".meta") %>% html_nodes("li") %>% html_text()
  temp = strsplit(grep("조회수|홈페이지접속|자사양식다운수",temp,value=T)," ")
  view_nm=c()
  view_cnt =c()
  for(i in temp){
    view_nm = c(view_nm,i[1])
    view_cnt = c(view_cnt,i[2])
  }
  Day_start = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(xpath='//*[@id="content"]/div[2]/div[1]/div[1]/div[4]/div[2]/div/dl/dd[1]') %>% html_text()
  Day_end = html_data %>% html_nodes(".jview") %>% extract(1) %>% html_nodes(xpath='//*[@id="content"]/div[2]/div[1]/div[1]/div[4]/div[2]/div/dl/dd[2]') %>% html_text()
  
  
  return(list("Company"=Company, "Title"=Title, "Favor"=Favor, "Infor_nm"=Infor_nm, 
              "Infor_data"=Infor_data, "view_nm"=view_nm, "view_cnt"=view_cnt, 
              "Day_start"=Day_start, "Day_end"=Day_end))
}



# ------------------------------- 수정 중 ----------------------------#


#
#------------------예제 -------------------#
# 총 몇페이지?
page = Page_total()


#url 저장 (카테고리도 여기서 추가)
num=c()
for(i in 1:page){
  num=unique(c(num,Read_url(i)$job_url_num))
}
write.csv(num,"T:/2019-1/bigdataanalysis/project/result/num_total.txt")
num2 = read.csv("T:/2019-1/bigdataanalysis/project/result/num_total.txt")[,2]
str(num2)
#없는 숫자만 찾아서 데이터를 저장 시키면 된다.


#html 저장
num = 35994221
Save_html(num)
num = 35912962
Save_html(num)

len = length(Read_url(page)$job_url_num)
temp = as.numeric(Read_url(page)$job_url_num)
for(i in 1:len){
  Save_html(temp[i])
  Sys.sleep(25)# 한번에 많이 하면 터진다.
  print(paste0(i,"/",len))
}
for(i in 55:50){
  Save_html(temp[i])
  Sys.sleep(10)# 한번에 많이 하면 터진다.
  print(paste0(i,"/",len))
}

#html 실행 후 내용
### 예제 1
html_data = Read_data(num)
Infor1(html_data)




```

### 2. 매일 데이터 자동 저장(그 전 데이터와 겹치는지도 비교)

