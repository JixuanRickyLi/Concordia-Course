import glob
import codecs
import collections
import json
import math

from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
import re
import CONFIGURATION


def block_reader(path):
    file_names = glob.glob(path + "/*.html")
    for file_name in file_names:
        iD = file_name[CONFIGURATION.START_INDEX:-5]
        with codecs.open(file_name, 'rb', errors='ignore', encoding='utf-8') as f:
            content = f.read()
        yield iD, content

def clean(body):
    body = body.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    body = body.replace('[  ]{1, }', ' ')
    body = re.sub("\t\n\r", " ", body)
    body = re.sub("( ){2,}", " ", body)
    return body

def block_document_segmenter(file_stream):
    for iD, html_doc in file_stream:
        soup = BeautifulSoup(html_doc, 'html.parser')
        yield iD, clean(soup.get_text())


def parse_tokens_from_documents(document_stream):
    for iD, document in document_stream:
        iD = int(iD)
        text_tokens = tokenizer.tokenize(document)
        for token in text_tokens:
            yield iD, token


def spimi(token_stream, k):
    dictionary = dict()
    term_counter = 0
    for new_id, token in token_stream:
        if term_counter < k:
            if token not in dictionary:
                dictionary[token] = [new_id]
            else:
                dictionary[token].append(new_id)
            term_counter = term_counter + 1
        else:
            write_to_block(dictionary)
            print("spimi is writing a new block")
            dictionary.clear()
            term_counter = 0
        stat(token, new_id)


def stat(token, new_id):
    if token not in tf_td:
        tf_td[token] = dict()
    if new_id not in tf_td[token]:
        tf_td[token][new_id] = 1
    else:
        tf_td[token][new_id] = tf_td[token][new_id] + 1
    if new_id not in l_d:
        l_d[new_id] = 0
    l_d[new_id] = l_d[new_id] + 1
    global N
    N = CONFIGURATION.NUM_OF_DOC


def build_tf_df_dictionary(file_path):
    print("Building tf_df_dictionary")
    docFrequency_F = {}
    word_counter = 0
    for iD, term in parse_tokens_from_documents(block_document_segmenter(block_reader(file_path))):
        word_counter += 1
        if term in docFrequency_F:
            posting_list = docFrequency_F.get(term)
            if int(iD) in posting_list:
                posting_list[int(iD)] = posting_list[int(iD)] + 1
            else:
                posting_list[int(iD)] = 1
        else:
            docFrequency_F[term] = {int(iD): 1}

    for key in docFrequency_F.keys():
        docFrequency_F[key] = collections.OrderedDict(docFrequency_F[key])

    completed_dict = {}
    for key in docFrequency_F.keys():
        new_key = key + "/" + str(docFrequency_F[key].__len__())
        completed_dict[new_key] = sorted(docFrequency_F[key].items(), key=lambda x: x[1], reverse=True)[:50]

    return completed_dict


def write_to_block(dictionary):
    global block_id
    sorted_dict = collections.OrderedDict(sorted(dictionary.copy().items()))
    print("writing block", block_id)
    blocks["Block" + str(block_id)] = sorted_dict
    block_id = block_id + 1


def merge_blocks():
    print('start merging')
    for sorted_dict in blocks.values():
        for key, val in sorted_dict.items():
            if key in global_index:
                global_index[key] = global_index[key] + val
            else:
                global_index[key] = val
    for key, val in global_index.items():
        posting_list = list(dict.fromkeys(val))
        posting_list.sort()
        global_index[key] = posting_list


def l_ave():
    sum_of_length = 0
    for doc_length in l_d.values():
        sum_of_length += doc_length
    return sum_of_length / N


def calculate_RSV(k1, b, query, new_id):
    ans = 0
    if new_id not in l_d:
        l_d[new_id] = 0
    L_d = l_d[new_id]
    for term in query:
        tftd = 0
        if term in global_index:
            df_t = len(global_index[term])
            if new_id in tf_td[term]:
                tftd = tf_td[term][new_id]
        else:
            df_t = 0
        ans = ans + ((math.log((1 + N) / (1 + df_t), 10) + 1)
                     * (((k1 + 1) * tftd) / (k1 * ((1 - b) + b * (L_d / L_ave)) + tftd)))
    return ans


def RSV_rank(query, k1, b):
    scores = dict()
    for new_id in range(len(l_d)):
        score = calculate_RSV(k1, b, query, new_id + 1)
        scores[new_id + 1] = score
    rank = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return rank[:15]


def tf_idf_and_query(query):
    ans = collections.OrderedDict()
    for term in query:
        if term not in tf_td:
            ans = {}
            break
        if len(ans) == 0:
            ans = execute_tf_idf_query(tf_td[term])
        else:
            new_ans = collections.OrderedDict()
            ans_temp = execute_tf_idf_query(tf_td[term])
            key_set = ans.keys() & ans_temp.keys()
            for key in key_set:
                new_ans[key] = ans_temp[key] + ans[key]
            ans = new_ans
    return sorted(ans.items(), key=lambda x: x[1], reverse=True)[:15]

def execute_tf_idf_query(ans_dict):
    ans = collections.OrderedDict()
    idf = math.log(CONFIGURATION.NUM_OF_DOC / len(ans_dict))
    for doc, word_count in ans_dict.items():
        tf = word_count / l_d[doc]
        if doc in list(ans.keys()):
            ans[doc] += tf * idf
            break
        ans[doc] = tf * idf
    return ans


def and_query(query):
    ans = set()
    for term in query:
        if term not in global_index:
            ans = set()
            break
        if len(ans) == 0:
            ans = set(global_index[term])
        else:
            ans = ans & set(global_index[term])
    return list(ans)


def or_query(query):
    ans = dict()
    for term in query:
        if term not in global_index:
            continue
        for doc_id in global_index[term]:
            if doc_id not in ans:
                ans[doc_id] = 0
            ans[doc_id] = ans[doc_id] + 1
    for k, v in ans.items():
        if v > 2:
            print(k, v)
    return [k for k, v in sorted(ans.items(), key=lambda item: item[1], reverse=True)]

def result_processing(result_list):
    counter = 0
    for iD, score in result_list:
        counter += 1
        file_name = CONFIGURATION.DATA_PATH + "/" + str(iD) + ".html"
        content = ""
        with codecs.open(file_name, 'rb', errors='ignore', encoding='utf-8') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        print("Result " + str(counter) + "\n")
        print("ID:", iD)
        print('score: ', score)
        print('title: ', soup.title.string)
        print('url: ', soup.url.string)
        print("=================================")

def query_RSV_IDF(query):
    print('''
    ______  _____  _   _    ______ _____ _____ _   _ _    _____ 
    | ___ \/  ___|| | | |   | ___ \  ___/  ___| | | | |  |_   _|
    | |_/ /\ `--. | | | |   | |_/ / |__ \ `--.| | | | |    | |  
    |    /  `--. \| | | |   |    /|  __| `--. \ | | | |    | |  
    | |\ \ /\__/ /\ \_/ /   | |\ \| |___/\__/ / |_| | |____| |  
    \_| \_|\____/  \___/    \_| \_\____/\____/ \___/\_____/\_/  

                                                                ''')
    result_processing(RSV_rank(query, 1.5, 0.75))
    print('''
     ___________    _________________  ______  ___   _   _  _   __
    |_   _|  ___|  |_   _|  _  \  ___| | ___ \/ _ \ | \ | || | / /
      | | | |_ ______| | | | | | |_    | |_/ / /_\ \|  \| || |/ / 
      | | |  _|______| | | | | |  _|   |    /|  _  || . ` ||    \ 
      | | | |       _| |_| |/ /| |     | |\ \| | | || |\  || |\  \ 
      \_/ \_|       \___/|___/ \_|     \_| \_\_| |_/\_| \_/\_| \_/

                                                                  ''')
    result_processing(tf_idf_and_query(query))

tokenizer = RegexpTokenizer(r'\w+')
tf_td = dict()
l_d = dict()
N = CONFIGURATION.NUM_OF_DOC

#
blocks = dict()
global_index = dict()
block_id = 1
spimi(parse_tokens_from_documents(block_document_segmenter(block_reader(CONFIGURATION.DATA_PATH))), 100000)
merge_blocks()
#
# global_index = {}
# with open("global_index.json", 'r', encoding='UTF-8') as f:
#     global_index = json.load(f)
#
# l_d = {}
# with open("l_d.json", 'r', encoding='UTF-8') as f:
#     l_d = json.load(f)
#
# tf_td = {}
# with open("tf_td.json", 'r', encoding='UTF-8') as f:
#     tf_td = json.load(f)
L_ave = l_ave()


test_query_a = ["COVID", "researcher"]
test_query_b = ["COVID", "related", "research"]
test_query_c = ["water", "conservation", "environmental", "energy", "department"]
test_query_d = ["research", "water", "environment", "sustainability", "energy"]

queries = [test_query_a, test_query_b, test_query_c, test_query_d]

for q in queries:
    query_RSV_IDF(q)


challenge_query = [
    ['water', 'management', 'sustainability', 'Concordia'],
    ['Concordia', 'COVID', 'faculty'],
    ['SARS', 'Concordia', 'faculty']
]

for q in challenge_query:
    query_RSV_IDF(q)
# print(and_query(test_query_a))
# print(or_query(test_query_a))
