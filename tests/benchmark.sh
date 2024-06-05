#!/bin/bash

# List all .mpileup files in the current directory
mpileup_files=$(ls tests/*.mpileup)

# Loop through each .mpileup file
for file in $mpileup_files; do
  echo "Processing $file..."
  # Count the number of lines in the current .mpileup file
  line_count=$(wc -l < "$file")
  echo "Line count for $file: $line_count"
  # Run the command on the current .mpileup file
  time python3 CSE-185-mVarScan/main.py "$file" --min-var-frequency 0.2 --min-freq-for-hom 0.8 --pvalue 0.01 --out "${file%.mpileup}_output.txt"
  rm ${file%.mpileup}_output.txt
done

echo "Processing complete."
