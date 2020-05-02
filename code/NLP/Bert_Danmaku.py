import codecs
import time
# from bert_serving.client import BertClient
import gensim
import jieba
import pandas as pd
# from bert_serving.server import get_args_parser, BertServer
import seaborn as sns
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#
from sklearn.metrics.pairwise import cosine_similarity


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
        words.extend(per_word)
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


# def bert_embed(doc):
#     bert_embed_danmaku =[]
    # ctx =mx.gpu(0)
    # print("begin bert embedding")
    # bert_embedding = BertEmbedding(model='bert_12_768_12')
    # for sentence in doc:
    #     while True:
    #         try:
    #             sentence.remove('\n')
    #             print(sentence)
    #             res = bert_embedding(sentence)
    #             bert_embed_danmaku.append(res)
    #         except ValueError:
    #             pass
    # sentences = doc.split('\n')
    # print(sentences)
    # result = bert_embedding(sentences)
    # first_sen = result[0]
    # print(first_sen[0])
    # print(len(first_sen[0]))
    # return result


def bert_consine_simi(window_size = 5, threshold =0.9, first_sentence_id=0, sencond_sentence_id=1):
    # window_size: internal length


    pass


# def main_bert_embedding():
#     output_seg_path = 'danmaku_seg_remove_stop_91101531.txt'
#     output_path1 = 'danmaku_91101531.txt'
#     # list of lists : Chinese tokens after jieba, list of danmaku(sentences)/tokens
#     doc = jieba_token(output_path1, output_seg_path)
#     str_doc = ''.join(doc)
#     model = bert_embed(str_doc)
#     print("finish bert embedding")
#     print(type(model))
#     print(model)
#     # X = np.array(model)
#     pca = PCA(n_components=2)
#     pca_result = pca.fit_transform(model)
#
#     # create a plot of the projection
#     plt.figure(figsize=(16, 10))
#     plt.scatter(pca_result[:, 0], pca_result[:, 1], cmap='rainbow')
#     plt.xlabel('First Principle Component')
#     plt.ylabel('Second Principle Component')
#     plt.savefig('pca_91101531.png')
#     plt.show()


def main1():
    filep1 = "../combined_data/61437877/combined_61437877.csv"
    column = 'Barrages_original'
    # output_path='danmaku.txt'
    output_path1 = 'data/danmaku_61437877.txt'
    extract_text(filep1,column,output_path1)
    output_seg_path = 'data/danmaku_seg_remove_stop_61437877.txt'

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
    plt.savefig('pca_61437877.png')
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
    plt.savefig('t-sne_61437877.png')
    plt.show()


def bert_service():
    # bert-serving-start -pooling_strategy REDUCE_MAX -cpu -max_batch_size 16 -model_dir chinese_L-12_H-768_A-12

    # bc = BertClient(ip="localhost")
    # sentence0 = '我确实不太爱你'
    # sentence1 = '我真不是不喜欢你'
    # sentence2 = '我不喜欢你'
    # sentences = bc.encode([sentence0,sentence1,sentence2])
    # cos_s = cosine_similarity(sentences[0][:].reshape(1,-1), sentences[1][:].reshape(1,-1))
    # print(cos_s)
    # cos_s1 = cosine_similarity(sentences[0].reshape(1,-1), sentences[2].reshape(1,-1))
    # cos_s2 = cosine_similarity(sentences[1][:].reshape(1,-1), sentences[2][:].reshape(1,-1))
    # print(sentences[1])
    # print(cos_s1>cos_s2)
    # ==========================================================================
    # list of lists : Chinese tokens after jieba, list of danmaku(sentences)/tokens
    output = 'data/danmaku_61437877.txt'
    with open(output, 'r', encoding='utf-8')as f:
        subset_text = [line.strip('\n') for line in f]

    common = [
        '-model_dir', 'chinese_L-12_H-768_A-12/',
        '-num_worker', '2',
        '-max_seq_len', '20',
        # '-client_batch_size', '2048',
        '-max_batch_size', '256',
        # '-num_client', '1',
        '-pooling_strategy', 'REDUCE_MEAN',
        '-pooling_layer', '-2',
        '-gpu_memory_fraction', '0.2',
    ]
    args = get_args_parser().parse_args(common)
    subset_vec_all_layers = []
    for pool_layer in range(1, 13):
        setattr(args, 'pooling_layer', [-pool_layer])
        server = BertServer(args)
        server.start()
        print('wait until server is ready...')
        time.sleep(20)
        print('encoding...')
        bc = BertClient(ip='localhost')
        subset_vec_all_layers.append(bc.encode(subset_text))
        bc.close()
        server.close()
        print('done at layer -%d' % pool_layer)

    # save bert vectors
    stacked_subset_vec_all_layers = np.stack(subset_vec_all_layers)
    np.save('model/Danmaku_model1',stacked_subset_vec_all_layers)

    # load bert vectors and labels
    subset_vec_all_layers = np.load('model/Danmaku_model1.npy')
    return subset_vec_all_layers


def vis(embed,vis_alg='pca',pool_alg='REDUCE_MEAN'):
    plt.ioff()
    fig = plt.figure()
    plt.rcParams['figure.figsize'] = [9, 11]
    for idx, ebd in enumerate(embed):
        ax = plt.subplot(3, 4, idx+1)
        vis_x = ebd[:, 0]
        vis_y = ebd[:, 1]
        plt.scatter(vis_x, vis_y,cmap='rainbow', alpha=0.7, s=2)
        ax.set_title(f'pool_layer=-{idx+1}')
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1, right=0.95, top=0.9)
    # fig.suptitle(f'{vis_alg} visualization of BERT layers using "bert-as-service"\n (-pool_strategy={pool_alg})')
    plt.savefig('figure/bert_pca_model1.png',bbox_inches='tight')
    plt.show()
    # plt.show()


def main_vis():
    subset_vec_p = 'model/Danmaku_model1.npy'
    # load bert vectors and labels
    subset_vec_all_layers = np.load(subset_vec_p)

    pca_embed = [PCA(n_components=3).fit_transform(v) for v in subset_vec_all_layers]
    vis(pca_embed)
    kmeans = KMeans(n_clusters=3, random_state=0)
    # X_clusters = [kmeans.fit_predict(x) for x in pca_embed]
    Label_color = {
        0: 'r',
        1: 'g',
        2: 'b',
    }
    # label_c = [Label_color[l] for l in X_clusters]
    fig = plt.figure()
    plt.rcParams['figure.figsize'] = [30, 7]
    for idx, ebd in enumerate(pca_embed):
        ax = plt.subplot(3, 4, idx + 1)
        X_clusters = kmeans.fit_predict(ebd)
        label_c = [Label_color[l] for l in X_clusters]
        vis_x = ebd[:, 0]
        vis_y = ebd[:, 1]
        plt.scatter(vis_x, vis_y, c = label_c, alpha=0.7, s=2)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1, right=0.95, top=0.9)
    # fig.suptitle(f'K-means visualization of BERT \nlayers using "bert-as-service" \n(-pool_strategy=REDUCE_MEAN)',
    #              fontsize=14)
    plt.savefig('figure/kmeans-pca-bert_model1.png',bbox_inches='tight')
    plt.show()


def main():
    filep1 = "../combined_data/61437877/combined_61437877.csv"
    column = 'Barrages_original'
    # output_path='danmaku.txt'
    output_path1 = 'data/danmaku_61437877.txt'
    extract_text(filep1, column, output_path1)
    bert_service()


if __name__ == '__main__':
    # main()
    main_vis()
