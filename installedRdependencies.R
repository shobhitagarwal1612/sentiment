library("rvest")
library("stringr")
library("methods")
library("xml2")

packages <- c("rvest","stringr","methods","xml2)

# Function to check whether package is installed
is.installed <- function(mypkg){
    is.element(mypkg, installed.packages()[,1])
}

for(package in packages){
    # check if package is installed
    if (!is.installed(package)){
        install.packages(package, repos="http://cran.rstudio.com/")
    }
}

