import requests
from dateutil.parser import parse

def github_check_issue(last_check_time, api_token, repo):
    request_url = f"https://api.github.com/repos/{repo['owner']}/{repo['repository']}/issues?since={last_check_time}"

    response = requests.get(url=request_url, headers={"Authorization" : f"Bearer {api_token}"})
    if response.status_code != 200:
        return {"update" : False, "error" : True, "msg" : f"API request failed: {response.text}"}
    
    lc_time = parse(last_check_time)
    issues = response.json()

    keywords = repo["issue"].get("keywords", [])
    labels = repo["issue"].get("labels", [])

    ret = {"error" : False, "update" : False, "data" : []}
    for i in issues:
        # this issue is pull request
        # not issue
        if i.get("pull_request") is not None:
            continue
        
        created_at = parse(i["created_at"])
        updated_at = parse(i["updated_at"])
        if need_to_notify(i, keywords, labels):
            if lc_time > created_at and lc_time < updated_at:
                i["flag_updated"] = True
            else:
                i["flag_updated"] = False

            ret["update"] = True
            ret["data"].append(i)

    return ret

def need_to_notify(issue, keywords, labels):
    if len(keywords) == 0 and len(labels) == 0:
        return True
    
    issue_title = issue["title"].lower()
    for k in keywords:
        if k.lower() in issue_title:
            return True

    issue_lables = issue.get("labels", [])
    if len(issue_lables) == 0:
        return True
    
    for l in labels:
        for i_label in issue_lables:
            if l == i_label["name"]:
                return True

    return False