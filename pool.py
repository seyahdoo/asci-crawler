
import browser

pool = []


def get():
    if len(pool) > 0:
        return pool.pop()
    else:
        return browser.get_browser()


def release(driver):
    pool.append(driver)
