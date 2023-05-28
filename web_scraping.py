import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    # Replace the URL with the website you want to scrape
    url = 'https://www.example.com/'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the <a> tags in the HTML content
    links = soup.find_all('a')

    # Loop through each link and print the text and href attribute
    for link in links:
        print(link.text.strip(), link.get('href'))
