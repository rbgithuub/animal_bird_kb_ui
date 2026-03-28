import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_compose():
    with open("../docker-compose.yml", "r") as f:
        return f.read()

def generate_azure_yaml(compose_content):
    prompt = f"""
You are a DevOps AI agent.

Convert this docker-compose YAML into Azure Container Instance YAML (deploy.yaml).

Rules:
- Include all services
- Map ports correctly
- Add CPU and memory
- Use Linux osType
- Add imageRegistryCredentials placeholder
- Use proper indentation
- Output ONLY valid YAML (no explanation)

docker-compose.yml:
{compose_content}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert DevOps engineer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def save_yaml(yaml_content):
    with open("../deploy.yaml", "w") as f:
        f.write(yaml_content)

def clean_yaml(content):
    return content.replace("```yaml", "").replace("```", "").strip()


if __name__ == "__main__":
    compose = read_compose()

    print("\n📄 docker-compose.yml:\n", compose)

    azure_yaml = generate_azure_yaml(compose)
    azure_yaml = clean_yaml(azure_yaml)

    print("\n🤖 Generated deploy.yaml:\n", azure_yaml)

    save_yaml(azure_yaml)

    print("\n✅ deploy.yaml created successfully!")