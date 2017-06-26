import pandas as pd
import numpy as np
import gensim
import jieba
import wordcloud
import matplotlib.pyplot as plt

#读取数据
loandata = pd.read_csv('./data/loandata_clean.csv')

#选取借款标题
loandata_title = loandata['loan_title']
#分词
#title_list = []
jieba.load_userdict('./customer_words.txt') #加载自定义词典
title_list = [list(jieba.cut(item)) for item in loandata_title]
#加载停用词
with open('./stop_words.txt','r') as f:
    stop_words = [line.strip() for line in f]
#去除停用词
def remove_stop_words(origin_list,stop_words):
    word_list_nostop = []
    for item in origin_list:
        word_list_nostop.append([word for word in item if str(word) not in set(stop_words)])
    return word_list_nostop

title_list_nostop = remove_stop_words(title_list,stop_words)
#将嵌套列表转为字符串，用于制作词云图
def list_to_string(list_origin):
    list_temp = []
    for item in list_origin:
        str_inner = ' '.join(item)
        list_temp.append(str_inner)
    return ' '.join(list_temp)

#词云图
bg_coloring = plt.imread('./background.jpg') #添加背景图片
wordcloud_title = wordcloud.WordCloud(font_path='./font/simkai.ttf',background_color='white',mask=bg_coloring,max_words=200,height=400,width=400)
wordcloud_title.generate(list_to_string(title_list_nostop))
plt.imshow(wordcloud_title)
plt.axis('off')
#添加背景色
'''
plt.figure()
image_colors = wordcloud.ImageColorGenerator(bg_coloring)
plt.imshow(wordcloud_title.recolor(color_func=image_colors))
plt.axis('off')
'''
plt.show()
#建立文档字典
title_dict = gensim.corpora.Dictionary(title_list_nostop)
#词频统计，构建词频稀疏矩阵
tf_matrix = [title_dict.doc2bow(item) for item in title_list_nostop]
#构建lda主题模型
topic_nums = 6 #人工设置主题数量
lda_model = gensim.models.LdaModel(tf_matrix,num_topics=topic_nums,id2word=title_dict,alpha='auto')
#输出到文件
#输出每个主题最相关的词条和概率（默认10个）
with open('./output/lda_topics.txt','w') as f:
    for item in lda_model.show_topics():
        f.write(str(item) + '\n')
#输出每个文档属于各个主题的概率
with open('./output/doc_topic.txt','w') as f:
    for i in tf_matrix:
        f.write(str(lda_model[i])+'\n')
#返回每个文档最相关主题
#取出[(),()...]元祖的第二个数据最大值所在的元祖索引
def get_index(list_input):
    list_output = []
    for i in list_input:
        list_output.append(i[1])
    return list_output.index(max(list_output))
#写入文件
with open('./output/doc_topic_one.txt','w') as f:
    best_topic = []
    for i in tf_matrix:
        doc_topics = lda_model[i]
        f.write(str(get_index(doc_topics)+1)+'\n') #主题从1开始
        best_topic.append(get_index(doc_topics)+1) #结果保存在列表中


