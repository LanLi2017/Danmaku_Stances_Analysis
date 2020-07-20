import re
from collections import defaultdict
from pprint import pprint

from nltk import CoreNLPParser, CoreNLPDependencyParser, Tree
from sematch.semantic.similarity import WordNetSimilarity
import pandas as pd
from polyglot.text import Text


def filter_data():
    # filter data
    pass


def find_NN(sentence, parser):
    ''' return the NN '''
    token_sen = list(parser.parse(parser.tokenize(sentence)))
    res = []
    for t in token_sen:
        # position of leaves
        pos = t.treepositions('leaves')
        # (NN 中国人)
        # print(t[0,0,0,0])
        # (AD 为什么)
        # print(t[0,0,1,0,0])
        # (AD 不)
        # print(t[0,0,1,1,0])
        # (VV 能)
        # print(t[0,0,1,2,0])
        # (VV 选择)
        # print(t[0,0,1,2,1,0])
        # (PU ？)
        idxs = []
        for p in pos:
            index = t.treepositions().index(p)
            # prev-leave (label, leaves)
            idx = index - 1
            idxs.append(t.treepositions()[idx])
        for id in idxs:
            res.append(t[id])
    subjects = []
    for r in res:
        if r.label() == 'NN':
            subjects.extend(r.leaves())
    return subjects


separator = [
    ',', '。', '?', '!', '.', ' ',','
]


def map_subjects(subjects: list, filter_dis= 0.2):
    wns = WordNetSimilarity()
    # enumerate pairing and calculate distances
    pair = []
    # return the indexes pairing
    pair_idxs = []
    for index, value in enumerate(subjects):
        i = index+1
        while i < len(subjects):
            # compare list : next list
            com_value = subjects[i]
            for v in value:
                for cv in com_value:
                    pair_distance = wns.monol_word_similarity(v, cv, 'cmn', 'wup')
                    print(f'{v} -> {cv}:  {pair_distance}')
                    if pair_distance> filter_dis:
                        pair.append(pair_distance)
                        # pairing index: (row, column)
                        pair_idxs.append(([index, value.index(v)], [i, com_value.index(cv)]))
            i += 1
    print(pair_idxs)
    return pair_idxs


def return_polarity(sur_words: list):
    ''' if has not/no/.... '''
    surrounding_wd = ''.join(sur for sur in sur_words)
    text = Text(surrounding_wd)
    pol_list = []
    for w in text.words:
        w_po = w.polarity
        pol_list.append(w_po)
        print(f'{w}: {w.polarity}')

    return pol_list


def return_sur(token_sentence, n_token, sub_id):
    '''
    
    Parameters
    ----------
    sentence: danmaku sentence
    n_token: number of surrounding words
    sub: subjects
    sub_id: index of subject in the tokenized sentence list
    Returns: surrounding words of subjects
    -------

    '''
    # separate sentence： 【生于忧患， 死于安乐】
    # sentence = re.split(r'\W+', sentence)
    # ['生于忧患', '死于安乐']
    # token_sentence = list(parser.tokenize(sentence))
    sur_words = []
    if sub_id - n_token < 0 and sub_id + n_token <= len(token_sentence):
        sur_words = token_sentence[sub_id+1: sub_id+n_token+1]
    elif sub_id + n_token > len(token_sentence) and sub_id - n_token >= 0:
        sur_words = token_sentence[-n_token+sub_id: sub_id]
    elif sub_id - n_token >= 0 and sub_id + n_token <= len(token_sentence):
        sur_words = token_sentence[-n_token+sub_id :sub_id]+ token_sentence[sub_id+1: sub_id+n_token+1]
    elif sub_id - n_token <0 and sub_id + n_token > len(token_sentence):
        sur_words = token_sentence[: sub_id] + token_sentence[sub_id + 1:]
    return sur_words


def process_padding(danmaku,parser, title_sub, n_token):
    ''' process padding subject with danmakus in different time scale
        Under Construction
    '''
    # danmaku: initial, middle, end;  danmaku list
    # different padding policy needed
    subjects = []
    sur_words = []
    for dan in danmaku:
        dan_sub = find_NN(dan, parser)  # list of subjects
        token_sentence = list(parser.tokenize(dan))
        if not dan_sub:
            # print(dan)
            # print('initial dont have subject')
            dan_sub = title_sub  # list of subjects in title
            # no subject, short sentence/ phrases
            sur_word = token_sentence
            sur_words.append(sur_word)

        else:
            for sub in dan_sub:
                sub_id = token_sentence.index(sub)
                # sub_id = initial_dan.index(dan) # index of NN/subject
                sur_word = return_sur(token_sentence, n_token, sub_id)
                sur_words.append(sur_word)
        subjects.append(dan_sub)
    return subjects, sur_words


def main():
    parser = CoreNLPParser('http://localhost:9001')
    # print(list(parser.tokenize(u'中国人为什么不能选择安乐死？')))
    # ['中国人', '为什么', '不', '能', '选择', '安乐死', '？']
    # title = '中国人为什么不能选择安乐死？'
    title = '中国人为什么不能选择安乐死?'
    title_sub = find_NN(title, parser)
    # tokenize
    title_token = list(parser.tokenize(title))
    # print(title_token)

    # parse danmaku and extract subjects
    # using windows : surrounding polarity
    data = pd.read_csv('demo.csv')
    danmaku_list = data.loc[:,'Barrages_original']

    # get index of 1. INITIAL 2. middle 3. end
    # for now: the same padding;
    initial_time = 5.0 # what's the inital time duration?
    start_idx = 0
    end_time = data.loc[len(data.index)-1, 'Showing_time']
    mid_time = end_time - 10.0
    mid_idx = 0
    for showing_time in data['Showing_time']:
        if showing_time < initial_time:
            start_idx += 1
        if showing_time < mid_time:
            mid_idx += 1

    # slice danmaku list
    initial_dan = data.loc[:start_idx, 'Barrages_original']
    end_dan = data.loc[mid_idx:,'Barrages_original']
    mid_dan = data.loc[start_idx+1:mid_idx-1, 'Barrages_original' ]

    # subjects = []
    token = 2
    # padding danmaku
    # processing padding on different timezone
    # subjects_ini = process_padding(initial_dan, parser,title_sub,token)[0]
    # subjects_mid = process_padding(mid_dan, parser,title_sub,token)[0]
    # subjects_end = process_padding(end_dan, parser,title_sub,token)[0]
    # subjects.extend(subjects_ini)
    # subjects.extend(subjects_mid)
    # subjects.extend(subjects_end)
    subjects = process_padding(danmaku_list, parser, title_sub, token)[0]
    sur_words = process_padding(danmaku_list, parser, title_sub, token)[1]

    # polarity, according to surrounding words to define the semantic
    po_list = []
    for sur in sur_words:
        po = return_polarity(sur)
        print(f'{sur}: {po}')
        po_list.append(po)
    pprint(po_list)

    # map subjects between each danmaku
    map_subjects(subjects)


def main_test():
    parser = CoreNLPParser('http://localhost:9001')
    # res = list(parser.tokenize('生于忧患,死于安乐'))
    #  downloader.download("sentiment2.zh")
    # data = pd.read_csv('demo.csv')
    # danmaku_list = data.loc[:, 'Barrages_original']
    # pprint(danmaku_list)
    # title = '中国人为什么不能选择安乐死?'
    title = '中国人为什么不能选择安乐死?'
    title_sub = find_NN(title, parser)
    print(title_sub)
    danmaku_list = ['因为人口会大量减少']
    token = 3
    subjects = process_padding(danmaku_list, parser, title_sub, token)[0]
    print(subjects)
    sur_words = process_padding(danmaku_list, parser, title_sub, token)[1]
    print(sur_words)


if __name__ == '__main__':
    main()
    # main_test()