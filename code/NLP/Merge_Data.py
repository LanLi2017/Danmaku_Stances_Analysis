import csv
import glob
import os

import jieba
# tokenization

# word2vec
# 90976388

import jieba
import pandas as pd
from fnmatch import fnmatch


def walk_danmaku_csv(av_id):
    root = f'../../data/{av_id}'
    pattern = '*.csv'
    res_path=[]
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name,pattern):
                res_path.append(os.path.join(path,name))

    return res_path


def composed_csv(input_path,output_path):
    # combine all files in the list
    # deduplicate the same danmaku from same time
    # combined_csv= pd.concat([pd.read_csv(p) for p in input_path],ignore_index=True)
                    # .drop_duplicates(subset='Converted_time', keep=False)
    dfs=[]
    for p in input_path:
        print(p)
        df=pd.read_csv(p)
        dfs.append(df)
    # export to csv
    frame=pd.concat(dfs,axis=0,ignore_index=True).sort_values('Showing_time')
    frame = frame.drop(['Row_no'],axis=1)
    # frame.to_csv(f'../combined_data/{90976388}/combined1_{90976388}.csv',index=False, encoding='utf-8')
    frame.drop_duplicates(inplace=True)
    # # print(frame['Converted_time'])
    frame.to_csv(output_path,index=False, encoding='utf-8')


def main():
    # av_id=90976388
    av_id=input('input the av id:')
    p=walk_danmaku_csv(av_id)

    os.makedirs(f"../combined_data/{av_id}", exist_ok=True)
    output_path=f'../combined_data/{av_id}/combined_{av_id}.csv'
    composed_csv(p,output_path)


if __name__=='__main__':
    main()
