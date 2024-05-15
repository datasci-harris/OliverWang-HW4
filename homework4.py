# Oliver Wang (Su Wang)
# suwang26
# oliverwang266

"""
INSTRUCTIONS

Available: May 9th at 11:59PM

Due: May 16th at 11:59PM

Gentle reminder that, among other things, you

(a) Must answer your questions in the homework4.py file
(b) Must commit homework4.py and movies.csv to your clone of the 
GitHub homework repo
(c) Must link your GitHub repo to GradeScope
(d) Must NOT repeatedly use a hard-coded path for the working directory

Failure to do any of these will result in the loss of points
"""


# HOMEWORK 4
# %% ===========================================================================
# Import necessary libraries
# ==============================================================================
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# %% ===========================================================================
# Define functions for fetching and parsing the data
# ==============================================================================
def fetch_html(year): 
    """Fetch the HTML content of the Wikipedia page for the given year.
    
    Args:
        year (int): The year for which to fetch the data.
    """
    url = f"https://en.wikipedia.org/wiki/List_of_American_films_of_{year}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_table(html, year):
    """Parse the top-grossing films table from the HTML content.
    
    Args:
        html (str): The HTML content of the Wikipedia page.
        year (int): The year for which the data is being parsed.
    """
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', class_='wikitable')
    # The first table after the heading is usually the one we need
    table = tables[0]
    
    rows = table.find_all('tr')
    data = []
    current_distributor = None
    
    for row in rows[1:]:
        cells = row.find_all(['th', 'td'])
        if len(cells) == 4:
            rank = cells[0].get_text(strip=True)
            title = cells[1].get_text(strip=True)
            distributor = cells[2].get_text(strip=True)
            domestic_gross = cells[3].get_text(strip=True)
            current_distributor = distributor
        elif len(cells) == 3:
            rank = cells[0].get_text(strip=True)
            title = cells[1].get_text(strip=True)
            domestic_gross = cells[2].get_text(strip=True)
            distributor = current_distributor
        else:
            continue

        data.append([rank, title, distributor, domestic_gross, year])
    
    return data

def get_movies_data(start_year, end_year):
    """Fetch and parse the top-grossing films for a range of years.
    
    Args:
        start_year (int): The first year to fetch data for.
        end_year (int): The last year to fetch data for.
    """
    all_data = []
    for year in range(start_year, end_year + 1):
        print(f"Fetching data for year: {year}")
        html = fetch_html(year)
        year_data = parse_table(html, year)
        all_data.extend(year_data)
        time.sleep(3)  # Pause to avoid hitting Wikipedia too frequently
    return all_data
# %% ===========================================================================
# Define the function to save and pick a random movie
# ==============================================================================
def save_to_csv(data, filename):
    """Save the movie data to a CSV file.
    
    Args:
        data (list): The list of movie data to save.
        filename (str): The name of the CSV file to save the data to.
    """
    df = pd.DataFrame(data, columns=['Rank', 'Title', 'Distributor', 'Domestic gross', 'Year'])
    df.to_csv(filename, index=False)

def pick_random_movie(filename):
    """Pick and print a random movie from the CSV file.
    
    Args:
        filename (str): The name of the CSV file containing the movie data.
    """
    df = pd.read_csv(filename)
    random_row = df.sample(n=1).iloc[0]
    print(f"{random_row['Title']} ({random_row['Year']})")
# %% ===========================================================================
# Define the main function and execute the program
# ==============================================================================
def main():
    start_year = 1970
    end_year = 2023
    csv_filename = "movies.csv"
    
    movies_data = get_movies_data(start_year, end_year)
    save_to_csv(movies_data, csv_filename)
    pick_random_movie(csv_filename)

if __name__ == "__main__":
    main()
