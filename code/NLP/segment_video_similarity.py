import os
from pprint import pprint

import matplotlib
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from scipy.spatial import distance
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from sklearn.metrics import pairwise_distances
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


def extract_text(file_path,column,data_p):
    df = pd.read_csv(file_path)
    extract_part = df[column]
    extract_part.to_csv(data_p, index=False)
    return extract_part


def load_np(model_p):
    data = np.load(model_p)
    return data


def chunks(lst, n):
    '''Yield successive n-sized chunks from lst.'''
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


def cal_distance(v):
    dis = distance.pdist(v, metric='cosine')
    return dis


def vis_pca(V):
    pca = PCA(n_components=2)
    feature_pca = pca.fit_transform(V)
    plt.scatter(feature_pca[:, 0], feature_pca[:, 1])
    plt.savefig('figure/demo_pca_sen_simi.png')
    plt.show()


def vis_tsne(V):
    tsne = TSNE(n_components=2).fit_transform(V)
    plt.scatter(tsne[:, 0], tsne[:, 1])
    plt.savefig('figure/demo_tsne_sen_simi.png')
    plt.show()


def istest(data):
    # test
    V1 = data[9]

    # reduce dimension and vis
    vis_tsne(V1)
    vis_pca(V1)

    # VISUALIZE distance distribution
    dis_metric = cal_distance(V1)
    pprint(dis_metric.size)
    dismetric = dis_metric.tolist()

    max_dis = max(dismetric)
    min_dis = min(dismetric)

    print(f'max distance : {max_dis}')
    print(f'min distance: {min_dis}')

    # casually set up threshold
    threshold = 0.5
    count = 0
    dis_count = 0
    for d in dismetric:
        if d < threshold:
            count += 1
        else:
            dis_count += 1

    print(f'count: {count}')
    print(f'discount: {dis_count}')

    plt.hist(dismetric, density=True, bins=30)
    plt.ylabel('Cosine Similarity')
    plt.xlabel('Data')
    plt.savefig('figure/sen_similarity.png')


def clustering_window(vector_dan, labels, no_chunks):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(vector_dan)
    print(no_chunks)

    dbscan = DBSCAN(eps=0.123, min_samples=2, metric='cosine')
    clusters = dbscan.fit_predict(X_scaled)
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    # pprint(clusters.labels_)
    plt.figure(figsize=(30, 10))
    plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap="plasma")
    for i,txt in enumerate(labels):
        plt.annotate(txt, (X_scaled[:,0][i], X_scaled[:,1][i]))
    plt.xlabel("Feature 0")
    plt.ylabel("Feature 1")
    plt.savefig(f'figure/window_subplot/cluster_win{no_chunks}.png')
    # plt.show()
    return clusters


def main():
    filep = "../combined_data/61437877/combined_61437877.csv"
    column = ['Barrages_original','Showing_time']
    # output_path='danmaku.txt'
    output_path = 'data/61437877'
    file_n = '61437877_dan.csv'
    data_p = output_path+'/'+file_n
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    n = 200
    # pandas dataframe : ['danmaku','converted_time']
    df = extract_text(filep, column, data_p)
    danmaku_label = list( df['Barrages_original'])
    # for label the points
    dan_labels = [danmaku_label[i:i + n] for i in range(0, len(danmaku_label), n)]

    # chunk danmaku
    # split_danmaku = [danmaku_lis[i:i + n] for i in range(0, len(danmaku_lis), n)]

    # load danmaku model .numpy file
    data = load_np('model/Danmaku_model1.npy')
    # last layer
    data = data[-1, :, :]

    d = data.tolist()
    # print(d[1])

    # split chunk, size n = 100/
    split_d = [d[i:i + n] for i in range(0, len(d), n)]

   # test
   #  test(split_d)

    # DBSCAN : Density-based spatial clustering of applications with noise
    # pprint(dan_labels[0])
    # clustering_window(split_d[0], dan_labels[0])

    for i in range(len(split_d)):
        clustering_window(split_d[i], dan_labels[i], i)
    # for vector_dan in split_d:
    #     print(len(vector_dan))
    #     clustering_window(vector_dan, dan_labels[0])
        # distance pairingly
        # dis_metric = cal_distance(vector_dan)
        # label: positive / neural / negative
    #     cluster_dan = DBSCAN(min_samples=3, metric='precomputed').fit(distance.pdist(vector_dan, metric='cosine'))


if __name__=='__main__':
    main()



