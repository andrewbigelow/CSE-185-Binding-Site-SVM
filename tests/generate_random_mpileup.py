# import random

# def generate_random_mpileup(parent_file, output_file, num_lines):
#     # Read all lines from the parent file
#     with open(parent_file, 'r') as file:
#         lines = file.readlines()
    
#     # Check if the requested number of lines is greater than the available lines
#     if num_lines > len(lines):
#         print(f"Requested number of lines ({num_lines}) exceeds the number of available lines ({len(lines)}).")
#         return
    
#     # Randomly select the specified number of lines
#     selected_lines = random.sample(lines, num_lines)
    
#     # Write the selected lines to the new output file
#     with open(output_file, 'w') as file:
#         file.writelines(selected_lines)
    
#     print(f"Randomly selected {num_lines} lines from {parent_file} and wrote to {output_file}.")

# # Example usage
# parent_file = 'tests/NA19240.mpileup' 
# num_lines = 2800000
# output_file = 'tests/NA19240_random_'+str(num_lines)+'.mpileup' 

# generate_random_mpileup(parent_file, output_file, num_lines)

import random

def generate_random_mpileup(parent_file, output_file, num_lines):
    # Read all lines from the parent file
    with open(parent_file, 'r') as file:
        lines = file.readlines()
    
    # Check if the requested number of lines is greater than the available lines
    if num_lines > len(lines):
        print(f"Requested number of lines ({num_lines}) exceeds the number of available lines ({len(lines)}).")
        return
    
    # Randomly select the specified number of lines
    selected_lines = random.sample(lines, num_lines)
    
    # Write the selected lines to the new output file
    with open(output_file, 'w') as file:
        file.writelines(selected_lines)
    
    print(f"Randomly selected {num_lines} lines from {parent_file} and wrote to {output_file}.")

def create_multiple_mpileup_files(parent_file, start, end, step):
    for num_lines in range(start, end + 1, step):
        output_file = f"{parent_file[:-8]}_random_{num_lines}.mpileup"
        generate_random_mpileup(parent_file, output_file, num_lines)

start = 2000000  # Starting line count
end = 2500000  # Ending line count
step = 100000  # Step size

# Repeat for other parent files if needed
parent_files = [
    'tests/NA12878_child.mpileup',
    'tests/NA12892_mother.mpileup',
    'tests/NA19240.mpileup'
]

for parent_file in parent_files:
    create_multiple_mpileup_files(parent_file, start, end, step)
