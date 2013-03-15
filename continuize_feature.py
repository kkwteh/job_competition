import numpy as np
import pandas as pd

def continuize_feature(train, test, group_feature_name, by_feature_name):
    """Adds a continuous version of a categorical column to data frames
    Typical usage: continuize_feature(train,test, "Company", "Salary")
    Args:
    train: a data frame which has the by_feature, which is typically a label
    that you're trying to predict
    test: a data frame which does not have the by_feature, typically it has
    validation data
    group_feature_name: name of the categorical column which you are trying to
    continuize
    by_feature_name: A numerical quantity which dictates how the categorical
    column gets transformed into a continuous one

    Returns:
    Nothing, the data frames get modified in place
    """
    gfn = group_feature_name
    default_value = np.mean(train[by_feature_name])
    feature_series =   train.groupby(gfn).agg(np.mean)[by_feature_name]
    feature_function = functionize_series(feature_series, default_value)
    train[group_feature_name + "_c"] = train[gfn].apply(feature_function)
    test[group_feature_name + "_c"] = test[gfn].apply(feature_function)

def functionize_series(s, default_value):
    """Turns a pandas series into a function
    """
    def s_as_function(key):
        if key in s.index:
            return s[key]
        else:
            return default_value
    return s_as_function
