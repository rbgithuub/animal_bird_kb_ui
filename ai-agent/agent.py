import os
import subprocess
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROJECT_PATH = "/Users/balajiraja/holy999d/holy999d/animal_bird_kb_ui"

def run_command(cmd):
    print(f"\n🔧 Running: {cmd}\n")

    result = subprocess.run(
        cmd,
        shell=True,
        cwd=PROJECT_PATH,   # 👈 THIS FIXES EVERYTHING
        capture_output=True,
        text=True
    )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    return result.returncode

def ask_agent(task):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a DevOps AI agent. Only return shell commands."},
            {"role": "user", "content": task}
        ]
    )

    return response.choices[0].message.content

def clean_commands(plan):
    cleaned = []

    for line in plan.split("\n"):
        line = line.strip()

        if (
            not line
            or line.startswith("```")
            or line.startswith("#")
        ):
            continue

        cleaned.append(line)

    return cleaned


def execute_plan(plan):
    commands = clean_commands(plan)

    for cmd in commands:
        run_command(cmd)

if __name__ == "__main__":
    task = """
    Generate ONLY shell commands to:
    1. Build docker image named animal-kb
    2. Tag it for Azure Container Registry: animalkbacr.azurecr.io
    3. Push the image
    """

    plan = ask_agent(task)

    print("\n🤖 AI Generated Commands:\n", plan)

    confirm = input("\nDo you want to execute these commands? (yes/no): ")

    if confirm.lower() == "yes":
        execute_plan(plan)