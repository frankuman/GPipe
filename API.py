import json
import requests
import pandas as pd
from pygerrit2 import HTTPBasicAuth
import sys
import GUI
#Big thanks to @larsks over at 
#https://stackoverflow.com/questions/75446633/how-do-i-get-more-than-500-codereviews-with-gerrit-rest-api

class Gerrit:
    """Wrap up Gerrit API functionality in a simple class to make
    it easier to consume from our code. This limited example only
    supports the `changes` endpoint.

    See https://gerrit-review.googlesource.com/Documentation/rest-api.html
    for complete REST API documentation.
    """

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def changes(self, PLATFORM, query, root, start=None, limit=None, options=None):
        """This implements the API described in [1].

        [1]: https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html
        """
        #This is so bad authentication, it does not say anywhere that this his how you should do. Gerrit/chromium
        # has this hidden in their "generate HTTP password and i had to figure this shit out by testing"
        
        
        #auth = HTTPBasicAuth(username=username,password=password) We can authenticate, but why? 
        params = {"q": query}
        
        if start is not None:
            params["-S"] = start
        if limit is not None:
            params["n"] = limit
        if options is not None:
            params["o"] = options
        if(PLATFORM != "https://review.opendev.org"):
            res = requests.get(f"{self.baseurl}/changes/", params=params)
        else:
            res = requests.get(f"{self.baseurl}/changes/", params=params,)
        root.textbox.configure(
            font=("Consolas", 20)
        )  # Only works with consolas, no matter
        print(f"fetched [{res.status_code}]: {res.url}", file=sys.stderr)
        a = "fetched: status = " + str(res.status_code)
        root.textbox.insert("1.0", a + "\n")

        #print(res.text[4:])
        error_code = res.status_code
        try:
            return json.loads(res.text[4:]),error_code
        except json.decoder.JSONDecodeError:
            return res,error_code


    @staticmethod
    def generateJSON(JSON_response):
        """
        Generates and saves the data as a JSON names out.json
        """
        # Here we're just dumping all the results as a JSON document on
        # stdout.
        file_name = "JSON/out.json"
        with open(file_name, "w") as json_file:
            json.dump(JSON_response, json_file, indent=4)
        return

    def requestAPICall(url,PLATFORM,DATE_1,DATE_2,SET_TIME_1,SET_TIME_2,root):
        """
        does API stuff
        """
        if(PLATFORM != "https://review.opendev.org"):
            error = Gerrit.REST_call_google(url,PLATFORM,DATE_1,DATE_2,SET_TIME_1,SET_TIME_2,root)
            return error
        else:
            response = Gerrit(PLATFORM)
            all_results = []
            date_string = 'since:"'+DATE_2+" "+SET_TIME_2+'" before:"'+DATE_1+" "+SET_TIME_1+'"'
            print(date_string)
            start = 0
            while True:
                res,error = response.changes(
                    PLATFORM,
                    date_string,
                    root,
                    limit=5000,
                    start=start
                    )
                if not res:
                    break
                all_results.extend(res)
                if not res[-1].get("_more_changes"):
                    break
                start += len(res)
            Gerrit.generateJSON(all_results)
            return error
    def REST_call_google(url,PLATFORM,DATE_1,DATE_2,SET_TIME_1,SET_TIME_2,root):
            all_results = []
            response = Gerrit(PLATFORM)
            more_data = True
            error = 0
            while more_data == True:
                
                date_string = 'since:"'+DATE_2+" "+SET_TIME_2+'" before:"'+DATE_1+" "+SET_TIME_1+'"'
                print(date_string)
                start = 0
                while True:
                    res,err = response.changes(
                        PLATFORM,
                        date_string,
                        root,
                        limit=5000,
                        start=start
                        
                        )
                    error = err
                    if start == 19500:
                        more_data = True
                        break
                    if not res:
                        more_data = False
                        break
                    all_results.extend(res)
                    if not res[-1].get("_more_changes"):
                        more_data = False
                        break
                    if error != 200:
                        break
                    start += len(res)
                if more_data:
                    Gerrit.generateJSON(all_results)
                    DATE_1,SET_TIME_1 = Gerrit.generate_new_date(all_results)
            Gerrit.generateJSON(all_results)
            return error
    def generate_new_date(all_results):
        with open("JSON/out.json", "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df = df["updated"].apply(lambda x: x.split(".")[0])
        
        last_updated = df.min()
        last_date, last_time = last_updated.split(' ')
        print(last_updated)
        return last_date,last_time