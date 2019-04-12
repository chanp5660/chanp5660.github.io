# 취직 공고에 대한 데이터 크롤링

### 1. 사람인, 잡코리아 등 공고 데이터를 날짜별로 .csv 파일로 저장


```r
library(rvest)
library(dplyr)
#사람인에 해당하는 공채의 정보를 구하기

#해당
page = 1
url = paste0("http://www.saramin.co.kr/zf_user/jobs/public/list/page/",page,"?sort=ed&listType=public&public_list_flag=y&page=",page,"#searchTitle")
html_data = read_html(url,encoding="UTF-8")


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

# 공고 url
job_url = unique(html_data %>% html_nodes(".str_tit") %>% html_attr("href"))
#

# 정규직, 계약직, 인턴직  고용형태

#






#공고 제목
Title_nm
#회사 이름
Company_nm
#범주
Category
# 공고 url
job_url
#고용형태
```

### 2. 매일 데이터 자동 저장(그 전 데이터와 겹치는지도 비교)

