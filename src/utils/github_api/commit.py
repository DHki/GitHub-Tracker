import requests
from dateutil.parser import parse

def github_check_commit(last_check_time, api_token, repo):
    request_url = f"https://api.github.com/repos/{repo['owner']}/{repo['repository']}/commits?since={last_check_time}"

    response = requests.get(url=request_url, headers={"Authorization" : f"Bearer {api_token}"})
    if response.status_code != 200:
        return {"update" : False, "error" : True, "msg" : f"API request failed: {response.text}"}

    commits = response.json()
    keywords = repo["commit"].get("keywords", [])

    ret = {"error" : False, "update" : False, "data" : []}
    for c in commits:
        if need_to_notify(c, keywords):
            ret["update"] = True
            ret["data"].append(c)

    return ret

def need_to_notify(commit, keywords):
    if len(keywords) == 0:
        return True
    
    commit_msg = commit["commit"]["message"].lower()
    for k in keywords:
        if k.lower() in commit_msg:
            return True

    return False