#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def get_recommendations(user, model, sparse_user_item, N=5):
    """Рекомендуем топ-N товаров"""
    
    res = [id_to_itemid[rec[0]] for rec in 
                    model.recommend(userid=userid_to_id[user], 
                                    user_items=sparse_user_item,   # на вход user-item matrix
                                    N=N, 
                                    filter_already_liked_items=False, 
                                    filter_items=[itemid_to_id[999999]],  # !!! 
                                    recalculate_user=True)]
    return res


# In[ ]:


def top_purchases(data):
    top_purchases = data.groupby(['user_id', 'item_id'])['quantity'].count().reset_index()
    top_purchases.sort_values('quantity', ascending=False, inplace=True)
    top_purchases = self.top_purchases[self.top_purchases['item_id'] != 999999]


# In[ ]:


def get_similar_item(item_id, N=2):
    """Находит товар, похожий на item_id"""
    recs = model.similar_items(itemid_to_id[item_id], N=2)  # N - количество товаров
    top_rec = recs[1][0]  
    return id_to_itemid[top_rec]


# In[ ]:


def get_similar_items_recommendation(self, user, N=5):
    """Рекомендуем товары, похожие на топ-N купленных юзером товаров"""
    top_users_purchases = top_purchases[top_purchases['user_id'] == user].head(N)
    res = top_users_purchases['item_id'].apply(lambda x: get_similar_item(x)).tolist()        
    return res


# In[ ]:


def get_similar_users_recommendation(user, N=5):
    """Рекомендуем топ-N товаров, среди купленных похожими юзерами"""
    res = []
        
    # Находим топ-N похожих пользователей
    similar_users = model.similar_users(userid_to_id[user], N=N+1)
    similar_users = [rec[0] for rec in similar_users]
    similar_users = similar_users[1:]   # удалим юзера из запроса

    for user in similar_users:
        userid = id_to_userid[user] #own recommender works with user_ids
        res.extend(get_recommendations(userid, N=1))
    return res

