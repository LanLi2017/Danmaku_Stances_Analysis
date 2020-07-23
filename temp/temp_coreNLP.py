import re
from collections import defaultdict, Counter
from pprint import pprint

from nltk import CoreNLPParser, CoreNLPDependencyParser, Tree
from sematch.semantic.similarity import WordNetSimilarity
import pandas as pd
from polyglot.text import Text


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
        parse, = parser.raw_parse(s)
        for governor, dep, dependent in parse.triples():
            if dep == 'nsubj':
                print(governor, dependent)
                print(governor[0])
                subj.append(dependent[0])
                subj.append(governor[0])
            if dep == 'dobj':
                print(dependent)
                subj.append(dependent[0])
    print(subj)
    return subj


def map_subjects(subjects: list, filter_dis=0.2):
    wns = WordNetSimilarity()
    # enumerate pairing and calculate distances
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
                    print(f'{v} -> {cv}:  {pair_distance}')
                    if pair_distance > filter_dis:
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
    [0, 4, 9]
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
        sur_words = token_sentence[sub_id: sub_id + n_token + 1]
    elif sub_id + n_token > len(token_sentence) and sub_id - n_token >= 0:
        sur_words = token_sentence[-n_token + sub_id: sub_id + 1]
    elif sub_id - n_token >= 0 and sub_id + n_token <= len(token_sentence):
        sur_words = token_sentence[-n_token + sub_id:sub_id + n_token + 1]
    elif sub_id - n_token < 0 and sub_id + n_token > len(token_sentence):
        sur_words = token_sentence
    return sur_words


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
            subjects.append(value[0])
    elif 0 < c_size < 3:
        for value in c.most_common(c_size):
            subjects.append(value[0])
    elif c_size == 0:
        subjects.append(title_sub)
    return subjects


def process_padding(data, parser, title_sub, n_token):
    ''' process padding subject with danmakus in different time scale
        Under Construction
    '''
    # context: [window] 10-15; most-frequent
    # danmaku: initial, middle, end;  danmaku list
    # different padding policy needed
    subjects = []
    sur_words = []
    danmaku = data.loc[:, 'Barrages_original']
    showing_time = data.loc[:, 'Showing_time']
    window_size = 5.0  # get most frequent from above 5 seconds
    for dan, dan_index in zip(danmaku, danmaku.index):
        dan_sub = find_NN(dan, parser)  # list of subjects
        token_sentence = list(parser.tokenize(dan))
        if not dan_sub:
            # corresponding showing time: s_time; get the previous 5 seconds
            s_time = showing_time[dan_index] - window_size
            time_index = data.index[data['Showing_time'] == s_time].tolist()[0]
            # using the most frequent subjects to pad
            dan_sub = most_freq(data[time_index:dan_index], parser, title_sub)
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


def padding_initial(title_sub, danmaku, parser, n_token):
    # padding the initial danmaku list with title subjects
    ini_subj = []
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
        ini_subj.append(dan_sub)

    return ini_subj


def main():
    parser = CoreNLPDependencyParser(url='http://localhost:9001')
    title = '中国人为什么不能选择安乐死?'
    # parse, = parser.raw_parse(title)
    title_sub = find_NN(title, parser)
    # tokenize
    title_token = list(parser.tokenize(title))
    # print(title_token)

    # parse danmaku and extract subjects
    # using windows : surrounding polarity
    data = pd.read_csv('demo.csv')
    danmaku_list = data.loc[:, 'Barrages_original']

    # get index of 1. INITIAL 2. middle 3. end
    # for now: the same padding;
    initial_time = 10.0  # what's the inital time duration?: initial 10 seconds
    start_idx = 0
    for showing_time in data['Showing_time']:
        if showing_time < initial_time:
            start_idx += 1

    # slice danmaku list
    initial_dan = data.loc[:start_idx, 'Barrages_original']

    # end_dan = data.loc[mid_idx:, 'Barrages_original']
    last_dan = data.loc[start_idx + 1:, 'Barrages_original']
    last_data = data[start_idx + 1:]
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
    subjects = process_padding(last_data, parser, title_sub, token)[0]
    sur_words = process_padding(last_data, parser, title_sub, token)[1]

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


def main_test1():
    parser = CoreNLPDependencyParser(url='http://localhost:9001')
    title = '请各位记住，口罩为了方便辨认正反，外部颜色不定，内部一定是白色。'
    # tit = re.split(r'\W+', title)
    res = list(parser.tokenize(title))
    print(res)
    # print(parse.to_conll(4))
    # print(type(parse.to_conll(4)))
    # print(parse)
    # res = parser.raw_parse(title)
    # print(res)
    # pprint(next(res).nodes)
    # print(iter(res))
    # pprint(next(res).tree())
    # print(parse.tree())
    # sub = []
    # for t in tit:
    #     print(t)
    #     parse, = parser.raw_parse(t)
    #     print(parse.to_conll(4))
    #     for governor, dep, dependent in parse.triples():
    #         if dep == 'nsubj':
    #             print(governor, dependent)
    #             print(governor[0])
    #             sub.append(governor[0])
    #             sub.append(dependent[0])
    #         if dep == 'dobj':
    #             print(dependent)
    #             sub.append(dependent[0])
    # print(sub)
    # print(governor, dep, dependent)


def main_test2():
    data = pd.read_csv('demo.csv')
    danmaku = data.loc[:, 'Showing_time']
    pprint(danmaku.index)
    print(data[:5])
    print(danmaku[5])
    # for dan, dan_index in zip(danmaku, danmaku.index):
    #     print(dan)
    #     print(dan_index)


if __name__ == '__main__':
    main_test2()
    # main()
    # main_test()
    # main_test1()
