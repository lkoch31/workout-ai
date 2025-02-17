# Integrate with AWS Anthropic API
# Create 6 day workout rotation (1 - butt, 2 - arms, 3 - legs, 4 - arms/shoulders, 5 - full body, 6 cardio)
# Create script I can run each day with which workout number I should be on

from anthropic import AnthropicBedrock
import boto3
import json

# create multiple tempo variations
# single set (40, 45, 50 seconds)
# super set (45, 45)
# triset (30, 30, 30)
# quad set (30s, 45s for glutes)

# define exercises for each muscle group
# glute
# hamstring
# quads
# shoulders
# back
# chest
# biceps
# triceps
# full body: snatch, squat to press, etc

# define appropriate combinations of two - three muscle groups to target in any given workout


client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "anthropic.claude-instant-v1"
prompt="""Create 30 minute workout sequence for back and biceps.
	Sets should be supersets consisting of two 45 second exercises in a row with a 30 second break between.
	Each set should only be for back exercises or for bicep exercises.\n\n
	Example back exercises are rows, supine rows, deadstop rows, pull ups, pullovers
	Example bicep exercises are hammer curls, wide curls, cheat curls, palms up curls"""

# Format the request payload using the model's native structure.
native_request = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 256,
    "temperature": 0.5,
    "messages": [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        }
    ],
}

# Convert the native request to JSON.
request = json.dumps(native_request)

# Invoke the model with the request.
streaming_response = client.invoke_model_with_response_stream(
    modelId=model_id, body=request
)

# Extract and print the response text in real-time.
for event in streaming_response["body"]:
    chunk = json.loads(event["chunk"]["bytes"])
    if chunk["type"] == "content_block_delta":
        print(chunk["delta"].get("text", ""), end="")
