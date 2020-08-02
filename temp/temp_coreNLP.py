import re
from array import array
from collections import defaultdict, Counter
from pprint import pprint

from nltk import CoreNLPParser, CoreNLPDependencyParser, Tree
from sematch.semantic.similarity import WordNetSimilarity
import pandas as pd
from polyglot.text import Text
import numpy as np


def filter_data():
    # filter data
    pass


separator = [
    ',', '。', '?', '!', '.', ' ', ','
]


def find_NN(sentence, parser):
    ''' return subjects '''
    # split sentence with separator : list
    sens = re.split(r'\W+', sentence)
    subj = []
    for s in sens:
        if not s:
            pass
        else:
            parse, = parser.raw_parse(s)
            for governor, dep, dependent in parse.triples():
                if dep == 'nsubj':
                    subj.append(dependent[0])
                    subj.append(governor[0])
                if dep == 'dobj':
                    subj.append(dependent[0])
    return subj


def most_freq(data, parser, title_sub):
    # data: previous 5 seconds [danmaku, showing_time]
    # using most frequent n subjects: depend on how many subjects have been collected
    danmaku = data.loc[:, 'Barrages_original']
    d_sub = []
    for d in danmaku:
        d_sub.extend(find_NN(d, parser))
    c = Counter(d_sub)
    c_size = sum(c.values())
    subjects = []
    if c_size >= 3:
        for value in c.most_common(3):
            subjects.extend(value[0])
    elif 0 < c_size < 3:
        for value in c.most_common(c_size):
            subjects.extend(value[0])
    elif c_size == 0:
        subjects.extend(title_sub)
    return subjects


def win_data(s_time, data, dan_index, parser, title_sub):
    # window-slice data
    # return the subject for the last data
    cut_time = 0.0
    for t in data['Showing_time']:
        if t >= s_time:  # if the difference is smaller than 0.1
            cut_time = t
            break
    time_index = data.index[data['Showing_time'] == cut_time].tolist()[0]
    # using the most frequent subjects to pad
    dan_sub = most_freq(data[time_index:dan_index], parser, title_sub)
    return dan_sub


def padding_initial(title_sub, danmaku, parser):
    # padding the initial danmaku list with title subjects
    ini_subj = []
    for dan in danmaku:
        dan_sub = find_NN(dan, parser)  # list of subjects
        if not dan_sub:
            # print('initial dont have subject')
            dan_sub = title_sub  # list of subjects in title
        ini_subj.append(dan_sub)
    return ini_subj


def process_padding_last(data, parser, title_sub, m_data):
    ''' process padding subject with danmakus in different time scale
        Under Construction
        m_data: the whole dataset; if the padding need the initial part
    '''
    # context: [window] 10-15; most-frequent
    # danmaku: initial, middle, end;  danmaku list
    # different padding policy needed
    subjects = []
    danmaku = data.loc[:, 'Barrages_original']
    showing_time = data.loc[:, 'Showing_time']
    window_size = 5.0  # get most frequent from above 5 seconds; find the round() index; might be out-of-boundary
    for dan, dan_index in zip(danmaku, danmaku.index):
        dan_sub = find_NN(dan, parser)  # list of subjects
        if not dan_sub:
            # corresponding showing time: s_time; get the previous 5 seconds
            s_time = showing_time[dan_index] - window_size
            if s_time < 10.0:
                dan_sub = win_data(s_time, m_data, dan_index, parser, title_sub)
            else:
                dan_sub = win_data(s_time, data, dan_index, parser, title_sub)
        subjects.append(dan_sub)
    return subjects


def map_subjects(subjects: list, filter_dis=0.2):
    # mapping the subjects, filter the i,j in M
    wns = WordNetSimilarity()
    # enumerate pairing and calculate distances
    # [['中国人', '安乐死'], ['太阳', '很好']]
    pair = []
    # return the indexes pairing
    pair_idxs = []
    for index, value in enumerate(subjects):
        i = index + 1
        while i < len(subjects):
            # compare list : next list
            com_value = subjects[i]
            for v in value:
                for cv in com_value:
                    pair_distance = wns.monol_word_similarity(v, cv, 'cmn', 'wup')
                    # print(f'{v} -> {cv}:  {pair_distance}')
                    if pair_distance > filter_dis:
                        pair.append(pair_distance)
                        # pairing index: (row, column)
                        pair_idxs.append(([index, value.index(v)], [i, com_value.index(cv)]))
            i += 1

    return pair_idxs


def mappingsen(pair_ids:list):
    map_sens = []
    for tuples in pair_ids:
        # the first opinion index
        op1 = tuples[0][0]
        op2 = tuples[1][0]
        map_sens.append((op1, op2))
    # map_sens = list(set(map_sens))
    return map_sens


def mappingset(pair_ids: list, m, n):
    # for opinion m and opinion n; how many mapping sets do they have?
    # what are the pairing index in m and in n
    # pair_ids: list of tuple of lists:  ([100, 2], [102, 0])
    count = 0
    map_ids = []
    for tuples in pair_ids:
        # the first opinion index
        op1 = tuples[0][0]
        op2 = tuples[1][0]
        if op1 == m and op2 == n:
            i = tuples[0][1]
            j = tuples[1][1]
            map_id = (i, j)
            map_ids.append(map_id)
            count += 1
        elif op1 == n and op2 == m:
            i = tuples[1][1]
            j = tuples[0][1]
            map_id = (i, j)
            map_ids.append(map_id)
            count += 1
        else:
            pass

    return count, map_ids


def sur_logic(token_sentence, n_token, sub_id):
    '''
    surrounding words rule:
    Parameters
    ----------
    sentence: danmaku sentence
    n_token: number of surrounding words
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
        sur_words = token_sentence[sub_id: sub_id + n_token + 1]
    elif sub_id + n_token > len(token_sentence) and sub_id - n_token >= 0:
        sur_words = token_sentence[-n_token + sub_id: sub_id + 1]
    elif sub_id - n_token >= 0 and sub_id + n_token <= len(token_sentence):
        sur_words = token_sentence[-n_token + sub_id:sub_id + n_token + 1]
    elif sub_id - n_token < 0 and sub_id + n_token > len(token_sentence):
        sur_words = token_sentence
    return sur_words


def surwords(subject: list, i, per_dan, n_token):
    # return surrounding words for each subject in the sentence.
    # i: ith position in sentence1
    # per_dan: tokenized danmaku
    sur_words = []
    if subject[i] not in per_dan:
        sur_words.extend(subject[i])
        sur_words.extend(per_dan)
    else:
        sub_id = per_dan.index(subject[i])
        sur_words = sur_logic(per_dan, n_token, sub_id)
    return sur_words


def return_polarity(sur_words: list):
    ''' using polarity of surrounding words to define subjects '''
    # from polyglot.downloader import downloader
    # downloader.download("sentiment2.zh_Hant")
    surrounding_wd = ''.join(sur for sur in sur_words)
    text = Text(surrounding_wd)
    pol_list = []
    count = 0
    for w in text.words:
        try:
            w_po = w.polarity
            pol_list.append(w_po)
        except:
            count += 1
            pass
    return pol_list


def check_neg_pos(pol: list):
    # check the polarity is negative or positive
    neg = 0
    pos = 0
    for p in pol:
        if p == -1:
            neg += 1
        elif p == 1:
            pos += 1
        else:
            pass
    if neg % 2 == 0 and neg != 0:
        return 1
    elif neg % 2 == 1:
        return -1
    elif pos != 0:
        return 1
    else:
        return 0


def diff_po(pol1, pol2):
    # [0,0,0,1]  [0,-1,1,0]
    # check the negative or positive for the polarity list
    p_1 = check_neg_pos(pol1)
    p_2 = check_neg_pos(pol2)
    return abs(p_1 - p_2)


def op_distance(subjects, m, n, data, parser, pair_idxs):
    # return opinion distance
    # OD(O1, O2) = sum_enumerate(f()) / 2*len_enumeration()
    # map subjects between each danmaku, filter

    # pairing index in op1 and op2, [(i,j)]
    len_M, mapids = mappingset(pair_idxs, m, n)
    # m= 1 n= 0
    # [(0, 1), (1, 1)]
    # obj1: sentence1, subj:0; obj0: sentence 0, subj:1
    # obj1: sentence1, subj:1; obj0: sentence 0, subj:1
    pol_distances = 0
    # surround words -2, +2
    n_token = 2
    danmaku = data.loc[:, 'Barrages_original']
    token_sen_0 = list(parser.tokenize(danmaku[m]))
    token_sen_1 = list(parser.tokenize(danmaku[n]))
    subject_0 = subjects[m]
    subject_1 = subjects[n]

    for id in mapids:
        i = id[0]
        j = id[1]
        surword_0 = surwords(subject_0, i, token_sen_0, n_token)
        pol_0 = return_polarity(surword_0)

        surword_1 = surwords(subject_1, j, token_sen_1, n_token)
        pol_1 = return_polarity(surword_1)

        pol_distance = diff_po(pol_0, pol_1)
        pol_distances += pol_distance
    res = pol_distances / (2 * len_M)
    return res


def main():
    parser = CoreNLPDependencyParser(url='http://localhost:9001')
    title = '中国人为什么不能选择安乐死?'
    # parse, = parser.raw_parse(title)
    title_sub = find_NN(title, parser)

    # parse danmaku and extract subjects
    # using windows : surrounding polarity
    data = pd.read_csv('../temp/demo.csv')

    # get index of 1. INITIAL 2. middle 3. end
    # for now: the same padding;
    initial_time = 10.0  # what's the inital time duration?: initial 10 seconds
    start_idx = 0
    for showing_time in data['Showing_time']:
        if showing_time < initial_time:
            start_idx += 1

    # slice danmaku list: initial + last, get subjects:list of lists
    initial_dan = data.loc[:start_idx, 'Barrages_original']
    ini_subj = padding_initial(title_sub, initial_dan, parser)
    last_data = data[start_idx + 1:]
    # padding danmaku
    # processing padding on different timezone
    last_subjects = process_padding_last(last_data, parser, title_sub, data)
    subjects = ini_subj + last_subjects
    pair_idxs = map_subjects(subjects)

    # mapping sentence index
    map_sens = mappingsen(pair_idxs)

    # enumerate all of the danmaku and pairlying output opinion distances
    row_length = data.shape[0]  # how many rows
    count_zero_dis = 0  # how many distances are 0 between sentences?
    count_zero_dis1=0

    # save res into table:
    # first sentence; second sentence; opinion distance
    sentence_0_list = []
    sentence_1_list = []
    op_dis_list = []
    df = pd.DataFrame(columns=('first sentence', 'second sentence', 'op_distance'))
    with open('distance.txt', 'w')as f:
        import time
        start_t = time.time()
        for m in range(row_length):
            n = m + 1
            while n < row_length:
                if (m,n) in map_sens:
                    sentence_0_list.append(m)
                    sentence_1_list.append(n)
                    op_d = op_distance(subjects, m, n, data, parser, pair_idxs)
                    op_dis_list.append(op_d)
                    count_zero_dis1 += 1
                    f.write(f'the distance between danmaku {m} and danmaku {n} is: {op_d}\n')

                else:
                    sentence_0_list.append(m)
                    sentence_1_list.append(n)
                    f.write(f'the distance between danmaku {m} and danmaku {n} is: 0.0 \n')
                    op_dis_list.append(0.0)
                    count_zero_dis += 1

                n += 1
        end_t = time.time()
        print(f'it takes {end_t-start_t} to run 104 danmakus')
        print(f'total zero distance: {count_zero_dis}')
        print(f'total non-zero distance: {count_zero_dis1}')
        print(len(op_dis_list))
    df['first sentence'] = sentence_0_list
    df['second sentence'] = sentence_1_list
    df['op_distance'] = op_dis_list
    df.to_csv('distance_table.csv', index=False)

    # total: 104*103/2=5356
    # zero distance:


if __name__ == '__main__':
    main()