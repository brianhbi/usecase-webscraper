'''
This script takes a use case category as an argument and will create a dataset ready to be used for fasttext.
You will need to put all the files together from the different use cases though.
'''
import pandas as pd
import wikipedia
import sys
import csv
import time
import os
from extract_text import *
from clean_my_data import *

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


# Input: use case you want to create dataset for
# Output: df (list of rows - [label, query, link, text,  #words]) with google and wiki data together
def pull_data_from_queries(use_case):
    start = time.time()

    curr_file_dir = os.path.dirname(os.path.realpath('__file__'))
    query_filename = os.path.join(curr_file_dir, 'keywords/' + use_case + '.txt')
    google_queries, wiki_queries = separate_google_and_wiki(query_filename)

    print("Google queries: ", google_queries)
    print("Wikipedia queries: ", wiki_queries, '\n')
    print("Initiating data extraction from queries...", "\n")

    label = "__label__" + use_case
    google_data = get_google_data(google_queries, label)
    wiki_data = get_wiki_data(wiki_queries, label)
    my_data = wiki_data + google_data

    end = time.time()
    print("\nFinished data extraction from", len(my_data), "queries in", (end-start), "seconds.")

    return my_data

# Input: name of file with google and wiki queries (separated by newline)
# Output: 2 dictionaries - one for google and one for wiki queries
def separate_google_and_wiki(query_filename):
    queries_dict = {}
    queries_dict['google'] = []
    queries_dict['wikipedia'] = []
    key = 'google'

    query_file = open(query_filename, 'r')
    f = query_file.readlines()
    for query in f:
        if query != "\n": # change key when there is a newline
            if key == 'google':
                queries_dict[key].append(query.strip('\n') + " iot") # add 2 queries for each query (gives more specific results to iot)
                queries_dict[key].append("iot " + query.strip('\n') + " use case")
            else:
                queries_dict[key].append(query.strip('\n'))
        else:
            key = 'wikipedia' # change key

    return queries_dict['google'], queries_dict['wikipedia']


# Input: list of google queries and label
# Output: df (list of rows - [label, query, link, text,  #words]) with scraped google links
def get_google_data(queries, label):
    print("Going through google data...\n")

    google_data = []
    links = [] # avoid repeats before scraping to save time
    for query in queries: # For each query
        for link in search(query, tld="co.in", start=0, stop=20, pause=1): # ...There are several links...
            if "pdf" not in link and "wikipedia" not in link:  # text extract does not support pdf and I handle wikipedia later
                if link not in links:
                    text = scrape_text(link) # ...With unique text output
                    google_data.append([label, query, link, text, len(text)])
                    links.append(link)

    print("Scraped a total of", len(links), "from", len(queries), "distinct google queries.\n")
    return google_data


# Input: list of wiki queries and label
# Output: df (list of rows - [label, query, link, text,  #words]) with scraped wiki links
def get_wiki_data(queries, label):
    print("Going through wikipedia data...\n")

    wiki_data = []
    for query in queries:
        page = wikipedia.page(query)
        link = page.url
        text = clean_text(page.content)
        wiki_data.append([label, query, link, text, len(text)])

    return wiki_data


def main():
    use_case = str(sys.argv[1])
    print("---------- USE CASE =", use_case, "----------\n")

    start = time.time()

    raw_data = pull_data_from_queries(use_case)
    df = pd.DataFrame(raw_data, columns=['Use Case Category', 'Query', 'Link', 'Text', 'number_of_words'])
    clean_df = remove_failed_links(df)
    # clean_df.to_csv('all_data_df.csv', index=False) # -- problem if more than 33,000 characters in a cell

    train, test = clean_data_for_fasttext(clean_df)
    save_file(train, 'train_' + use_case + '.txt')
    save_file(test, 'test_' + use_case + '.txt')

    train['number_of_words'] = train.Text.apply(lambda x: len(x.split()))  # add column with num of words in text
    test['number_of_words'] = train.Text.apply(lambda x: len(x.split()))  # add column with num of words in text
    print("Num words in train:", train['number_of_words'].sum())
    print("Num words in test:", test['number_of_words'].sum())

    end = time.time()
    print("\nFinished building dataset for", use_case, "in", (end-start), "seconds.")


if __name__ == "__main__":
    main()
