import copy
import csv
import json
import pymysql
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render

con_engine = pymysql.connect(host='8.142.138.101',
                             user="root",
                             password="0552fe7ad2067bda",
                             database="database",
                             port=3306,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor  # 返回对象类型为json格式
                             )

# 使用cursor()方法获取游标
cursor = con_engine.cursor()


# 跳转Ajax页面
def test1(request):
    return render(request, 'test1.html')


# 处理Ajax请求
def ajax_params(request):
    # 接收参数
    name = request.POST.get('name')

    # 返回模板
    print(name)

    list2 = ['title', 'release_source', 'release_time', 'key_words', 'abstract', 'details', ]
    sql = 'select title,release_source,release_time,key_words,abstract,details from jincheng where title = ' + '"' + str(
        name) + '"'

    print(sql)
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    print(result)
    string1 = str(result)
    string2 = string1.replace("'", '').replace('(', '').replace(')', '').replace('“', '').replace('\\u2002', '')
    # print(string1)
    # print(string2)
    string = string2.split(',', 6)  # 元组类型
    # print(string)
    list3 = list(string)
    print(list3)
    dict1 = dict(zip(list2, list3))
    print(dict1)
    print(json.dumps(dict1))

    # 返回上下文数据
    context = dict1

    return render(request, 'test1.html', context)
    # return HttpResponse(json.dumps(dict1))


# 查询政策详情
def search_policy(request):
    policy = request.GET.get('policy', None)
    sql = 'select * from policy where title = ' + '"' + policy + '"'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    return HttpResponse(json.dumps(result[0]))


# 查询企业详情
def search_company(request):
    company = request.GET.get('company', None)
    sql = 'select * from company where name = ' + '"' + company + '"'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    print(result)
    return HttpResponse(json.dumps(result[0]))


# 查询最热政策
def search_hotpolicy(self):
    sql = 'select title,release_source,abstract from policy order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print(result[0])
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# search_title()

# 查询最热企业
def search_hotcompany(self):
    sql = 'select name,industry,address from company order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 查询最新政策
def search_newpolicy(self):
    sql = 'select * from policy group by release_time desc,number desc limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 查询最新企业
def search_newcompany(self):
    sql = 'select * from company group by regis_time desc,number desc limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 给企业推荐政策
def recom_policy(request):
    name = request.GET.get('name', None)
    sql = 'select number from company where name =' + '"' + name + '"'
    cursor.execute(sql)
    con_engine.commit()
    number = cursor.fetchall()  # 获取所查询企业的编号
    # print(type(number))    #list型
    # print(type(number[0]))   #dict型
    # print(number[0]['number'])  #拿到企业的编号

    num = number[0]['number']
    # print(num)
    line = linecache.getline("D:\科研/recom_system/recom/recom/result.csv",num+1)
    # print(line)
    list1 = line.split(",")
    # print(list1)

    min_index = [index for index,value in sorted(list(enumerate(list1)),key = lambda x:x[1])]  #政策编号倒序列表
    # print(min_index)
    max_index = list(reversed(min_index))
    # print(max_index)  # max_index为得分最高的政策的number排序列表 max_index[1]为第1政策number为max_index[1]-1，共10个政策，最后一个政策number为max_index[10]-1

    sql = 'select * from policy where number = ' + str(max_index[1]-1) + ' or ' + 'number = ' + str(max_index[2]-1) + ' or ' + 'number = ' + str(max_index[3]-1) + \
          ' or ' + 'number = ' + str(max_index[4]-1) + ' or ' + 'number = ' + str(max_index[5]-1) + ' or ' + 'number = ' + str(max_index[6]-1) + \
          ' or ' + 'number = ' + str(max_index[7]-1) + ' or ' + 'number = ' + str(max_index[8]-1) + \
          ' or ' + 'number = ' + str(max_index[9]-1) + ' or ' + 'number = ' + str(max_index[10]-1)

    print(sql)
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print(result)


# 查询带有关键字的企业（最多支持6个关键词）
# 前端搜索框初始化显示“请输入关键词，多个关键词请用空格隔开”
# 在字段name,legal_person,address,phone,scope,industry中查询
def kw_company(request):
    kw = request.GET.get('kw', None)
    kws = kw.split()  # 输入多个关键词以空格隔开，kws为列表
    # print(kws)
    length = len(kws)
    if length == 1:
        sql = 'select * from company where concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[0] + "%'" + 'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))

    if length == 2:
        sql = 'select * from company where concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[0] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[1] + "%'" + 'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))

    elif length == 3:
        sql = 'select * from company where concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[0] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[1] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[2] + "%'" + 'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))

    elif length == 4:
        sql = 'select * from company where concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[0] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[1] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[2] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[3] + "%'" + 'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))

    elif length == 5:
        sql = 'select * from company where concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[0] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[1] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[2] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[3] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[4] + "%'" + 'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))


    elif length == 6:
        sql = 'select * from company where concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[0] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[1] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[2] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[3] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[4] + "%'" + \
              'and concat(name,legal_person,address,phone,scope,industry) like ' + "'%" + kws[5] + "%'" + 'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))


# 查询带有关键字的政策（最多支持6个关键词搜索）
# 前端搜索框初始化显示“请输入关键词，多个关键词请用空格隔开”
# 在字段title,department,release_source,prefecture_city,key_words中查询
def kw_policy(request):

    kw = request.GET.get('kw', None)
    kws = kw.split()
    length = len(kws)

    if length == 1:
        sql = 'select * from policy where concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[0] + "%'" + \
              'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))

    if length == 2:
        sql = 'select * from policy where concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + \
              kws[0] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[1] + "%'" + 'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))

    if length == 3:
        sql = 'select * from policy where concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[0] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[1] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[2] + "%'" + 'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))

    if length == 4:
        sql = 'select * from policy where concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + \
              kws[0] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[1] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[2] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[3] + "%'" + 'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))

    if length == 5:
        sql = 'select * from policy where concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + \
              kws[0] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[1] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[2] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[3] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[4] + "%'" + 'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))

    if length == 6:
        sql = 'select * from policy where concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + \
              kws[0] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[1] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[2] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[3] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[4] + "%'" + \
              'and concat(title,department,release_source,prefecture_city,details,key_words) like ' + "'%" + kws[5] + "%'" + 'limit 20'

        print(sql)
        cursor.execute(sql)
        con_engine.commit()
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))


# 按照产业类型查找企业#
# 农林、牧、渔业
def search_agriculture(self):
    sql = 'select * from company where industry = " 农、林、牧、渔业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 批发和零售业
def search_wholesale(self):
    sql = 'select * from company where industry = " 批发和零售业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 文化和娱乐业
def search_amusement(self):
    sql = 'select * from company where industry = " 文化、体育和娱乐业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 建筑业
def search_building(self):
    sql = 'select * from company where industry like "%建筑业%" order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 教育业
def search_education(self):
    sql = 'select * from company where industry = "教育" order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 金融业
def search_finance(self):
    sql = 'select * from company where industry like "%金融业%" order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 卫生和社会工作业
def search_health_society(self):
    sql = 'select * from company where industry = " 卫生和社会工作 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 住宿和餐饮业
def search_hotel_restaurant(self):
    sql = 'select * from company where industry = " 住宿和餐饮业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 信息传输、软件和信息技术服务业
def search_information_transmission(self):
    sql = 'select * from company where industry = " 信息传输、软件和信息技术服务业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 租赁和商务服务业
def search_leasing_business_service(self):
    sql = 'select * from company where industry = " 租赁和商务服务业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 制造业
def search_manufacturing(self):
    sql = 'select * from company where industry like "%制造业%" order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 采矿业
def search_mining(self):
    sql = 'select * from company where industry like "%采矿业%" order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 电力、热力、燃气及水生产和供应业
def search_power(self):
    sql = 'select * from company where industry = " 电力、热力、燃气及水生产和供应业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 公共管理、社会保障和社会组织
def search_public_admin(self):
    sql = 'select * from company where industry = " 公共管理、社会保障和社会组织 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 房地产业
def search_real_estate(self):
    sql = 'select * from company where industry = " 房地产业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 居民服务、修理和其他服务业
def search_resident_service(self):
    sql = 'select * from company where industry = " 居民服务、修理和其他服务业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 科学研究和技术服务业
def search_science(self):
    sql = 'select * from company where industry = " 科学研究和技术服务业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 交通运输、仓储和邮政业
def search_traffic(self):
    sql = 'select * from company where industry = " 交通运输、仓储和邮政业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    # return HttpResponse(json.dumps(result[0]))
    return HttpResponse(json.dumps(result))


# 水利、环境和公共设施管理业
def search_water_conservancy(self):
    sql = 'select * from company where industry = " 水利、环境和公共设施管理业 " order by rand() limit 10'
    cursor.execute(sql)
    con_engine.commit()
    result = cursor.fetchall()
    # print (type(result[0]))
    print(result)
    return HttpResponse(json.dumps(result))
    # return JsonResponse(result[0])


# 返回图片给前端
# 点击企业名称跳转出现政策图谱表
def pic(request):
    name = request.GET.get('name',None)
    sql = 'select number from company where name = ' +'"' + name + '"'
    print(sql)
    cursor.execute(sql)
    con_engine.commit()
    number = cursor.fetchall()
    # print(number[0])
    # print(number[0]['number'])
    file = open('D:/科研/recom_system/recom/picture/'+ str(number[0]['number']) +'.png','rb')

    # file = open('D:\科研/recom_system/recom\picture/0.png','rb')
    response = HttpResponse(content=file.read(), content_type='image/jpeg')

    return response



def index(request):
    return render(request, '首页.html')


def form(request):
    return render(request, '搜索界面.html')


def muban(request):
    return render(request, 'muban.html')


def xiangqing(request):
    return render(request, '详细内容.html')


def company(request):
    return render(request, '公司.html')
