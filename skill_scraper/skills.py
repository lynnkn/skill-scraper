import scrapy


class AlexaSkillItem(scrapy.Item):
  skill_name = scrapy.Field()
  skill_link = scrapy.Field()
  skill_description = scrapy.Field()
  skill_rating = scrapy.Field()
  skill_reviews = scrapy.Field()

  pass
