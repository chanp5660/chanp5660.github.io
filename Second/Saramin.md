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

# # 정규직, 계약직, 인턴직  고용형태
# employment_type = html_data %>% html_nodes(".employment_type") %>% html_text()
# temp = html_data %>% html_nodes(".company_info") %>%html_text()
# Delstr ="^\\r\\n                |\\r\\n            $"
# strsplit(gsub(Delstr,"",temp),"\\r\\n                        ")
# 
# temp = html_data %>% html_nodes(".company_info p")
# (grep("employment",temp)[2:93]-grep("employment",temp)[1:92]-3)/2
# grep("salary",temp)
# grep("work_place",temp)
# temp[1]
# #
# 
# temp = html_data %>% html_nodes(".company_info p")
# bind_rows(lapply(xml_attrs(temp), function(x) data.frame(as.list(x), stringsAsFactors=FALSE)))

#공고 제목
Title_nm
#회사 이름
Company_nm
#범주
Category
#고용형태
