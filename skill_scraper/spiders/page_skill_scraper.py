import scrapy
import re
from ..skills import AlexaSkillItem


'''
This class is a spider that scrapes information about Amazon Alexa Skills
'''
class AlexaSkillSpider(scrapy.Spider):
  name = 'page_skill_spider'
  allowed_domains = ['amazon.com']
  start_urls = ['https://www.amazon.com/s?i=alexa-skills&bbn=14284832011&rh=n%3A13727921011%2Cn%3A14284832011%2Cn%3A19353814011&s=featured-rank&dc&qid=1604460859&rnid=14284832011&ref=sr_nr_n_5']

  '''
  This funciton parses the Amazon page of skills and scrapes the URLs of all
  the skills that are on the page
  '''
  def parse(self, response):
    skills = AlexaSkillItem()

    # Get the skill URLs we want
    # Adds the skill URLs on that page into a list
    temp = response.css('a.a-link-normal.a-text-normal::attr(href)').extract()
    # Initiates a 
    item_links = ['https://www.amazon.com' + i for i in temp]

    for l in item_links:
      request = scrapy.Request(l, callback=self.parse_skill)
      request.meta['links'] = skills
      yield request

    yield skills

    # Go onto next page of Alexa Skills
    next_page = response.css('.a-last > a::attr(href)').extract_first()
    if next_page is not None:
      next_page = "https://www.amazon.com" + next_page
      yield scrapy.Request(url=next_page, callback=self.parse)

  '''
  This function takes the URL of the skill that was scraped from the parse
  method and then parses the title, rating, # of reviews, description, and URL
  of the skill
  '''
  def parse_skill(self, response):
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
