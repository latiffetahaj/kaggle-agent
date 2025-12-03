from langchain.tools import tool
from e2b_code_interpreter import Sandbox
from langsmith import traceable
from daytona import Daytona, DaytonaConfig
import os
from dotenv import load_dotenv
load_dotenv()
# Define the configuration
config = DaytonaConfig(api_key=os.getenv("DAYTONA_API_KEY"))



@tool
@traceable(name="execute_python_code")
def execute_python_code(code: str) -> dict:
    """
    Executes Python code in a secure  sandbox.
    Returns:
    {
        "status": "success" or "error",
        "output": str,
        "error_name": Optional[str],
        "error_value": Optional[str]
    }
    """
    # Initialize the Daytona client
    daytona = Daytona(config)

    try:
        sandbox = daytona.create()
        response = sandbox.process.code_run(code)

        if response.exit_code != 0:
            return {'status': 'error', 'output': f"Error: {response.exit_code} {response.result}"}
        else:
            return {'status': 'success', 'output': response.result}

    except Exception as e:
        return {'status': 'error', 'output': f"Error executing code: {e}"}