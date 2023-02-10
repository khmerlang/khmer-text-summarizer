import argparse
import numpy as np
from math import sqrt
import networkx as nx
from khmernltk import sentence_tokenize
from khmernltk import word_tokenize

def cosine_distance(u, v):
    """
    Returns 1 minus the cosine of the angle between vectors v and u. This is
    equal to ``1 - (u.v / |u||v|)``.
    """
    return 1 - (np.dot(u, v) / (sqrt(np.dot(u, u)) * sqrt(np.dot(v, v))))

def read_article(file_name):
    """
    Read text from file.
    Return list [setences[words]]
    """
    file = open(file_name, "r")
    lines_data = file.readlines()
    sentences = []
    for line in lines_data:
        line = line.strip()
        if len(line) > 0:
            line_sentences = sentence_tokenize(line)
            for sentence in line_sentences:
                sentences.append(word_tokenize(sentence, return_tokens=True))

    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    """
    Return similarity scoring between two sentences
    """

    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n=5):
    # load stopwords
    stop_words = []
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  read_article(file_name)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    # print("Indexes of top ranked_sentence order are ", ranked_sentence)    

    for i in range(top_n):
      summarize_text.append("​".join(ranked_sentence[i][1]))

    # Step 5 - Offcourse, output the summarize text
    return "។ ".join(summarize_text).replace("។។", "។").replace(" ។", "។")


if __name__ == "__main__": 
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-f", "--file", help = "File input", required=True)
    parser.add_argument("-l", "--line", help = "Number of line", default="2")
    
    # Read arguments from command line
    args = parser.parse_args()
    file_name = args.file
    line = int(args.line)

    print(generate_summary(file_name, line))