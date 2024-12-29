import requests
from dateutil.parser import parse

def github_check_release(last_check_time, api_token, repo):
    request_url = f"https://api.github.com/repos/{repo['owner']}/{repo['repository']}/releases"

    response = requests.get(url=request_url, headers={"Authorization" : f"Bearer {api_token}"})
    if response.status_code != 200:
        return {"update" : False, "error" : True, "msg" : f"API request failed: {response.text}"}
    
    lc_time = parse(last_check_time)
    releases = response.json()

    ret = {"error" : False, "update" : False, "data" : []}
    for r in releases:
        created_at = parse(r["created_at"])

        if lc_time < created_at:
            ret["update"] = True
            ret["data"].append(r)

    return ret