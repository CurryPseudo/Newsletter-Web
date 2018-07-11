# -*- encoding: utf8 -*-
source = "../captured/"
file = "*.html"

import re
def pre_process(c):
    c = c.rsplit("</div>", 1)
    c = c[0] + c[1]
    return c

import glob
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsletter.settings')
import django
django.setup()
from news import models
models.News.objects.all().delete()
for file in glob.glob(source + file):
    jsonName = file.rsplit('.', 1)[0] + ".json"
    i = open(file, 'r', encoding='utf-8')
    c = i.read()
    c = pre_process(c)
    i.close()
    meta_data = json.load(open(jsonName, 'r'))
    tags = models.Tag.objects.filter(name__in=meta_data['key_tag'])
    import datetime
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    pub_date = date
    news = models.News(title=meta_data['title'], pub_user=None, author=meta_data['writer'], cover_image = meta_data['first_image'], pub_date = pub_date, content=c, review_pass=True)
    news.save()
    news.tags.set(tags)
    news.save()






