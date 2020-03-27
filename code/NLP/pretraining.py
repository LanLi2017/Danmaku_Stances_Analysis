import codecs
import time

import gensim
import jieba
import pandas as pd
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from Bert_Embedding.bert_embedding import BertEmbedding


def extract_text(file_path,column,output_path):
    df=pd.read_csv(file_path)
    extract_part=df[column]
    with open(output_path,'w')as f:
        for e in extract_part:
            f.write(e+'\n')


#jieba
def jieba_token(file_path,target_path):
    f=codecs.open(file_path,'r',encoding='utf8')
    target= codecs.open(target_path,'w',encoding='utf8')
    lineNum=1
    line=f.readline()
    # jieba stpp words
    jieba_stop_words=[
        '的','了','，','！','？','。','和','是',
        '都','而','及','与','或','一个','我们','你们','','那','他们','她们',
        '在',
    ]
    words=[]
    while line:
        print('----processing',lineNum,'article------')
        seg_list=jieba.cut(line, cut_all=False)
        per_word = [str(word) for word in seg_list if not str(word) in jieba_stop_words]
        words.append(per_word)
        line_seg=' '.join(w for w in per_word)
        target.writelines(line_seg)
        lineNum=lineNum+1
        line=f.readline()
    f.close()
    target.close()
    print(words)
    return words


def word2vect(wordvectors, doc):
    # word to vectors Chinese model
    word_vectors = gensim.models.KeyedVectors.load_word2vec_format(wordvectors)
    import logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # model=Word2Vec.load(w2v)
    vectors=[]
    count=0
    for sentence in doc:
        # embedding_vector=[]
        for token in sentence:
            try:
                embedding_vector = word_vectors.wv[token]
                # print(embedding_vector)
                vectors.append(embedding_vector)
            except:
                count+=1
                print(token, 'not found')
        # print(vectors)
    # vectors=[model[d.split(' ')] for d in danmaku_seg]
    # vectors.save("danmaku_vect.model")
    print(count)
    return vectors


def bert_embedding(doc):
    bert_embed_danmaku =[]
    bert_embedding = BertEmbedding()
    for sentence in doc:
        res = bert_embedding(sentence)
        bert_embed_danmaku.append(res)

    return bert_embed_danmaku

def main():
    filep="../combined_data/90976388/combined_90976388.csv"
    filep1 = "../combined_data/91101531/combined_91101531.csv"
    column = 'Barrages_original'
    # output_path='danmaku.txt'
    output_path1 = 'danmaku_91101531.txt'
    extract_text(filep1,column,output_path1)
    output_seg_path = 'danmaku_seg_remove_stop_91101531.txt'

    # list of lists : Chinese tokens after jieba, list of danmaku(sentences)/tokens
    doc = jieba_token(output_path1,output_seg_path)

    # after word embedding
    model = word2vect("chinese_L-12_H-768_A-12.zip", doc)
    # model = word2vect("wordvectors/sgns.merge.word.bz2", doc)
    print(model)
    # with open('danmaku_seg_remove_stop_91101531.txt','r')as f:
    #     danmaku_seg = [x.strip() for x in f.readlines()]
    # model = word2vect("wordvectors/sgns.merge.word.bz2",danmaku_seg)
    # print(type(model))
    X = np.array(model)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(X)

    # create a plot of the projection
    plt.figure(figsize=(16,10))
    plt.scatter(pca_result[:,0], pca_result[:,1], cmap='rainbow')
    plt.xlabel('First Principle Component')
    plt.ylabel('Second Principle Component')
    plt.savefig('pca_91101531.png')
    plt.show()


    # t-SNE
    time_start = time.time()
    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
    tsne_results = tsne.fit_transform(X)

    print(f't-SNE done! Time elapsed : {time.time()-time_start} seconds')

    plt.figure(figsize=(16,10))
    palette = sns.color_palette("bright", 10)
    sns.scatterplot(
        tsne_results[:,0],
        tsne_results[:,1],
        legend='full',
        palette=palette)
    # Y = TSNE(X, 2, 50, 30.0)
    # # plot the t-SNE output
    # fig, ax = plt.subplots()
    # ax.plot(Y[:,0],Y[:,1], 'o')
    # ax.set_title('Danmakus')
    # ax.set_yticklabels([]) # hide ticks
    # ax.set_xticklabels([]) #hide ticks
    plt.savefig('t-sne_91101531.png')
    plt.show()


if __name__=='__main__':
    main()