from langchain.tools import tool
from langsmith import traceable
import subprocess
import tempfile
import os

VENV_PYTHON = os.getenv("VENV_PYTHON")

@tool
@traceable(name="execute_python_code_local")
def execute_python_code_locally(code: str) -> dict:
    """
    Executes Python code locally using the specified virtual environment.
    Returns:
    {
        "status": "success" or "error",
        "output": str,
        "error_name": Optional[str],
        "error_value": Optional[str]
    }
    """
    try:
        # Write code to a temporary file
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp_file:
            tmp_file.write(code)
            tmp_file_path = tmp_file.name

        # Run the code using the virtual env python
        result = subprocess.run(
            [VENV_PYTHON, tmp_file_path],
            capture_output=True,
            text=True
        )

        # Remove the temp file
        os.unlink(tmp_file_path)

        output = ""
        if result.stdout:
            output += "STDOUT:\n" + result.stdout
        if result.stderr:
            output += "STDERR:\n" + result.stderr

        if result.returncode != 0:
            return {
                "status": "error",
                "output": output,
                "error_name": "PythonExecutionError",
                "error_value": f"Return code {result.returncode}"
            }

        return {"status": "success", "output": output or "Code executed successfully but produced no output."}

    except Exception as e:
        return {"status": "error", "output": f"Error executing code: {e}", "error_name": type(e).__name__, "error_value": str(e)}