# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 17:38:47 2017

@author: qiu
"""

import os
import io

from surprise import KNNBaseline, Reader
from surprise import Dataset

import pickle as pickle
# 重建歌单id到歌单名的映射字典
r = open("popular_playlist.pkl","rb")
id_name_dic = pickle.load(r)
print("加载歌单id到歌单名的映射字典完成...")
id_name_dic

# 重建歌单名到歌单id的映射字典
name_id_dic = {}
for playlist_id in id_name_dic:
    name_id_dic[id_name_dic[playlist_id]] = playlist_id
print("加载歌单名到歌单id的映射字典完成...")

file_path = os.path.expanduser('./popular_music_suprise_format.txt')
#### 指定文件格式# 指定文件格式：歌单id、歌曲id、评分和时间戳
reader = Reader(line_format='user item rating timestamp', sep=',')
#### 从文件读取数据
music_data = Dataset.load_from_file(file_path, reader=reader)
#### 计算歌曲和歌曲之间的相似度
print("构建数据集...")
trainset = music_data.build_full_trainset()
#sim_options = {'name': 'pearson_baseline', 'user_based': False}
trainset

print("开始训练模型...")
sim_options = {'user_based': True}
#利用KNNBaseline进行预测
algo = KNNBaseline(sim_options=sim_options)
algo.train(trainset)

current_playlist = list(name_id_dic.keys())[39]
print("歌单名称", current_playlist)

# 取出近邻
# 利用歌单名到歌单id的映射矩阵，找到歌单名第39+1个歌单所对应的id
playlist_id = name_id_dic[current_playlist]
print("歌单id", playlist_id)
# 利用trainset.to_inner_uid函数找到歌单id所对应的内部id
playlist_inner_id = algo.trainset.to_inner_uid(playlist_id)
print("内部id", playlist_inner_id)
#algo.get_neighbors 利用内部id和.get_neighbors函数得到最近邻的10个歌单的内部id
playlist_neighbors = algo.get_neighbors(playlist_inner_id, k=10)

#利用algo.trainset.to_raw_uid将10个歌单的内部id逐条映射回歌单id
playlist_neighbors_raw_uid = (algo.trainset.to_raw_uid(inner_id)
                       for inner_id in playlist_neighbors)
#利用id_name_dic[playlist_id]，找到歌单id对应的歌单名
playlist_neighbors = (id_name_dic[playlist_id]
                       for playlist_id in playlist_neighbors_raw_uid)

print()
print("和歌单 《", current_playlist, "》 最接近的10个歌单为：\n")
for playlist in playlist_neighbors:
    print(playlist, algo.trainset.to_inner_uid(name_id_dic[playlist]))
    
import pickle as pickle
# 重建歌曲id到歌曲名的映射字典
song_id_name_dic = pickle.load(open("popular_song.pkl","rb"))
song_id_rating_dic = pickle.load(open("popular_song_rating.pkl","rb"))
print("加载歌曲id到歌曲名的映射字典完成...")
print("加载歌曲id到评分的映射字典完成...")
# 重建歌曲名到歌曲id的映射字典
print(song_id_rating_dic[song_id])
for song_id in song_id_name_dic:
    song_name_id_dic[song_id_name_dic[song_id]] = song_id
    print(song_id_rating_dic[song_id])
print("加载歌曲名到歌曲id的映射字典完成...")

#内部编码的4号用户
user_inner_id = 4
#获取用户内部id为4的对应的商品列表的内部id和评分
user_rating = trainset.ur[user_inner_id]
print(user_rating)
#基于前面训练的模型algo，对用户(内部id为4)的所有歌曲打分进行预测，
for song,rui in user_rating:
    #print(song,rui)
    #print(algo.trainset.to_raw_uid(song))
    #print (song_id_rating_dic[algo.trainset.to_raw_uid(song)])
    #print(song_name_id_dic[algo.trainset.to_raw_uid(song)])
    print(algo.predict(user_inner_id, song, r_ui=rui), song_id_name_dic[algo.trainset.to_raw_iid(song)])
    
import surprise
surprise.dump.dump('./recommendation.model', algo=algo)
# 可以用下面的方式载入
algo = surprise.dump.load('./recommendation.model')

import os
from surprise import Reader, Dataset
# 指定文件路径
file_path = os.path.expanduser('./popular_music_suprise_format.txt')
# 指定文件格式:# 指定文件格式：歌单id、歌曲id、评分和时间戳
reader = Reader(line_format='user item rating timestamp', sep=',')
# 从文件读取数据
music_data = Dataset.load_from_file(file_path, reader=reader)
# 分成5折
music_data.split(n_folds=5)

### 使用NormalPredictor
from surprise import NormalPredictor, evaluate
algo = NormalPredictor()
perf = evaluate(algo, music_data, measures=['RMSE', 'MAE'])

### 使用BaselineOnly
from surprise import BaselineOnly, evaluate
algo = BaselineOnly()
perf = evaluate(algo, music_data, measures=['RMSE', 'MAE'])

### 使用基础版协同过滤
from surprise import KNNBasic, evaluate
algo = KNNBasic()
perf = evaluate(algo, music_data, measures=['RMSE', 'MAE'])

### 使用均值协同过滤
from surprise import KNNWithMeans, evaluate
algo = KNNWithMeans()
perf = evaluate(algo, music_data, measures=['RMSE', 'MAE'])

### 使用协同过滤baseline
from surprise import KNNBaseline, evaluate
algo = KNNBaseline()
perf = evaluate(algo, music_data, measures=['RMSE', 'MAE'])

### 使用SVD
from surprise import SVD, evaluate
algo = SVD()
perf = evaluate(algo, music_data, measures=['RMSE', 'MAE'])

### 使用SVD++
from surprise import SVDpp, evaluate
algo = SVDpp()
perf = evaluate(algo, music_data, measures=['RMSE', 'MAE'])