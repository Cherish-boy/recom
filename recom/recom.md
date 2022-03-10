

#### 查询企业详情信息

```python
#返回所有字段
#具体使用哪些字段由前端负责筛选

#查询企业详情
def search_company(request):
    company = request.GET.get('company',None)
    sql = 'select name,legal_person,contacts,phone,email,regis_time,regis_capital,credit_code,tax_iden_number,industry,kind,size,address,scope,number from company where name = ' + '"' + company + '"'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    print(result)
    return HttpResponse(json.dumps(result[0]))

url
   #查询企业信息
    path('index/gongsi/',views.search_company,name = 'gongsi'),
    
#返回数据如下：
```

![image-20220308184137304](C:\Users\29242\AppData\Roaming\Typora\typora-user-images\image-20220308184137304.png)



#### 查询政策详情

```python
#返回所有字段
#具体使用哪些字段由前端负责筛选

#查询政策详情
def search_policy(request):
    policy = request.GET.get('policy', None)
    sql = 'select * from policy where title = ' + '"' + policy + '"'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    return HttpResponse(json.dumps(result[0]))

#url不变
#返回数据如下：
```

![image-20220308185242234](C:\Users\29242\AppData\Roaming\Typora\typora-user-images\image-20220308185242234.png)



#### 最热政策查询并返回

```python
#随机查询10条数据
#查询最热政策，返回所有字段，前端使用时选择
def search_hotpolicy(self):
    sql = 'select title,release_source,abstract from policy order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print(result[0])
    print(result)
    #result为元组带下标，其中每一个元素为json对象
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


#url
#最热政策
    path('hotpolicy/',views.search_hotpolicy,name = 'hotpolicy'),

#结果如下：
```

![image-20220308193436163](C:\Users\29242\AppData\Roaming\Typora\typora-user-images\image-20220308193436163.png)



#### 最热企业查询并返回

```python
#随机查询10条数据
#查询最热企业，返回所有字段，前端使用时选择
#查询最热企业
def search_hotcompany(self):
    sql = 'select name,industry,address from company order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    #result为元组带下标，其中每一个元素为json对象
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))

#url
#最热企业
    path('hotcompany/',views.search_hotcompany,name = 'hotcompany'),
#结果如下：
```

![image-20220308193957327](C:\Users\29242\AppData\Roaming\Typora\typora-user-images\image-20220308193957327.png)



#### 最新政策查询并返回

```python
#按照时间顺序查询最新政策并排序

#查询最新政策
def search_newpolicy(self):
    sql = 'select * from policy group by release_time desc,number desc limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    #result为元组带下标，其中每一个元素为json对象
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))

#url
#最新政策
    path('newpolicy/',views.search_newpolicy,name = 'newpolicy'),

#结果如下：（以release_time发布时间降序排序，有10个）
```

![image-20220308192941898](C:\Users\29242\AppData\Roaming\Typora\typora-user-images\image-20220308192941898.png)





#### 最新企业查询并返回

```python
#按照时间顺序查询最新企业并返回

#查询最新企业
def search_newcompany(self):
    sql = 'select * from company group by regis_time desc,number desc limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    #result为元组带下标，其中每一个元素为json对象
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))

#url
#最新企业
    path('newcompany/',views.search_newcompany,name = 'newcompany')

#结果如下：（以regis_time注册时间降序排序，有10个）
```

![image-20220308193143083](C:\Users\29242\AppData\Roaming\Typora\typora-user-images\image-20220308193143083.png)





#### 给企业推荐政策

```python
#企业名字跳转
#从已跑出的数据里查找得分最高的政策信息并按顺序返回
#给企业推荐政策（暂定10条）
def recom_policy(request):
    name = request.GET.get('name',None)
    sql = 'select number from company where name =' + '"' + name + '"'
    cursor.execute(sql)
    con_engine.commit()
    number = cursor.fetchall()  #获取所查询企业的编号
    # print(type(number))    #list型
    # print(type(number[0]))   #dict型
    # print(number[0]['number'])  #拿到企业的编号

    num = number[0]['number']
    with open('D:\科研/recom_system/recom\curd\工作簿1.csv', 'r') as f:
        reader = csv.reader(f)
        list = [row[num+1] for row in reader]  # row[x]中的x代表第几列，即企业标号（number），不过实际上row[3]代表2号企业
    #print(list)  #list为政策推荐得分的列表，
    tmp_list = copy.deepcopy(list)
    tmp_list.sort()
    max_index = [list.index(one) for one in tmp_list[::-1][:11]]
    # print(max_index)  #max_index为得分最高的政策的number排序列表 max_index[1]为第1政策的number，共10哥政策，最后一个编号为max_index[10]
    sql = 'select * from policy where number = '+ str(max_index[1]) + ' or '+ 'number = '+str(max_index[2])+ ' or '+ 'number = '+str(max_index[3])+ \
          ' or ' + 'number = ' + str(max_index[4])+ ' or ' + 'number = ' + str(max_index[5])+ ' or ' + 'number = ' + str(max_index[6])+ \
          ' or ' + 'number = ' + str(max_index[7])+ ' or ' + 'number = ' + str(max_index[8])+ \
          ' or ' + 'number = ' + str(max_index[9])+ ' or ' + 'number = ' + str(max_index[10])

    # print(sql)
    cursor.execute(sql)
    con_engine.commit()
    result= cursor.fetchall()
    # print(result)

    return HttpResponse(json.dumps(result))

#url
#给企业推荐政策
    path('recom/',views.recom_policy,name = 'recom')
#返回数据格式如下
```

![image-20220308224314986](C:\Users\29242\AppData\Roaming\Typora\typora-user-images\image-20220308224314986.png)
