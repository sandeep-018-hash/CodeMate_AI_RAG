
import subprocess
import sys
import tempfile
import os


def run_python_code(code, timeout=5):
    """
    Run Python code with a time limit.

    WARNING:
    This is for trusted, local development only.
    A subprocess timeout is not a security sandbox.
    """

    if not isinstance(code, str) or not code.strip():
        return {
            "success": False,
            "output": "Please enter some Python code."
        }

    # Limit the amount of code accepted.
    if len(code) > 10_000:
        return {
            "success": False,
            "output": "Code is too long. Maximum size is 10,000 characters."
        }

    # Create a temporary Python file.
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            encoding="utf-8",
            delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name

        result = subprocess.run(
            [sys.executable, "-I", temp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=tempfile.gettempdir(),
            env={
                "PATH": os.environ.get("PATH", ""),
                "PYTHONIOENCODING": "utf-8"
            },
            check=False
        )

        output = result.stdout

        if result.stderr:
            output += "\nErrors:\n" + result.stderr

        if not output.strip():
            output = (
                "Code executed successfully with no output."
                if result.returncode == 0
                else f"Python exited with code {result.returncode}."
            )

        return {
            "success": result.returncode == 0,
            "output": output[:20_000]
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": f"Execution stopped: time limit of {timeout} seconds exceeded."
        }

    except OSError as error:
        return {
            "success": False,
            "output": f"Could not run Python: {error}"
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
