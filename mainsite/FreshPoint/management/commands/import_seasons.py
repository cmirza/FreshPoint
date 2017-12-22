from django.core.management.base import BaseCommand
from FreshPoint.models import Season, Vegetable, State
import json
import re


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('us_vegetable_season_data.json') as json_file:
            data = json.load(json_file)

        for product in data:  # for each item in JSON file
            name = product['name']  # get name of item
            states = product['states'][0]  # get states dict from item

            for state_name in states:  # for each item in states dict

                # regex and substitution
                regex = r"\b([0-9])\b"
                subst = r"0\1"

                seasons = states[state_name]['seasons']  # get list of seasons
                seasons = str(seasons)  # turn list of seasons into a string
                seasons = re.sub(regex, subst, seasons) # perform regex to add 0 to single digit numbers

                # get objects from model
                season_veg = Vegetable.objects.get(veg_name=name)
                season_state = State.objects.get(state_name=state_name)

                # create new season item and save to model
                season_data = Season(seasons=seasons, seasons_veg=season_veg, seasons_state=season_state)
                season_data.save()

                # print confirmation of item imported
                print(name+' '+state_name+' imported.')
                print(seasons)
    pass
