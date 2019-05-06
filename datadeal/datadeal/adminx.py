# -*- coding: utf-8 -*-
import xadmin
from xadmin.views.base import CommAdminView
from xadmin.plugins.themes import ThemePlugin
from django.http import HttpResponseRedirect
from datadeal.settings import BASE_DIR
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from distribute.models import *
from company.models import *
from .views import *
import subprocess
import datetime
import json
import time
import os

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class AdminSettings(object):
    menu_style = "accordion"
    site_title = '爬虫管理系统'
    site_footer = '爬虫管理系统'

    def get_site_menu(self):
        return [
            {'title': '爬虫管理','icon':'fa fa-bug', 'perm': self.get_model_perm(scrapySetting, 'change'), 'menus':(
                {'title': '爬虫生成配置', 'url': self.get_model_url(scrapySetting, 'changelist'), 
                'perm': self.get_model_perm(scrapySetting, 'changelist')},
                {'title': '域名白名单', 'url': self.get_model_url(AllowDomains, 'changelist'),
                'perm': self.get_model_perm(AllowDomains, 'changelist')},
                {'title': '一级爬取地址', 'url': self.get_model_url(startUrls, 'changelist'),
                'perm': self.get_model_perm(startUrls, 'changelist')},
                {'title': '循环体列表', 'url': self.get_model_url(CycleObj, 'changelist'),
                'perm': self.get_model_perm(CycleObj, 'changelist')},
                {'title': '变量列表', 'url': self.get_model_url(Variable, 'changelist'),
                'perm': self.get_model_perm(Variable, 'changelist')},
                {'title': '爬虫列表', 'url': self.get_model_url(scrapyList, 'changelist'),
                'perm': self.get_model_perm(scrapyList, 'changelist')},
            )},
            {'title': '节点管理','icon':'fa fa-chain', 'perm': self.get_model_perm(Node, 'change'), 'menus':(
                {'title': '节点管理', 'url': self.get_model_url(Node, 'changelist'), 
                'perm': self.get_model_perm(Node, 'changelist')},
                {'title': '节点IP管理', 'url': self.get_model_url(NodeIp, 'changelist'), 
                'perm': self.get_model_perm(NodeIp, 'changelist')},
                {'title': '任务管理', 'url': self.get_model_url(NodeTask, 'changelist'),
                'perm': self.get_model_perm(NodeTask, 'changelist')},
            )},
            {'title': '数据管理','icon':'fa fa-bar-chart-o', 'perm': self.get_model_perm(SpiderData, 'change'), 'menus':(
                {'title': '数据信息', 'url': self.get_model_url(SpiderData, 'changelist'),
                'perm': self.get_model_perm(SpiderData, 'changelist')},
                {'title': '错误信息', 'url': self.get_model_url(ErrorData, 'changelist'),
                'perm': self.get_model_perm(ErrorData, 'changelist')},
                {'title': '预警信息', 'url': self.get_model_url(DataAlarm, 'changelist'),
                'perm': self.get_model_perm(DataAlarm, 'changelist')},
                {'title': '公司信息', 'url': self.get_model_url(Company, 'changelist'),
                'perm': self.get_model_perm(Company, 'changelist')},
                {'title': '股东信息', 'url': self.get_model_url(Shareholders, 'changelist'),
                'perm': self.get_model_perm(Shareholders, 'changelist')},
                {'title': '成员信息', 'url': self.get_model_url(Member, 'changelist'),
                'perm': self.get_model_perm(Member, 'changelist')},
            )},
            {'title': '文件管理','icon':'fa fa-file', 'perm': self.get_model_perm(SpiderData, 'change'), 'menus':(
                {'title': '图片管理', 'url':'/admin/images_admin/', 'perm': ''},
                {'title': '文件管理', 'url':'/admin/files_admin/', 'perm': ''},
            )},
        ]

xadmin.site.register(xadmin.views.BaseAdminView,BaseSetting)
xadmin.site.register(xadmin.views.CommAdminView,AdminSettings)

class scrapySettingAdmin(object):
    list_display = ['name', 'allow_domains','start_urls','cycleobj','variable','num','kind','create_at','modify_at']
    search_fields = ['name','allow_domains']
    list_filter = ['kind','create_at','modify_at']
    style_fields = {'allow_domains': 'm2m_transfer','start_urls': 'm2m_transfer','cycleobj': 'm2m_transfer','variable': 'm2m_transfer'}
    actions = ['create_spider','create_tasks']
    def create_spider(self, request, queryset):
        for q in queryset:
            if scrapyList.objects.filter(name=q.name).count() == 0:
                create_scrapy_file(q)
                self.message_user(u'%s 爬虫创建成功' % q.name)
                scrapyList.objects.create(name=q.name)
            else:
                self.message_user(u'%s 爬虫名已被使用' % q.name)
    create_spider.short_description = "创建爬虫"
    def create_tasks(self, request, queryset):
        from distribute.models import NodeTask
        for q in queryset:
            try:
                scrapy = scrapyList.objects.get(name=q.name)
            except:
                scrapy = ''
            if scrapy:
                urls = q.start_urls.all()
                total = urls.count()
                count,last = divmod(total,q.num)
                for n in range(0,count+1):
                    start = n*q.num
                    if n == count:
                        if last > 0:
                            end = total
                        else:
                            end = 'pass'
                    else:
                        end = (n+1)*q.num
                    if not end == 'pass':
                        name = q.name+'_'+str(n+1)
                        already = NodeTask.objects.filter(name=name).count()
                        if not already:
                            obj = NodeTask.objects.create(name=name,scrapy=scrapy,priority=n+1)
                            for i in urls[start:end]:
                                obj.urls.add(i)
                self.message_user(u'%s 爬虫任务分发完毕' % q.name)
            else:
                self.message_user(u'请先创建%s爬虫' % q.name)
    create_tasks.short_description = "生成任务"    
xadmin.site.register(scrapySetting, scrapySettingAdmin)

class AllowDomainsAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = []
xadmin.site.register(AllowDomains, AllowDomainsAdmin)

class startUrlsAdmin(object):
    list_display = ['url']
    search_fields = ['url']
    list_filter = []
xadmin.site.register(startUrls, startUrlsAdmin)

class CycleObjAdmin(object):
    list_display = ['name','xpath','variable']
    search_fields = ['name','xpath']
    list_filter = ['variable']
xadmin.site.register(CycleObj, CycleObjAdmin)

class VariableAdmin(object):
    list_display = ['name','xpath','kind','all_text']
    search_fields = ['name','xpath']
    list_filter = ['kind','all_text']
xadmin.site.register(Variable, VariableAdmin)

class scrapyListAdmin(object):
    list_display = ['name','priority','alarm_day','create_at','is_open']
    search_fields = ['name']
    list_filter = ['create_at','is_open']
    list_editable = ['alarm_day','is_open']
    actions = ['start_spider','download']
    def start_spider(self, request, queryset):
        for q in queryset:
            self.message_user(u'%s 爬虫正在爬取数据...  %s' % (q.name,datetime.datetime.now().strftime('%H:%M:%S')))
            subprocess.call('cd ../searchInfo && scrapy crawl %s -o ../datadeal/datadeal/medias/%s_data.json' % (q.name,q.name), shell=True)
            self.message_user(u'%s 爬虫已经抓取完数据  %s' % (q.name,datetime.datetime.now().strftime('%H:%M:%S')))
    start_spider.short_description = "运行爬虫"
    def download(self, request, queryset):
        for q in queryset:
            if os.path.exists(BASE_DIR+'/datadeal/medias/%s_data.json' % q.name):
                return HttpResponseRedirect('/medias/%s_data.json' % q.name)
            else:
                self.message_user(u'%s 数据不存在，请先运行爬虫' % q.name)
    download.short_description = "数据下载"
xadmin.site.register(scrapyList, scrapyListAdmin)

class SpiderDataAdmin(object):
    list_display = ['scrapyname','create_at','data_str','page_pdf']
    search_fields = ['scrapyname','uid','data','url','file']
    list_filter = ['scrapyname','create_at']
xadmin.site.register(SpiderData, SpiderDataAdmin)

class ErrorDataAdmin(object):
    list_display = ['scrapyname','uid','create_at','url','content']
    search_fields = ['scrapyname','uid','url','content']
    list_filter = ['scrapyname','create_at']
xadmin.site.register(ErrorData, ErrorDataAdmin)

class DataAlarmAdmin(object):
    list_display = ['scrapyname','is_alarm','remark','create_at']
    search_fields = ['scrapyname','remark']
    list_filter = ['scrapyname','is_alarm','create_at']
    list_editable = ['is_alarm','remark']
xadmin.site.register(DataAlarm, DataAlarmAdmin)

class ImagesAdminView(CommAdminView):

    def get(self, request, *args, **kwargs):
        images_dir = BASE_DIR+'/datadeal/medias/images'
        images = os.listdir(images_dir)
        img_list = []
        for image in images:
            url = images_dir+'/'+image
            ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getctime(url)+8*3600))
            img_list.append({'url':image,'ctime':ctime})
        img_list.sort(key=lambda x:x['ctime'],reverse=True)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(img_list,12, request=request)
        img_list = p.page(page)

        context = self.get_context()
        context.update({
            'p':p,
            'img_list':img_list
        })
        return self.template_response('images_admin.html',context)
xadmin.site.register_view(r'^images_admin/$', ImagesAdminView, name='images_admin')

class FilesAdminView(CommAdminView):

    def get(self, request, *args, **kwargs):
        dir_list = ['common','risk']
        file_list = []
        for d in dir_list:
            files_dir = BASE_DIR+'/datadeal/medias/'+d
            files = os.listdir(files_dir)
            for file in files:
                import locale
                file = file.decode(locale.getdefaultlocale()[1])
                url = files_dir+'/'+file
                ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getctime(url)+8*3600))
                file_list.append([file,ctime,'<a href="/medias/'+d+'/'+file+'" style="margin-right:20px;">下载</a><a data-toggle="modal" data-target="#myModal" onclick="set_val(\''+file+'\');" >删除</a>'])

        context = self.get_context()
        context.update({
            'file_list':json.dumps(file_list)
        })
        return self.template_response('files_admin.html',context)
xadmin.site.register_view(r'^files_admin/$', FilesAdminView, name='files_admin')