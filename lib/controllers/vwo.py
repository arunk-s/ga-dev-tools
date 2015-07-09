import webapp2
import urllib2
import urllib
import json
import re
import logging


class VwoController(webapp2.RequestHandler):

    def get(self):
        token = self.request.get("api_token")
        account_id = self.request.get("vwo_account")
        goal_urls = self.request.get("goal_urls").split(",")
        correct = False
        payload = {
            "type": "conversion",
            "urls": [{
                "type": "url",
                "value": "",
            }],
            "primaryUrl": "",
            "goals": []
        }
        url = "https://app.vwo.com/api/v2/accounts/" + \
            account_id + "/campaigns"
        pattern = re.compile(
            "^(http[s]?:\\/\\/(www\\.)?|ftp:\\/\\/(www\\.)?|www\\.){1}([0-9A-Za-z-\\.@:%_\+~#=]+)+((\\.[a-zA-Z]{2,3})+)(/(.)*)?(\\?(.)*)?")
        if token != None and account_id != None and goal_urls != None:
            for index,goal in enumerate(goal_urls):
                if goal != "" and pattern.match(goal):
                    correct = True
                    if payload["primaryUrl"] == "":
                        payload["primaryUrl"] = goal
                    if payload["urls"][0]["value"] == "":
                        payload["urls"][0]["value"] = goal
                    payload["goals"].append(
                        {
                            "name": "New goal"+str(index),
                            "type": "visitPage",
                            "urls": [{
                                "type": "url",
                                "value": goal}]
                        }
                    )

        payload = json.dumps(payload)
        if correct:
            r = urllib2.Request(url, payload)
            r.add_header('token', token)
            req = urllib2.urlopen(r)
            response = req.read()
            self.code = req.getcode()
        else:
            logging.error("Payload Not Correctly formed")
        if self.code and (self.code == 201 or self.code == 200):
            self.response.out.write("Success!")
        else:
            self.response.out.write("Request Failed")
