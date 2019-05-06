# -*- coding: utf-8 -*-
import xadmin
from .models import *

class CompanyAdmin(object):
    list_display = ['name','address','creditcode','registration','organization','kind','status','legalperson','start_at','capital','deadline','give_at','webpage','authority','scope']
    search_fields = ['name','address','creditcode','registration','organization','kind','status','legalperson','capital','deadline','webpage','authority','scope']
    list_filter = ['start_at','give_at']
xadmin.site.register(Company, CompanyAdmin)

class ShareholdersAdmin(object):
    list_display = ['name','kind','subcribe_money','subcribe_date','real_money','real_date','company']
    search_fields = ['name','kind','subcribe_money','subcribe_date','real_money','real_date']
    list_filter = ['company']
xadmin.site.register(Shareholders, ShareholdersAdmin)

class MemberAdmin(object):
    list_display = ['name','kind','company']
    search_fields = ['name','kind']
    list_filter = ['company']
xadmin.site.register(Member, MemberAdmin)