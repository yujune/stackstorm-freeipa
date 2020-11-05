from st2common.runners.base_action import Action
import requests
import json


class GetEmail(Action):
    def run(self, user_id):

        apiURL = 'http://10.13.17.38:30778/api/v4/users/' + user_id
        response = requests.get(
            apiURL, headers={'Authorization': 'Bearer qtnkoa33138ibexnn1cdfwfkqr'})

        if response.status_code != 200:

            raise ValueError(

                'Request to mattermost returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )

        print(response)

        return(True, response)
