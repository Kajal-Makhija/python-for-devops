#Github-JIRA intergration Project 
from flask import Flask, request
import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route("/createJIRA", methods=["POST"])
def createJIRA():

    # Read GitHub webhook payload
    incoming = request.get_json(force=True)
    comment_body = incoming["comment"]["body"]

    # Only create JIRA if comment is /jira
    if comment_body.strip().lower() != "/jira":
        return "No JIRA created. To create a JIRA, comment '/jira'"

    # --- JIRA details ---
    url = "https://makhejakajal9.atlassian.net/rest/api/3/issue"
    API_TOKEN = "YOUR_API_TOKEN"

    auth = HTTPBasicAuth("makhejakajal9@gmail.com", API_TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Build actual JIRA ticket payload
    jira_payload = {
        "fields": {
            "project": {"key": "MYF"},
            "summary": "Created from GitHub comment trigger",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "Trigger comment: /jira"}
                        ]
                    }
                ]
            },
            "issuetype": {"id": "10011"}
        }
    }

    response = requests.post(
        url,
        headers=headers,
        auth=auth,
        data=json.dumps(jira_payload),
        verify=False
    )

    return response.text


app.run("0.0.0.0")
