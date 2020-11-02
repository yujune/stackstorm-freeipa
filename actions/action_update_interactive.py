import sys
import requests
from st2common.runners.base_action import Action
import json


class UpdateMessage(Action):
    def run(self, webhook_data):
        URL = 'http://10.13.17.38:30778/hooks/7cr3y16a5jgtuexwikfy4pomoa'
        update_post_api = 'http://10.13.17.38:30778/api/v4/posts/{post_id}'
        token = 'kbj3jhd7mt87ub8kxp6hbjyj3a'
        payload = json.dumps(
            {
                "channel": "freeipa",
                "post_id": "6bgr18jo5t8tbqm7fe5mfzu7se",
                "text": "testing123",
                "update": {
                    "message": "Updated!",
                    "props": {}
                },
                "ephemeral_text": "You updated the post!"
            })
        response = requests.post(URL, data=payload, headers={
                                 'Content-Type': 'application/json'}, verify=False)

        if response.status_code != 200:

            raise ValueError(

                'Request to mattermost returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )

        return(True, webhook_data)
