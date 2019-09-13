from googletrans import Translator
import json

filename = "quotes.json"

if filename:
    # Writing JSON data
    with open(filename, 'r') as f:
        datastore = json.load(f)
        strs = str(json.dumps(datastore))

        translator = Translator()
        steps = [" 2 cups besan (gram flour)", " \u00bd to \u2154 cup ghee - add more ghee, if required", " 1 cup powdered sugar or boora", " 4 green cardamoms - powdered in a mortar-pestle (choti elaichi or hari elaichi)", " 1 or 2 tablespoon golden raisins (kishmish)"]
        translations = translator.translate(steps, dest='hi')
        # print(translations)
        for translation in translations:
        	print(translation.origin, ' -> ', translation.text)