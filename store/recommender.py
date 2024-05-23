import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_products(product_id, df, similarity_matrix, top_k=5):
    k_product_link = {}
    # Lấy chỉ số của sản phẩm mục tiêu
    idx = df.index.get_loc(product_id)
    print('adu: ' + str(idx))
    # Lấy các điểm tương đồng của sản phẩm mục tiêu với tất cả các sản phẩm khác
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    
    # Sắp xếp các sản phẩm theo điểm tương đồng
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Lấy top_k sản phẩm tương tự (bỏ qua sản phẩm mục tiêu)
    top_k_indices = [i[0] for i in similarity_scores[1:top_k+1]]
    top_k_product_ids = df.iloc[top_k_indices].index.tolist()  # dạng list các index
    for cid in top_k_product_ids:
        k_product_link[cid] = df.loc[cid, 'img_path']
    return k_product_link # trả về dict, khóa là cid, value là link
