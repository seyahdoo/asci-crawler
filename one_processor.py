import db
import browser
import pool


def process_one():

    link = db.get_one_link()
    driver = pool.get()

    is_not_relative = True

    # if "game" keyword exist, if url contains "linkedin.com"
    if browser.get_game_exists(driver) and driver.current_url.lower().__contains__("linkedin.com"):
        db.mark_relative(driver.current_url)

    for link in browser.get_links(driver):
        db.add_link(driver.current_url, link, 0)

    pool.release(driver)
    return