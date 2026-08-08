import requests

# API URLs
url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
url1 = "https://catfact.ninja/fact"

# Technology fact
def get_random_technology_fact():
    response = requests.get(url)
    if response.status_code == 200:
        fact_data = response.json()
        print(f"Did you know? {fact_data['text']}")
    else:
        print("Failed to fetch fact")

# Cat fact
def get_random_cat_fact():
    response = requests.get(url1)
    if response.status_code == 200:
        fact_data = response.json()
        print(f"Did you know? {fact_data['fact']}")
    else:
        print("Failed to fetch cat fact")

# Main loop
while True:
    print("\nChoose category: technology / cat")
    user_input = input("Type category or 'q' to quit: ")

    if user_input.lower() == 'q':
        break

    elif user_input.lower() == "technology":
        get_random_technology_fact()

    elif user_input.lower() == "cat":
        get_random_cat_fact()

    else:
        print("Invalid input! Please choose 'technology' or 'cat'")