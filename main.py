from bs4 import BeautifulSoup
import time
from selenium import webdriver


def scanner(url):
    # Driver for selenium to automatically scroll
    # to the bottom of the page to update the search results
    driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.get(url)

    # Automatically scroll till the end of the page
    len_of_page = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while not match:
        last_count = len_of_page
        time.sleep(3)
        len_of_page = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if last_count == len_of_page:
            match = True

    # The Html of the website
    time.sleep(4)
    response = driver.page_source
    # Instance of bs4
    soup = BeautifulSoup(response, 'lxml')
    # The HTML tag containing the list of the games
    game_list = soup.find('div', {'id': 'search_resultsRows'})
    # Every game is an a tag
    games = game_list.find_all('a')

    # For every game in the list, add appropriate games to final list
    game_selection = []
    for game in games:
        title = game.find('span', {'class': 'title'}).text
        release_date = game.find('div', {'class': 'col search_released responsive_secondrow'}).text
        review = game.find('span', {'class': 'search_review_summary positive'})
        img = game.find('img')['src']
        # Try except statement to catch games that don't have a price
        try:
            price = game.find('div', {'class': 'col search_price responsive_secondrow'}).text
        except:
            # Try except statement to account for discounted games
            try:
                price = game.find('div', {'class': 'col search_price discounted responsive_secondrow'}).text
            except:
                price = ""

        # Apply the last filters
        if ('a' not in title) and review and price:
            game_information = {
                "Title": title,
                "price": price.strip(),
                "release date": release_date,
                "image source": img
            }
            game_selection.append(game_information)
    # Close the driver for selenium
    driver.quit()


scanner('https://store.steampowered.com/search/?maxprice=10&tags=5350&category1=998&supportedlang=norwegian')
