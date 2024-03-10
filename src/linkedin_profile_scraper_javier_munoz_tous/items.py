# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Profile(scrapy.Item):
    name = scrapy.Field()
    image_url = scrapy.Field()
    location = scrapy.Field()
    job_history = scrapy.Field()
    education_history = scrapy.Field()
