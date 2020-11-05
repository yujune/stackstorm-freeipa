import requests
from st2common.runners.base_action import Action
import sys


class Http200(Action):
    def run(self, response_url):
        print(type(str(response_url)))
        formated = response_url.splitlines()
        print(formated)

        response = requests.get('https://www.google.com')
        return(True, response)
