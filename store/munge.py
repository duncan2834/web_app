import pandas as pd
import mat4py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Munger():
    
    def __init__(self):
        self.df = pd.read_csv('meta-data.csv')
        self.df = self.df.head(100) 
        self.df.index = self.df['CID']
        self.df['combined_features'] = self.df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        vectorizer = TfidfVectorizer(stop_words='english')
        feature_matrix = vectorizer.fit_transform(self.df['combined_features'])
        similarity_matrix = cosine_similarity(feature_matrix)
        self.feature_matrix = feature_matrix
        self.similarity_matrix = similarity_matrix
        img_paths = mat4py.loadmat('image-path.mat')
        img_paths = list(map(lambda x: x[0], img_paths['imagepath']))  # list chứa các path ảnh
        img_paths = img_paths[:100]  # chỉ lấy 10000 link đầu
        self.df['img_path'] = img_paths
        # init có (df bao gồm metadata + cột combine và imgpath, gồm feature_matrix và similarity_matrix)