from django.core.management.base import BaseCommand
from FreshPoint.models import Vegetable
import json


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('us_vegetable_season_data.json') as json_file:
            data = json.load(json_file)

        for veg in data:  # for each item in JSON file
            veg_name = veg['name']  # get item name
            veg_type = veg['type']  # get item type
            veg_image = veg['image']  # get item image
            veg_desc = veg['desc']  # get item description

            # create new Vegetable item and save to model
            product_item = Vegetable(veg_name=veg_name, veg_type=veg_type, veg_image=veg_image, veg_desc=veg_desc)
            product_item.save()

            # print confirmation of item imported
            print(veg_name+' imported.')
            print(veg_type+' '+veg_image+'\n'+veg_desc)
    pass
