import os
import subprocess

# Define the categories
categories = ["women", "baby_girl", "baby_boy", "men", "kids"]

# Define the base directory for the CSV data
base_csv_dir = "csv_data_"

# Loop through each category
for category in categories:
    # Construct the paths
    input_dir = f"{base_csv_dir}{category}_sizes_v4"
    output_file = f"combined_file_sizes_{category}_.csv"

    # Check if the input directory exists
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist. Skipping {category}.")
        continue

    # Construct the awk command
    awk_command = f"awk '(NR == 1) || (FNR > 1)' {input_dir}/*.csv > {output_file}"

    try:
        # Execute the command
        print(f"Running command: {awk_command}")
        subprocess.run(awk_command, shell=True, check=True)
        print(f"Combined file created: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {category}: {e}")
