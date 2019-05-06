# -*- coding: utf-8 -*-
from searchInfo import settings
import requests
import hashlib
import os

class FilesDownloadPipeline(object):
    def process_item(self, item, spider):

        if 'file_urls' in item:
            dir_path = '%s/%s' % (settings.FILES_STORE, spider.name)
            img_path = settings.IMAGES_STORE
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            if not os.path.exists(img_path):
                os.makedirs(img_path)
            for file_url in item['file_urls']:
                file_name = file_url.split('/')[-1]
                back = file_name.split('.')[-1]
                m = hashlib.md5()
                m.update(file_name)
                file_name = m.hexdigest()
                if spider.name == 'shandong':
                    file_name = file_name+'.png'
                    file_path = '%s/%s' % (img_path, file_name)
                elif back == 'png' or back == 'jpg' or back == 'gif':
                    file_name = file_name+'.'+back
                    file_path = '%s/%s' % (img_path, file_name)
                else:
                    file_name = spider.name+'_'+file_name+'.'+back
                    file_path = '%s/%s' % (dir_path, file_name)
                if os.path.exists(file_path):
                    continue
                with open(file_path, 'wb') as handle:
                    response = requests.get(file_url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
        return item