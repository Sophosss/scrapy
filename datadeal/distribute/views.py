#!coding=utf-8
from django.views.generic import TemplateView,View
from django.http import HttpResponse,HttpResponseRedirect
from datadeal.settings import BASE_DIR
from .models import Node,NodeIp,NodeTask
from datadeal.models import SpiderData,ErrorData
import os
import urllib,urllib2
import json
import uuid
import datetime
import pdfkit
import hashlib
import time

# HOST = 'http://192.168.211.1:8000'
HOST = 'http://10.20.1.52:8000'
TASK_NUM = 1

def get_mac_address():
    '''
    获取本机mac地址
    '''
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

def set_url_head(url,r_url):
    '''
    设置url前缀
    '''
    if url:
        if url.startswith('http://') or url.startswith('https://'):
            new_url = url
        else:
            if r_url.endswith('.html'):
                last = r_url.split('/')[-1]
                r_url = r_url.split(last)[0]
            if r_url.startswith('http://'):
                if url.startswith('/'):
                    new_url = 'http://'+r_url.split('http://')[1].split('/')[0]+url
                else:
                    new_url = r_url+url
            elif r_url.startswith('https://'):
                if url.startswith('/'):
                    new_url = 'https://'+r_url.split('https://')[1].split('/')[0]+url
                else:
                    new_url = r_url+url
            else:
                new_url = url
    else:
        new_url = ''
    return new_url

class CreateNode(View):
    name = '注册mac地址(主机)'

    def post(self,request):
        uid = request.POST.get('uid','')
        already = Node.objects.filter(uid=uid).count()
        if not already and uid:
            Node.objects.create(uid=uid)
            msg = u'注册成功'
        else:
            msg = u'该节点已注册'
        return HttpResponse(msg)

class getSpiders(View):
    name = '获取spider文件(主机)'

    def post(self,request):
        uid = request.POST.get('uid','')
        already = Node.objects.filter(uid=uid).count()
        if already and uid:
            dir_name = BASE_DIR+'/../searchInfo/searchInfo/spiders'
            files = os.listdir(dir_name)
            new_files = []
            for f in files:
                if not f.endswith('.pyc') and not f == '__init__.py':
                    new_files.append(f)
            result = {}
            for i in new_files:
                f_name = dir_name+'/'+i
                with open(f_name,'r') as spider:
                    text = spider.read()
                    result[i] = text
        else:
            result = {'error':u'节点未注册'}
        return HttpResponse(json.dumps(result))

def getTasks(name):
    '''
    获取任务(节点)
    '''
    mac = get_mac_address()
    posturl = HOST+'/distribute/handle_tasks/'
    data = {'uid':mac,'num':TASK_NUM,'name':name}
    data = urllib.urlencode(data)
    f = urllib2.urlopen(posturl,data)
    result = json.loads(f.read())
    return result

class handleTasks(View):
    name = '分发任务(主机)'

    def post(self,request):
        uid = request.POST.get('uid','')
        num = int(request.POST.get('num',0))
        name = request.POST.get('name','')
        try:
            node = Node.objects.get(uid=uid,status=True)
        except:
            node = ''
        if node:
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip =  request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            try:
                nip = NodeIp.objects.get(ip=ip)
            except:
                nip = NodeIp.objects.create(ip=ip)
            if not nip in node.ips.all():
                node.ips.add(nip)
            today = datetime.datetime.now().date()
            start = today.strftime('%Y-%m-%d 00:00')
            end = today.strftime('%Y-%m-%d 23:59')
            count = NodeTask.objects.filter(nodeip=nip,get_at__gte=start,get_at__lte=end,scrapy__name=name).count()
            if count < node.max_num:
                if count+num <= node.max_num:
                    result = []
                    tasks = NodeTask.objects.filter(scrapy__name=name,status=1,node__uid__isnull=True).order_by('priority')[0:num]
                    for t in tasks:
                        task = {'id':'','urls':[]}
                        task['id'] = t.id
                        for i in t.urls.all():
                            task['urls'].append(i.url)
                        result.append(task)
                        t.get_at = datetime.datetime.now()
                        t.node = node
                        t.nodeip = nip
                        t.save()
                else:
                    msg = ip+' 单次获取任务个数超过频度限制，请减少单次获取任务个数'
                    print(unicode(msg))
                    result = {'error':msg} 
            else:
                msg = ip+' 超过今日该项目领取任务限制'
                print(unicode(msg))
                result = {'error':msg} 
        else:
            msg = uid+' 节点未注册或已关闭'
            print(unicode(msg))
            result = {'error':msg}
        return HttpResponse(json.dumps(result))

def afterTasks(task_id):
    '''
    完成任务(节点)
    '''
    posturl = HOST+'/distribute/over_tasks/'
    nowtime = datetime.datetime.now()
    data = {'task_id':task_id,'nowtime':nowtime}
    data = urllib.urlencode(data)
    f = urllib2.urlopen(posturl,data)
    result = f.read()
    return result

class overTasks(View):
    name = '任务结束(主机)'

    def post(self,request):
        task_id = request.POST.get('task_id','')
        nowtime = request.POST.get('nowtime','')
        try:
            task = NodeTask.objects.get(id=task_id)
            task.over_at = nowtime
            task.status = 2
            task.save()
        except Exception, e:
            print unicode(e)
        return HttpResponse('over')

def sendData(name,data,url,error=False):
    '''
    发送爬取信息(节点)
    '''
    mac = get_mac_address()
    posturl = HOST+'/distribute/save_data/'
    data = {'uid':mac,'data':data,'name':name,'error':error,'url':url}
    data = urllib.urlencode(data)
    f = urllib2.urlopen(posturl,data)
    result = f.read()
    return result

class SaveData(View):
    name = '保存数据(主机)'

    def post(self,request):
        uid = request.POST.get('uid','')
        name = request.POST.get('name','')
        data = request.POST.get('data','')
        if data:
            try:
                data = eval(data)
            except Exception, e:
                print unicode(e)
                print data
        else:
            data = {}
        url = request.POST.get('url','')
        error = request.POST.get('error','False')

        if error == 'True':
            ErrorData.objects.create(uid=uid,scrapyname=name,url=data['url'],content=data['error'])
            msg = 'error'
        else:
            # 加入保存每条数据访问的页面url与pdf
            m = hashlib.md5()
            # m.update(url+str(time.time()))
            m.update(url)
            pdfname = m.hexdigest()+'.pdf'
            file_dir = BASE_DIR+'/datadeal/medias/web/'
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
            if os.path.exists(file_dir+pdfname):
                pass
            else:
                try:
                    options = {
                        'page-size': 'B3',
                    }
                    pdfkit.from_url(url,file_dir+pdfname,options=options)
                except:
                    pass
   
            SpiderData.objects.create(uid=uid,scrapyname=name,data=data,url=url,file=pdfname)
            msg = 'ok'
        return HttpResponse(msg)

class GetSpiderName(View):
    name = '获取优先可爬取项目名(主机)'

    def post(self,request):
        tasks = NodeTask.objects.filter(get_at__isnull=True).order_by('scrapy__priority')
        print tasks
        if len(tasks) == 0:
            result = ''
        else:
            result = tasks[0].scrapy.name
        return HttpResponse(result)