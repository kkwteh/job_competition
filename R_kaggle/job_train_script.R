library(roxygen)

col_mean <- function(df,col_name){
  return(mean(df[[col_name]]))
}

continuize.feature <- function(df, feature.name, by.feature){
  feature.list <- dlply(df, c(feature.name), Curry(col_mean, col_name=by.feature))
  feature.function <- functionize.feature(feature.list)
  feature.name.c <- paste(feature.name,'.c',sep="")
  df[[feature.name.c]] <- sapply(df[[feature.name]], feature.function)
  df[[feature.name]] <- NULL
  return(df)
}


functionize.feature <- function(feature.list){
  return (function(class){return(feature.list[[class]])})
}

e.train <- read.csv("~/code/kaggle/enhanced_mini_train.csv")
e.train <- continuize.feature(e.train,'LocationNormalized', 'SalaryNormalized')
e.train <- continuize.feature(e.train,'ContractType', 'SalaryNormalized')
e.train <- continuize.feature(e.train,'Category', 'SalaryNormalized')
e.train <- continuize.feature(e.train,'Company', 'SalaryNormalized')