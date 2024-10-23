#!/bin/bash

# Define the list of elements
elements=("red_1" "red_2" "red_4" "green_3")

# Create the YAML file
output_file="base_recipes.yml"
echo "transitions:" > "$output_file"

# Generate all combinations
for actor_start in "${elements[@]}"; do
  for target_start in "${elements[@]}"; do
    echo "  - actor_start: $actor_start" >> "$output_file"
    echo "    actor_end: $actor_start" >> "$output_file"
    echo "    target_start: $target_start" >> "$output_file"
    echo "    target_end: $target_start" >> "$output_file"
    echo "" >> "$output_file"
  done
done

echo "Base recipes generated successfully."
