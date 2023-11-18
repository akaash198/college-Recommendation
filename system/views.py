from django.shortcuts import render
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from django.utils.datastructures import MultiValueDictKeyError

import warnings
warnings.filterwarnings('ignore')
# Create your views here.
def home(request):
    return render(request,'home.html')
def home1(request):
    return render(request,'home1.html')
def home2(request):
    return render(request,'home2.html')
def branch(request):
    return render(request,'branch.html')
def college(request):
    return render(request,'college.html')
def empty(request):
  return render(request,'empty.html')

def main(request):
    return render(request,'main.html')

def recommend(AM,COM,BC):
    data = pd.read_csv('college.csv',usecols=['AM','RANK','COM','CGCODE','CGNAME','BC','AC'])
    data = data.dropna(axis = 0, subset = ['CGNAME'])
    ae=AM-8
    ad=AM+9
    rt=data[(data.AM >=ae)&(data.AM <=ad) & (data.COM ==COM) &(data.BC==BC)]
    features_df=rt.pivot_table(index=['CGNAME'],columns=['COM'],values='AM',aggfunc='count').fillna(0)
    features_df.sort_values(COM, axis = 0, ascending = False,
                inplace = True, na_position ='last')
    features_df.reindex(features_df[COM].sort_values(ascending=False).index)
    result=features_df.index.tolist()
    result1=features_df[COM].tolist() 
    return result[0:3],result1[0:3]

def result(request):
    if request.method == 'GET':
        try:
            AM = float(request.GET['AM'])
            COM = str(request.GET['COM'])
            BC = str(request.GET['BC'])
            result = recommend(AM,COM,BC)
            result1=result[0][0]
            ts1=result[1][0]
            result2=result[0][1]
            ts2=result[1][1]
            result3=result[0][2]
            ts3=result[1][2]
            return render(request,'college.html',{'result1':result1,'ts1':ts1,'result2':result2,'ts2':ts2,'result3':result3,'ts3':ts3,'AM':AM,'COM':COM,'BC':BC})
        except:
            return render(request,'empty.html')
    else:
        return render(request,'empty.html')
 
 
def brancRecommend(AM,COM):
    data1 = pd.read_csv('college2.csv',usecols=['AM','RANK','COM','CGCODE','BRC','AC'])
    data1 = data1.dropna(axis = 0, subset = ['BRC'])
    ae=AM-10
    ad=AM+10
    rt=data1[(data1.AM >=ae)&(data1.AM <=ad) & (data1.COM ==COM)]
    features_df=rt.pivot_table(index=['BRC'],columns=['COM'],values='AM',aggfunc='count').fillna(0)
    features_df.sort_values(COM, axis = 0, ascending = False,
                inplace = True, na_position ='last')
    # features_df.sort_values("BC", axis = 0, ascending = False,
    #              inplace = True, na_position ='last')
    features_df.reindex(features_df[COM].sort_values(ascending=False).index)
    bresult=features_df.index.tolist()
    bresult1=features_df[COM].tolist() 
    return bresult[0:3],bresult1[0:3]

def bresult(request):
    if request.method == 'GET':
        try:
            AM = float(request.GET['AM'])
            COM = str(request.GET['COM'])
            bresult = brancRecommend(AM,COM)
            bresult1=bresult[0][0]
            rs1=bresult[1][0]
            bresult2=bresult[0][1]
            rs2=bresult[1][1]
            bresult3=bresult[0][2]
            rs3=bresult[1][2]
            return render(request,'branch.html',{'bresult1':bresult1,'rs1':rs1,'bresult2':bresult2,'rs2':rs2,'bresult3':bresult3,'rs3':rs3,'AM':AM,'COM':COM})
        except:
            return render(request,'empty.html')
    else:
        return render(request,'empty.html')
def locationRecommend(AM,COM,BC,location):
    data2=pd.read_csv('college1.csv',usecols=['AM','RANK','COM','CGCODE','CGNAME','BC','location'])
    data2 = data2.dropna(axis = 0, subset = ['CGNAME'])
    ae=AM-15
    ad=AM+15
    rt=data2[(data2.AM >=ae)&(data2.AM <=ad) & (data2.COM ==COM) &(data2.BC==BC) & (data2.location==location)]
    features_df=rt.pivot_table(index=['CGNAME'],columns=['COM'],values='AM',aggfunc='count').fillna(0)
    features_df.sort_values(COM, axis = 0, ascending = False,
                inplace = True, na_position ='last')
    data_features_df_matrix = csr_matrix(features_df.values)
    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    model_knn.fit(data_features_df_matrix)
    query_index = np.random.choice(features_df.shape[0])
    distances, indices = model_knn.kneighbors(features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors =4)
    for i in range(0, len(distances.flatten())):
        features_df.index[indices]
        result=features_df.index[indices].tolist()
    result=features_df.index.tolist()
    result1=features_df[COM].tolist()
    return result[0:3],result1[0:3]

def lresult(request):
    if request.method == 'GET':
        try:
            AM = float(request.GET['AM'])
            COM = str(request.GET['COM'])
            BC = str(request.GET['BC'])
            location = str(request.GET['location'])
            result = locationRecommend(AM,COM,BC,location)
            result1=result[0][0]
            ts1=result[1][0]
            result2=result[0][1]
            ts2=result[1][1]
            result3=result[0][2]
            ts3=result[1][2]
            return render(request,'location.html',{'result1':result1,'ts1':ts1,'result2':result2,'ts2':ts2,'result3':result3,'ts3':ts3,'AM':AM,'COM':COM,'BC':BC,'location':location})
        except:
            return render(request,'empty.html')
    else:
        return render(request,'empty.html')
    
