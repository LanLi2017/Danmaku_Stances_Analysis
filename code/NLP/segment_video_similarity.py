import os
from collections import Counter
from pprint import pprint
from typing import List

import matplotlib
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from scipy.spatial import distance
from sklearn import metrics
from sklearn.cluster import DBSCAN, KMeans
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
    plt.savefig('figure/55573492/demo_pca_sen_simi.png')
    plt.show()


def vis_tsne(V):
    tsne = TSNE(n_components=2).fit_transform(V)
    plt.scatter(tsne[:, 0], tsne[:, 1])
    plt.savefig('figure/55573492/demo_tsne_sen_simi.png')
    plt.show()


def isdistribute(data):
    plt.hist(data, density=True, bins=30)
    plt.ylabel('frequency')
    plt.xlabel('showing time')
    plt.savefig('figure/55573492/time_distribute.png')


def plot_simi_pairs(data,idx):
    # test
    # reduce dimension and vis
    # vis_tsne(V1)
    # vis_pca(V1)

    # VISUALIZE distance distribution
    # idx = 4
    dis_metric = cal_distance(data)
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

    # ax.set_title(f'window{i}={i + 1}')
    plt.hist(dismetric,bins=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    plt.ylabel('Counts')
    plt.xlabel('Cosine Similarity')
    plt.savefig(f'figure/55573492/simi_pairs1/simi{idx}.png')


def kmeans_window(vector_dan, labels,no_chunks):
    X_scaled = PCA(n_components=3).fit_transform(vector_dan)
    kmeans = KMeans(n_clusters=3, random_state=0)
    Label_color = {
        0: 'r',
        1: 'g',
        2: 'b',
    }
    clusters = kmeans.fit_predict(X_scaled)
    label_c = [Label_color[l] for l in clusters]
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    # pprint(clusters.labels_)
    plt.figure(figsize=(30, 10))
    plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=label_c)

    # annotation with text
    # for i, txt in enumerate(labels):
    #     plt.annotate(txt, (X_scaled[:, 0][i], X_scaled[:, 1][i]))
    plt.xlabel("Feature 0")
    plt.ylabel("Feature 1")
    # plt.savefig(f'figure/55573492/kmeans/counts_subplot_200/cluster_win{no_chunks}.png')

    # no annotations for the nodes
    plt.savefig(f'figure/55573492/kmeans/F_counts_subplot_200/cluster_win{no_chunks}.png')
    return clusters


def clustering_window(vector_dan, labels, no_chunks):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(vector_dan)

    dbscan = DBSCAN(eps=0.123, min_samples=2, metric='cosine')
    clusters = dbscan.fit_predict(X_scaled)
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    # pprint(clusters.labels_)
    plt.figure(figsize=(30, 10))
    plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap="plasma")

    # annotate
    # for i,txt in enumerate(labels):
    #     plt.annotate(txt, (X_scaled[:,0][i], X_scaled[:,1][i]))
    plt.xlabel("Feature 0")
    plt.ylabel("Feature 1")

    # n = 200
    # plt.savefig(f'figure/55573492/DBSCAN/time_subplot_50/cluster_win{no_chunks}.png')

    # n = 300
    # plt.savefig(f'figure/window_subplot1/cluster_win{no_chunks}.png')

    # n = 400
    # plt.savefig(f'figure/55573492/window_subplot_400/cluster_win{no_chunks}.png')

    # n = 50
    # plt.savefig(f'figure/55573492/window_time_50/cluster_win{no_chunks}.png')

    # no annotation
    plt.savefig(f'figure/55573492/DBSCAN/F_time_subplot_50/cluster_win{no_chunks}.png')
    plt.show()
    return clusters


def slice_list_by_idx_list(data:list, idx_list:list) -> List[list]:
    return [
        data[start+1: end+1]
        for start, end in zip(
            [-1] + idx_list,
            idx_list + [len(data) - 1],
        )
        if start < end
    ]


def crt_danmakulist():
    # create danmaku + showingtime
    filep = "../combined_data/61437877/combined_61437877.csv"

    column = ['Barrages_original', 'Showing_time']
    # output_path='danmaku.txt'
    output_path = 'data/61437877'
    file_n = '61437877_dan.csv'
    data_p = output_path + '/' + file_n
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    df = extract_text(filep, column, data_p)
    return df


def main(n):
    # chunk by danmaku counts
    # df = crt_danmakulist()
    df = pd.read_csv("data/55573492/55573492_dan.csv")
    danmaku_label = list( df['Barrages_original'])

    # for label the points
    dan_labels = [danmaku_label[i:i + n] for i in range(0, len(danmaku_label), n)]

    # chunk danmaku
    # split_danmaku = [danmaku_lis[i:i + n] for i in range(0, len(danmaku_lis), n)]

    # load danmaku model .numpy file
    data = load_np('model/55573492/Danmaku_model.npy')
    # last layer
    data = data[-1, 1:, 1:]

    d = data.tolist()
    # print(d[1])

    # split chunk, size n = 100/
    split_d = [d[i:i + n] for i in range(0, len(d), n)]

    # similarity distribution
    for i in range(len(split_d)):
        plot_simi_pairs(split_d[i],i)
    # plot_simi_pairs(split_d)

    # k-means clustering
    # for i in range(len(split_d)):
        # clustering_window(split_d[i], dan_labels[i], i)
        # kmeans_window(split_d[i],dan_labels[i],i)


def main1():
    # 2-10 seconds
    # showing time distribute
    # path = 'data/61437877/61437877_dan.csv'
    path = 'data/55573492/55573492_dan.csv'
    # data = extract_text(path,'Showing_time','data/61437877/61437877_time.csv')

    data = extract_text(path, 'Showing_time', 'data/55573492/55573492_time.csv')
    isdistribute(data)


def main2(n):
    # chunk by showing time: 50
    # file_p = 'data/61437877/61437877_dan.csv'
    # "data/55573492/55573492_dan.csv"
    file_p = 'data/55573492/55573492_dan.csv'
    data = pd.read_csv(file_p)

    # add new column

    data['timedel'] = data['Showing_time'] // n

    # data = data.groupby(['timedel']).indices
    data = data.groupby(['timedel']).apply(lambda x: x.index.tolist())
    pprint(data[0][-1])
    idx = []
    for d in data:
        idx.append(d[-1])

    # [292, 440, 608, 760, 886, 1063]
    # df = crt_danmakulist()
    df = pd.read_csv("data/55573492/55573492_dan.csv")
    danmaku_label = list( df['Barrages_original'])

    # for label the points
    dan_labels = slice_list_by_idx_list(danmaku_label, idx)

    # chunk danmaku
    # split_danmaku = [danmaku_lis[i:i + n] for i in range(0, len(danmaku_lis), n)]

    # load danmaku model .numpy file
    data = load_np('model/55573492/Danmaku_model.npy')
    # last layer
    data = data[-1, 1:, 1:]

    d = data.tolist()

    # print(d[1])

    # split chunk, size n = 100/
    split_d = slice_list_by_idx_list(d, idx)

    # test
    # istest(split_d)

    # DBSCAN : Density-based spatial clustering of applications with noise
    # pprint(dan_labels[0])
    # clustering_window(split_d[0], dan_labels[0])

    for i in range(len(split_d)):
        clustering_window(split_d[i], dan_labels[i], i)
    # n = 50
    # main(n)


if __name__=='__main__':
    # main(200)
    main2(50)
    # main2(50) time


