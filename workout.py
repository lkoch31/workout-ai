# Integrate with AWS Anthropic API
# Create 6 day workout rotation (1 - glute, 2 - arms, 3 - legs, 4 - arms/shoulders, 5 - full body, 6 cardio)
# Create script I can run each day with which workout number I should be on

from anthropic import AnthropicBedrock
import boto3
import json
import random

# create multiple tempo variations
single_set_v1 = "45 second exercise with 15 second rest"
single_set_v2 = "40 second exercise with 20 second rest"
single_set_v3 = "50 second exercise with 10 second rest"
super_set = "two 45 second exercises in a row with 30 second rest"
tri_set = "three 30 second exercises in a row with 30 second rest"
quad_set = "four 30 second exercises in a row with 30 second rest"
tempo_variations = [single_set_v1, single_set_v2, single_set_v3, super_set, tri_set, quad_set]
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

glute_exercises = ["hip thrusts", "hip thrust pulse", "glute hold", "forward lean elevated lunge", "single leg hip thrust", "single leg hold", "single leg pulse"]
hamstring_exercises = ["hamstring thrust", "hamstring hold", "romanian deadlift", "roman deadleft slow eccentric"]
quad_exercises = ["weighted squat", "heel elevated squat", "weighted squat with pause", "lunge", "elevated lunge", "squat to kneel"]
back_exercises = ["rows", "supine rows", "deadstop rows", "pull ups", "pullovers", "row slow eccentric", "momentum row", "renegade row", "swimmer"]
bicep_exercises = ["hammer curls", "wide curls", "cheat curls", "palms up curls"]


#get random tempo variation from the six possibilities listed above 
tempo = tempo_variations[random.randint(1,len(tempo_variations))]

client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "anthropic.claude-instant-v1"
prompt= ("Create 30 minute workout sequence for back and biceps. Each exercise will have a number of seconds and the total number of seconds involved should add up to 1800 seconds"
	"Sets should be " + tempo + " "
	"Each set should only be for back exercises or for bicep exercises.\n\n"
	"Example back exercises are " + ",".join(back_exercises) + " "
	"Example bicep exercises are " + ",".join(bicep_exercises))

# Format the request payload using the model's native structure.
native_request = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 256,
    "temperature": 0.7,
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
