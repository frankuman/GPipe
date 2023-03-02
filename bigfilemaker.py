import json
import io
import requests
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

    def changes(self, PLATFORM, query, start=None, limit=None, options=None):
        """This implements the API described in [1].

        [1]: https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html
        """

        params = {"q": query}
        if start is not None:
            params["S"] = start
        if limit is not None:
            params["n"] = limit
        if options is not None:
            params["o"] = options
        if(PLATFORM != "https://review.opendev.org"):
            res = requests.get(f"{self.baseurl}/changes", params=params)
        else:
            res = requests.get(f"{self.baseurl}/changes/", params=params)
        print(f"fetched [{res.status_code}]: {res.url}", file=sys.stderr)

        error_code = res.status_code
        return json.loads(res.text[4:]),error_code

    @staticmethod
    def generateJSON(JSON_response):
        """
        Generates and saves the data as a JSON names out.json
        """
        # Here we're just dumping all the results as a JSON document on
        # stdout.
        file_name = "JSON/big_out.json"
        with open(file_name, "w") as json_file:
            json.dump(JSON_response, json_file, indent=4)
        return

    def requestAPICall(PLATFORM):
        """
        does API stuff
        """
        response = Gerrit(PLATFORM)
        all_results = []
        #date_string = 'since:"'+DATE_2+" "+SET_TIME_2+'" before:"'+DATE_1+" "+SET_TIME_1+"'
        date_string = 'since"2011-04-07 00:00:01" before"2022-02-27 23:59:59"'
        print(date_string)
        start = 0
        while True:
            res,error = response.changes(
                PLATFORM,
                date_string,
                limit=500,
                start=start,
            )
            if not res:
                break
            all_results.extend(res)
            if not res[-1].get("_more_changes"):
                break
            start += len(res)
        Gerrit.generateJSON(all_results)
        return error
    def date_creator(url,PLATFORM,DATE_1,DATE_2,SET_TIME_1,SET_TIME_2):
    
if __name__ == "__main__":
    Gerrit.requestAPICall("https://chromium-review.googlesource.com")
    