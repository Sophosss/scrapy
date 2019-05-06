#!coding=utf-8
from django.views.generic import TemplateView,View
from django.http import HttpResponse,HttpResponseRedirect
from datadeal.settings import BASE_DIR
from .models import scrapySetting
import urllib,urllib2
import bs4
import os

def get_nocycle_variables(nocycle_variable):
    v_dict = ''
    result = ''
    nvname_list = []
    for nov in nocycle_variable:
        nvname_list.append(nov.name)
        v_dict += '\'%s\':%s,' % (nov.name,nov.name)
        if nov.all_text:
            all_text = '.xpath(\'string(.)\')'
        else:
            all_text = ''
        result += ' '*8+nov.name+' = response.xpath(\''+nov.xpath+'\')'+all_text+'.extract_first()\n'
    return v_dict,result,nvname_list


def create_scrapy_file(q):
    """
    创建scrapy爬虫文件方法
    """
    allow_domains = '['
    for i,val in enumerate(q.allow_domains.all()):
        if i == len(q.allow_domains.all())-1:
            allow_domains += '"'+val.name+'"'
        else:
            allow_domains += '"'+val.name+'"'+ ','
    allow_domains += ']'
    start_requests = '    def start_requests(self):\n'+' '*8+'results = getTasks(\''+q.name+'\')\n'+' '*8+'self.taks_urls = {}\n'+' '*8+'self.tasks = {}\n'+' '*8+'if isinstance(results,dict):\n'+' '*12+'print results[\'error\']\n'+' '*8+'else:\n'+' '*12+'for re in results:\n'+' '*16+'self.tasks[re[\'id\']] = {\'t_count\':len(re[\'urls\']),\'count\':0}\n'+' '*16+'for u in re[\'urls\']:\n'+' '*20+'self.taks_urls[u] = re[\'id\']\n'+' '*20+'yield self.make_requests_from_url(u)\n\n'
    after_parse = '    def after_parse(self,url):\n'+' '*8+'task_id = self.taks_urls[url]\n'+' '*8+'self.tasks[task_id][\'count\'] += 1\n'+' '*8+'if self.tasks[task_id][\'count\'] == self.tasks[task_id][\'t_count\']:\n'+' '*12+'afterTasks(task_id)\n\n'

    nocycle_variable = q.variable.filter(kind=1)
    v_dict,cycleobj,nvname_list = get_nocycle_variables(nocycle_variable)
    cycleobjs = q.cycleobj.all()
    if len(cycleobjs):
        next_url = ''                               #判断是否有子查询链接
        next_variable = []
        v_list = []
        total_v_list = []
        total_v_list += nvname_list
        v_list += nvname_list
        c_dict = ''
        for c in cycleobjs:
            variables = c.variable.all()
            variable = ''
            for v in variables:
                #包含子标签文本提取
                if v.all_text:
                    v_str = '%s = i.xpath(\'%s\').xpath(\'string(.)\').extract_first()\n' % (v.name,v.xpath)
                else:
                    v_str = '%s = i.xpath(\'%s\').extract_first()\n' % (v.name,v.xpath)
                if v.kind == 1:
                    variable += ' '*12+v_str
                    v_dict += '\'%s\':%s,' % (v.name,v.name)
                    c_dict += '\'%s\':%s,' % (v.name,v.name)
                    v_list.append(v.name)
                    total_v_list.append(v.name)
                elif v.kind == 2:
                    next_variable.append({'name':v.name,'xpath':v.xpath,'all_text':v.all_text})
                    if not v.name in total_v_list:
                        total_v_list.append(v.name)
                elif v.kind == 3:
                    next_url = v.name
                    variable += ' '*12+v_str
            if next_url:
                cycleobj += ' '*8+c.name+' = response.xpath(\''+c.xpath+'\')\n'+' '*8+'for i in %s:\n%s' % (c.name,variable)
                cycleobj += ' '*12+next_url+' = set_url_head('+next_url+',response.url)\n'+' '*12+'if '+next_url+':\n'+' '*16+'yield scrapy.Request('+next_url+', callback=self.parse_item,meta={'+v_dict+'})\n'
            else:
                nvname_list.append(c.name+'_data')
                c_dict = c_dict[0:-1]
                cycleobj += ' '*8+c.name+' = response.xpath(\''+c.xpath+'\')\n'+' '*8+c.name+'_data = []\n'+' '*8+'for i in '+c.name+':\n'+variable+' '*12+c.name+'_data.append({'+c_dict+'})\n'
        cycleobj += ' '*8+'self.after_parse(response.url)\n'
        if next_url:
            cycleobj += '\n'+' '*4+'def parse_item(self, response):\n'
            for vl in v_list:
                cycleobj += ' '*8+vl+' = response.meta[\''+vl+'\']\n'
            for nv in next_variable:
                if nv['all_text']:
                    cycleobj += ' '*8+'%s = response.xpath(\'%s\').xpath(\'string(.)\').extract_first()\n' % (nv['name'],nv['xpath'])
                else:
                    cycleobj += ' '*8+'%s = response.xpath(\'%s\').extract_first()\n' % (nv['name'],nv['xpath'])
            data = ''
            for total in total_v_list:
                data += '\'%s\':%s,' % (total,total)
            data = data[0:-1]
            cycleobj += ' '*8+'sendData(\'%s\',{%s},response.url)' % (q.name,data)
        else:
            no_next = ''
            for n in nvname_list:
                no_next += '\'%s\':%s,' % (n,n)
            no_next = no_next[0:-1]
            cycleobj += ' '*8+'sendData(\'%s\',{%s},response.url)' % (q.name,no_next)
    else:                                               # 单页面爬虫
        v_dict = v_dict[0:-1]
        cycleobj = nv_str+' '*8+'data = {'+v_dict+'}\n'+' '*8+'self.after_parse(response.url)\n'+' '*8+'sendData(\''+q.name+'\',data,response.url)'

    with open(BASE_DIR+'/../searchInfo/searchInfo/spiders/%s.py' % q.name,'w') as f:
        f.write('# -*- coding: utf-8 -*-\nimport scrapy\nfrom distribute.views import *\n\nclass '+q.name+'Spider(scrapy.Spider):\n    name = "'+q.name+'"\n    allowed_domains = '+allow_domains+'\n\n'+start_requests+after_parse+'    def parse(self, response):\n'+cycleobj)

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        
        context.update({
            'kind':scrapySetting.KIND_CHOICES
        })
        return context

class AjaxBackHtmlView(View):
   
    def post(self,request):
        url = request.POST.get('url','')
        frame = request.POST.get('frame','')
        proto, rest = urllib.splittype(url)
        domain, rest = urllib.splithost(rest)
        f = urllib2.urlopen(url)
        result = f.read()
        soup = bs4.BeautifulSoup(result,'lxml')
        body = soup.find('html')
        # css样式链接替换
        link = body.find_all('link')
        for l in link:
            if l['href'].startswith('/'):
                l['href'] = proto+'://'+domain+l['href']
            elif l['href'].startswith('../'):
                last = l['href'].split('../')[-1]
                l['href'] = proto+'://'+domain+'/'+last
        # js链接替换
        script = body.find_all('script')
        for s in script:
            if s.has_key('src'):
                if s['src'].startswith('/'):
                    s['src'] = proto+'://'+domain+s['src']
                elif s['src'].startswith('../'):
                    last = s['src'].split('../')[-1]
                    s['src'] = proto+'://'+domain+'/'+last
        # img链接替换
        img = body.find_all('img')
        for g in img:
            if g.has_key('src'):
                if g['src'].startswith('/'):
                    g['src'] = proto+'://'+domain+g['src']
                elif g['src'].startswith('../'):
                    last = g['src'].split('../')[-1]
                    g['src'] = proto+'://'+domain+'/'+last
        # a标签链接禁止点击
        a = body.find_all('a')
        for i in a:
            href = i['href']
            i['href'] = 'javascript:void(0);'
            i['href_bak'] = href
            
        if frame == 'list_iframe':
            result = 'list/'
            with open(BASE_DIR+'/datadeal/templates/'+frame+'.html','w') as f:
                f.write(str(body))
                f.write('\n{% load staticfiles %}<script type="text/javascript" src="{% static \'js/jquery-3.2.0.min.js\' %}"></script><script type="text/javascript" src="{% static \'js/iframe_common.js\' %}"></script><script type="text/javascript" src="{% static \'js/iframe_list.js\' %}"></script>')
        elif frame == 'detail_iframe':
            result = 'detail/'
            with open(BASE_DIR+'/datadeal/templates/'+frame+'.html','w') as f:
                f.write(str(body))
                f.write('\n{% load staticfiles %}<script type="text/javascript" src="{% static \'js/jquery-3.2.0.min.js\' %}"></script><script type="text/javascript" src="{% static \'js/iframe_common.js\' %}"></script><script type="text/javascript" src="{% static \'js/iframe_detail.js\' %}"></script>')
        else:
            result = 'other'
        return HttpResponse(result)

class ListFrameView(TemplateView):
    template_name = 'list_iframe.html'

class DetailFrameView(TemplateView):
    template_name = 'detail_iframe.html'


class UploadFilesView(View):
    def post(self,request):
        count = 0
        for name,file in request.FILES.items():
            dir_path = BASE_DIR+'/datadeal/medias/'+name.split('/')[0]
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            path = BASE_DIR+'/datadeal/medias/'+name
            if not os.path.exists(path):
                with open(path, 'wb') as f:
                    f.write(file.read())
                count += 1
        return HttpResponse(u'已上传%s项文件' % count)

class ZipFilesView(View):
    def post(self,request):
        file_type = request.POST.get('type','')
        import zipfile
        zp_name = BASE_DIR+'/datadeal/medias/'+file_type+'.zip' 
        file_list = []
        if os.path.exists(zp_name):
            z_r = zipfile.ZipFile(zp_name, mode='r')
            for filename in z_r.namelist():
                file_list.append(filename)
            z_r.close()

        file_dir = BASE_DIR+'/datadeal/medias/'+file_type
        files = os.listdir(file_dir)
        for f in files:
            if not f in file_list:
                zpfd = zipfile.ZipFile(zp_name, mode='a',compression=zipfile.ZIP_DEFLATED)
                zpfd.write(file_dir+'/'+f,f)
                zpfd.close()
        return HttpResponse('/medias/'+file_type+'.zip')

class DeleteFilesView(View):
    def post(self,request):
        file_name = request.POST.get('file_name','')
        file_path = BASE_DIR+'/datadeal/medias/common/'+file_name 
        status = False
        if os.path.exists(file_path):
            os.remove(file_path)
            status = True
        return HttpResponse(status)