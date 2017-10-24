# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 17:36:55 2017

@author: qiu
"""

#coding: utf-8
#解析成userid itemid rating timestamp行格式
import json
import sys

def is_null(s): 
	return len(s.split(","))>2
"""
评分数据格式为 user item rating timestamp
在第一步解析出来的歌单信息+歌曲信息基础上，进一步解析歌曲信息，获得歌曲id、评分和时间戳
"""
def parse_song_info(song_info):
    try:
        song_id, name, artist, popularity = song_info.split(":::")
        min_p = min(popularity)
        max_p = max(popularity)
        n = len(popularity)
        for i,p in enumerate(n,popularity):
            pp[i] = int((p-min_p)/(max_p -min_p)*5)
		#return ",".join([song_id, name, artist, popularity])
        return ",".join([song_id,pp,'1300000'])
    except Exception as e:
		#print e
		#print song_info
        return ""

def parse_playlist_line(in_line):
    '''
    在第一步解析出来的歌单信息+歌曲信息基础上，用\t拆分获得第一个元素是歌单信息，后面的是这个歌单中歌曲信息，即歌曲id、评分和时间戳
    '''
    try:
        contents = in_line.strip().split("\t")
        name, tags, playlist_id, subscribed_count = contents[0].split("##")
        songs_info = map(lambda x:playlist_id+","+parse_song_info(x), contents[1:])
        songs_info = filter(is_null, songs_info)
        return "\n".join(songs_info)
    except Exception as e:
        print (e)
        return False
                                    

def parse_file(in_file, out_file):
    '''
    对第一步得到的数据进一步解析，最终获得所有歌单的歌曲的信息汇总：歌单id、歌曲id、评分和时间戳
    '''
    out = open(out_file, 'w')
    with open(in_file,encoding = 'utf-8') as file:
        data = file.readlines()
    for line in data:
        result = parse_playlist_line(line)
        if(result):
            out.write(result.strip()+"\n")
    out.close()
    
song_info = "./popular.playlist"
with open(song_info,encoding = 'utf-8') as file:
    data = file.readlines()
contents = data[1].strip().split("\t")
song_id, name, artist, popularity = contents[2].split(":::")
print(popularity)
max_p = max(popularity)
n = len(popularity)
parse_file("./popular.playlist", "./popular_music_suprise_format.txt")
#所有歌单的歌曲的信息汇总：歌单id、歌曲id、评分和时间戳，保存在"./popular_music_suprise_format.txt"文件中
#coding: utf-8
import pickle as pickle
import sys

def parse_playlist_get_info(in_line, playlist_dic, song_dic, song_rating):
    '''
    建立歌单id和歌单名称的映射关系：playlist_dic[playlist_id] = name
    建立歌曲id和歌取名称的映射关系：song_dic[song_id] = song_name+"\t"+artist
    '''
    contents = in_line.strip().split("\t")
    name, tags, playlist_id, subscribed_count = contents[0].split("##")
    playlist_dic[playlist_id] = name
    for song in contents[1:]:
        try:
            song_id, song_name, artist, popularity = song.split(":::")
            song_dic[song_id] = song_name+"\t"+artist
            song_rating[song_id] = popularity
        except:
            print ("song format error")
            print (song+"\n")

def parse_file(in_file, out_playlist, out_song,out_song_rating):
    '''
    对第一步解析出来的文件逐条完成从歌单id到歌单名称的映射字典、从歌曲id到歌曲名称的映射字典
    并利用pickle序列化模块，把映射字典保存在二进制文件中，便于以后加载：playlist_dic = pickle.load(open("playlist.pkl","rb"))重新载入
    '''
	#从歌单id到歌单名称的映射字典
    playlist_dic = {}
	#从歌曲id到歌曲名称的映射字典
    song_dic = {}
    song_rating = {}
    for line in open(in_file,encoding = 'utf-8'):
        parse_playlist_get_info(line, playlist_dic, song_dic,song_rating)
    #把映射字典保存在二进制文件中
    pickle.dump(playlist_dic, open(out_playlist,"wb")) 
    #可以通过 playlist_dic = pickle.load(open("playlist.pkl","rb"))重新载入
    pickle.dump(song_dic, open(out_song,"wb"))
    pickle.dump(song_rating, open(out_song_rating,"wb"))
    print(song_rating)
    
parse_file("./popular.playlist", "popular_playlist.pkl", "popular_song.pkl","popular_song_rating.pkl")