#This script continiuizes various categorical features of a dataframe
#read from a csv.

library(roxygen)

col_mean <- function(df,col_name){
  #Computes mean of a column of a data frame
  #Args:
  #df: A data frame
  #col_name: Name of the column in the data frame which you want the mean of
  #Returns:
  #A single number, the mean of the column
  return(mean(df[[col_name]]))
}

functionize.list <- function(a.list){
  #turns a list of entries where each entry has a name into a function
  #which sends a name to the entry of the list with that name
  #Args:
  #a.list: a list each of whose entries is named
  #Returns:
  #a function such that f(<name>) returns the contents of the
  #list at that name
  return (function(class){return(a.list[[class]])})
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
  
  feature.list <- dlply(df, c(feature.name), Curry(col_mean, col_name=by.feature))
  feature.function <- functionize.list(feature.list)
  feature.name.c <- paste(feature.name,'.c',sep="")
  df[[feature.name.c]] <- sapply(df[[feature.name]], feature.function)
  df[[feature.name]] <- NULL
  return(df)
}




e.train <- read.csv("~/code/kaggle/enhanced_mini_train.csv")

continuize_df(df){
  df <- continuize.feature(df,'LocationNormalized', 'SalaryNormalized')
  df <- continuize.feature(df,'ContractType', 'SalaryNormalized')
  df <- continuize.feature(df,'Category', 'SalaryNormalized')
  df <- continuize.feature(df,'Company', 'SalaryNormalized')
  df <- continuize.feature(df,'ContractTime', 'SalaryNormalized')
  df <- continuize.feature(df,'SourceName', 'SalaryNormalized')
}

continuize_df(e.train)