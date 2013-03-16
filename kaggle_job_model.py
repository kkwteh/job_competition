#!/Users/teh/code/kaggle/ENV/bin/python
from continuize_feature import *
from word_feature_enhance import *
from sklearn.ensemble import RandomForestRegressor
import re
import sys
import datetime
from nltk.corpus import stopwords


def make_model_and_predict(train_file, test_file):
    """Given name of training csv file, name of test csv file, constructs
    a random forest model and outputs predictions to a time-stampled csv file
    """

    train = pd.read_csv(train_file)
    valid = pd.read_csv(test_file)

    number_of_word_features = 200
    title_words = count_words_in_column(train, "Title")
    key_count_pairs = [(k,v) for (k,v) in title_words.items() if k not in
                                                stopwords.words('english')]

    key_count_pairs.sort(key=lambda (k,v): -v)

    for word, count in key_count_pairs[:number_of_word_features]:
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

    date_string = re.sub("[ :.]", "", str(datetime.datetime.now()))
    prelim_filename = 'raw_predict' + date_string + '.csv'
    final_filename = 'predict' + date_string + '.csv'

    with open(prelim_filename,'wb') as f:
        valid[["Id","SalaryNormalized_Predict"]].to_csv(f)


    with open(prelim_filename,'rb') as f:
        with open(final_filename,'wb') as g:
            f.readline()           #Throw away the header, don't need it.
            for line in f.xreadlines():
                g.write(re.sub('^[^,]*,', '', line))

def main():
    """
    Standard main function boilerplate to accept command line arguments
    """
    args = sys.argv[1:]

    if not args:
        print 'usage: train_file test_file'
        sys.exit(1)

    train_file = args[0]
    test_file = args[1]
    make_model_and_predict(train_file, test_file)

if __name__ == '__main__':
    main()
