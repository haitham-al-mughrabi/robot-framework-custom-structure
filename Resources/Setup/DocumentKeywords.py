import os
import argparse
from robot.libdoc import libdoc

# Set up argument parser
parser = argparse.ArgumentParser(description = "Generate Robot Framework documentation for libraries or resources.")
parser.add_argument(
    "--input-directory",
    type = str,
    required = True,
    help = "Path to the directory containing the resource files (e.g., Libraries/Utilities)."
)
parser.add_argument(
    "--output-directory",
    type = str,
    required = True,
    help = "Path to the directory where the documentation will be generated (e.g., Documentations)."
)

# Parse arguments
args = parser.parse_args()
input_directory = args.input_directory
output_directory = args.output_directory

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok = True)

# Iterate over all files in the input directory
for filename in os.listdir(input_directory):
    # Check if the file is a .resource or .py file
    if filename.endswith('.resource') or filename.endswith('.py'):
        # Generate the input and output file paths
        input_file = os.path.join(input_directory, filename)
        output_file = os.path.join(
            output_directory,
            filename.replace('.resource', '.html').replace('.py', '.html')
        )
        # Generate the documentation
        libdoc(input_file, output_file)
        print(f"Generated documentation for {filename}: {output_file}")
