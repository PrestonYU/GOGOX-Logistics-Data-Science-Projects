#!/usr/bin/env python
# coding: utf-8

# In[143]:


#########################################################################
# Created by Preston Yu (TW Team)
# 2021-06-04
#########################################################################
# 1 : Import Google Sheet to Jupyter Notebook
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import numpy as np
import math
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', None)


    # The scope is always look like this so we did not need to change anything
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # Name of our Service Account Key
    # https://console.developerxxxxxxxxxxxxxxxxxxxxxxxx
google_key_file = '/Users/prxxxxxxxxxxxc9.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

    # Opening the worksheet by using Worksheet ID
workbook = gc.open_by_key('xxxxxxxxxxxxyXae_c')

    # Selecting which sheet to pulling the data
sheet = workbook.worksheet('orders')

    # Pulling the data and transform it to the data frame
values = sheet.get_all_values()
df = pd.DataFrame(values[:], columns = values[0])
df = df[1:]
df['Longitude'] = df['Longitude'].astype(np.float64)
df['Latitude'] = df['Latitude'].astype(np.float64)
df = df[(df['Latitude'] >= 24.7) & (df['Latitude'] < 25.3) & (df['Longitude'] < 122.0) & (df['Longitude'] >= 121.2)]  # TPE Area
df = df.reset_index(drop = True)


# In[144]:


# 2 : Segment Regions and Num of Clusters
region_list = list(df['收件地區'].unique())
df_list = {}
location_list = {}
route_nums = {}
for i in range(0,len(region_list)):
    df_list[i]  = df[df['收件地區'] == region_list[i]]
    df_list[i] = df_list[i].reset_index(drop = True)
    location_list[i] = df[df['收件地區'] == region_list[i]].iloc[:,12:]
    location_list[i] = location_list[i].reset_index(drop = True)
    if len(location_list[i]) > 2 and len(location_list[i]) < 8 and len(location_list[i]) %3 != 0:
        route_nums[i] = math.ceil(len(location_list[i])/3)-1
    elif len(location_list[i]) > 2 and len(location_list[i])/2 < 8 and len(location_list[i]) %3 == 0:
        route_nums[i] = math.ceil(len(location_list[i])/3)
    elif len(location_list[i]) >= 8 and len(location_list[i]) %4 == 0:
        route_nums[i] = math.ceil(len(location_list[i])/4)
    elif len(location_list[i]) >= 8 and len(location_list[i]) %4 == 1:
        route_nums[i] = math.ceil(len(location_list[i])/4)-1
    elif len(location_list[i]) >= 8 and len(location_list[i]) %4 == 2:
        route_nums[i] = math.ceil(len(location_list[i])/3)-1
    elif len(location_list[i]) >= 8 and len(location_list[i]) %4 == 3:
        route_nums[i] = math.ceil(len(location_list[i])/3)-1
    else:
        route_nums[i] = 1


# In[145]:


# 3 : Run KMeans Algorithm

# import necessary packages
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, MiniBatchKMeans

label_list = {}

# segment clusters
for i in range(0,len(region_list)):
    kmeans = MiniBatchKMeans(n_clusters = int(route_nums[i]), reassignment_ratio = 1, batch_size = 1)
    #kmeans = KMeans(n_clusters = int(route_nums[i]), n_jobs = -1)  # <--- NOTICE: you can change the cluster count by yourself
    kmeans.fit(location_list[i])

# labels
    labels = kmeans.predict(location_list[i])
    label_list[i] = labels
    centroids = kmeans.cluster_centers_

    fig = plt.figure(figsize=(5, 5))
    colmap = {1: 'r', 2: 'g', 3: 'b', 4:'y',5:'m',6:'c',7:'k',8:'navy',9:'teal',10:'gold',
              11:'dimgray',12:'darkviolet',13:'slategrey',14:'peru',15:'tomato',16:'crimson',17:'darkkhaki',18:'azure',19:'lavender',20:'bisque',
              21:'silver',22:'indianred',23:'olive',24:'slateblue',25:'orchid',26:'olivedrab',27:'lightseagreen',28:'lime',29:'tan',30:'lightcoral'}
    colors = list(map(lambda x: colmap[x+1], labels))

    plt.scatter(location_list[i]['Longitude'],location_list[i]['Latitude'], color = colors, alpha=0.5, edgecolor='k')
    
    for idx, centroid in enumerate(centroids):
        plt.scatter(*centroid, color=colmap[idx+1])
    plt.xlim(121.1, 121.7)
    plt.ylim(24.7, 25.5)
    


# In[146]:


# 4 : 路線生成與整理
route_num_df_list = {}
new_df_list = {}
for i in range(0,len(region_list)):
    route_num_df_list[i] = pd.DataFrame(data = label_list[i], columns = ['路線代碼'])
    new_df_list[i] = pd.concat([df_list[i],route_num_df_list[i]], axis=1)
    new_df_list[i]['路線名稱'] = '0'
    
    for j in range(0,len(new_df_list[i])):
        new_df_list[i]['路線名稱'][j] = new_df_list[i]['收件地區'][j] +'-'+str(new_df_list[i]['路線代碼'][j])

master_df = new_df_list[0]
for i in range(1,len(new_df_list)):
    master_df = pd.concat([master_df,new_df_list[i]], axis=0)
master_df = master_df.reset_index(drop = True)


# In[147]:


# 5 : 路線均勻度檢查
a = pd.DataFrame(master_df['路線名稱'].unique())
b = pd.DataFrame(master_df.groupby(['路線名稱']).count()['訂單編號'])
b = b.reset_index()
c = pd.DataFrame(a[0].str.split('-').str.get(0))
route_analysis = pd.concat([c,a],axis=1)
route_analysis.columns = ['收件地區','路線名稱']
route_analysis = route_analysis.join(b.set_index('路線名稱'),on = '路線名稱')
route_analysis.columns = ['收件地區','路線名稱','訂單數量']
#route_analysis['order_rank'] = route_analysis.groupby(['收件地區'])['訂單數量'].rank(method = 'min')


# 5-1 : 處理路線訂單過於集中問題 （上限5單/路線）
m1 = master_df[master_df['路線名稱'].isin(route_analysis['路線名稱'][route_analysis['訂單數量'] >= 6])]
m1 = m1.reset_index(drop=True)
m2 = master_df[master_df['路線名稱'].isin(route_analysis['路線名稱'][route_analysis['訂單數量'] < 6])]
m2 = m2.reset_index(drop=True)

adj_df = route_analysis[route_analysis['訂單數量'] >= 6]
adj_df = adj_df.reset_index(drop=True)
adj_df['校正訂單數'] = round(adj_df['訂單數量']/2)
adj_df

m1['訂單編號'] = m1['訂單編號'].astype(float)
m1['order_rank'] = m1.groupby(['路線名稱'])['訂單編號'].rank()
for i in range(0,len(adj_df)):
    m1['路線名稱'][(m1['路線名稱'] == adj_df['路線名稱'][i]) & (m1['order_rank'] <= adj_df['校正訂單數'][i])] =     m1['路線名稱'][(m1['路線名稱'] == adj_df['路線名稱'][i]) & (m1['order_rank'] <= adj_df['校正訂單數'][i])] + 'a'
del m1['order_rank']    
master_df = pd.concat([m1,m2],axis = 0)
master_df = master_df.reset_index(drop=True)


# In[148]:


# 5-2 : 處理路線間訂單分配不均問題 (該路線只有1單) 
x = 1

while x < 10:

    m1 = master_df[master_df['路線名稱'].isin(route_analysis['路線名稱'][route_analysis['訂單數量'] <= 1])]
    m1 = m1.reset_index(drop=True)
    m2 = master_df[(master_df['路線名稱'].isin(route_analysis['路線名稱'][route_analysis['訂單數量'] == 2]))&                (master_df['收件地區'].isin(m1['收件地區']))]
    m2 = m2.reset_index(drop=True)
    m3 = master_df[(master_df['路線名稱'].isin(route_analysis['路線名稱'][route_analysis['訂單數量'] == 3]))&                (master_df['收件地區'].isin(m1['收件地區']))]
    m3 = m3.reset_index(drop=True)
    m4 = master_df[(master_df['路線名稱'].isin(route_analysis['路線名稱'][route_analysis['訂單數量'] == 4]))&                (master_df['收件地區'].isin(m1['收件地區']))]
    m4 = m4.reset_index(drop=True)

    m5 = master_df[~master_df['訂單編號'].isin(m1['訂單編號'])]
    m5 = m5.reset_index(drop=True)
    
    if len(m2) > 0 :
        alternative_route_cluster = m2[['收件地區','路線名稱']]   
    elif len(m3) > 0 :
        alternative_route_cluster = m3[['收件地區','路線名稱']]
    elif len(m4) > 0:
        alternative_route_cluster = m4[['收件地區','路線名稱']]

    try:
        alternative_route_cluster = alternative_route_cluster.drop_duplicates()
        alternative_route_cluster = alternative_route_cluster.reset_index(drop=True)

        for i in range(0,len(m1)):
            try:
                m1['路線名稱'][i] =                 alternative_route_cluster['路線名稱'][(m1['收件地區'][i] == alternative_route_cluster['收件地區'])].reset_index(drop=True)[0]
            except:
                m1['路線名稱'][i] = m1['路線名稱'][i]
    except:
        m1 = m1

    master_df = pd.concat([m1,m5],axis = 0)
    master_df = master_df.reset_index(drop=True)
    
    x = x+1


# In[149]:


# 5-3 : 處理路線間訂單分配不均問題 (該地區有多個只有2單的路線)
m2 = master_df[master_df['路線名稱'].isin(route_analysis['路線名稱'][route_analysis['訂單數量'] == 2])]
d = pd.DataFrame(m2.groupby(['收件地區']).count()['訂單編號'])
d = d.reset_index()
d = d[d['訂單編號'] == 4] # 有2個2單的路線
d = d.reset_index(drop=True)
#e = d[d['訂單編號'] == 6] # 有3個2單的路線 --> 暫不處理，表一開始的路線區隔就有問題
#e = e.reset_index(drop=True)
#f = d[d['訂單編號'] == 8] # 有4個2單的路線 --> 暫不處理，表一開始的路線區隔就有問題
#f = f.reset_index(drop=True)
#g = d[d['訂單編號'] == 10] # 有5個2單的路線 --> 暫不處理，表一開始的路線區隔就有問題
#g = g.reset_index(drop=True)

m2 = master_df[(master_df['路線名稱'].isin(route_analysis['路線名稱'][route_analysis['訂單數量'] == 2])) &                (master_df['收件地區'].isin(d['收件地區']))]
m2 = m2.reset_index(drop=True)
m4 = master_df[~master_df['訂單編號'].isin(m2['訂單編號'])]
m4.reset_index(drop=True)

adjust_route_name_list = m2.groupby(['收件地區'])['路線名稱'].min().reset_index()

for i in range(0,len(m2)):
    try:
        m2['路線名稱'][i] =         adjust_route_name_list['路線名稱'][(m2['收件地區'][i] == adjust_route_name_list['收件地區'])].reset_index(drop=True)[0]
    except:
        m2['路線名稱'][i] = m2['路線名稱'][i]
        
master_df = pd.concat([m2,m4],axis = 0)
master_df = master_df.reset_index(drop=True) 


# In[150]:


# 5-4 : 最終路線均勻度檢查
a = pd.DataFrame(master_df['路線名稱'].unique())
b = pd.DataFrame(master_df.groupby(['路線名稱']).count()['訂單編號'])
b = b.reset_index()
c = pd.DataFrame(a[0].str.split('-').str.get(0))
route_analysis = pd.concat([c,a],axis=1)
route_analysis.columns = ['收件地區','路線名稱']
route_analysis = route_analysis.join(b.set_index('路線名稱'),on = '路線名稱')
route_analysis.columns = ['收件地區','路線名稱','訂單數量']
route_analysis


# In[151]:


# 6 : 導入站所位置資料
    # The scope is always look like this so we did not need to change anything
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # Name of our Service Account Key
    # https://console.devexxxxxxxxx
google_key_file = '/Users/pxxxxxxxxxxxxxxx53c9.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

    # Opening the worksheet by using Worksheet ID
workbook = gc.open_by_key('1Pxxxxxxxxxae_c')

    # Selecting which sheet to pulling the data
sheet = workbook.worksheet('warehouse')

    # Pulling the data and transform it to the data frame
values = sheet.get_all_values()
dfw = pd.DataFrame(values[:], columns = values[0])
dfw = dfw[1:]
dfw['Longitude'] = dfw['Longitude'].astype(np.float64)
dfw['Latitude'] = dfw['Latitude'].astype(np.float64)
dfw = dfw.reset_index(drop = True)


route_list = master_df['路線名稱'].unique()
route_df_list = {}
for i in range(0,len(route_list)):
    route_df_list[i] = master_df[master_df['路線名稱'] == route_list[i]]
    
for i in range(0,len(route_df_list)):
    test = route_df_list[i]
    test = test.reset_index(drop = True)
    depot = dfw[dfw['收件地區'] == test['收件地區'][0]]
    test = pd.concat([depot,test], ignore_index = True)
    test['路線名稱'][0] = test['路線名稱'][1]
    route_df_list[i] = test
    
master_df2 = route_df_list[0]
for i in range(1,len(route_df_list)):
    master_df2 = pd.concat([master_df2,route_df_list[i]], ignore_index = True)


# In[152]:


# 7 : 排路線
final_route = master_df2['路線名稱'].unique()
df_list = {}


for e in range(0,len(final_route)):
    k = master_df2[master_df2['路線名稱'] == final_route[e]] 
    k = k.reset_index(drop=True)
    
    """Capacited Vehicles Routing Problem (CVRP)."""
    
# [START import]
    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp
# [END import]


# [START data_model]
    def build_distance_matrix(dff):
        dff['distance_matrix'] = ''
        for i in range(0,len(dff)):
            distance_matrix = []
            for j in range(0,len(dff)):
                distance_matrix.append(int(round((math.sqrt(pow(float(dff['Latitude'][i])-float(dff['Latitude'][j]),2) + pow(float(dff['Longitude'][i])-float(dff['Longitude'][j]),2))*111000))))
            dff['distance_matrix'][i] = distance_matrix
        return list(dff['distance_matrix'])


    def create_data_model():
        """Stores the data for the problem."""
        data = {}
        data['distance_matrix'] = build_distance_matrix(k)
    # [START demands_capacities]
        data['demands'] = [0, 0, 0, 0, 0, 0] 
        data['vehicle_capacities'] = [6]
    # [END demands_capacities]
        data['num_vehicles'] = 1
        data['depot'] = 0
        data['route_name'] = k['路線名稱'][0] 
        data['shipment'] = k['訂單編號']
        data['deliver_order'] = list(np.zeros(len(data['distance_matrix']),dtype=np.int))
        
        return data
    # [END data_model]


# [START solution_printer]
    def print_solution(data, manager, routing, solution):
        """Prints solution on console."""
        
        total_distance = 0
        total_load = 0
        
        df1 = pd.DataFrame(data['shipment'], columns = ['訂單編號'])
        df1['路線名稱'] = data['route_name']
        df3 = pd.DataFrame(data['deliver_order'], columns = ['配送路順'])
        df = pd.concat([df1,df3], axis = 1)
        
        
        #print(f'路線總公尺數: {solution.ObjectiveValue()}')
        """
        if len(data['distance_matrix']) == 2+1 and solution.ObjectiveValue() <= 2500*1.1:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 2+1 and solution.ObjectiveValue() <= 3500*1.1:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 3+1 and solution.ObjectiveValue() <= 5500*1.1:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 3+1 and solution.ObjectiveValue() <= 6500*1.1:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 4+1 and solution.ObjectiveValue() <= 7500*1.1:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 4+1 and solution.ObjectiveValue() <= 9500*1.1:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 5+1 and solution.ObjectiveValue() <= 9500*1.1:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 5+1 and solution.ObjectiveValue() <= 11500*1.1:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 6+1 and solution.ObjectiveValue() <= 11500*1.1:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 6+1 and solution.ObjectiveValue() <= 14500*1.1:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        else:
            print('平台能否承接：不可，低於平台里程價')
            df['平台可承接與否'] = '不可以'
            df['訂單單價'] = 0
        """
        
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            plan_output = '路線名稱 {}:\n'.format(data['route_name'])
            route_distance = 0
            route_load = 0
            
            node_index_list = []
            shipment_order_list = []
            iterr = 1
            
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route_load += data['demands'][node_index]
                plan_output += '訂單編號 {0} -> '.format(data['shipment'][node_index])
                
                previous_index = index
                
                shipment_order_list.append(data['shipment'][node_index])
                node_index_list.append(iterr)
                iterr += 1
                
                index = solution.Value(routing.NextVar(index))
                
                try:
                    route_distance = route_distance + round(data['distance_matrix'][previous_index][index]*1.3)
                except:
                    continue 
                
                #route_distance += routing.GetArcCostForVehicle(
                #    previous_index, index, vehicle_id)
            #plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
            #                                         route_load)
            #plan_output += 'Distance of the route: {}m\n'.format(route_distance)
            #plan_output += 'Load of the route: {}\n'.format(route_load)
            
            df_dic1 = pd.DataFrame(shipment_order_list)
            df_dic2 = pd.DataFrame(node_index_list)
            df_dic = pd.concat([df_dic1,df_dic2] , axis = 1)
            df_dic.columns = ['訂單編號','配送路順']

            df = df.merge(df_dic, left_on = '訂單編號', right_on = '訂單編號')
            df = df.drop(['配送路順_x'], axis = 1)
            df.columns = ['訂單編號','路線名稱','配送路順']
            
            print(plan_output)
            
            #print(df)
            #print("===============================================")
            #df_list[len(df_list)] = df
            #total_distance += route_distance
            #total_load += route_load
        
        buffer_zone = 1.1
        
        # ⚠️ 暫時不管距離限制，如要加回距離限制，將route_distance criteria 的最後一碼刪除即可
        
        print(f'路線總公尺數: {route_distance}')
        if len(data['distance_matrix']) == 2+1 and route_distance <= 25009*buffer_zone:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 2+1 and route_distance <= 35009*buffer_zone:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 3+1 and route_distance <= 55009*buffer_zone:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 3+1 and route_distance <= 65009*buffer_zone:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 4+1 and route_distance <= 75009*buffer_zone:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 4+1 and route_distance <= 95009*buffer_zone:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 5+1 and route_distance <= 95009*buffer_zone:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 5+1 and route_distance <= 115009*buffer_zone:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 6+1 and route_distance <= 115009*buffer_zone:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 6+1 and route_distance <= 145009*buffer_zone:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        else:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
            
            #print('平台能否承接：不可，低於平台里程價')  #⚠️ 暫時隱藏，解除距離限制
            #df['平台可承接與否'] = '不可以'           #⚠️ 暫時隱藏，解除距離限制
            #df['訂單單價'] = 0                      #⚠️ 暫時隱藏，解除距離限制
        
        df_list[len(df_list)] = df
        
        print("===============================================")
        
        return df_list
        #print('Total distance of all routes: {}m'.format(total_distance))
        #print('Total load of all routes: {}'.format(total_load))
    # [END solution_printer]


    
    
    def main():
        """Solve the CVRP problem."""
    # Instantiate the data problem.
    # [START data]
        data = create_data_model()
    # [END data]

    # Create the routing index manager.
    # [START index_manager]
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    # [END index_manager]

    # Create Routing Model.
    # [START routing_model]
        routing = pywrapcp.RoutingModel(manager)

    # [END routing_model]

    # Create and register a transit callback.
    # [START transit_callback]
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    # [END transit_callback]

    # Define cost of each arc.
    # [START arc_cost]
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # [END arc_cost]

    # Add Capacity constraint.
    # [START capacity_constraint]
        def demand_callback(from_index):
            """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data['demands'][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data['vehicle_capacities'],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')
    # [END capacity_constraint]

    # Setting first solution heuristic.
    # [START parameters]
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_ARC) #PATH_CHEAPEST_ARC)
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT) #GUIDED_LOCAL_SEARCH) 
        search_parameters.time_limit.FromSeconds(1)
    # [END parameters]

    # Solve the problem.
    # [START solve]
        solution = routing.SolveWithParameters(search_parameters)
    # [END solve]

    # Print solution on console.
    # [START print_solution]
        if solution:
            print_solution(data, manager, routing, solution)
            
            #print(solution)
            
                
    # [END print_solution]


    if __name__ == '__main__':
        try:
            main()
        except:
            continue
# [END program]


# In[135]:


# XL ORDER 1 : Import Google Sheet to Jupyter Notebook
    # The scope is always look like this so we did not need to change anything
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # Name of our Service Account Key
    # https://console.developerxxxxxxxxxxxxxxxxxxxxxx
google_key_file = '/Users/xxxxxxxxxxc9.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

    # Opening the worksheet by using Worksheet ID
workbook = gc.open_by_key('1PxxxxxxxxxxxxxxxxxxyXae_c')

    # Selecting which sheet to pulling the data
sheet = workbook.worksheet('oversize暫存區')

    # Pulling the data and transform it to the data frame
values = sheet.get_all_values()
df2 = pd.DataFrame(values[:], columns = values[0])
df2 = df2[1:]
df2['Longitude'] = df2['Longitude'].astype(np.float64)
df2['Latitude'] = df2['Latitude'].astype(np.float64)
df2 = df2[(df2['Latitude'] >= 24.7) & (df2['Latitude'] < 25.3) & (df2['Longitude'] < 122.0) & (df2['Longitude'] >= 121.2)]  # TPE Area
df2 = df2.reset_index(drop = True)

df2['路線代碼'] = df2.index
df2['路線名稱'] = '-'
for i in range(0,len(df2)):
    df2['路線名稱'][i] = str(df2['收件地區'][i]) + '-' + str(df2['路線代碼'][i]) + '-XL'

    
# XL ORDER 2 : 導入站所位置資料
route_list = df2['路線名稱'].unique()
route_df_list = {}
for i in range(0,len(route_list)):
    route_df_list[i] = df2[df2['路線名稱'] == route_list[i]]
    
for i in range(0,len(route_df_list)):
    test = route_df_list[i]
    test = test.reset_index(drop = True)
    depot = dfw[dfw['收件地區'] == test['收件地區'][0]]
    test = pd.concat([depot,test], ignore_index = True)
    test['路線名稱'][0] = test['路線名稱'][1]
    route_df_list[i] = test
    
df3 = route_df_list[0]
for i in range(1,len(route_df_list)):
    df3 = pd.concat([df3,route_df_list[i]], ignore_index = True)


# XL ORDER 3 : 排路線
df3['配送路順'] = 0
for i in range(0,len(df3)):
    if df3['貨件尺寸'][i] == '':
        df3['配送路順'][i] = 1
    elif df3['貨件尺寸'][i] != '':
        df3['配送路順'][i] = 2
        
df3['平台可承接與否'] = '可以'
df3['訂單單價'] = 60


# In[153]:


# ⚠️ Warning : Run it when you want to bypass step 8

dff = pd.DataFrame(df_list[0])
for i in range(1,len(df_list)):
    dff = pd.concat([dff,pd.DataFrame(df_list[i])]) 
dff = dff.reset_index(drop=True)
All_df = master_df2.merge(dff, left_on = ['訂單編號','路線名稱'], right_on = ['訂單編號','路線名稱'])
All_df = All_df.drop("日期", axis = 1)
All_df = All_df.drop("時段", axis = 1)
#df4 = df3.drop("日期", axis = 1)
#df4 = df4.drop("時段", axis = 1)
#All_df = pd.concat([All_df,df4])
All_df = All_df.reset_index(drop = True)
All_df


# In[ ]:


# 8 : 資料整合與重組
"""
dff = pd.DataFrame(df_list[0])
for i in range(1,len(df_list)):
    dff = pd.concat([dff,pd.DataFrame(df_list[i])]) 
dff = dff.reset_index(drop=True)
All_df = master_df2.merge(dff, left_on = ['訂單編號','路線名稱'], right_on = ['訂單編號','路線名稱'])

All_ok_df = All_df[All_df['平台可承接與否'] == '可以']
All_ok_df = All_ok_df.reset_index(drop = True)

All_no_df = All_df[All_df['平台可承接與否'] == '不可以']
All_no_df = All_no_df.reset_index(drop = True)

#All_no_df = All_no_df[All_no_df['貨件尺寸'].str.contains('V')]
All_no_df = All_no_df[All_no_df['貨件尺寸'] != '']
All_no_df = All_no_df.drop(columns = ['路線代碼','路線名稱','配送路順','平台可承接與否','訂單單價'])
All_no_df = All_no_df.reset_index(drop = True)


# 8-1 : Re-segment
region_list = list(All_no_df['收件地區'].unique())
df_list = {}
location_list = {}
route_nums = {}
for i in range(0,len(region_list)):
    df_list[i]  = All_no_df[All_no_df['收件地區'] == region_list[i]]
    df_list[i] = df_list[i].reset_index(drop = True)
    location_list[i] = All_no_df[All_no_df['收件地區'] == region_list[i]].iloc[:,14:]
    location_list[i] = location_list[i].reset_index(drop = True)
    if len(location_list[i]) > 2 and len(location_list[i]) < 16 and len(location_list[i]) %3 != 0:
        route_nums[i] = math.ceil(len(location_list[i])/4)
    elif len(location_list[i]) > 2 and len(location_list[i])/2 < 16 and len(location_list[i]) %3 == 0:
        route_nums[i] = math.ceil(len(location_list[i])/4)
    elif len(location_list[i]) >= 16 and len(location_list[i]) %4 == 0:
        route_nums[i] = math.ceil(len(location_list[i])/5)
    elif len(location_list[i]) >= 16 and len(location_list[i]) %4 == 1:
        route_nums[i] = math.ceil(len(location_list[i])/4)-1
    elif len(location_list[i]) >= 16 and len(location_list[i]) %4 == 2:
        route_nums[i] = math.ceil(len(location_list[i])/4)-1
    elif len(location_list[i]) >= 16 and len(location_list[i]) %4 == 3:
        route_nums[i] = math.ceil(len(location_list[i])/4)-1
    else:
        route_nums[i] = 1


# 8-2 : Re-cluster
label_list = {}

# segment clusters
for i in range(0,len(region_list)):
    kmeans = MiniBatchKMeans(n_clusters = int(route_nums[i]), reassignment_ratio = 1, batch_size = 1)
    #kmeans = KMeans(n_clusters = int(route_nums[i]), n_jobs = -1)  # <--- NOTICE: you can change the cluster count by yourself
    kmeans.fit(location_list[i])

# labels
    labels = kmeans.predict(location_list[i])
    label_list[i] = labels
    centroids = kmeans.cluster_centers_

    fig = plt.figure(figsize=(5, 5))
    colmap = {1: 'r', 2: 'g', 3: 'b', 4:'y',5:'m',6:'c',7:'k',8:'navy',9:'teal',10:'gold',
              11:'dimgray',12:'darkviolet',13:'slategrey',14:'peru',15:'tomato',16:'crimson',17:'darkkhaki',18:'azure',19:'lavender',20:'bisque',
              21:'silver',22:'indianred',23:'olive',24:'slateblue',25:'orchid',26:'olivedrab',27:'lightseagreen',28:'lime',29:'tan',30:'lightcoral'}
    colors = list(map(lambda x: colmap[x+1], labels))

    plt.scatter(location_list[i]['Longitude'],location_list[i]['Latitude'], color = colors, alpha=0.5, edgecolor='k')
    
    for idx, centroid in enumerate(centroids):
        plt.scatter(*centroid, color=colmap[idx+1])
    plt.xlim(121.1, 121.7)
    plt.ylim(24.7, 25.5)
    

# 8-3 : Re-generate routes
route_num_df_list = {}
new_df_list = {}
for i in range(0,len(region_list)):
    route_num_df_list[i] = pd.DataFrame(data = label_list[i], columns = ['路線代碼'])
    new_df_list[i] = pd.concat([df_list[i],route_num_df_list[i]], axis=1)
    new_df_list[i]['路線名稱'] = '0'
    
    for j in range(0,len(new_df_list[i])):
        new_df_list[i]['路線名稱'][j] = new_df_list[i]['收件地區'][j] +'-0-'+str(new_df_list[i]['路線代碼'][j])

master_df3 = new_df_list[0]
for i in range(1,len(new_df_list)):
    master_df3 = pd.concat([master_df3,new_df_list[i]], axis=0)
master_df3 = master_df3.reset_index(drop = True)


# 8-4 : 最終路線均勻度檢查
a = pd.DataFrame(master_df3['路線名稱'].unique())
b = pd.DataFrame(master_df3.groupby(['路線名稱']).count()['訂單編號'])
b = b.reset_index()
c = pd.DataFrame(a[0].str.split('-').str.get(0))
route_analysis = pd.concat([c,a],axis=1)
route_analysis.columns = ['收件地區','路線名稱']
route_analysis = route_analysis.join(b.set_index('路線名稱'),on = '路線名稱')
route_analysis.columns = ['收件地區','路線名稱','訂單數量']
route_analysis


# 8-5 : 重新導入站所資料
route_list = master_df3['路線名稱'].unique()
route_df_list = {}
for i in range(0,len(route_list)):
    route_df_list[i] = master_df3[master_df3['路線名稱'] == route_list[i]]
    
for i in range(0,len(route_df_list)):
    test = route_df_list[i]
    test = test.reset_index(drop = True)
    depot = dfw[dfw['收件地區'] == test['收件地區'][0]]
    test = pd.concat([depot,test], ignore_index = True)
    test['路線名稱'][0] = test['路線名稱'][1]
    route_df_list[i] = test
    
master_df4 = route_df_list[0]
for i in range(1,len(route_df_list)):
    master_df4 = pd.concat([master_df4,route_df_list[i]], ignore_index = True)

    
# 8-6 : 重安排路順
final_route = master_df4['路線名稱'].unique()
df_list = {}


for e in range(0,len(final_route)):
    k = master_df4[master_df4['路線名稱'] == final_route[e]] 
    k = k.reset_index(drop=True)
    
    """Capacited Vehicles Routing Problem (CVRP)."""
    
# [START import]
    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp
# [END import]


# [START data_model]
    def build_distance_matrix(dff):
        dff['distance_matrix'] = ''
        for i in range(0,len(dff)):
            distance_matrix = []
            for j in range(0,len(dff)):
                distance_matrix.append(int(round((math.sqrt(pow(float(dff['Latitude'][i])-float(dff['Latitude'][j]),2) + pow(float(dff['Longitude'][i])-float(dff['Longitude'][j]),2))*111000))))
            dff['distance_matrix'][i] = distance_matrix
        return list(dff['distance_matrix'])


    def create_data_model():
        """Stores the data for the problem."""
        data = {}
        data['distance_matrix'] = build_distance_matrix(k)
    # [START demands_capacities]
        data['demands'] = [0, 0, 0, 0, 0, 0] 
        data['vehicle_capacities'] = [6]
    # [END demands_capacities]
        data['num_vehicles'] = 1
        data['depot'] = 0
        data['route_name'] = k['路線名稱'][0] 
        data['shipment'] = k['訂單編號']
        data['deliver_order'] = list(np.zeros(len(data['distance_matrix']),dtype=np.int))
        
        return data
    # [END data_model]


# [START solution_printer]
    def print_solution(data, manager, routing, solution):
        """Prints solution on console."""
        
        total_distance = 0
        total_load = 0
        
        df1 = pd.DataFrame(data['shipment'], columns = ['訂單編號'])
        df1['路線名稱'] = data['route_name']
        df3 = pd.DataFrame(data['deliver_order'], columns = ['配送路順'])
        df = pd.concat([df1,df3], axis = 1)
        
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            plan_output = '路線名稱 {}:\n'.format(data['route_name'])
            route_distance = 0
            route_load = 0
            
            node_index_list = []
            shipment_order_list = []
            iterr = 1
            
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route_load += data['demands'][node_index]
                plan_output += '訂單編號 {0} -> '.format(data['shipment'][node_index])
                
                previous_index = index
                
                shipment_order_list.append(data['shipment'][node_index])
                node_index_list.append(iterr)
                iterr += 1
                
                index = solution.Value(routing.NextVar(index))
                
                try:
                    route_distance = route_distance + round(data['distance_matrix'][previous_index][index]*1.3)
                except:
                    continue 
                
                #route_distance += routing.GetArcCostForVehicle(
                #    previous_index, index, vehicle_id)
            #plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
            #                                         route_load)
            #plan_output += 'Distance of the route: {}m\n'.format(route_distance)
            #plan_output += 'Load of the route: {}\n'.format(route_load)
            
            df_dic1 = pd.DataFrame(shipment_order_list)
            df_dic2 = pd.DataFrame(node_index_list)
            df_dic = pd.concat([df_dic1,df_dic2] , axis = 1)
            df_dic.columns = ['訂單編號','配送路順']

            df = df.merge(df_dic, left_on = '訂單編號', right_on = '訂單編號')
            df = df.drop(['配送路順_x'], axis = 1)
            df.columns = ['訂單編號','路線名稱','配送路順']
            
            print(plan_output)
            
            #print(df)
            #print("===============================================")
            #df_list[len(df_list)] = df
            #total_distance += route_distance
            #total_load += route_load
        
        buffer_zone = 1.1
        
        
        # ⚠️ 暫時不管距離限制，如要加回距離限制，將route_distance criteria 的最後一碼刪除即可
        
        print(f'路線總公尺數: {route_distance}')
        if len(data['distance_matrix']) == 2+1 and route_distance <= 25009*buffer_zone:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 2+1 and route_distance <= 35009*buffer_zone:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 3+1 and route_distance <= 55009*buffer_zone:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 3+1 and route_distance <= 65009*buffer_zone:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 4+1 and route_distance <= 75009*buffer_zone:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 4+1 and route_distance <= 95009*buffer_zone:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 5+1 and route_distance <= 95009*buffer_zone:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 5+1 and route_distance <= 115009*buffer_zone:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        elif len(data['distance_matrix']) == 6+1 and route_distance <= 115009*buffer_zone:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
        elif len(data['distance_matrix']) == 6+1 and route_distance <= 145009*buffer_zone:
            print('平台能否承接：可，單件價格$60')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 60
        else:
            print('平台能否承接：可，單件價格$54')
            df['平台可承接與否'] = '可以'
            df['訂單單價'] = 54
            
            #print('平台能否承接：不可，低於平台里程價') #⚠️ 暫時隱藏，解除距離限制
            #df['平台可承接與否'] = '不可以'           #⚠️ 暫時隱藏，解除距離限制
            #df['訂單單價'] = 0                      #⚠️ 暫時隱藏，解除距離限制
        
        df_list[len(df_list)] = df
        
        print("===============================================")
        
        return df_list
        #print('Total distance of all routes: {}m'.format(total_distance))
        #print('Total load of all routes: {}'.format(total_load))
    # [END solution_printer]


    
    
    def main():
        """Solve the CVRP problem."""
    # Instantiate the data problem.
    # [START data]
        data = create_data_model()
    # [END data]

    # Create the routing index manager.
    # [START index_manager]
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    # [END index_manager]

    # Create Routing Model.
    # [START routing_model]
        routing = pywrapcp.RoutingModel(manager)

    # [END routing_model]

    # Create and register a transit callback.
    # [START transit_callback]
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    # [END transit_callback]

    # Define cost of each arc.
    # [START arc_cost]
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # [END arc_cost]

    # Add Capacity constraint.
    # [START capacity_constraint]
        def demand_callback(from_index):
            """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data['demands'][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data['vehicle_capacities'],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')
    # [END capacity_constraint]

    # Setting first solution heuristic.
    # [START parameters]
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_ARC) #PATH_CHEAPEST_ARC)
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT) #GUIDED_LOCAL_SEARCH) 
        search_parameters.time_limit.FromSeconds(1)
    # [END parameters]

    # Solve the problem.
    # [START solve]
        solution = routing.SolveWithParameters(search_parameters)
    # [END solve]

    # Print solution on console.
    # [START print_solution]
        if solution:
            print_solution(data, manager, routing, solution)
            
            #print(solution)
            
                
    # [END print_solution]


    if __name__ == '__main__':
        try:
            main()
        except:
            continue
# [END program]


# 8-7 : 重組資料
dff = pd.DataFrame(df_list[0])
for i in range(1,len(df_list)):
    dff = pd.concat([dff,pd.DataFrame(df_list[i])]) 
dff = dff.reset_index(drop=True)
All_no_df = master_df4.merge(dff, left_on = ['訂單編號','路線名稱'], right_on = ['訂單編號','路線名稱'])
All_df = pd.concat([All_ok_df,All_no_df], ignore_index = True)
All_df = All_df.drop("日期", axis = 1)
All_df = All_df.drop("時段", axis = 1)
All_df
"""


# In[ ]:





# In[ ]:





# In[154]:


# 9 : Upload prediction data to Google Sheet

    # Backend Setting : https://console.developers.xxxxxxxxxxxx
    # Connect to Google Sheet
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
    
    # Configure the connection
scope = ['https://spreadsheets.google.com/feeds']
    
    # Give the path to the Service Account Credential 
credentials = ServiceAccountCredentials.from_json_keyfile_name('xxxxxxxxxxx9.json')
    
    # Authorize Jupyter Notebook
gc = gspread.authorize(credentials)
    
    # The gsheet ID
    # Sheet URL : https://docs.google.com/spreadsheets/xxxxxxxxxxxxx
spreadsheet_key = 'xxxxaxxxxxae_c'
        
    # Set the sheet name for uploading the dataframe
wks_name = 'results'
cell_of_start_df = 'A1'
    
    # Upload the dataframe
d2g.upload(All_df,
            spreadsheet_key,
            wks_name,
            credentials = credentials,
            start_cell = cell_of_start_df,
            clean = True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[155]:


# 10 : 下單
All_df['收件地址-路段'] = ''
All_df['收件地址-門牌號碼'] = ''

for i in range(0,len(All_df)):
    All_df['收件地址'][i] = All_df['收件地址'][i].replace('号','號')
    All_df['收件地址-路段'][i] = All_df['收件地址'].str.split('號')[i][0]
    All_df['收件地址-門牌號碼'][i] = All_df['收件地址'].str.split('號')[i][1].replace(',','-')

    
ready_df = All_df[All_df['平台可承接與否'] == '可以']
ready_df = ready_df.reset_index(drop = True)
u = ready_df['路線名稱'].unique()

ready_df_list = {}
notes = {}
for i in range(0,len(u)):
    ready_df_draft = ready_df[ready_df['路線名稱'] == u[i]]
    ready_df_draft = ready_df_draft.sort_values(by = ['配送路順'])
    ready_df_list[i] = ready_df_draft.reset_index(drop = True)
    notes[i] = '📦 路線代碼：' + ready_df_list[i]['路線名稱'][0] + ' // 請至' + ready_df_list[i]['訂單編號'][0] + '取件，取件編號：' + str(list(ready_df_list[i]['訂單編號'][1:])) +                '，取件後，各地址送件編號依序為：' + str(list(ready_df_list[i]['訂單編號'][1:])) + ' // 💡 不一定要按照路順配送，但要留意不要送錯件喔～ ⚠️ 請於35分之前至取件點完成取件，超過取件時間仍未取件將會自動取消訂單'
    


# In[156]:


import requests

url = "https://tw-api.gogox.com/oauth/token"

payload = {
    "grant_type": "client_credentials",
    "client_id": "bcexxxxxxxx4",
    "client_secret": "9xxxx5dfxxxxxxx2"
}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

import json
res = json.loads(response.text)
token = 'Bearer ' + res['access_token']
payment_method = "monthly_settlement"
order_id_list = {}

for i in range(0,len(ready_df_list)):
    if len(ready_df_list[i]) == 2:
        url = "https://tw-api.gogox.com/transport/orders"

        payload = {
            "pickup": {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][0],
                    "lng": ready_df_list[i]['Longitude'][0]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][0],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][0]
                    },
                #"schedule_at": 0,
                "street_address": ready_df_list[i]['收件地址-路段'][0],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][0],
                "name": ready_df_list[i]['訂單編號'][0]
                },
    
            "destinations": [
            # dropoff point 1
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][1],
                    "lng": ready_df_list[i]['Longitude'][1]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][1],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][1]
                    },
                "name": ready_df_list[i]['備註'][1],
                "street_address": ready_df_list[i]['收件地址-路段'][1],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][1]
                }
                
            ],
            "extra_requirements": {"delivery_box": True},
            "vehicle_type": "motorcycle",
            "payment_method": payment_method,
            "note_to_courier": notes[i]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": token
            }

        response = requests.request("POST", url, json=payload, headers=headers)

        order_id_list[i] = json.loads(response.text)['id']
    
    
    elif len(ready_df_list[i]) == 3:
        
        url = "https://tw-api.gogox.com/transport/orders"

        payload = {
            "pickup": {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][0],
                    "lng": ready_df_list[i]['Longitude'][0]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][0],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][0]
                    },
                #"schedule_at": 0,
                "street_address": ready_df_list[i]['收件地址-路段'][0],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][0],
                "name": ready_df_list[i]['訂單編號'][0]
                },
    
            "destinations": [
            # dropoff point 1
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][1],
                    "lng": ready_df_list[i]['Longitude'][1]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][1],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][1]
                    },
                "name": ready_df_list[i]['備註'][1],
                "street_address": ready_df_list[i]['收件地址-路段'][1],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][1]
                },
             # dropoff point 2   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][2],
                    "lng": ready_df_list[i]['Longitude'][2]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][2],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][2]
                    },
                "name": ready_df_list[i]['備註'][2],
                "street_address": ready_df_list[i]['收件地址-路段'][2],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][2]
                }
                
            ],
            "extra_requirements": {"delivery_box": True},
            "vehicle_type": "motorcycle",
            "payment_method": payment_method,
            "note_to_courier": notes[i]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": token
            }

        response = requests.request("POST", url, json=payload, headers=headers)

        order_id_list[i] = json.loads(response.text)['id']
        
        
    elif len(ready_df_list[i]) == 4:
        
        url = "https://tw-api.gogox.com/transport/orders"

        payload = {
            "pickup": {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][0],
                    "lng": ready_df_list[i]['Longitude'][0]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][0],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][0]
                    },
                #"schedule_at": 0,
                "street_address": ready_df_list[i]['收件地址-路段'][0],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][0],
                "name": ready_df_list[i]['訂單編號'][0]
                },
    
            "destinations": [
            # dropoff point 1
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][1],
                    "lng": ready_df_list[i]['Longitude'][1]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][1],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][1]
                    },
                "name": ready_df_list[i]['備註'][1],
                "street_address": ready_df_list[i]['收件地址-路段'][1],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][1]
                },
             # dropoff point 2   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][2],
                    "lng": ready_df_list[i]['Longitude'][2]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][2],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][2]
                    },
                "name": ready_df_list[i]['備註'][2],
                "street_address": ready_df_list[i]['收件地址-路段'][2],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][2]
                },
            # dropoff point 3   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][3],
                    "lng": ready_df_list[i]['Longitude'][3]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][3],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][3]
                    },
                "name": ready_df_list[i]['備註'][3],
                "street_address": ready_df_list[i]['收件地址-路段'][3],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][3]
                }
                
            ],
            "extra_requirements": {"delivery_box": True},
            "vehicle_type": "motorcycle",
            "payment_method": payment_method,
            "note_to_courier": notes[i]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": token
            }

        response = requests.request("POST", url, json=payload, headers=headers)

        order_id_list[i] = json.loads(response.text)['id']    
        
        
    elif len(ready_df_list[i]) == 5:
        
        url = "https://tw-api.gogox.com/transport/orders"

        payload = {
            "pickup": {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][0],
                    "lng": ready_df_list[i]['Longitude'][0]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][0],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][0]
                    },
                #"schedule_at": 0,
                "street_address": ready_df_list[i]['收件地址-路段'][0],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][0],
                "name": ready_df_list[i]['訂單編號'][0]
                },
    
            "destinations": [
            # dropoff point 1
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][1],
                    "lng": ready_df_list[i]['Longitude'][1]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][1],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][1]
                    },
                "name": ready_df_list[i]['備註'][1],
                "street_address": ready_df_list[i]['收件地址-路段'][1],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][1]
                },
             # dropoff point 2   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][2],
                    "lng": ready_df_list[i]['Longitude'][2]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][2],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][2]
                    },
                "name": ready_df_list[i]['備註'][2],
                "street_address": ready_df_list[i]['收件地址-路段'][2],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][2]
                },
            # dropoff point 3   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][3],
                    "lng": ready_df_list[i]['Longitude'][3]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][3],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][3]
                    },
                "name": ready_df_list[i]['備註'][3],
                "street_address": ready_df_list[i]['收件地址-路段'][3],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][3]
                },  
            # dropoff point 4   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][4],
                    "lng": ready_df_list[i]['Longitude'][4]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][4],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][4]
                    },
                "name": ready_df_list[i]['備註'][4],
                "street_address": ready_df_list[i]['收件地址-路段'][4],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][4]
                }
                
            ],
            "extra_requirements": {"delivery_box": True},
            "vehicle_type": "motorcycle",
            "payment_method": payment_method,
            "note_to_courier": notes[i]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": token
            }

        response = requests.request("POST", url, json=payload, headers=headers)

        order_id_list[i] = json.loads(response.text)['id']     
        
        
    elif len(ready_df_list[i]) == 6:
        
        url = "https://tw-api.gogox.com/transport/orders"

        payload = {
            "pickup": {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][0],
                    "lng": ready_df_list[i]['Longitude'][0]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][0],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][0]
                    },
                #"schedule_at": 0,
                "street_address": ready_df_list[i]['收件地址-路段'][0],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][0],
                "name": ready_df_list[i]['訂單編號'][0]
                },
    
            "destinations": [
            # dropoff point 1
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][1],
                    "lng": ready_df_list[i]['Longitude'][1]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][1],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][1]
                    },
                "name": ready_df_list[i]['備註'][1],
                "street_address": ready_df_list[i]['收件地址-路段'][1],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][1]
                },
             # dropoff point 2   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][2],
                    "lng": ready_df_list[i]['Longitude'][2]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][2],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][2]
                    },
                "name": ready_df_list[i]['備註'][2],
                "street_address": ready_df_list[i]['收件地址-路段'][2],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][2]
                },
            # dropoff point 3   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][3],
                    "lng": ready_df_list[i]['Longitude'][3]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][3],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][3]
                    },
                "name": ready_df_list[i]['備註'][3],
                "street_address": ready_df_list[i]['收件地址-路段'][3],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][3]
                },  
            # dropoff point 4   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][4],
                    "lng": ready_df_list[i]['Longitude'][4]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][4],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][4]
                    },
                "name": ready_df_list[i]['備註'][4],
                "street_address": ready_df_list[i]['收件地址-路段'][4],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][4]
                },
            # dropoff point 5   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][5],
                    "lng": ready_df_list[i]['Longitude'][5]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][5],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][5]
                    },
                "name": ready_df_list[i]['備註'][5],
                "street_address": ready_df_list[i]['收件地址-路段'][5],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][5]
                }
                
            ],
            "extra_requirements": {"delivery_box": True},
            "vehicle_type": "motorcycle",
            "payment_method": payment_method,
            "note_to_courier": notes[i]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": token
            }

        response = requests.request("POST", url, json=payload, headers=headers)

        order_id_list[i] = json.loads(response.text)['id']   
        
        
    elif len(ready_df_list[i]) == 7:
        
        url = "https://tw-api.gogox.com/transport/orders"

        payload = {
            "pickup": {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][0],
                    "lng": ready_df_list[i]['Longitude'][0]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][0],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][0]
                    },
                #"schedule_at": 0,
                "street_address": ready_df_list[i]['收件地址-路段'][0],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][0],
                "name": ready_df_list[i]['訂單編號'][0]
                },
    
            "destinations": [
            # dropoff point 1
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][1],
                    "lng": ready_df_list[i]['Longitude'][1]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][1],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][1]
                    },
                "name": ready_df_list[i]['備註'][1],
                "street_address": ready_df_list[i]['收件地址-路段'][1],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][1]
                },
             # dropoff point 2   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][2],
                    "lng": ready_df_list[i]['Longitude'][2]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][2],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][2]
                    },
                "name": ready_df_list[i]['備註'][2],
                "street_address": ready_df_list[i]['收件地址-路段'][2],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][2]
                },
            # dropoff point 3   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][3],
                    "lng": ready_df_list[i]['Longitude'][3]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][3],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][3]
                    },
                "name": ready_df_list[i]['備註'][3],
                "street_address": ready_df_list[i]['收件地址-路段'][3],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][3]
                },  
            # dropoff point 4   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][4],
                    "lng": ready_df_list[i]['Longitude'][4]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][4],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][4]
                    },
                "name": ready_df_list[i]['備註'][4],
                "street_address": ready_df_list[i]['收件地址-路段'][4],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][4]
                },
            # dropoff point 5   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][5],
                    "lng": ready_df_list[i]['Longitude'][5]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][5],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][5]
                    },
                "name": ready_df_list[i]['備註'][5],
                "street_address": ready_df_list[i]['收件地址-路段'][5],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][5]
                },
            # dropoff point 6   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][6],
                    "lng": ready_df_list[i]['Longitude'][6]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][6],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][6]
                    },
                "name": ready_df_list[i]['備註'][6],
                "street_address": ready_df_list[i]['收件地址-路段'][6],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][6]
                }
                
            ],
            "extra_requirements": {"delivery_box": True},
            "vehicle_type": "motorcycle",
            "payment_method": payment_method,
            "note_to_courier": notes[i]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": token
            }

        response = requests.request("POST", url, json=payload, headers=headers)

        order_id_list[i] = json.loads(response.text)['id']
        
        
    elif len(ready_df_list[i]) == 8:
        
        url = "https://tw-api.gogox.com/transport/orders"

        payload = {
            "pickup": {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][0],
                    "lng": ready_df_list[i]['Longitude'][0]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][0],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][0]
                    },
                #"schedule_at": 0,
                "street_address": ready_df_list[i]['收件地址-路段'][0],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][0],
                "name": ready_df_list[i]['訂單編號'][0]
                },
    
            "destinations": [
            # dropoff point 1
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][1],
                    "lng": ready_df_list[i]['Longitude'][1]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][1],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][1]
                    },
                "name": ready_df_list[i]['備註'][1],
                "street_address": ready_df_list[i]['收件地址-路段'][1],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][1]
                },
             # dropoff point 2   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][2],
                    "lng": ready_df_list[i]['Longitude'][2]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][2],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][2]
                    },
                "name": ready_df_list[i]['備註'][2],
                "street_address": ready_df_list[i]['收件地址-路段'][2],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][2]
                },
            # dropoff point 3   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][3],
                    "lng": ready_df_list[i]['Longitude'][3]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][3],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][3]
                    },
                "name": ready_df_list[i]['備註'][3],
                "street_address": ready_df_list[i]['收件地址-路段'][3],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][3]
                },  
            # dropoff point 4   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][4],
                    "lng": ready_df_list[i]['Longitude'][4]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][4],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][4]
                    },
                "name": ready_df_list[i]['備註'][4],
                "street_address": ready_df_list[i]['收件地址-路段'][4],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][4]
                },
            # dropoff point 5   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][5],
                    "lng": ready_df_list[i]['Longitude'][5]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][5],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][5]
                    },
                "name": ready_df_list[i]['備註'][5],
                "street_address": ready_df_list[i]['收件地址-路段'][5],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][5]
                },
            # dropoff point 6   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][6],
                    "lng": ready_df_list[i]['Longitude'][6]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][6],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][6]
                    },
                "name": ready_df_list[i]['備註'][6],
                "street_address": ready_df_list[i]['收件地址-路段'][6],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][6]
                },
            # dropoff point 7   
                {
                "location": {
                    "lat": ready_df_list[i]['Latitude'][7],
                    "lng": ready_df_list[i]['Longitude'][7]
                    },
                "contact": {
                    "name": ready_df_list[i]['收件人'][7],
                    "phone_number": '0' + ready_df_list[i]['收件人手機'][7]
                    },
                "name": ready_df_list[i]['備註'][7],
                "street_address": ready_df_list[i]['收件地址-路段'][7],
                "floor_or_unit_number": ready_df_list[i]['收件地址-門牌號碼'][7]
                },
                
            ],
            "extra_requirements": {"delivery_box": True},
            "vehicle_type": "motorcycle",
            "payment_method": payment_method,
            "note_to_courier": notes[i]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": token
            }

        response = requests.request("POST", url, json=payload, headers=headers)

        order_id_list[i] = json.loads(response.text)['id']
        


# In[1]:


i


# In[20]:


# 11 : 改訂單價格 >> 有可能不需要跑
# import selenium chromedriver
"""
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select 
import requests
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np 

# Load Google Spreadsheet
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

Admin_User_Email = str('xxxxxx')
Admin_User_Password = str('xxxxxxxx')
SCROLL_PAUSE_TIME = 1

browser = webdriver.Chrome(executable_path='xxxxxx')
browser.get('xxxxxxxx')
browser.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser.find_element_by_xpath('//*[@id="admin_user_submit_action"]/input').click()

for i in range(0,len(order_id_list)):
    browser.get('xxxxxxxxx' + str(order_id_list[i]) + '/edit')
    time.sleep(1)
    price = str(ready_df_list[i]['訂單單價'].sum()*((len(ready_df_list[i])-1)/len(ready_df_list[i])))
    browser.find_element_by_id("order_request_price_incl_vat").clear()
    browser.find_element_by_id("order_request_price_incl_vat").send_keys(price)
    browser.find_element_by_id("order_request_price_ex").clear()
    browser.find_element_by_id("order_request_price_ex").send_keys(price)
    browser.find_element_by_id("order_request_customer_price").clear()
    browser.find_element_by_id("order_request_customer_price").send_keys(price)
    browser.find_element_by_xpath('//*[@id="order_request_submit_action"]/input').click()
    time.sleep(2)

browser.close()
"""


# In[157]:


# 12-1 : 貨態回拋1
join_df = ready_df[ready_df['備註'] != '']
join_df = join_df.reset_index(drop = True)
join_df = join_df[['訂單編號','備註']]
join_df.columns = ['訂單編號','Remark']
join_df['訂單編號連結'] = '-'
for i in range(0,len(join_df)):
    link = 'http://xxxxxxxxx?shipment_no=' + str(int(join_df['訂單編號'][i]))
    join_df.iloc[i,join_df.columns.get_loc('訂單編號連結')] = link

from selenium import webdriver
from selenium.webdriver import ActionChains

Admin_User_Email1 = 'xxxxxxxx'
Admin_User_Password1 = 'xxxxxxxxx'
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument('--headless') # 啟動無頭模式
browser = webdriver.Chrome(executable_path='xxxxxxxxxxxxx', options=chrome_options)
join_df['託運單連結'] = '-'

browser.get('xxxxxxxxxxxxx')
time.sleep(1)
browser.find_element_by_xpath('/html/body/div/div/form/div[1]/input').send_keys(Admin_User_Email1)
browser.find_element_by_xpath('/html/body/div/div/form/div[2]/input').send_keys(Admin_User_Password1)
browser.find_element_by_xpath('/html/body/div/div/form/div[3]/div[2]/button').click()

for i in range(0,len(join_df)):    
    browser.get(join_df['訂單編號連結'][i])
    time.sleep(3)
    try:
        browser.find_element_by_xpath('/html/body/div[1]/div/section[2]/div[3]/div[1]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr/td[2]/a[1]').click()
        browser.switch_to_window(browser.window_handles[-1])
    except:
        browser.get(join_df['訂單編號連結'][i])
        time.sleep(3)
        browser.find_element_by_xpath('/html/body/div[1]/div/section[2]/div[3]/div[1]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr/td[2]/a[1]').click()
        browser.switch_to_window(browser.window_handles[-1])
    join_df['託運單連結'][i] = browser.current_url + '/edit'
    
browser.close()


# In[ ]:


# 12-2 : 貨態回拋2
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select 
import requests
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np 

# Load Google Spreadsheet
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

Admin_User_Email = str('xxxxxxxx')
Admin_User_Password = str('xxxxxxxxxx')
SCROLL_PAUSE_TIME = 1
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument('--headless') # 啟動無頭模式

browser = webdriver.Chrome(executable_path='xxxxxxxxxx',options=chrome_options)
browser.get('xxxxxxxxxxxxx')
browser.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser.find_element_by_xpath('//*[@id="admin_user_submit_action"]/input').click()

import ast

while True:
    #waypoint_df_list = {}
    
    for k in range(0,len(order_id_list)):
        browser.get('xxxxxxxxx' + str(order_id_list[k]))
        time.sleep(3)
        html = browser.page_source
        soup = BeautifulSoup(html,"lxml")
        group_block = soup.find_all('table')
        
        try:
            t = group_block[7] #active order
            elements = {}
            rows = []
            for tr in t.findAll('tr'):
                elements[tr] = tr.getText()
            columns = list(elements.values())[0].replace('\n',',').split(',')
            for i in range(1,len(elements)):
                rows.append(list(elements.values())[i].replace(', 2021','- 2021').replace('\n',',').split(','))
            time.sleep(1)
            waypoint_df = pd.DataFrame(rows)
            
            for i in range(0,len(waypoint_df)):
                try:
                    if waypoint_df[16][i] == None:
                        continue
                    elif waypoint_df[16][i] == '':
                        for j in range(4,len(waypoint_df.iloc[i,:])-1):
                            waypoint_df.iloc[i,j] = waypoint_df.iloc[i,j+1]
                except:
                    continue

            try:
                waypoint_df = waypoint_df.drop(16, axis = 1)
            except:
                waypoint_df = waypoint_df
            
            
            waypoint_df.columns = columns
            html = browser.page_source
            soup = BeautifulSoup(html,"lxml")
            group_block = soup.find_all('td',attrs={'class':'col col-signature'})
            
            for p in range(0,len(waypoint_df)):
                try:
                    pp = ast.literal_eval(group_block[p].find('a').get('data-image-urls'))[0]
                except:
                    pp = '-'
                waypoint_df.iloc[p,waypoint_df.columns.get_loc('Signature')] = pp
                #waypoint_df['Signature'][]
        
            waypoint_info_df = pd.merge(waypoint_df, join_df)
        
            stat_df = waypoint_info_df[waypoint_info_df['Signature'] != '-']
            stat_df = stat_df.reset_index(drop = True)
            pass
            
            
        except:
            t = group_block[8] # non active order
            elements = {}
            rows = []
            for tr in t.findAll('tr'):
                elements[tr] = tr.getText()
            columns = list(elements.values())[0].replace('\n',',').split(',')
            for i in range(1,len(elements)):
                rows.append(list(elements.values())[i].replace(', 2021','- 2021').replace('\n',',').split(','))
            time.sleep(1)
            waypoint_df = pd.DataFrame(rows)
            
            for i in range(0,len(waypoint_df)):
                try:
                    if waypoint_df[16][i] == None:
                        continue
                    elif waypoint_df[16][i] == '':
                        for j in range(4,len(waypoint_df.iloc[i,:])-1):
                            waypoint_df.iloc[i,j] = waypoint_df.iloc[i,j+1]
                except:
                    continue

            try:
                waypoint_df = waypoint_df.drop(16, axis = 1)
            except:
                waypoint_df = waypoint_df
            
            
            waypoint_df.columns = columns
            html = browser.page_source
            soup = BeautifulSoup(html,"lxml")
            group_block = soup.find_all('td',attrs={'class':'col col-signature'})
            
            for p in range(0,len(waypoint_df)):
                try:
                    pp = ast.literal_eval(group_block[p].find('a').get('data-image-urls'))[0]
                except:
                    pp = '-'
                waypoint_df.iloc[p,waypoint_df.columns.get_loc('Signature')] = pp
                #waypoint_df['Signature'][]
        
            waypoint_info_df = pd.merge(waypoint_df, join_df)
        
            stat_df = waypoint_info_df[waypoint_info_df['Signature'] != '-']
            stat_df = stat_df.reset_index(drop = True)
            pass

        
        
        try:
            for q in range(0,len(stat_df)):
                browser2 = webdriver.Chrome(executable_path='xxxxxxxxxxx',options=chrome_options)
                browser2.get(stat_df['託運單連結'][q])
                time.sleep(1)
                browser2.find_element_by_xpath('/html/body/div/div/form/div[1]/input').send_keys(Admin_User_Email1)
                browser2.find_element_by_xpath('/html/body/div/div/form/div[2]/input').send_keys(Admin_User_Password1)
                browser2.find_element_by_xpath('/html/body/div/div/form/div[3]/div[2]/button').click()
                browser2.get(stat_df['託運單連結'][q])
                time.sleep(5)
                
                browser2.find_element_by_xpath('//*[@id="status"]/option[5]').click()
                browser2.find_element_by_xpath('//*[@id="owner_id"]/option[2]').click()
                l1 = stat_df['Signature'][q].split('Fap')[0]
                l2 = 'Fap' + stat_df['Signature'][q].split('Fap')[1]
                browser2.find_element_by_xpath('//*[@id="shipment_form"]/div[9]/div[2]/div/textarea').clear()
                browser2.find_element_by_xpath('//*[@id="shipment_form"]/div[9]/div[2]/div/textarea').send_keys(l1)
                browser2.find_element_by_xpath('//*[@id="get_memo"]').clear()
                browser2.find_element_by_xpath('//*[@id="get_memo"]').send_keys(l2)
                browser2.find_element_by_xpath('//*[@id="btn_submit"]').click()
                time.sleep(5)
                browser2.close()
        except:
            continue
        
        print(k)
        
    


# In[ ]:





# In[ ]:





# In[141]:


join_df


# In[89]:


stat_df


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# 0 : Build Pseudo Shipments
"""
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import numpy as np
import math
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', None)


    # The scope is always look like this so we did not need to change anything
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # Name of our Service Account Key
    # https://console.developers.xxxxxxxxx
google_key_file = 'xxxxxxxxxxxxxx'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

    # Opening the worksheet by using Worksheet ID
workbook = gc.open_by_key('xxxxxxxxxx')

    # Selecting which sheet to pulling the data
sheet = workbook.worksheet('orders')

    # Pulling the data and transform it to the data frame
values = sheet.get_all_values()
df = pd.DataFrame(values[:], columns = values[0])
df = df[1:]
df['Longitude'] = df['Longitude'].astype(np.float64)
df['Latitude'] = df['Latitude'].astype(np.float64)
df = df[(df['Latitude'] >= 24.7) & (df['Latitude'] < 25.3) & (df['Longitude'] < 122.0) & (df['Longitude'] >= 121.2)]  # TPE Area
df = df.reset_index(drop = True)
#
df = df.iloc[0,:]
df = pd.DataFrame(df).T

res_list = {}
for i in range(0,len(df)):
    columns = ['original_id','ship_no','pics','weight','address','zip_code','city_name','zip_name','put_name','area_code','phone','ext','mobile','goods_items','content','memo','get_city','get_zip_code','get_zip','get_address','cod','warehouse_city_name','warehouse_zip_name','warehouse_address','pickup']
    values = {0:df['訂單編號'][i], 1:None ,2:1,3:0,4:df['收件地址'][i], 5:"10685", 6:"台北市", 7:"大安區", 8:df['收件人'][i], 9:None, 10:'0'+df['收件人手機'][i], 11:0, 12:'0'+df['收件人手機'][i], 13:{df['訂單編號'][i][:7]:df['品項'][i]}, 14:df['備註'][i], 15:df['客戶備註'][i], 16:None, 17:"243", 18:None, 19:'新北市泰山區新北大道六段196號之6', 20:0, 21:None, 22:None, 23:None, 24:0 }
    #7:df['收件地區'][i]
    w = pd.DataFrame.from_dict(values,orient='index').T
    w.columns = columns
    res_list[i] = w.to_dict('records')[0] 

    
import requests
import hashlib
import json
for i in range(0,len(res_list)):
    data = []
    data.append(res_list[i])
    data1 = str(data).replace("'",'"').replace("None","null").replace(' ','')
    data2 = 'gogo' + data1
    
    
    hl = hashlib.md5()
    hl.update( data2.encode(encoding = 'utf-8'))

    url = "http://gogovantw.com/api/order"
    payload={'data': str(data1),
    'check_sum': hl.hexdigest()}
    files=[
    ]
    headers = {
      'Authorization': 'xxxxxxxxxxxxx'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    
    print(response.text)
"""


# In[ ]:



# In[ ]:




