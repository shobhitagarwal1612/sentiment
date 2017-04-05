library("rvest")
library("methods")
library("stringr")

myArgs <- commandArgs(trailingOnly = TRUE)

productPage <- read_html(myArgs)
capture.output(productPage %>% html_nodes(".col1 td") %>% html_text(), file="specs.txt",append=FALSE);


#screen title
title <- NA
while(is.na(title)) {
    title <- productPage %>% html_node("#revMHLContainer h2") %>% html_text()
    print(title)
}

#write title
#NOTE this file should already exist
#fileConn<-file("product-title.txt")
#writeLines(c(title), fileConn)
#close(fileConn)


#scrape specifications
# specifications <- productPage %>% html_node(xpath='//*[@id="prodDetails"]/div[2]/div[1]/div/div[2]/div/div/table') %>% html_table()
# fileConn<-file("specifications.txt")
# paste(c(specifications), fileConn)
# close(fileConn)

#scrape image
image <- NA
while(is.na(image)) {
    image <- productPage %>% html_node("#landingImage") %>% html_attr("src")
    # image <-  sub('.', '', image)
    capture.output(str_replace_all(image, "[\r\n]" , ""), file="imageData.txt", append=FALSE)
}

#userReviewsPage <- productPage %>% html_nodes(".a-link-emphasis") %>% html_attr("href")
#print(userReviewsPage[1])
#userReviewsPage = userReviewsPage[1]

#while (userReviewsPage != "http://www.amazon.in") {

#	allReviews <- read_html(userReviewsPage);
#	capture.output( allReviews %>%  html_nodes(".review-text")  %>%  html_text(),file="userReviews.txt", append=TRUE)

#	userReviewsPage = allReviews %>% html_nodes(".a-last a") %>% html_attr("href")
#	userReviewsPage = paste("http://www.amazon.in",userReviewsPage,sep="")

#Sys.sleep(3)
#}
