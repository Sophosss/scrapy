#coding:utf8
from django.db import models
from datadeal.settings import BASE_DIR
from django.contrib.postgres.fields import HStoreField

class scrapySetting(models.Model):
    KIND_CHOICES = ((1, u'列表及详情'),(2, u'列表'),(3,u'单页面'),(4,u'其他'))
    name = models.CharField(u'名称',max_length=20,help_text='不要输入中文和特殊符号')
    allow_domains = models.ManyToManyField('AllowDomains',verbose_name=u'域名白名单')
    start_urls = models.ManyToManyField('startUrls',verbose_name=u'一级爬取地址列表')
    cycleobj = models.ManyToManyField('CycleObj',verbose_name=u'循环体',blank=True)
    variable = models.ManyToManyField('Variable',verbose_name=u'非循环变量',blank=True)
    num = models.IntegerField(u'单个任务链接数',default=1)
    kind = models.IntegerField(u'类型', choices=KIND_CHOICES,default=1)
    create_at = models.DateTimeField(u'创建时间', auto_now_add=True)
    modify_at = models.DateTimeField(u'修改时间', auto_now=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'爬虫配置'
        verbose_name_plural = u'爬虫配置管理'

class AllowDomains(models.Model):
    name = models.CharField(u'名称',max_length=500)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'域名白名单'
        verbose_name_plural = u'域名白名单管理'

class startUrls(models.Model):
    url = models.URLField(u'名称',max_length=500)

    def __unicode__(self):
        return self.url

    class Meta:
        verbose_name = u'一级爬取地址列表'
        verbose_name_plural = u'一级爬取地址列表管理'

class CycleObj(models.Model):
    name = models.CharField(u'循环体名称',max_length=50,help_text='不要输入中文和特殊符号')
    xpath = models.CharField(u'查询规则',max_length=200,help_text='使用xpath规则：\nnodename 选择所有目前节的子节\n/ 从根节进行选择\n// 选择文档中相吻合的节而不管其在文档的何处\n. 选择当前节\n.. 当前节的父节\n@ 选择属性')
    variable = models.ManyToManyField('Variable',verbose_name=u'变量')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'循环体列表'
        verbose_name_plural = u'循环体列表管理'

class Variable(models.Model):
    KIND_CHOICES = ((1, u'一级变量'), (2, u'二级变量'),(3,u'二级链接'))
    name = models.CharField(u'变量名称',max_length=50,help_text='不要输入中文和特殊符号,建议用对应的循环体做前缀加以区分')
    xpath = models.CharField(u'查询规则',max_length=200,help_text='使用xpath规则：\nnodename 选择所有目前节的子节\n/ 从根节进行选择\n// 选择文档中相吻合的节而不管其在文档的何处\n. 选择当前节\n.. 当前节的父节\n@ 选择属性')
    kind = models.IntegerField(u'类型', choices=KIND_CHOICES,default=1)
    all_text = models.BooleanField(u'子标签文本提取',default=False,help_text='将提取该标签下文本及所有子标签文本,开启后不要写/text()')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'变量列表'
        verbose_name_plural = u'变量列表管理'

class scrapyList(models.Model):
    name = models.CharField(u'名称',max_length=500)
    priority = models.IntegerField(u'项目优先级',default=10,help_text='值越小越优先')
    alarm_day = models.IntegerField(u'预警天数',default=30,help_text='超过时间无数据则生成预警')
    is_open = models.BooleanField(u'是否启用',default=True)
    create_at = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'爬虫列表'
        verbose_name_plural = u'爬虫列表管理'

class SpiderData(models.Model):
    scrapyname = models.CharField(u'项目来源',max_length=50)
    uid = models.CharField(u'设备来源',max_length=50)
    create_at = models.DateTimeField(u'创建时间', auto_now_add=True)
    data = HStoreField()
    url = models.CharField(u'访问地址',max_length=300,null=True,blank=True)
    file = models.CharField(u'原页面',max_length=100,null=True,blank=True)
    
    def __unicode__(self):
        return self.scrapyname

    def data_str(self):
        data_str = ''
        for key,val in self.data.items():
            if not val:
                val = ''
            data_str += key+'=>'+val+'///'
        return data_str
    data_str.short_description = u'数据信息'

    def page_pdf(self):
        if self.file:
            url = '/medias/web/'+self.file
            return '<a target=_blank href="%s">%s</a>' % (url,self.file)
        else:
            return ''
    page_pdf.allow_tags = True
    page_pdf.short_description = u'页面pdf'

    class Meta:
        verbose_name = u'数据信息'
        verbose_name_plural = u'数据信息管理'

class ErrorData(models.Model):
    scrapyname = models.CharField(u'爬虫名',max_length=50)
    uid = models.CharField(u'设备来源',max_length=50)
    create_at = models.DateTimeField(u'创建时间', auto_now_add=True)
    url = models.CharField(u'访问地址',max_length=300)
    content = models.CharField(u'错误信息',max_length=300)
    
    def __unicode__(self):
        return self.scrapyname

    class Meta:
        verbose_name = u'错误信息'
        verbose_name_plural = u'错误信息管理'


class DataAlarm(models.Model):
    scrapyname = models.CharField(u'爬虫名',max_length=50)
    is_alarm = models.BooleanField(u'是否预警',default=True)
    remark = models.TextField(u'原因备注',null=True,blank=True)
    create_at = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __unicode__(self):
        return self.scrapyname

    class Meta:
        verbose_name = u'爬虫预警'
        verbose_name_plural = u'爬虫预警管理'