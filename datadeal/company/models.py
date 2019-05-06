#coding:utf8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(u'企业名称',max_length=50)
    address = models.CharField(u'企业地址',max_length=100)
    creditcode = models.CharField(u'统一社会信用代码',max_length=50,null=True)
    registration = models.CharField(u'注册号',max_length=50)
    organization = models.CharField(u'组织机构代码',max_length=50,null=True)
    kind = models.CharField(u'公司类型',max_length=50,null=True)
    status = models.CharField(u'经营状态',max_length=50,null=True)
    legalperson = models.CharField(u'法定代表人',max_length=50)
    start_at = models.DateField(u'经营日期',null=True)
    capital = models.CharField(u'注册资本',max_length=50,null=True)
    deadline = models.CharField(u'营业期限',max_length=50,null=True)
    give_at = models.DateField(u'发照日期',null=True)
    webpage = models.CharField(u'网址',max_length=50,null=True)
    authority = models.CharField(u'登记机关',max_length=50,null=True)
    scope = models.TextField(u'经营范围',null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'公司信息'
        verbose_name_plural = u'公司信息管理'


class Shareholders(models.Model):
    name = models.CharField(u'股东',max_length=50)
    kind = models.CharField(u'类型',max_length=50)
    subcribe_money = models.CharField(u'认缴出资金额',max_length=50,null=True)
    subcribe_date = models.DateField(u'认缴出资时间',null=True)
    real_money = models.CharField(u'实缴出资金额',max_length=50,null=True)
    real_date = models.DateField(u'实缴出资时间',null=True)
    company = models.ForeignKey('Company',verbose_name=u'公司')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'股东信息'
        verbose_name_plural = u'股东信息管理'

class Member(models.Model):
    name = models.CharField(u'名字',max_length=50)
    kind = models.CharField(u'身份',max_length=50)
    company = models.ForeignKey('Company',verbose_name=u'公司')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'成员信息'
        verbose_name_plural = u'成员信息管理'