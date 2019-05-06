# -*- coding: utf-8 -*-
from distribute.views import sendData
from searchInfo.items import FileItem
from scrapy.loader import ItemLoader
from datadeal.models import SpiderData
from selenium import webdriver
import scrapy
import urllib
import urllib2
import json
import re
import time

URL_DICT = {
    'http://www.jnfda.gov.cn/col/col6341/index.html':{
        'name':'jnfda',
        'domain':'www.jnfda.gov.cn',
        'list_xpath':'//*[@id="29920"]/div//a',
        'detail_xpath':'//*[@id="zoom"]//tr',
        'need_selenium':False,
    },
    'http://lx.jnfda.gov.cn/col/col1171/index.html':{
        'name':'jnfda',
        'domain':'lx.jnfda.gov.cn',
        'list_xpath':'//*[@id="2071"]/div//a',
        'detail_xpath':'//*[@id="zoom"]//tr',
        'need_selenium':False,
    },
    'http://sz.jnfda.gov.cn/col/col1408/index.html':{
        'name':'jnfda',
        'domain':'sz.jnfda.gov.cn',
        'list_xpath':'//*[@id="2302"]/div//a',
        'detail_xpath':'//*[@id="zoom"]//tr',
        'need_selenium':False,
    },
    'http://hy.jnfda.gov.cn/col/col1436/index.html':{
        'name':'jnfda',
        'domain':'hy.jnfda.gov.cn',
        'list_xpath':'//*[@id="container"]/table[5]//tr/td[3]/table[2]//a',
        'detail_xpath':'//*[@id="zoom"]//tr',
        'need_selenium':False,
    },
    'http://tq.jnfda.gov.cn/col/col1464/index.html':{
        'name':'jnfda',
        'domain':'tq.jnfda.gov.cn',
        'list_xpath':'//*[@id="15577"]/div//a',
        'detail_xpath':'//*[@id="container"]/table[6]//tr',
        'need_selenium':False,
    },
    'http://lc.jnfda.gov.cn/col/col1492/index.html':{
        'name':'jnfda',
        'domain':'lc.jnfda.gov.cn',
        'list_xpath':'//*[@id="15566"]/div//a',
        'detail_xpath':'//*[@id="zoom"]//tr',
        'need_selenium':False,
    },
    'http://zq.jnfda.gov.cn/col/col1576/index.html':{
        'name':'jnfda',
        'domain':'zq.jnfda.gov.cn',
        'list_xpath':'//*[@id="15511"]/div//a',
        'detail_xpath':'//*[@id="container"]/table[6]//tr',
        'need_selenium':False,
    },
    'http://py.jnfda.gov.cn/col/col1604/index.html':{
        'name':'jnfda',
        'domain':'py.jnfda.gov.cn',
        'list_xpath':'//*[@id="15497"]/div//a',
        'detail_xpath':'//*[@id="zoom"]//tr',
        'need_selenium':False,
    },
    'http://cq.jnfda.gov.cn/col/col1520/index.html':{
        'name':'jnfda',
        'domain':'cq.jnfda.gov.cn',
        'list_xpath':'//*[@id="15530"]//a',
        'detail_xpath':'/html/body//tr',
        'need_selenium':False,
    },
    'http://www.tzsfda.gov.cn/news6.asp?id=76&page=1':{
        'name':'tzsfda',
        'domain':'www.tzsfda.gov.cn',
        'list_xpath':'/html/body/table[2]//tr[2]/td[2]/table//tr/td/table[3]//tr[1]/td/table//tr/td[2]/table[2]//a',
        'detail_xpath':'/html/body/table[2]//tr[2]/td/table//tr/td/table//tr/td[1]/table[1]//tr',
        'need_selenium':False,
    },
    'http://www.dyfda.gov.cn/CL0223/':{
        'name':'dyfda',
        'domain':'www.dyfda.gov.cn',
        'list_xpath':'//*[@id="box"]/div/div[3]/div//a',
        'detail_xpath':'//*[@class="articlecontent1"]//tr',
        'need_selenium':False,
    },
    'http://hkfda.huanghekou.gov.cn/Get/zwgk/index.htm':{
        'name':'jnfda',
        'domain':'hkfda.huanghekou.gov.cn',
        'list_xpath':'//*[@id="content"]/table[2]//a',
        'detail_xpath':'//*[@id="content"]/table//tr',
        'need_selenium':False,
    },
    'http://www.wffda.gov.cn/ZWGK/GST/HHB/XZCF/index.html':{
        'name':'wffda',
        'domain':'www.wffda.gov.cn',
        'list_xpath':'/html/body/div[3]/table//tr/td[3]/div[2]/table//a',
        'detail_xpath':'/html/body/div[3]/table//tr/td/div[2]//tr',
        'need_selenium':False,
    },
    'http://www.weihaifda.gov.cn/col/col14562/index.html':{
        'name':'weihaifda',
        'domain':'www.weihaifda.gov.cn',
        'list_xpath':'/html/body/div[2]/div[2]//a',
        'detail_xpath':'/html/body/div[2]/div[2]/div[2]/table[1]//tr',
        'need_selenium':True,
    },
    'http://xxgk.eweihai.gov.cn/news_list.aspx?t=77':{
        'name':'jnfda',
        'domain':'xxgk.eweihai.gov.cn',
        'list_xpath':'//*[@id="newsquery"]//a',
        'detail_xpath':'//*[@id="rightside"]/div[2]/div[3]/table//tr',
        'need_selenium':False,
    },
    'http://dcfda.gov.cn/n3922434/n3922580/index.html?COLLCC=705750791&':{
        'name':'jnfda',
        'domain':'dcfda.gov.cn',
        'list_xpath':'/html/body/div[3]/div/div[2]/table//tr/td[1]/div[2]//a',
        'detail_xpath':'//*[@id="nr"]/table//tr',
        'need_selenium':False,
    },
    'http://yj.nanning.gov.cn/xzcfa/':{
        'name':'guangxi_nanning',
        'domain':'yj.nanning.gov.cn',
        'list_xpath':'//*[@id="common_list_box"]/div[2]/div/div[2]/div/div[2]//a',
        'detail_xpath':'/html/body//tr',
        'need_selenium':False,
    },
    'http://www.jlfda.gov.cn/xzcfaj/index.jhtml':{
        'name':'jilin',
        'domain':'www.jlfda.gov.cn',
        'list_xpath':'/html/body/div[3]/div[3]/ul[1]//a',
        'detail_xpath':'/html/body/div[3]/div/div[2]//tr',
        'need_selenium':False,
    },
    'http://xxgk.tonggu.gov.cn/tgxgsj_25516/zfxxgk_25518/gzdt_25524/gggs_25530/':{
        'name':'jiangxi_tonggu',
        'domain':'xxgk.tonggu.gov.cn',
        'list_xpath':'/html/body/table[2]//tr/td[3]/table[4]//tr/td[2]/table[3]//a',
        'detail_xpath':'//*[@id="fontzoom"]//tr',
        'need_selenium':True,
    },
    'http://www.sxjzfda.gov.cn/info/iList.jsp?cat_id=10019':{
        'name':'shanxi_jinzhong',
        'domain':'www.sxjzfda.gov.cn',
        'list_xpath':'/html/body/div[3]/div[2]/div[2]/ul//a',
        'detail_xpath':'/html/body/div[3]/div[1]/div[2]/div[2]/div[1]//tr',
        'need_selenium':False,
    },
    'http://www.zkfda.gov.cn/Home/NewsList?Id=1352':{
        'name':'henan_zhoukou',
        'domain':'www.zkfda.gov.cn',
        'list_xpath':'//*[@id="container"]/div[1]/div/ul//a',
        'detail_xpath':'//*[@id="sdcms_content"]//tr',
        'need_selenium':False,
    },
    'http://www.wnsfda.gov.cn/col/col51/index.html':{
        'name':'wnsfda',
        'domain':'www.wnsfda.gov.cn',
        'list_xpath':'//*[@id="71"]/div//a',
        'detail_xpath':'//*[@id="zoom"]//tr',
        'need_selenium':True,
    },
    'http://www.rzdonggang.gov.cn/rzdggov/_2386/xxgkml42/_20236/87ce358c-1.html':{
        'name':'rzdonggang',
        'domain':'www.rzdonggang.gov.cn',
        'list_xpath':'//*[@id="87ce358cd42843f6a8ea19a1a24fe3ca"]/div[3]/div[2]/table[2]//a',
        'detail_xpath':'//*[@id="5fc10071dfec4b75a802e57310f1fd17"]/div[2]/div[2]/div/div[1]/div/div//tr',
        'need_selenium':False,
    },
    'http://laishan.gov.jiaodong.net/zhengwu/xxgk/gk_list.asp?sortid=183&sorname=%B9%A4%C9%CC%BE%D6&key=&page=1':{
        'name':'laishan',
        'domain':'laishan.gov.jiaodong.net',
        'list_xpath':'/html/body/table[1]//tr/td/table[8]//tr/td/table//tr/td[3]//a',
        'detail_xpath':'/html/body/table[1]//tr/td/table[8]//tr/td/table//tr/td[3]/table[5]//tr',
        'need_selenium':False,
    },
    'http://www.wxfda.gov.cn/ztzl/a5/Index.html':{
        'name':'gansu_longnan',
        'domain':'www.wxfda.gov.cn',
        'list_xpath':'//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[2]/ul//a',
        'detail_xpath':'//*[@id="wrap"]/div/div[2]/div[2]/div/div[2]/div[2]//table//tr',
        'need_selenium':False,
    },
    'http://ls.sxjzfda.gov.cn/info/iList.jsp?cat_id=10738':{
        'name':'shanxi_lingshi',
        'domain':'ls.sxjzfda.gov.cn',
        'list_xpath':'//*[@id="rit"]/div[2]/ul//a',
        'detail_xpath':'/html/body/div[3]/div[2]/div/table//tr',
        'need_selenium':False,
    },
    'http://www.gscxsyj.gov.cn/index.php?s=/List/index/cid/15.html':{
        'name':'gansu_chengxian',
        'domain':'www.gscxsyj.gov.cn',
        'list_xpath':'/html/body/div[5]/div[2]/div/div[2]/div[1]//a',
        'detail_xpath':'/html/body/div[6]/div[2]/div/div[2]/div[2]//tr',
        'need_selenium':False,
    },
    'http://www.dxfda.gov.cn/list/?76_1.html':{
        'name':'gansu_zhangxian',
        'domain':'www.dxfda.gov.cn',
        'list_xpath':'/html/body/div[5]/div[2]/ul//a',
        'detail_xpath':'/html/body/div[5]/div[1]//tr',
        'need_selenium':False,
    },
    'http://www.pingyi.gov.cn/tabid/5657/Default.aspx':{
        'name':'pingyi',
        'domain':'www.pingyi.gov.cn',
        'list_xpath':'//*[@id="ess_ctr9785_ListC_Info_LstC_Info"]//a',
        'detail_xpath':'//*[@id="ess_ctr9786_ModuleContent"]/table[3]//tr',
        'need_selenium':False,
    },
    'http://www.lanling.gov.cn/mb_zwbk/a_list_ejlist.jsp?urltype=tree.TreeTempUrl&wbtreeid=1269':{
        'name':'lanling',
        'domain':'www.lanling.gov.cn',
        'list_xpath':'/html/body/div[3]/div/div[4]/div[2]/div[2]/ul//a',
        'detail_xpath':'/html/body/div[2]/div/div[4]/div[2]/div[3]//tr',
        'need_selenium':True,
    },
    'http://www.juxfda.gov.cn/plus/list.php?tid=4':{
        'name':'juxfda',
        'domain':'www.juxfda.gov.cn',
        'list_xpath':'/html/body/div[5]/div[1]/div[3]/ul//a',
        'detail_xpath':'/html/body/div[5]/div[1]/div[2]/div[3]//tr',
        'need_selenium':False,
    },
    'https://www.xmscjg.gov.cn/xxgk/zfxxgk/zfxxgkml/36/05/xzcfaj/':{
        'name':'fujian_xiamen',
        'domain':'www.xmscjg.gov.cn',
        'list_xpath':'/html/body/table[2]//a',
        'detail_xpath':'//*[@id="fontzoom"]/table[2]//tr',
        'need_selenium':False,
    },
    'http://www.xincheng.gov.cn/new_ztzl/news/list/1980.html':{
        'name':'shan3xi_xincheng',
        'domain':'www.xincheng.gov.cn',
        'list_xpath':'//*[@id="content"]/div/div[3]/div/div/ul//a',
        'detail_xpath':'//*[@id="content"]/div/div[3]/div//tr',
        'need_selenium':False,
    },
    'http://xxgk.hainan.gov.cn/tcxxgk/yjjxxgk/zzzxgklist.html':{
        'name':'hainan_tunchang',
        'domain':'xxgk.hainan.gov.cn',
        'list_xpath':'//*[@id="documentContainer"]//a',
        'detail_xpath':'/html/body/div/table[1]//tr[2]/td/table//tr',
        'need_selenium':False,
    },
    'http://dongkeng.dg.gov.cn/zhengwugonggao/tongzhigonggao/':{
        'name':'guangdong_dongkeng',
        'domain':'dongkeng.dg.gov.cn',
        'list_xpath':'/html/body/table[2]//tr/td[1]/table//tr[3]/td/table//tr/td/table//a',
        'detail_xpath':'/html/body/table[2]//tr/td[1]/table//tr[3]/td/table//tr/td/table//tr',
        'need_selenium':False,
    },
    'http://fda.pingliang.gov.cn/cfgs/':{
        'name':'gansu_pingliang',
        'domain':'fda.pingliang.gov.cn',
        'list_xpath':'//*[@id="warp"]/div[2]/ul//a',
        'detail_xpath':'//*[@id="yjcontent"]/div[2]/div[2]//tr',
        'need_selenium':False,
    },
    'http://dbyj.dabu.gov.cn/Article/List_36.html':{
        'name':'guangdong_dapu',
        'domain':'dbyj.dabu.gov.cn',
        'list_xpath':'/html/body/table[3]//tr/td[3]/table[1]//tr/td/table[2]//a',
        'detail_xpath':'/html/body/table[3]//tr/td[3]/table//tr',
        'need_selenium':False,
    },
    'http://www.gdscjg.gov.cn/html/xuanchuanlan/':{
        'name':'hunan_guidong',
        'domain':'www.gdscjg.gov.cn',
        'list_xpath':'/html/body/div/div[3]/div[1]/div[1]//a',
        'detail_xpath':'/html/body/div/div[3]/div/div[3]//tr',
        'need_selenium':False,
    },
    'http://www.furong.gov.cn/xxgk/gov1/sab/safe/spjd/':{
        'name':'hunan_furong',
        'domain':'www.furong.gov.cn',
        'list_xpath':'/html/body/div[1]/div[1]/div/ul//a',
        'detail_xpath':'/html/body//article/div[2]//tr',
        'need_selenium':False,
    },
    'http://www.yzlfda.gov.cn/list/?84_1.html':{
        'name':'yzlfda',
        'domain':'www.yzlfda.gov.cn',
        'list_xpath':'/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/table//a',
        'detail_xpath':'/html/body/div[2]/div[2]/div[3]/div/div[2]/div[3]/table//tr',
        'need_selenium':False,
    },
    'http://public.zhengzhou.gov.cn/info/index.jhtml?a=priority&p=h9':{
        'name':'henan_zhengzhou',
        'domain':'public.zhengzhou.gov.cn',
        'list_xpath':'//*[@id="priority-list"]/div/ul//a',
        'detail_xpath':'//div[@class="content-wrap"]//tr',
        'need_selenium':False,
    },
    'http://www.acec.gov.cn/chuz_adda/ztbd/yxajxxgk/':{
        'name':'anhui_chuzhou',
        'domain':'www.acec.gov.cn',
        'list_xpath':'/html/body/div[2]/div/div[2]/div[2]/ul//a',
        'detail_xpath':'/html/body/div[2]/div/div[2]/div[2]/div//tr',
        'need_selenium':False,
    },
    'http://www.gao-ling.gov.cn/html/xxgk/gkml/syaq/index.html':{
        'name':'shan3xi_gaoling',
        'domain':'www.gao-ling.gov.cn',
        'list_xpath':'//*[@id="main"]/div/div[2]/div[2]/div/div[3]/table//a',
        'detail_xpath':'//*[@id="main"]/div/div[2]//tr',
        'need_selenium':False,
    },
    'http://fda.changyuan.gov.cn/channels/gongkai/anjianxx.html':{
        'name':'henan_changyuan',
        'domain':'fda.changyuan.gov.cn',
        'list_xpath':'/html/body/div[3]/div[2]/div[2]/ul//a',
        'detail_xpath':'/html/body/div[3]/div[2]/div[2]//tr',
        'need_selenium':False,
    },
    'http://www.yongning.gov.cn/shiyaoju/channels/7845.html':{
        'name':'guangxi_yongning',
        'domain':'www.yongning.gov.cn',
        'list_xpath':'//*[@id="mainleft"]/div/ul//a',
        'detail_xpath':'//*[@id="mainleft"]/div[3]/table//tr',
        'need_selenium':False,
    },
    'http://www.yzx.gov.cn/2/3958/3965/4016/4034/':{
        'name':'hunan_yizhang',
        'domain':'www.yzx.gov.cn',
        'list_xpath':'/html/body/div[4]/div[3]/ul//a',
        'detail_xpath':'//*[@id="zoom"]//tr',
        'need_selenium':False,
    },
    'http://www.gzhezhang.gov.cn/HZGOV/A/11/08/03/index.shtml':{
        'name':'guizhou_hezhang',
        'domain':'www.gzhezhang.gov.cn',
        'list_xpath':'//*[@id="content"]//a',
        'detail_xpath':'//*[@id="textBox"]/table[2]//tr',
        'need_selenium':False,
    },
    'http://sshfda.gov.cn/xzcf.html':{
        'name':'sshfda',
        'domain':'sshfda.gov.cn',
        'list_xpath':'//*[@id="right"]/div[2]/ul//a',
        'detail_xpath':'//*[@id="right"]/div[2]/div[3]//tr',
        'need_selenium':False,
    },
    'http://www.xianfeng.gov.cn/spypgsgg/index.jhtml':{
        'name':'hubei_xianfeng',
        'domain':'www.xianfeng.gov.cn',
        'list_xpath':'//*[@id="xxgklb_table"]//a',
        'detail_xpath':'/html/body/div[3]/div/div[2]//tr',
        'need_selenium':False,
    },
    'http://www.zmdfda.gov.cn/CL0983/':{
        'name':'shanxi_zhumadian',
        'domain':'www.zmdfda.gov.cn',
        'list_xpath':'//*[@id="sRcon"]/table[1]//a',
        'detail_xpath':'//*[@id="sDetail"]/div/div[1]/table//tr',
        'need_selenium':False,
    },
    'http://www.daojiao.gov.cn/Category_863/Index.aspx':{
        'name':'guangdong_daojiao',
        'domain':'www.daojiao.gov.cn',
        'list_xpath':'/html/body/div[2]/div[1]/div/div[2]/div/div[1]/div/ul//a',
        'detail_xpath':'/html/body/div[3]/div[1]/div/div[2]/div[4]//tr',
        'need_selenium':False,
    },
    'http://www.thsfda.gov.cn/xxgk/xzcfajxxgk/':{
        'name':'jilin_tonghua',
        'domain':'www.thsfda.gov.cn',
        'list_xpath':'/html/body/div[3]/div[3]/ul[1]//a',
        'detail_xpath':'/html/body/div[3]/div/div[2]/div[2]/span/div//tr',
        'need_selenium':False,
    },
    'http://www.scqs.gov.cn/xxgk/zdlyxxgk/spybaq.htm':{
        'name':'sichuan_qingshen',
        'domain':'www.scqs.gov.cn',
        'list_xpath':'//*[@id="leftboxList"]//a',
        'detail_xpath':'/html/body/div[3]/div[1]/div/div[2]/div/form/table//tr',
        'need_selenium':False,
    },
    # 'http://spypjdglj.gdmx.gov.cn/index.php?m=content&c=index&a=lists&catid=1446':{
    #     'name':'guangzhou_meixian',
    #     'domain':'spypjdglj.gdmx.gov.cn',
    #     'list_xpath':'/html/body/table[2]//tr[1]/td/table//tr[3]/td[3]/table//tr/td/table[2]//tr[2]/td/table//a',
    #     'detail_xpath':'/html/body/table[2]//tr/td/table//tr[3]/td/table[1]//tr',
    #     'need_selenium':False,
    # },
    'http://hb.ada.gov.cn/list.aspx?id=36':{
        'name':'anhui_huaibei',
        'domain':'hb.ada.gov.cn',
        'list_xpath':'//*[@id="container"]/div[3]/div[2]/ul//a',
        'detail_xpath':'//*[@id="container"]/div[3]/div[2]//tr',
        'need_selenium':False,
    },
    'http://fda.taizhou.gov.cn/col/col17402/index.html':{
        'name':'jiangsu_taizhou',
        'domain':'fda.taizhou.gov.cn',
        'list_xpath':'//*[@id="newslist"]//a',
        'detail_xpath':'//*[@id="article"]//tr',
        'need_selenium':True,
    },
    'http://fda.cnxuanen.cn/html/government/e/':{
        'name':'hubei_xuanen',
        'domain':'fda.cnxuanen.cn',
        'list_xpath':'/html/body/div[4]/div/div[2]/div//a',
        'detail_xpath':'/html/body/div[4]/div/span[2]/span[2]/table//tr',
        'need_selenium':False,
    },
    'http://syjdj.luzhai.gov.cn/spypaq_3/spypxzcfajxxgk/index.shtml':{
        'name':'guangxi_luzhai',
        'domain':'syjdj.luzhai.gov.cn',
        'list_xpath':'/html/body/div[2]/div/div[2]/div//a',
        'detail_xpath':'//*[@id="Zoom"]//tr',
        'need_selenium':False,
    },
    'http://lingang.linyi.gov.cn/zwgk/zdly/ggjg/scjgxx.htm':{
        'name':'linyi',
        'domain':'lingang.linyi.gov.cn',
        'list_xpath':'/html/body/div[4]/div[2]/div[2]/div/table//a',
        'detail_xpath':'//*[@id="vsb_content_2"]//tr',
        'need_selenium':False,
    },
    'http://www.gztaijiang.gov.cn/zwgk/zdlygk/jdjc/spyp/':{
        'name':'guizhou_taijiang',
        'domain':'www.gztaijiang.gov.cn',
        'list_xpath':'/html/body/div[2]/div[3]/div[2]/div[2]/ul//a',
        'detail_xpath':'//*[@id="Zoom"]//tr',
        'need_selenium':False,
    },
    'http://www.czs.gov.cn/html/zwgk/ztbd/11819/11856/11877/13219/default.htm':{
        'name':'hunan_chenzhou',
        'domain':'www.czs.gov.cn',
        'list_xpath':'/html/body/div[3]/div[2]/div[2]/ul//a',
        'detail_xpath':'//*[@id="zoom"]//tr',
        'need_selenium':False,
    },
    'http://www.xysfda.gov.cn/info/iList.jsp?cat_id=23202':{
        'name':'shan3xi_xianyang',
        'domain':'www.xysfda.gov.cn',
        'list_xpath':'//*[@id="center"]/table//tr/td[6]/table//tr[2]//a',
        'detail_xpath':'//*[@id="center"]/table//tr/td[6]/table//tr[2]/td/div[2]/div[5]//tr',
        'need_selenium':False,
    },
    'http://yjj.fengshun.gov.cn/czcfaj/class/?132.html':{
        'name':'guangdong_fengshun',
        'domain':'yjj.fengshun.gov.cn',
        'list_xpath':'/html/body/table[4]//tr/td[3]/table[3]//tr/td/table//a',
        'detail_xpath':'/html/body/table[4]//tr/td/table//tr/td/table[4]//tr',
        'need_selenium':False,
    },
    'http://www.jxda.gov.cn/Column.shtml?p5=2642':{
        'name':'jiangxi',
        'domain':'www.jxda.gov.cn',
        'list_xpath':'//*[@id="Table"]//a',
        'detail_xpath':'/html/body//tr',
        'need_selenium':False,
    },
    'http://www.hepu.gov.cn/html/organ/gzdt2-134.aspx':{
        'name':'guangxi_hepu',
        'domain':'www.hepu.gov.cn',
        'list_xpath':'/html/body/div/table//tr/td[2]/div[2]/div/ul//a',
        'detail_xpath':'//*[@id="content"]//tr',
        'need_selenium':False,
    },
    'http://www.wnfda.gov.cn/CL1159/':{
        'name':'shan3xi_weinan',
        'domain':'www.wnfda.gov.cn',
        'list_xpath':'/html/body/table//tr[3]/td/table//tr/td/table[2]//tr/td/table//tr[2]/td/table//tr/td/div/span/table//a',
        'detail_xpath':'/html/body/table//tr',
        'need_selenium':False,
    },
    'http://www.pqfda.gov.cn/?list-1851.html':{
        'name':'henan_xinyang',
        'domain':'www.pqfda.gov.cn',
        'list_xpath':'/html/body/div/div[4]/table//tr/td[3]/ul//a',
        'detail_xpath':'/html/body//tr',
        'need_selenium':False,
    },
    'http://www.aphf.com.cn/list/?108_1.html':{
        'name':'hebei_anping',
        'domain':'www.aphf.com.cn',
        'list_xpath':'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]//a',
        'detail_xpath':'//*[@id="post-724"]//tr',
        'need_selenium':False,
    },
    'http://www.gxqzfda.gov.cn/Item/list.asp?id=1300':{
        'name':'guangxi_qinzhou',
        'domain':'www.gxqzfda.gov.cn',
        'list_xpath':'/html/body/table//tr[2]/td/table//tr[1]/td[1]/table//tr[3]/td/table//tr[2]//a',
        'detail_xpath':'//*[@id="MyContent"]//tr',
        'need_selenium':False,
    },
    'http://www.tancheng.gov.cn/xxgk/xxgk_lmzl.jsp?urltype=tree.TreeTempUrl&wbtreeid=1222':{
        'name':'tancheng',
        'domain':'www.tancheng.gov.cn',
        'list_xpath':'//*[@id="ainfolist1369"]/div[1]/table//a',
        'detail_xpath':'/html/body/div[2]/div/div[2]/table//tr[1]/td/table//tr[4]/td//tr',
        'need_selenium':False,
    },
    'http://chashan.dg.gov.cn/publicfiles/business/htmlfiles/chashan/s40400/index.htm':{
        'name':'guangdong_chashan',
        'domain':'chashan.dg.gov.cn',
        'list_xpath':'//*[@id="pageSize_8"]//a',
        'detail_xpath':'//*[@id="zoomcon"]//tr',
        'need_selenium':True,
    },
    'http://www.lxzfda.gov.cn/news_list.asp?subclass_id=59':{
        'name':'gansu_lxz',
        'domain':'www.lxzfda.gov.cn',
        'list_xpath':'//*[@id="news_lst"]/ul//a',
        'detail_xpath':'//*[@id="divContent"]//tr',
        'need_selenium':False,
    },
    'http://www.tfjy.gov.cn/govopen/list.cdcb?channel=%E9%A3%9F%E8%8D%AF%E8%BF%9D%E6%B3%95%E8%BF%9D%E8%A7%84%E4%BC%81%E4%B8%9A':{
        'name':'sichuan_jingyang',
        'domain':'www.tfjy.gov.cn',
        'list_xpath':'//*[@id="container"]/div[2]/div[5]/div[2]/div[1]/ul//a',
        'detail_xpath':'//*[@id="content"]//tr',
        'need_selenium':False,
    },
    'http://www.ahfyfda.gov.cn/content/channel/551cd9cdaf88bcbe51dd37fa/':{
        'name':'anhui_fuyang',
        'domain':'www.ahfyfda.gov.cn',
        'list_xpath':'//ul[@class="is-listnews"]//a',
        'detail_xpath':'//*[@id="zoom"]//tr',
        'need_selenium':False,
    },
    'http://yjj.kaiping.gov.cn/NewsList.asp?SortID=63':{
        'name':'guangdong_kaiping',
        'domain':'yjj.kaiping.gov.cn',
        'list_xpath':'/html/body/table[3]//tr/td[3]/table[2]//tr[1]/td/table[1]//a',
        'detail_xpath':'/html/body/table[3]//tr/td[3]/table[2]//tr[4]/td/table//tr',
        'need_selenium':False,
    },
    'http://www.wuhaifda.gov.cn/newslist.aspx?o=ss&t=title&k=%u884C%u653F%u5904%u7F5A':{
        'name':'nmg_wuhai',
        'domain':'www.wuhaifda.gov.cn',
        'list_xpath':'//*[@id="DataList1"]//a',
        'detail_xpath':'//*[@id="NewsInfoTd"]/table[3]//tr/td/table//tr',
        'need_selenium':False,
    },
    'http://www.gxczfda.gov.cn/list.asp?bid=66':{
        'name':'guangxi_chongzuo',
        'domain':'www.gxczfda.gov.cn',
        'list_xpath':'/html/body/div/table[2]//tr/td[3]/table[2]//tr[1]/td/table//a',
        'detail_xpath':'/html/body/div/table[2]//tr/td/table[2]//tr/td/table//tr[3]/td/table//tr',
        'need_selenium':False,
    },
    'http://www.huoqiu.gov.cn/tmp/xxgklist2.shtml?unitsId=1&SSIDS=0&action=list&SS_Path=/-020-038-008-010&types=2&smonth=0&pp=1':{
        'name':'anhui_huoqiu',
        'domain':'www.huoqiu.gov.cn',
        'list_xpath':'/html/body/div[2]/div[4]//a',
        'detail_xpath':'//*[@id="Zoom2"]//tr',
        'need_selenium':False,
    },
    'http://www.als.gov.cn/syjj/channels/7743.html':{
        'name':'nmg_als',
        'domain':'www.als.gov.cn',
        'list_xpath':'/html/body/div[4]/div[2]/div[3]/ul//a',
        'detail_xpath':'/html/body/div[4]/div[2]/div[3]/div[2]/table//tr',
        'need_selenium':False,
    },
    'http://yjj.jiaoling.gov.cn/index.php?m=content&c=index&a=lists&catid=30':{
        'name':'guangdong_jiaoling',
        'domain':'yjj.jiaoling.gov.cn',
        'list_xpath':'/html/body/table[2]//tr[2]/td/table//tr/td[3]/table//tr[2]/td/table//tr[2]/td/table//a',
        'detail_xpath':'/html/body/table[2]//tr[1]/td/table//tr[4]/td/table[2]//tr[3]//tr',
        'need_selenium':False,
    },
    'http://www.qingxiu.gov.cn/syjgj/channels/9202.html':{
        'name':'guangxi_qingxiu',
        'domain':'www.qingxiu.gov.cn',
        'list_xpath':'//*[@id="mainleft"]//a',
        'detail_xpath':'//*[@id="content_mainleft"]//tr',
        'need_selenium':True,
    },
    'http://yjj.neijiang.gov.cn/list/%E7%9B%91%E7%9D%A3%E6%A3%80%E6%9F%A5':{
        'name':'sichuan_neijiang',
        'domain':'yjj.neijiang.gov.cn',
        'list_xpath':'//*[@id="container"]/table//tr/td/div/div/div[1]//a',
        'detail_xpath':'//*[@id="content_zoom"]//tr',
        'need_selenium':False,
    },
    'http://www.hcfda.gov.cn/jx/xzzf/index.html':{
        'name':'guangxi_hechi',
        'domain':'www.hcfda.gov.cn',
        'list_xpath':'/html/body/div[2]/div[2]/div/ul//a',
        'detail_xpath':'//*[@id="content"]/li/table//tr',
        'need_selenium':False,
    },
    'http://zwgk.ptjp.gov.cn/search?k=%E8%A1%8C%E6%94%BF%E5%A4%84%E7%BD%9A%E6%A1%88%E4%BB%B6%E4%BF%A1%E6%81%AF%E5%85%AC%E7%A4%BA&s=15&p=1':{
        'name':'guizhou_pingtang',
        'domain':'zwgk.ptjp.gov.cn',
        'list_xpath':'/html/body/div[5]/div[1]/div[5]//a',
        'detail_xpath':'//div[@class="content"]//tr',
        'need_selenium':False,
    },
    'http://www.huainan.gov.cn/public/column/4971284?type=4&catId=4977426&action=list':{
        'name':'anhui_huainan',
        'domain':'www.huainan.gov.cn',
        'list_xpath':'//*[@id="xxgk_lmcon"]/div[3]//a',
        'detail_xpath':'//*[@id="wenzhang"]/div[3]//tr',
        'need_selenium':'need_click',
        'click_path_list':['//*[@id="organ_catalog_tree_231_switch"]','//*[@id="organ_catalog_tree_234_a"]'],
    },
    'http://www.cqda.gov.cn/CL0166/':{
        'name':'chongqin',
        'domain':'www.cqda.gov.cn',
        'list_xpath':'//*[@id="_ctl0_MainContent_plListSyle0"]/table//tr/td/table//tr/td/table//a',
        'detail_xpath':'/html/body/table[4]//tr/td/table[2]//tr',
        'need_selenium':False,
    },
    'http://www.shxda.gov.cn/structure/ztzl/xzcfxxgs/xzcf.htm':{
        'name':'shanxi',
        'domain':'www.shxda.gov.cn',
        'list_xpath':'/html/body/table[5]//tr/td[4]/table[2]//tr/td/table[3]//a',
        'detail_xpath':'www.hn-fda.gov.cn/table[7]//tr/td[2]/table//tr',
        'need_selenium':False,
    },
    'http://www.lnfda.gov.cn/CL1134/':{
        'name':'liaoning',
        'domain':'www.lnfda.gov.cn',
        'list_xpath':'//*[@id="gernalsearch"]/table//a',
        'detail_xpath':'//*[@id="zoom"]//tr',
        'need_selenium':False,
    },
    'http://www.hn-fda.gov.cn/ztzl/xzcf/':{
        'name':'hunan',
        'domain':'www.hn-fda.gov.cn',
        'list_xpath':'/html/body/div[4]/div/div/div/div[4]/div[2]/ul//a',
        'detail_xpath':'//*[@id="j-show-body"]//tr',
        'need_selenium':False,
    },
    'http://www.gdda.gov.cn/publicfiles/business/htmlfiles/jsjzz/s8242/list.htm':{
        'name':'guangdong',
        'domain':'www.gdda.gov.cn',
        'list_xpath':'/html/body/div[3]/div[2]/ul//a',
        'detail_xpath':'/html/body/div[4]/div/div[2]//tr',
        'need_selenium':True,
    },
    'http://www.scfda.gov.cn/CL3369/':{
        'name':'sichuan',
        'domain':'www.scfda.gov.cn',
        'list_xpath':'//*[@id="list"]/table[1]//a',
        'detail_xpath':'/html/body/div/table[2]//tr[2]/td[2]/table//tr[5]/td/table//tr',
        'need_selenium':False,
    },
    'http://www.kmfda.gov.cn/zfxxgkml/spypaqxxgk/xzcfxx/':{
        'name':'yunnan_kunming',
        'domain':'www.kmfda.gov.cn',
        'list_xpath':'//*[@id="listblock"]//a',
        'detail_xpath':'/html/body/div[14]/div[1]/div[2]/table//tr',
        'need_selenium':False,
    },
    'http://www.nxfda.gov.cn/html/xzcf/index.html':{
        'name':'ningxia',
        'domain':'www.nxfda.gov.cn',
        'list_xpath':'//*[@id="div148"]/ul//a',
        'detail_xpath':'//*[@id="cont"]//tr',
        'need_selenium':False,
    },
    'http://www.glfda.gov.cn/index.php?c=content&a=list&catid=36':{
        'name':'guangxi_guilin',
        'domain':'www.glfda.gov.cn',
        'list_xpath':'//*[@id="list_article"]//tr[2]/td/table//a',
        'detail_xpath':'//*[@id="view_article"]//tr[1]/td/table[1]//tr',
        'need_selenium':False,
    },
    'http://www.gzss.gov.cn/zwgk/xxgkml/zdlygk/spypaq/wfxwcc/':{
        'name':'guizhou_sansui',
        'domain':'www.gzss.gov.cn',
        'list_xpath':'//*[@id="datalist"]//a',
        'detail_xpath':'//*[@id="Zoom"]//tr',
        'need_selenium':True,
    },
    'http://www.cnll.gov.cn/Category_214/Index.aspx':{
        'name':'hunan_lingling',
        'domain':'www.cnll.gov.cn',
        'list_xpath':'//*[@id="content"]/div[3]/div[2]/div/div[2]//a',
        'detail_xpath':'//*[@id="fontzoom"]//tr',
        'need_selenium':False,
    },
    'http://syjc.hefei.gov.cn/index.php/List/index/cid/16/p/1.html':{
        'name':'anhui_hefei',
        'domain':'syjc.hefei.gov.cn',
        'list_xpath':'/html/body/div[2]/div/div[2]/div[2]/div/ul//a',
        'detail_xpath':'/html/body/div[2]/div/div[2]/div/div[3]/table//tr',
        'need_selenium':False,
    },
    'http://www.thnet.gov.cn/thxxw/spypaq/2016_zdly_list.shtml':{
        'name':'guangzhou_tianhe',
        'domain':'www.thnet.gov.cn',
        'list_xpath':'/html/body/div[5]/div[2]/ul//a',
        'detail_xpath':'/html/body/div[5]/div[2]//tr',
        'need_selenium':False,
    },
    'http://www.gxhzfda.gov.cn/e/action/ListInfo/?classid=16':{
        'name':'guangxi_hezhou',
        'domain':'www.gxhzfda.gov.cn',
        'list_xpath':'/html/body/div/div/table[4]//tr/td/table[1]//tr/td/ul[1]//a',
        'detail_xpath':'//*[@id="text"]//tr',
        'need_selenium':False,
    },
    'http://www.gdczfda.gov.cn/zt/zt_list.asp?groupid=38&cgroupid=76':{
        'name':'guangdong_chaozhou',
        'domain':'www.gdczfda.gov.cn',
        'list_xpath':'//*[@id="main"]/ul//a',
        'detail_xpath':'//*[@id="page_newsview"]/div[1]/table//tr',
        'need_selenium':False,
    },
    'http://yjj.hnloudi.gov.cn/wfcc/index.html':{
        'name':'hunan_loudi',
        'domain':'yjj.hnloudi.gov.cn',
        'list_xpath':'/html/body/div[2]/div[2]/ul//a',
        'detail_xpath':'//*[@id="fontzoom"]/div[1]/div/table[1]//tr',
        'need_selenium':False,
    },
    'http://www.scdongqu.gov.cn/qzwgk/xzqlgk/xzqlyx/index.shtml':{
        'name':'sichuan_pzh_dongqu',
        'domain':'www.scdongqu.gov.cn',
        'list_xpath':'//*[@id="container"]/div[1]/div[2]/div/div[2]/div[1]//a',
        'detail_xpath':'//div[@class="editor-content"]//tr',
        'need_selenium':False,
    },
}

def format_url(url,domain,res_url):
    if res_url.startswith('http://'):
        head = 'http://'
    elif res_url.startswith('https://'):
        head = 'https://'
    if url.startswith('/'):
        url = head+domain+ url
    elif url.startswith('http://') or url.startswith('https://'):
        pass
    elif url.startswith('./') or url.startswith('../'):
        count = 0
        if '../' in url:
            count = url.count('../')
        elif './' in url:
            count = url.count('./')
        url_list = res_url.split(head)[1].split('/')
        if res_url.endswith('/') and count > 0:
            count -= 1
        if count:
            url_list.pop()
        if '' in url_list:
            url_list.remove('')
        url = head+'/'.join(url_list)+'/'+url
    else:
        url_list = res_url.split(head)[1].split('/')
        if res_url.endswith('/'):
            pass
        else:
            url_list.pop()
        if '' in url_list:
            url_list.remove('')
        url = head+'/'.join(url_list)+'/'+url
    return url 

def clear_fuc(string):
    return string.replace(" ","").replace("\n", "").replace("\r", "").replace("\t","").replace(u"\u3000","").replace(u"\xa0","")

class CaseSpider(scrapy.Spider):
    name = "common"
    allowed_domains = ['www.jnfda.gov.cn','lx.jnfda.gov.cn','sz.jnfda.gov.cn','hy.jnfda.gov.cn','tq.jnfda.gov.cn','lc.jnfda.gov.cn','cq.jnfda.gov.cn','zq.jnfda.gov.cn','py.jnfda.gov.cn','www.tzsfda.gov.cn','www.dyfda.gov.cn','hkfda.huanghekou.gov.cn','www.wffda.gov.cn','www.weihaifda.gov.cn','xxgk.eweihai.gov.cn','dcfda.gov.cn','yj.nanning.gov.cn','www.jlfda.gov.cn','xxgk.tonggu.gov.cn','www.sxjzfda.gov.cn','www.zkfda.gov.cn','www.wnsfda.gov.cn','www.rzdonggang.gov.cn','laishan.gov.jiaodong.net','www.wxfda.gov.cn','ls.sxjzfda.gov.cn','www.gscxsyj.gov.cn','www.dxfda.gov.cn','www.pingyi.gov.cn','www.lanling.gov.cn','www.juxfda.gov.cn','www.xmscjg.gov.cn','www.xincheng.gov.cn','xxgk.hainan.gov.cn','dongkeng.dg.gov.cn','fda.pingliang.gov.cn','dbyj.dabu.gov.cn','www.gdscjg.gov.cn','www.furong.gov.cn','www.yzlfda.gov.cn','public.zhengzhou.gov.cn','www.acec.gov.cn','www.gao-ling.gov.cn','fda.changyuan.gov.cn','www.yongning.gov.cn','www.yzx.gov.cn','www.gzhezhang.gov.cn','sshfda.gov.cn','www.xianfeng.gov.cn','www.zmdfda.gov.cn','www.daojiao.gov.cn','www.thsfda.gov.cn','www.scqs.gov.cn','spypjdglj.gdmx.gov.cn','hb.ada.gov.cn','fda.taizhou.gov.cn','fda.cnxuanen.cn','syjdj.luzhai.gov.cn','lingang.linyi.gov.cn','www.gztaijiang.gov.cn','www.czs.gov.cn','www.xysfda.gov.cn','yjj.fengshun.gov.cn','www.jxda.gov.cn','www.hepu.gov.cn','www.wnfda.gov.cn','www.pqfda.gov.cn','www.dgboftec.gov.cn','www.aphf.com.cn','www.gxqzfda.gov.cn','www.tancheng.gov.cn','chashan.dg.gov.cn','www.lxzfda.gov.cn','www.tfjy.gov.cn','www.ahfyfda.gov.cn','yjj.kaiping.gov.cn','www.wuhaifda.gov.cn','www.gxczfda.gov.cn','www.huoqiu.gov.cn','www.als.gov.cn','yjj.jiaoling.gov.cn','www.qingxiu.gov.cn','yjj.neijiang.gov.cn','www.hcfda.gov.cn','zwgk.ptjp.gov.cn','www.huainan.gov.cn','www.cqda.gov.cn','www.shxda.gov.cn','www.lnfda.gov.cn','www.hn-fda.gov.cn','www.gdda.gov.cn','www.scfda.gov.cn','www.kmfda.gov.cn','www.nxfda.gov.cn','www.glfda.gov.cn','www.gzss.gov.cn','www.cnll.gov.cn','syjc.hefei.gov.cn','www.thnet.gov.cn','www.gxhzfda.gov.cn','www.gdczfda.gov.cn','yjj.hnloudi.gov.cn','www.scdongqu.gov.cn']
    start_urls = ['http://www.jnfda.gov.cn']
    url_names = ['行政处罚','信息公开','信息公示表','信息表','不合格名单','案件公开','抽检信息','企业名单','案件处罚信息']

    def parse(self, response):
        for key,val in URL_DICT.items():
            if val['need_selenium']:
                yield scrapy.Request(key, callback=self.parse_selenium,meta={'settings':val})
            else:
                yield scrapy.Request(key, callback=self.parse_list,meta={'settings':val})

    def parse_list(self, response):
        settings = response.meta['settings']
        urls = response.xpath(settings['list_xpath'])
        for url in urls:
            text = url.xpath('string(.)').extract_first()
            if text:
                next_step = False
                for i in self.url_names:
                    if i in text:
                        next_step = True
                        break
                if next_step:
                    url = url.xpath('@href').extract_first()
                    url = format_url(url,settings['domain'],response.url)
                    if not url.endswith('.xls'):
                        already = SpiderData.objects.filter(url=url)
                        if already.count() == 0:
                            yield scrapy.Request(url, callback=self.parse_item,meta={'settings':settings,'url':url})
                        else:
                            pass
                            # print 'already crawled'

    def parse_selenium(self, response):
        settings = response.meta['settings']
        browser = webdriver.PhantomJS()
        browser.get(response.url)
        time.sleep(1)
        if settings['need_selenium'] == 'need_click':
            for cp in settings['click_path_list']:
                browser.find_element_by_xpath(cp).click()
                time.sleep(1)
        urls = browser.find_elements_by_xpath(settings['list_xpath'])
        for url in urls:
            text = url.text
            if text:
                next_step = False
                for i in self.url_names:
                    if i in text:
                        next_step = True
                        break
                if next_step:
                    url = url.get_attribute("href")
                    already = SpiderData.objects.filter(url=url)
                    if already.count() == 0:
                        yield scrapy.Request(url, callback=self.parse_item,meta={'settings':settings,'url':url})
                    else:
                        pass
                        # print 'already crawled'
        browser.quit()

    def parse_item(self, response):
        settings = response.meta['settings']
        trs = response.xpath(settings['detail_xpath'])
        tr_list = []                        # 有效tr数
        if len(trs) > 1:
            for tr in trs:
                if len(tr.xpath('td').extract()) > 5:
                    has_val = 0
                    for td_str in tr.xpath('td').xpath('string(.)').extract():
                        if clear_fuc(td_str):
                            has_val += 1
                    if has_val > 3:
                        tr_list.append(tr)
        if len(tr_list) <= 1:                            # 存文件
            urls = response.xpath('//a/@href')
            l = ItemLoader(item=FileItem(), response=response)
            for url in urls.extract():
                if url.endswith('.doc') or url.endswith('.xlsx') or url.endswith('.xls') or url.endswith('.docx') or url.endswith('.rar') or url.endswith('.pdf') or url.endswith('.zip'):
                    url = format_url(url,settings['domain'],response.url)
                    l.add_value('file_urls',url)
            if not len(urls.extract()):                 # 存图片
                img_urls = response.xpath(settings['detail_xpath'].split('//tr')[0]+'//img/@src')
                for img_url in img_urls.extract():
                    img_url = format_url(img_url,settings['domain'],response.url)
                    l.add_value('file_urls',img_url)
            return l.load_item()
        else:                                             # 存表格
            global_row = {}                               # 判断合并单元格
            for i,tr in enumerate(tr_list):
                data = {}
                blank = 0
                if i > 0 :
                    for j,td in enumerate(tr.xpath('td')):
                        try:
                            rows = td.xpath('@rowspan').extract_first()
                            if rows:
                                if global_row.has_key(i):
                                    global_row[i].append([j,int(rows)])
                                else:
                                    global_row[i] = [[j,int(rows)]]

                            key = clear_fuc(tr_list[0].xpath('td').xpath('string(.)').extract()[j])
                            val = ''
                            back = 0
                            for x,y in global_row.items():
                                for m,n in y:
                                    if i <= x+n-1 and i > x:
                                        back += 1
                                        if m == j: 
                                            val = clear_fuc(tr_list[x].xpath('td').xpath('string(.)').extract()[j])
                            if not val:
                                val = clear_fuc(tr.xpath('td')[j-back].xpath('string(.)').extract_first())
                            if key or val:
                                data[key] = val
                        except:
                            pass
                        if not val or val == u'\xa0' or val == u'\u3000' or key == val:
                            blank += 1

                    if blank <= len(tr.xpath('td'))-2:
                        sendData(settings['name'],data,response.meta['url'])