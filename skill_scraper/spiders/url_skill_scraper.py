import scrapy
import re
from ..skills import AlexaSkillItem
from pandas import *


'''
This class is a spider that scrapes information about Amazon Alexa Skills
'''
class AlexaSkillSpider(scrapy.Spider):
  name = 'url_skill_spider'
  allowed_domains = ['amazon.com']
  # Get the start URLs
  data = read_csv("skill_URLs.csv")
  start_urls = data['skill_link'].tolist()
 
  '''
  This function takes the URL of the skills from the CSV and then parses the
  title, rating, # of reviews, description, and URL of the skill
  '''
  def parse(self, response):
    skills = AlexaSkillItem()

    # Get the page information we want
    skill_name = re.sub(
      '[\r\n\t]','', str(response.css('.a2s-title-content::text').extract_first()))
    skill_link =  response.url
    skill_rating = response.css('.a-size-medium.a-color-base').css('::text').extract_first(default='No Rating')
    skill_reviews = re.sub("[^0-9]", "", response.css('.a-size-small.a-color-link.a2s-review-star-count').css('::text').extract_first())
    # Extract the description
    temp = response.css('#a2s-description > span').css('::text').extract()
    skill_description = re.sub('[\r\n\t]','', " ".join(temp))

    # Set values for lists
    skills['skill_name'] = skill_name
    skills['skill_description'] = skill_description
    skills['skill_link'] = skill_link
    skills['skill_reviews'] = skill_reviews
    skills['skill_rating'] = skill_rating

    yield skills
