# Integrate with AWS Anthropic API
# Create 6 day workout rotation (1 - glute, 2 - arms, 3 - legs, 4 - arms/shoulders, 5 - full body, 6 cardio)
# Create script I can run each day with which workout number I should be on

from anthropic import AnthropicBedrock
import boto3
import json
import random

# create multiple tempo variations
single_set_v1 = "45 second exercise with 15 second rest. There is one exercise in this set. The set takes 1 minute total to complete."
single_set_v2 = "40 second exercise with 20 second rest. There is one exercise in this set. The set takes 1 minute total to complete"
single_set_v3 = "50 second exercise with 10 second rest. There is one exercise in this set. The set takes 1 minute total to complete"
super_set = "two 45 second exercises in a row with 30 second rest. There are 2 exercises in this set. The set takes 2 minutes total to complete"
tri_set = "three 30 second exercises in a row with 30 second rest. There are 3 exercises in this set. The set takes 2 minutes total to complete."
quad_set = "four 30 second exercises in a row with 30 second rest. There are 4 exercises in this set. The set takes 2.5 minutes total to complete."
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
arms = ["shoulders", "triceps", "biceps", "back", "chest"]

glute_exercises = ["hip thrusts", "hip thrust pulse", "glute hold", "forward lean elevated lunge", "single leg hip thrust", "single leg hold", "single leg pulse"]
hamstring_exercises = ["hamstring thrust", "hamstring hold", "romanian deadlift", "roman deadleft slow eccentric"]
quad_exercises = ["weighted squat", "heel elevated squat", "weighted squat with pause", "lunge", "elevated lunge", "squat to kneel"]
back_exercises = ["rows", "supine rows", "deadstop rows", "pull ups", "pullovers", "row slow eccentric", "momentum row", "renegade row", "swimmer"]
biceps_exercises = ["hammer curls", "wide curls", "cheat curls", "palms up curls"]
shoulders_exercises = ["shoulder press", "alternating shoulder press", "arnold press", "rear delt fly", "lateral raise", "partial lateral raise", "frontal raise", "around the world", "arc raise"]
triceps_exercises = ["tricep kickbacks", "cobra pushups", "tricep pushups", "skull crusher", "shoulder crusher", "tate press", "tricep dips", "slow tricep dips"]
chest_exercises = ["chest press", "deadstop chest press", "alternating chest press", "palms facing chest press", "diamond press", "flys", "push ups", "wide push ups", "slow push ups"]

muscle_group_and_exercises = {"back":back_exercises, "biceps":biceps_exercises, "shoulders":shoulders_exercises, "triceps":triceps_exercises, "chest":chest_exercises}

def get_arm_combinations():
    num_muscle_groups = random.randint(2,3)
    return random.sample(arms,num_muscle_groups)

#get random tempo variation from the six possibilities listed above 
tempo = tempo_variations[random.randint(1,len(tempo_variations)-1)]

muscle_groups = get_arm_combinations()
optionalThirdExercise = "" if len(muscle_groups) < 3  else "Example " + muscle_groups[2] + " exercises are " + ",".join(muscle_group_and_exercises.get(muscle_groups[2]))
client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "anthropic.claude-instant-v1"
prompt= ("Create workout sequence between 30 and 35 minutes long for " + "and".join(muscle_groups) + "."
    " A set of exercises is a group of between 1 - 4 exercises."
    " Multiply the number of sets by the length in minutes of each set until the result is between 30 and 35 minutes."
    " For example, a superset is 2 minutes long. There could be 15 supersets in a workout because 15 x 2 minutes = 30 minutes."
    " There could be 16 supersets in a workout because 16 x 2 minutes = 32 minutes."
    " There could not be 18 supersets in a workout because 18 x 2 is = 26 minutes which is greater than the 35 minute limit."
    " If the total time is less than 30 minutes, more sets should be added until the total time is >= 30 minutes."
    " The exercises should not be the same across multiple sets."
    " Please show your math"
	"Sets should be " + tempo + " "
	"Each set should only be for either " + "or".join(muscle_groups) + " exercises.\n\n"
	"Example " + muscle_groups[0] + " exercises are " + ",".join(muscle_group_and_exercises.get(muscle_groups[0])) + " "
	"Example " + muscle_groups[1] + " exercises are " + ",".join(muscle_group_and_exercises.get(muscle_groups[1])) + optionalThirdExercise)

# Format the request payload using the model's native structure.
native_request = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 512,
    "temperature": 0.6,
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
