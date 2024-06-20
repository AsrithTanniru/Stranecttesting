import csv

csv_file_path = 'example.csv'

# Read the existing CSV file
with open(csv_file_path, mode='r+', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

    # Add new data to the list
    new_data = ['Eva', '22', 'San Francisco']
    data.append(new_data)

    # Move the file pointer to the end before writing
    file.seek(0, 2)

    # Write the modified data back to the CSV file
    writer = csv.writer(file)
    writer.writerows(data)

print("Data added successfully.")
