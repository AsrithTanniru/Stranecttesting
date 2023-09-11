import json

# Create a dictionary representing your data
data = {
    "name": "Jane Smith",
    "age": 25,
    "location": "Suburb"
}

# Serialize the dictionary to a JSON-formatted string
json_string = json.dumps(data, indent=2)  # indent for pretty formatting

# Specify the full path and filename for the new JSON file
file_path = "./new_data.json"  # Update this with the desired path

# Write the JSON string to the new file
with open(file_path, "w") as json_file:
    json_file.write(json_string)

print(f"JSON data saved to {file_path}")
