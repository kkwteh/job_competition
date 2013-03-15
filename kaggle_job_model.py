#!/Users/teh/code/kaggle/ENV/bin/python
from continuize_feature import *
from word_feature_enhance import *
from sklearn.ensemble import RandomForestRegressor
import re

train = pd.read_csv("Train_rev1.csv")
valid = pd.read_csv("Valid_rev1.csv")

title_words = count_words_in_column(train, "Title")
for word, count in title_words.items():
    add_appearance_count_feature(train, word, "Title")
    add_appearance_count_feature(valid, word, "Title")

group_features = ["LocationNormalized", "Category", "Company", "SourceName"]

for f in group_features:
    continuize_feature(train, valid, f, "SalaryNormalized")

feature_columns = train.columns[12:]

feature=train[feature_columns]
label=train.SalaryNormalized
clf = RandomForestRegressor()
clf.fit(feature, label)

valid_salary_predict = clf.predict(valid[feature_columns])
valid["SalaryNormalized_Predict"] = valid_salary_predict

prelim_filename = 'kaggle_job_predict.csv'

with open(prelim_filename,'wb') as f:
    valid[["Id","SalaryNormalized_Predict"]].to_csv(f)


with open(prelim_filename,'rb') as f:
    with open('refined_kaggle_job_predict.csv','wb') as g:
        for line in f.xreadlines():
            g.write(re.sub('^[^,]*,', '', line))
