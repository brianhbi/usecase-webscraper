'''
Contains functions that clean the dataframe scraped from links
to create txt files ready to be used by fasttext.
'''
import pandas as pd
import wikipedia
import time
import csv
import random
import os


# Input: df [label, query, link, text, # words], not cleaned
# Output: df without repeats and short inputs
def remove_failed_links(data):
    data_row_count = data.shape[0]

    final_data = data[data['number_of_words'] > 200]  # keep everything > 200
    repeats = final_data['number_of_words'].shift(1) == final_data['number_of_words']  # removes repeats
    norepeats = final_data[-repeats]

    norepeats_row_count = norepeats.shape[0]
    print("removed_failed_links got rid of", (data_row_count-norepeats_row_count), "links.")

    return norepeats


# Input: df [label, query, link, text, # words (all mixed, original size)], cleaned
# Output: train and test file ready for fasttext
def clean_data_for_fasttext(data):
    data = data.drop(data.columns[[1, 2, 4]], axis=1).reset_index(drop=True)  # drop the query, link and num words columns
    # data = data.sort_values(by=['Use Case Category']).reset_index(drop=True)
    # data.to_csv("after_dropping_columns.csv", index=False)

    brokenup_text = split_text(data)
    brokenup_text.to_csv("brokenup.csv", index=False)

    train, test = split_train_test(brokenup_text)

    return train, test


# Input: df [label, text (all mixed, original size)]
# Output: df [label, text (same size)]
def split_text(data):
    testdataframe = pd.DataFrame(columns=['Use Case Category', "Text"])

    for index, row in data.iterrows():
        label = row['Use Case Category']
        text = row['Text'].split()
        break_size = 100 # random.randint(50,200)
        splittext = [" ".join(text[i: i + break_size]) for i in range(0, len(text), break_size)]

        for x in splittext:
            if len(x.split()) > break_size/3: # only input if it has more than 2/3 of splitnum
                testdataframe = testdataframe.append({'Use Case Category': label, 'Text': x}, ignore_index=True)
    # testdataframe = testdataframe.reset_index(drop=True)

    return testdataframe


# Input: empty train and test df
# Output: filled up train and test with respective percentage of dataset
def update_train_test(dataframe, train, test, percentage):
    for index, row in dataframe.iterrows():
        if index < (dataframe.shape[0] * percentage):
            train = train.append({'Use Case Category': row['Use Case Category'], 'Text': row['Text']}, ignore_index=True)
        else:
            test = test.append({'Use Case Category': row['Use Case Category'], 'Text': row['Text']}, ignore_index=True)

    return train, test


# Input: df [label, text]
# Output: filled up train and test with respective percentage of dataset
def split_train_test(data):
    train = pd.DataFrame(columns=['Use Case Category', "Text"])
    test = pd.DataFrame(columns=['Use Case Category', "Text"])

    train, test = update_train_test(data, train, test, 0.8) # data was all_im before

    print("Number of rows in train =", train.shape[0])
    print("Number of rows in test =", test.shape[0])
    print("Sum =", train.shape[0] + test.shape[0])

    return train, test


# Input: df and filename
# Output: df saved as csv in usecase_data folder with filename
def save_file(dataframe, savename):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_path = os.path.join(file_dir, "usecase_data", savename)
    dataframe.to_csv(file_path, index=False, sep=' ', header=False, quoting=csv.QUOTE_NONE, quotechar="", escapechar=" ")
