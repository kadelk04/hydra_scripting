#!/bin/bash
# uses pydictor to generate usernames and passwords given text input

company_name=$1
echo "Company Name: $company_name"
cd pydictor 

echo "Generating numerous pydictor results"

./pydictor.py --len 3 3 --base 'c' --head "$company_name" --output "./passwords.txt"

echo "ran this"

cd ..

