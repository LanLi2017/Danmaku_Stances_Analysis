from gensim.models import KeyedVectors
from gensim.test.utils import datapath

wordvectors ='wordvectors/sgns.weibo.word.bz2'
word_vectors = KeyedVectors.load_word2vec_format(wordvectors, binary=True)
print(word_vectors)
vocab = word_vectors.vocab

# import os
# from fnmatch import fnmatch
# av_id=90976388
# root=f'../../data/{av_id}'
# extension='*.csv'
# path_list=[]
# for path,subdirs,files in os.walk(root):
#     for name in files:
#         if fnmatch(name,extension):
#             path_list.append(os.path.join(path,name))
# print(path_list)
# import gensim
# #
# # with open('danmaku_seg.txt','r')as f:
# #     data=f.readlines()
# #     for d in data:
# #         print(d)
# #     print(type(data))
# with open('danmaku_seg_part.txt', 'r')as f:
#     danmaku_seg = [x.strip() for x in f.readlines()]
# print(danmaku_seg)
#
# model = gensim.models.KeyedVectors.load_word2vec_format("wordvectors/sgns.weibo.word.bz2")
#
# # model=Word2Vec.load(w2v)
# vectors=[]
# for d in danmaku_seg:
#     sentence=d.split(' ')
#     print(sentence)
#     embedding_vector=[]
#     for s in sentence:
#         try:
#             embedding_vector=model.wv[s]
#             print(embedding_vector)
#             print('----------------')
#         except:
#             print(s, 'not found')
#     vectors.append(embedding_vector)
#     # print(vectors)
#
