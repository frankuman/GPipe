"""
Gpipe API.py
"""
import json
import sys

import pandas as pd
import requests

# Big thanks to @larsks over at
# https://stackoverflow.com/questions/75446633/how-do-i-get-more-than-500-codereviews-with-gerrit-rest-api


class Gerrit:
    """Wrap up Gerrit API functionality in a simple class to make
    it easier to consume from our code.
    """

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def changes(self, selected_pf, query, root, start=None, limit=None, options=None):
        """This implements the REST API .

        [1]: https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html
        """
        # auth = HTTPBasicAuth(username=username,password=password) We can authenticate, but why?
        params = {"q": query}
        #We check if we have options or limits
        if start is not None:
            params["-S"] = start
        if limit is not None:
            params["n"] = limit
        if options is not None:
            params["o"] = options
        #Opendev works differently than chromium and android
        if selected_pf != "https://review.opendev.org":
            res = requests.get(f"{self.baseurl}/changes/", params=params,timeout=30)
        else:
            res = requests.get(
                f"{self.baseurl}/changes/",
                params=params,timeout=30
            )
        root.textbox.configure(
            font=("Consolas", 20)
        )  # Only works with consolas
        print(f"fetched [{res.status_code}]: {res.url}", file=sys.stderr)
        status_string = "fetched: status = " + str(res.status_code) + " query = " + query
        #We can actually print this in the GUI
        root.textbox.insert("1.0", status_string + "\n")

        error_code = res.status_code
        #We can't use json.loads if we don't get a successful fetch,
        #so we try to do it, and if it doesn't work we return a
        #empty list, and the response so we can fetch the error
        try:
            return json.loads(res.text[4:]), error_code, None
        except json.decoder.JSONDecodeError:
            empty_list = []
            return empty_list, error_code, res


def generate_json(json_respone):
    """
    Generates and saves the data as a JSON names out.json
    """
    # Here we're just dumping all the results as a JSON document
    file_name = "src/JSON/out.json"
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(json_respone, json_file, indent=4)
    return

def request_api_call(
    selected_pf, date_1, date_2, set_time_1, set_time_2, root, crawl=None
):
    """
    requests from the platform, if platform is not OPENDEV is calls on rest_api_google
    """
    if selected_pf != "https://review.opendev.org":
        error = rest_api_google(
            selected_pf, date_1, date_2, set_time_1, set_time_2, root, crawl
        )
        return error
    else:
        response = Gerrit(selected_pf)
        is_query = get_is_queries(root)
        #We get the response, and we get the is_queries (if any excists)
        all_results = []
        if crawl is None:
            date_string = (
                is_query
                + 'since:"'
                + date_2
                + " "
                + set_time_2
                + '" before:"'
                + date_1
                + " "
                + set_time_1
                + '"'
            )
        else:
            date_string = (
                crawl
                + " "
                + is_query
                + 'since:"'
                + date_2
                + " "
                + set_time_2
                + '" before:"'
                + date_1
                + " "
                + set_time_1
                + '"'
            )
        #We have now created the full date_string
        print(date_string)
        start = 0
        #We start from 0, and since Opendev doesn't have a super secret
        #limit, we can go forever here
        while True:
            res, error,msg = response.changes(
                selected_pf, date_string, root, limit=5000, start=start
            )
            if not res and msg is not None:
                if error != 200:
                    all_results.append(str(msg.content))
                break
            if not res:
                break
            all_results.extend(res)
            #If there is _more_changes in the response, more data can be found
            if not res[-1].get("_more_changes"):
                break
            start += len(res)
        generate_json(all_results)
        return error

def rest_api_google(
    selected_pf, date_1, date_2, set_time_1, set_time_2, root, crawl=None
):
    """
    Google platforms need a special api call where we use a algoritm to see latest date and refresh
    from there    
    """
    all_results = []
    response = Gerrit(selected_pf)
    is_query = get_is_queries(root)

    more_data = True
    error = 0
    #While there is more data we need to check for a new date and start from there
    while more_data is True:

        if crawl is None:
            date_string = (
                is_query
                + 'since:"'
                + date_2
                + " "
                + set_time_2
                + '" before:"'
                + date_1
                + " "
                + set_time_1
                + '"'
            )
        else:
            date_string = (
                crawl
                + " "
                + is_query
                + 'since:"'
                + date_2
                + " "
                + set_time_2
                + '" before:"'
                + date_1
                + " "
                + set_time_1
                + '"'
            )
        print(date_string)
        start = 0
        while True:
            res, err,msg = response.changes(
                selected_pf, date_string, root, limit=5000, start=start
            )
            error = err
            #We only go to 5000, then we start from the next date
            if start == 5000:
                more_data = True
                break
            if not res and msg is not None:
                more_data = False
                if error != 200:
                    all_results.append(str(msg.content))
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
            #If more data is to be found, i.e S went to 5000
            #We need to generate a new date
            generate_json(all_results)
            date_1, set_time_1 = generate_new_date()
    generate_json(all_results)
    return error

def generate_new_date():
    """
    Algoritm to help find the new date in the output from the rest_api_google
    """
    #We load it as a dataframe and find the last date in it.
    with open("src/JSON/out.json", "r", encoding="utf-8") as out_file:
        data = json.load(out_file)
    data_frame = pd.DataFrame(data)
    data_frame = data_frame["updated"].apply(lambda x: x.split(".")[0])
    #the min function works for this
    last_updated = data_frame.min()
    last_date, last_time = last_updated.split(" ")
    print(last_updated)
    return last_date, last_time

def get_is_queries(root):
    """
    If is: queries is used this function helps to find 
    them and convert them into a string usable for queries
    """
    #Very simple, we use root with the get to see if the
    #they are true or not
    open_q = root.open_v.get()
    watched = root.watched_v.get()
    unassigned = root.unassigned_v.get()
    reviewed = root.reviewed_v.get()
    closed = root.closed_v.get()
    merged = root.merged_v.get()
    pending = root.pending_v.get()
    abandoned = root.abandoned_v.get()
    query_string = ""
    if open_q == 1:
        query_string += "+is:open"
    if watched == 1:
        query_string += "+is:watched"
    if unassigned == 1:
        query_string += "+is:unassigned"
    if reviewed == 1:
        query_string += "+is:reviewed"
    if closed == 1:
        query_string += "+is:closed"
    if merged == 1:
        query_string += "+is:merge"
    if pending == 1:
        query_string += "+is:pending"
    if abandoned == 1:
        query_string += "+is:abandoned"
    if query_string != "":
        #We create a good string for it after
        query_string = query_string[1:]
        query_string = query_string.strip()
        query_string = query_string + " "

    return query_string
