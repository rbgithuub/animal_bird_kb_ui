import os
import subprocess

import os
import subprocess
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_command(cmd):
    print(f"\n🔧 Running: {cmd}\n")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    return result.stdout

def ask_agent(task):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a DevOps AI agent."},
            {"role": "user", "content": task}
        ]
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    task = """
    Give step-by-step shell commands to:
    1. Build docker image for animal kb app
    2. Tag for Azure Container Registry
    3. Push to ACR
    """

    steps = ask_agent(task)
    print("\n🤖 AI Plan:\n", steps)