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

# Example usage
parent_file = 'tests/NA19240.mpileup' 
num_lines = 2800000
output_file = 'tests/NA19240_random_'+str(num_lines)+'.mpileup' 

generate_random_mpileup(parent_file, output_file, num_lines)
