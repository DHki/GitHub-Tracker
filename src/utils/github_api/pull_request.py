import requests
from dateutil.parser import parse

def github_check_pull_request(last_check_time, api_token, repo):
    request_url = f"https://api.github.com/repos/{repo['owner']}/{repo['repository']}/pulls"

    response = requests.get(url=request_url, headers={"Authorization" : f"Bearer {api_token}"})
    if response.status_code != 200:
        return {"update" : False, "error" : True, "msg" : f"API request failed: {response.text}"}
    
    lc_time = parse(last_check_time)
    pull_requests = response.json()

    keywords = repo["pull_request"].get("keywords", [])
    labels = repo["pull_request"].get("labels", [])

    ret = {"error" : False, "update" : False, "data" : []}
    for pr in pull_requests:
        
        created_at = parse(pr["created_at"])
        updated_at = parse(pr["updated_at"])
        if lc_time < created_at or lc_time < updated_at:
            if need_to_notify(pr, keywords, labels):
                if lc_time > created_at and lc_time < updated_at:
                    pr["flag_updated"] = True
                else:
                    pr["flag_updated"] = False

                ret["update"] = True
                ret["data"].append(pr)

    return ret

def need_to_notify(pr, keywords, labels):
    if len(keywords) == 0 and len(labels) == 0:
        return True
    
    pr_title = pr["title"].lower()
    for k in keywords:
        if k.lower() in pr_title:
            return True

    pr_labels = pr.get("labels", [])
    if len(pr_labels) == 0:
        return True
    
    for l in labels:
        for i_label in pr_labels:
            if l == i_label["name"]:
                return True

    return False