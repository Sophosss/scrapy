# python manage.py register_node   注册节点
# python manage.py get_spiders     同步爬虫文件
# scrapy crawl spider_name         开始爬虫(根据爬虫名)
# python manage.py start_spider    开始爬虫(自动获取主机任务)

#上传已下载文件至主机方法
# python manage.py upload_files (可选medias下的单个目录，不加目录名则默认所有目录上传)  

# 企业爬虫
# python manage.py save_company

# 爬取行政处罚
scrapy crawl case                   # 山东行政处罚
scrapy crawl shanghai               
scrapy crawl beijing
scrapy crawl hainan
scrapy crawl gansu
scrapy crawl common

scrapy crawl shandong               # 信用山东图片
scrapy crawl risk                   # 国家风险检测文件