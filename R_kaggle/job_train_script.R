#This script continiuizes various categorical features of a dataframe
#read from a csv.

library(roxygen)
library(randomForest)

col_mean <- function(df,col_name){
  #Computes mean of a column of a data frame
  #Args:
  #df: A data frame
  #col_name: Name of the column in the data frame which you want the mean of
  #Returns:
  #A single number, the mean of the column
  return(mean(df[[col_name]]))
}

functionize.list <- function(the.list, default.value){
  #turns a list of entries where each entry has a name into a function
  #which sends a name to the entry of the list with that name
  #Args:
  #a.list: a list each of whose entries is named
  #default.value: the default value to return in case an argument
  #to the function is not a name in the list
  #Returns:
  #a function such that f(<name>) returns the contents of the
  #list at that name
  return (function(class){
      if (class %in% names(the.list)){
        return(the.list[[class]])
      } else {
        return(default.value)
      }
    })
}

continuize.feature <- function(df, feature.name, by.feature){
  #Replaces a categorical column with a column of continuous values
  # the continuous values are the mean of the by.feature column when
  # restricted to a fixed class of the categorical column. Does not
  # modify the original data frame
  #Args:
  #df: dataframe
  #feature.name: name of column with categorical variable to be replaced
  # by a continuous one
  #by.feature: name of column whose mean is computed for each class of the
  #categorical column
  #Returns:
  #A data frame with the categorical feature removed, replaced with a
  #continuous version of it, denoted by a '.c' at the end of the old name.
  default.value <- col_mean(df,by.feature)
  feature.list <- dlply(df, c(feature.name), Curry(col_mean, col_name=by.feature))
  feature.function <- functionize.list(feature.list, default.value)
  feature.name.c <- paste(feature.name,'.c',sep="")
  df[[feature.name.c]] <- sapply(df[[feature.name]], feature.function)
  df[[feature.name]] <- NULL
  return(df)
}


continuize_df <- function(df){
  #Continuizes all categorical features in the job kaggle competition
  df <- continuize.feature(df,'LocationNormalized', 'SalaryNormalized')
  df <- continuize.feature(df,'LocationRaw', 'SalaryNormalized')
  df <- continuize.feature(df,'ContractType', 'SalaryNormalized')
  df <- continuize.feature(df,'ContractTime', 'SalaryNormalized')
  df <- continuize.feature(df,'Category', 'SalaryNormalized')
  df <- continuize.feature(df,'Company', 'SalaryNormalized')
  df <- continuize.feature(df,'SourceName', 'SalaryNormalized')
  return(df)
}

e.train <- read.csv("~/code/kaggle/enhanced_mini_train.csv")
e.train <- continuize_df(e.train)
e.train$SalaryRaw <- NULL
e.train$FullDescription <- NULL
e.train$Title <- NULL
e.train$Id <- NULL
e.train$X <- NULL
randomForest(formula = SalaryNormalized ~ ., data=e.train, importance=TRUE)