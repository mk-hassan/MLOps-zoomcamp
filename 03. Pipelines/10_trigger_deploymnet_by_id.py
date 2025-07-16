import requests


# Replace with your actual deployment ID after registration
deployment_id = "f6ff5056-ee57-4c8f-8de3-554fd26898f7"

# Local Prefect API URL
url = f"http://localhost:4200/api/deployments/{deployment_id}/create_flow_run"

# Parameters to pass to the flow
payload = {
    "parameters": {
        "user_id": 101  # Example user ID
    }
}

# Make the API request
response = requests.post(url, json=payload)


# Check the response
if 200 <= response.status_code < 300:
    print("Flow run triggered successfully:", response.json())
else:
    print("Error triggering flow run:", response.status_code, response.text)
