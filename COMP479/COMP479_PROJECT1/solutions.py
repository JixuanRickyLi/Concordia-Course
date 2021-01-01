"""
Write your reusable code here.
Main method stubs corresponding to each block is initialized here. Do not modify the signature of the functions already
created for you. But if necessary you can implement any number of additional functions that you might think useful to you
within this script.

Delete "Delete this block first" code stub after writing solutions to each function.

Write you code within the "WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv" code stub. Variable created within this stub are just
for example to show what is expected to be returned. You CAN modify them according to your preference.
"""
import glob
import codecs
import nltk

def block_reader(path):
    # Delete this block first
    # raise NotImplementedError("Please implement your solution in block_reader function in solutions.py")
    # ##############

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    file_names = glob.glob(path + "/*.sgm")
    for file_name in file_names:
        with codecs.open(file_name, 'rb', errors='ignore', encoding='utf8') as f:
            content = f.read()
        yield content
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_document_segmenter(INPUT_STRUCTURE):
    # Delete this block first
    # raise NotImplementedError("Please implement your solution in block_document_segmenter function in solutions.py")
    # ##############
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    for single_line in INPUT_STRUCTURE:
        single_line = single_line.strip('<!DOCTYPE lewis SYSTEM "lewis.dtd">')
        single_line = single_line.split('</REUTERS>')
        for document_text in single_line:
            if document_text != '\n':
                if document_text[0] == '\n':
                    document_text = document_text[1:]
                document_text += '</REUTERS>'
                print("\n\nthis is the document :", document_text)
                yield document_text

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_extractor(INPUT_STRUCTURE):

    # is there any faster way in doing this?

    # Delete this block first
    # raise NotImplementedError("Please implement your solution in block_extractor function in solutions.py")
    # ##############

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    content_dict = {}
    for single_news in INPUT_STRUCTURE:
        if single_news.find("<BODY>") == -1:
            continue
        i = single_news.find("NEWID")
        j = single_news.find("\n<DATE>")
        id = single_news[i+7:j-2]
        temp = single_news.split("<BODY>", 1)[-1]
        temp = temp.split("</BODY>", 1)[0]
        content_dict["ID"] = id
        content_dict["TEXT"] = temp
        print(content_dict)
        yield content_dict
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_tokenizer(INPUT_STRUCTURE):
    # Delete this block first
    # raise NotImplementedError("Please implement your solution in block_tokenizer function in solutions.py")
    # ##############

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    for post in INPUT_STRUCTURE:
        text = post["TEXT"]
        tokens = nltk.word_tokenize(text)
        for token in tokens:
            token_tuple = (post["ID"], token)  # Sample id, token tuple structure of output
            print(token_tuple)
            yield token_tuple
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stemmer(INPUT_STRUCTURE):
    # Delete this block first
    # raise NotImplementedError("Please implement your solution in block_stemmer function in solutions.py")
    # ##############

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv

    porter = nltk.PorterStemmer()
    for cur_tuple in INPUT_STRUCTURE:
        i, token = cur_tuple
        token_tuple = (i, porter.stem(token))
        print(token_tuple)
        yield token_tuple
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stopwords_removal(INPUT_STRUCTURE, stopwords):
    # Delete this block first
    # raise NotImplementedError("Please implement your solution in block_stopwords_removal function in solutions.py")
    # ##############

    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    stop_list = stopwords.split(" ")
    for cur_tuple in INPUT_STRUCTURE:
        i, token = cur_tuple
        if token in stop_list:
            continue
        print(cur_tuple)
        yield cur_tuple
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^
