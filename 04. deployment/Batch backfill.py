import requests
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

BASE_URL = "http://127.0.0.1:4200"
DEFAULT_WAITING_TIME = 5

def check_flow_run_status(flow_run_id):
    url = f"{BASE_URL}/api/flow_runs/{flow_run_id}"
    response = requests.get(url)

    if response.status_code == 200:
        flow_run = response.json()
        return flow_run['state']
    else:
        raise Exception(f"Error checking flow run status: {response.status_code} - {response.text}")

def wait_for_flow_completion(flow_run_id: str, check_interval: int | None = None) -> str:
    while True:
        state = check_flow_run_status(flow_run_id)
        print(f"Current flow state: {state['type']}")

        # Check if the flow is in a final state (either "COMPLETED", "FAILED", or "CANCELLED")
        if state['type'] in ["COMPLETED", "FAILED", "CANCELLED"]:
            print(f"Flow is in terminal state: {state['type']}")
            break

        # Wait for the specified interval before checking again
        time.sleep(check_interval if check_interval != None else DEFAULT_WAITING_TIME)

    return state['type']

def get_deployment_id_by_name(deployment_name: str, flow_name: str) -> str:
    """
    Fetches the deployment ID from Prefect server given a deployment name and flow name.

    Parameters
    ----------
    deployment_name : str
        The name of the deployment.
    flow_name : str
        The name of the flow the deployment belongs to.

    Returns
    -------
    str
        The deployment ID.

    Raises
    ------
    RuntimeError
        If the deployment could not be found or another error occurred.
    """
    url = f"{BASE_URL}/api/deployments/name/{flow_name}/{deployment_name}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        raise RuntimeError(
            f"Failed to fetch deployment ID: {response.status_code} - {response.text}"
        )

def create_backfills(deployment_id):
	url = f"{BASE_URL}/api/deployments/{deployment_id}/create_flow_run"

	start_date = datetime(day=1, month=2, year=2022)
	end_date = datetime(day=1, month=1, year=2023)

	curr = start_date
	while curr <= end_date:
		payload = {
			"parameters": {
				"date": str(curr)
			}
		}
            
		response = requests.post(url, json=payload)
		wait_for_flow_completion(response.json()["id"])
		curr = curr + relativedelta(months=1)
        

if __name__ == "__main__":
    deployment_id = get_deployment_id_by_name(deployment_name="batch-run", flow_name="batch-run")
    create_backfills(deployment_id)