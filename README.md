# MINDS-Sage-Project-Assignment

- Developed this repository as a part of MINDS MS Student Position - coding challenge 

- Solution provided to the Web Scraping Assignment by creating a python script

To run the script and generate the CSV file, follow the following steps

1. Create a virtual environment  
2. pip install -r requirements.txt
3. python scraper.py

Clarifications:

- For Date and time 20 December 11:36:43, outcome is "Spacecraft anomaly, recovered successfully". Here, the word successfully is not being matched through the script written.
    - Outcomes are matched only with words - 'Successful', 'Operational', 'En Route'.