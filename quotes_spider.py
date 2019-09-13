# -*- coding: utf-8 -*-

import scrapy
import logging
import urllib
from googletrans import Translator


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }
    start_urls = [
        'https://www.vegrecipesofindia.com/recipes/desserts-recipes/',
    ]

    def __repr__(self):
        data = self.copy()
        for k in data.keys():
            if type(data[k]) is unicode:
                data[k] = data[k].encode('utf-8')
        return super.__repr__(data)

    def parse(self, response):
        translator = Translator()

        mainHeading = response.css("main.site-main h1.entry-title::text").extract_first()
        for quote in response.css("div.wprm-recipe-template-vroi"):

            prepTime = ''
            for span in quote.css("div.wprm-recipe-prep-time-container span.wprm-recipe-time"):
                text = span.css("span::text").getall()
                for t in text:
                    prepTime = prepTime + ' ' + t.strip()

            cookTime = ''
            for span in quote.css("div.wprm-recipe-cook-time-container span.wprm-recipe-time"):
                text = span.css("span::text").getall()
                for t in text:
                    cookTime = cookTime + ' ' + t.strip()

            ing = []
            for ingredient in quote.css("ul.wprm-recipe-ingredients li.wprm-recipe-ingredient"):
                amount = ingredient.css("span.wprm-recipe-ingredient-amount::text").extract_first()
                unit = ingredient.css("span.wprm-recipe-ingredient-unit::text").extract_first()
                name = ingredient.css("span.wprm-recipe-ingredient-name::text").extract_first()
                notes = ingredient.css("span.wprm-recipe-ingredient-notes::text").extract_first()
                ingred = ''
                if amount:
                    ingred = ingred + ' ' + amount
                if unit:
                    ingred = ingred + ' ' + unit
                if name:
                    ingred = ingred + ' ' + name
                if notes:
                    ingred = ingred + ' ' + notes
                ing.append(ingred)

            translatedIngedients = []
            translations = translator.translate(ing, dest='hi')
            for translation in translations:
                translatedIngedients.append(translation.text)

            instructionsData = []
            for instructions in quote.css("div.wprm-recipe-instruction-group"):
                steps = []
                instru = []
                heading = instructions.css("h4::text").extract_first()
                if heading:
                    instru.insert(0, heading.strip());
                for instruction in instructions.css("ul.wprm-recipe-instructions li.wprm-recipe-instruction"):
                    step = instruction.css("div.wprm-recipe-instruction-text::text").extract_first()
                    if step:
                        step = step.strip()
                        steps.append(step)
                    step = instruction.css("div.wprm-recipe-instruction-text span::text").extract_first()
                    if step:
                        step = step.strip()
                        steps.append(step)

                translatedSteps = []
                translations = translator.translate(steps, dest='hi')
                for translation in translations:
                    translatedSteps.append(translation.text)
                instru.insert(1, translatedSteps);
                instructionsData.append(instru)

            yield {
                'heading': mainHeading.strip(),
                'prepTime': prepTime.strip(),
                'cookTime': cookTime.strip(),
                'ingredients': translatedIngedients,
                'instructions': instructionsData
            }
        for anchor in response.selector.xpath("//h2/a/@href"):
            next_page_url = anchor.get()
            if next_page_url is not None:
                yield scrapy.Request(response.urljoin(next_page_url))