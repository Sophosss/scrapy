#coding:utf8
from __future__ import unicode_literals

from django.db import models

class Node(models.Model):
    uid = models.CharField(u'uid',max_length=50)
    status = models.BooleanField(u'是否开启',default=True)
    ips = models.ManyToManyField('NodeIp',verbose_name=u'历史IP',blank=True)
    max_num = models.IntegerField(u'最大任务频度',help_text='单位: 次/天(同项目同ip)',default=10)

    def __unicode__(self):
        return self.uid

    class Meta:
        verbose_name = u'节点管理'
        verbose_name_plural = u'节点管理'

class NodeIp(models.Model):
    ip = models.CharField(u'ip地址',max_length=100)
    create_at = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __unicode__(self):
        return self.ip

    class Meta:
        verbose_name = u'节点IP管理'
        verbose_name_plural = u'节点IP管理'

class NodeTask(models.Model):
    STATUS_CHOICES = ((1, u'待采集'),(2, u'已完成'))
    name = models.CharField(u'任务名',max_length=50)
    scrapy = models.ForeignKey('datadeal.scrapyList',verbose_name=u'项目')
    priority = models.IntegerField(u'任务优先级',default=10,help_text='值越小越优先')
    urls = models.ManyToManyField('datadeal.startUrls',verbose_name=u'爬取链接')
    status = models.IntegerField(u'任务状态', choices=STATUS_CHOICES,default=1)
    create_at = models.DateTimeField(u'创建时间', auto_now_add=True)
    get_at = models.DateTimeField(u'任务领取时间',null=True,blank=True)
    over_at = models.DateTimeField(u'任务完成时间',null=True,blank=True)
    node = models.ForeignKey('Node',verbose_name=u'执行节点',blank=True,null=True)
    nodeip = models.ForeignKey('NodeIp',verbose_name=u'执行IP',blank=True,null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'任务管理'
        verbose_name_plural = u'任务管理'