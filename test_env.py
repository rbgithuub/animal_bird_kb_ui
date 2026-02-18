from app.core.environment import Environment

print("Available Environments:")
for env in Environment:
    print(env.value)
