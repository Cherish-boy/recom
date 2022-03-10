from django.contrib import admin
from django.urls import path


from recom import views
from recom.views import search_policy

# #命名空间设置
# app_name = 'recom'

urlpatterns = [

    path('admin/', admin.site.urls),

   #测试首页
    path('index/',views.index),

    #测试公司界面
    path('gongsi/',views.company,name = 'gongsi'),



    #查询政策信息
    path('index/详细内容.html',search_policy),

    #查询企业信息
    path('index/gongsi/',views.search_company,name = 'gongsi'),

    #测试
    path('test1html/',views.test1,name = 'test1'),
    path('ajax_params/',views.ajax_params,name = 'ajax_params'),

    #页面
    path('xiangqing/',views.xiangqing,name = 'xiangqing'),


    #按类型查找企业
    #农林、牧、渔业
    path('agriculture/',views.search_agriculture,name='agriculture'),

    #批发和零售业
    path('wholesale/',views.search_wholesale,name = 'wholesale'),

    #文化、体育和娱乐业
    path('amusement/',views.search_amusement,name = 'amusement'),

    #建筑业
    path('building/',views.search_building,name = 'building'),

    #教育业
    path('education/',views.search_education,name = 'education'),

    #金融业
    path('finance/',views.search_finance,name = 'finance'),

    #卫生和社会工作业
    path('health_society/',views.search_health_society,name = 'health_society'),

    #住宿和餐饮业
    path('hotel_restaurant/',views.search_hotel_restaurant,name = 'hotel_restaurant'),

    #信息传输、软件和信息技术服务业
    path('information_transmission/',views.search_information_transmission,name ='information_transmission' ),

    #租赁和商务服务业
    path('leasing_business_service/',views.search_leasing_business_service,name = 'leasing_business_service'),

    #制造业
    path('manufacturing/',views.search_manufacturing,name = 'manufacturing'),

    #采矿业
    path('mining/',views.search_mining,name = 'mining'),

    #电力、热力、燃气及水生产和供应业
    path('power/',views.search_power,name = 'power'),

    #公共管理、社会保障和社会组织
    path('public_admin/',views.search_public_admin,name = 'public_admin'),

    #房地产业
    path('real_estate/',views.search_real_estate,name = 'real_estate'),

    #居民服务、修理和其他服务业
    path('resident_service/',views.search_resident_service,name = 'resident_service'),

    #科学研究和技术服务业
    path('science/',views.search_science,name = 'science'),

    #交通运输、仓储和邮政业
    path('traffic/',views.search_traffic,name = 'traffic'),

    #水利、环境和公共设施管理业
    path('water_conservancy/',views.search_water_conservancy,name = 'water_conservancy'),



    #最热政策
    path('hotpolicy/',views.search_hotpolicy,name = 'hotpolicy'),

    #最热企业
    path('hotcompany/',views.search_hotcompany,name = 'hotcompany'),

    #最新政策
    path('newpolicy/',views.search_newpolicy,name = 'newpolicy'),

    #最新企业
    path('newcompany/',views.search_newcompany,name = 'newcompany'),

    #给企业推荐政策
    path('recom/',views.recom_policy,name = 'recom'),

    #查询带有关键字的企业
    path('kwcompany/',views.kw_company,name = 'kwcompany'),

    #查询带有关键字的政策
    path('kwpolicy/',views.kw_policy,name = 'kwpolicy')


]
