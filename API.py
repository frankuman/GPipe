import json
import requests
import sys
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

    def changes(self, query, start=None, limit=None, options=None):
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

        res = requests.get(f"{self.baseurl}/changes", params=params)
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
        file_name = "JSON/out.json"
        with open(file_name, "w") as json_file:
            json.dump(JSON_response, json_file, indent=4)
        return

    def requestAPICall(url):
        """
        does API stuff
        """
        response = Gerrit("https://chromium-review.googlesource.com")
        all_results = []

        start = 0
        while True:
            res,error = response.changes(
                'since:"2022-12-25 00:00:00" before:"2022-12-28 00:30:00"',
                limit=1000,
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
        
