# -*- coding: utf-8 -*-

# Importing Scrapy Library
import scrapy


# Creating a new class to implement Spide
class AmazonReviewsSpider(scrapy.Spider):
    # Spider name
    name = 'amazon_reviews'

    # Domain names to scrape
    allowed_domains = ['amazon.in']

    # Base URL for the MacBook air reviews
    myBaseUrl = "https://www.amazon.in/product-reviews/B07DJHY82F/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
    start_urls = []

    # Creating list of urls to be scraped by appending page number a the end of base url
    for i in range(1, 100):
        start_urls.append(myBaseUrl + str(i))

    # Defining a Scrapy parser
    def parse(self, response):
        data = response.css('#cm_cr-review_list')

        # Collecting product star ratings
        star_rating = data.css('.review-rating')

        # Collecting user reviews
        comments = data.css('.review-text')

        # review_votes = data.css('.cr-vote-text')

        reviewer_name = data.css('.a-profile-name')

        review_title = data.css('.review-title')
        count = 0

        for review in star_rating:
            yield {
                'review_title': (''.join(review_title[count].xpath(".//text()").extract())).replace("\n", ""),
                'reviewer_name': (''.join(reviewer_name[count].xpath(".//text()").extract())).replace("\n", ""),
                'stars': (''.join(review.xpath('.//text()').extract())).replace(" out of 5 stars", ""),
                'comment': (''.join(comments[count].xpath(".//text()").extract())).replace("\n", ""),
                'asin': response.request.url.split('/')[4],
                # 'review': (''.join(review_votes[count].xpath(".//text()").extract())).replace("\n", "").replace(' people found this helpful',''),
            }
            count = count + 1
