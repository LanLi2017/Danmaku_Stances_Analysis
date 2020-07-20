from sematch.semantic.similarity import WordNetSimilarity
# import jieba
# import synonyms
# import jieba.posseg as pseg

wns = WordNetSimilarity()
wns.monol_word_similarity('狗', '猫', 'cmn', 'wup')
# print(wns.word_similarity('dog', 'cat', 'li'))
print(wns.monol_word_similarity('忧患', '安乐', 'cmn', 'wup'))
print(wns.monol_word_similarity('忧患', '灾难', 'cmn', 'wup'))
print(wns.monol_word_similarity('忧患', '担忧', 'cmn', 'wup'))
print(wns.monol_word_similarity('电脑', '键盘', 'cmn', 'wup'))
print(wns.monol_word_similarity('电脑', '电脑', 'cmn', 'wup'))
print(wns.monol_word_similarity('国家', '国家', 'cmn', 'wup'))
#
# def parse_token(data):
#     # words = []
#     # for d in data:
#     #     # jieba.enable_paddle()
#     seg_data = pseg.cut(data, use_paddle=True) #default
#     # per_word = [str(word) for word in seg_data if not str(word) in jieba_sp_words]
#     # for word, flag in seg_data:
#     #     print(f'{word}, {flag}')
#     # words.append(seg_data)
#     return seg_data
#
#
# def word_flag(sentence:list):
#     for word,flag in sentence:
#         return word,flag
#
#
# with open('demo.csv','r')as f:
#     # data = f.read().splitlines()
#     data = [line.rstrip() for line in f]
#
#
# # n: 普通名词, nr:人名 ,ns:地名,  nz:其他专名, nt:机构名, nw:作品名
# # vn: 名动词,
# # f: 方位名词, s: 处所名词, PER: 人名, LOC: 地名, ORG: 机构名
# # give weights and aggret
# # 需要提取的是否应该根据TITLE
# title = '中国人为什么不能选择安乐死?'
# title_token = parse_token(title)
# title_flag = []
# for t_word,t_flag in title_token:
#     print(f'{t_word}, the flag is {t_flag}')
#     title_flag.append(t_flag)
# print(title_flag)  # ['ns', 'n', 'r', 'v', 'v', 'nr', 'x']
#
#
# # danmaku demo
# words = []
# for d in data:
#     print(d)
#     words.append(parse_token(d))
# print(words)
#
# subjects = []
# for w in words:
#     subject = []
#     # res = word_flag(pairs)
#     for word,flag in w:
#         if flag in title_flag:
#             print(f'{word}, and flag is {flag}')
#             subject.append(word)
#     subjects.append(subject)
# #         print(word)
# #         print(flag)
# #         print(title_flag)
# #         if flag in title_flag:
# #             print(flag)
# #             subject.append(res[0])
# #         subjects.append(subject)
# print(subjects)
#
# '''before filter: # [[], ['人口', '大量'], ['安乐死', '病', '子女', '时候', '百草']]'''
# '''after pairing with title:
# [['，', '讨论', '完毕'],
#  ['人口', '会', '大量', '减少'],
#  ['"', '支持', '安乐死', ',', '他', '病', ',', '没', '子女', ',', '时候', '他', '自己', '百草', '枯', '"']]
#  '''
#
#
# # special symbols
# # jieba_sp_words=[
# #      '"'
# #     ]
#
#
#
# # subjects = []
# # for w in words:
# #     subject = []
# #     for word,flag in w:
# #         print(f'{word}, {flag}')
# #         if flag == 'n' or flag=='nr':
# #             subject.append(word)
# #         else:
# #             pass
# #     subjects.append(subject)
#
# # print(subjects)
#
#
# #     print(' '.join(per_word) )
# #     words.append(per_word)
# # print(words)
# #
# # sen1 = '旗帜引领方向'
# # sen2 = '旗帜决定命运'
# # r = synonyms.compare(sen1, sen2, seg=True)
# # print(r)
#
