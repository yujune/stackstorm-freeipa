import sys
import requests
from st2common.runners.base_action import Action
import json


class UpdateMessage(Action):
    def run(self, webhook_data):
        # use web APIs which send data back and forth using HTTP requests. These requests often return JSON or XML response
        # print(webhook_data)
        postId = webhook_data
        update_post_api = "http://10.13.17.38:30778/api/v4/posts/" + postId
        #print('Post url', update_post_api)

        payload = {
            "id": postId,
            "is_pinned": True,
            "message": "Updated Successfully",
            "has_reactions": True,
            "props": "string"
        }

        response = requests.put(update_post_api, json=payload,
                                headers={'Authorization': 'Bearer qtnkoa33138ibexnn1cdfwfkqr', 'Content-Type': 'application/json'})

        if response.status_code != 200:

            raise ValueError(

                'Request to mattermost returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )

        print(response)

        return(True, webhook_data)
