job_competition
===============

line 1588 of the training file has NaN for the Job Title

-It takes 7.5 seconds to load the training data into a data frame

-Taking top 10 most common words appearing in job title, model creation took a
couple of minutes

-Taking top 200 most common words appearing in job title, model creation took
about 25 minutes

-It takes 1 minute to add 40 word appearance features to the training dataset.

-It takes 2 minutes to train a Lasso Regression Model on these 40 features

-It takes 3 minutes to add 40 word appearance features to the training dataset
and train a RandomForestRegressor and rank the importance of words.
