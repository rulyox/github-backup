import os
import pathlib
from selenium import webdriver
import config

current_directory = pathlib.Path(__file__).parent.absolute()
download_directory = 'downloads'

selenium_options = webdriver.ChromeOptions()
selenium_options.add_argument('headless')
selenium_options.add_experimental_option('prefs', {
    'download.default_directory': os.path.join(current_directory, download_directory),
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
})
selenium_driver = webdriver.Chrome(config.CHROME_DRIVER, options=selenium_options)

list_repository = []


def login():
    login_link = 'https://github.com/login'
    selenium_driver.get(login_link)

    # find elements
    element_id = selenium_driver.find_element_by_id('login_field')
    element_pw = selenium_driver.find_element_by_id('password')
    element_button = selenium_driver.find_element_by_name('commit')

    # authenticate
    element_id.send_keys(config.GITHUB_ID)
    element_pw.send_keys(config.GITHUB_PW)
    element_button.click()


def get_repository(link):
    selenium_driver.get(link)

    # find elements
    elements_repository = selenium_driver.find_elements_by_css_selector('li > div > div > h3 > a')
    elements_button = selenium_driver.find_elements_by_css_selector('div.paginate-container > div.BtnGroup > a')

    # get repository links
    for element in elements_repository:
        repository_link = element.get_attribute('href')
        list_repository.append(repository_link)

    # recursive call if next page exists
    for element in elements_button:
        button_text = element.get_attribute('innerHTML')
        if button_text == 'Next':
            next_link = element.get_attribute('href')
            get_repository(next_link)


def download_zip():
    for repository in list_repository:
        print('Download : ' + repository)
        zip_link = repository + '/archive/master.zip'
        selenium_driver.get(zip_link)


def main():
    print('Logging in...')
    login()

    print('Getting repositories...')
    profile_link = 'https://github.com/' + config.GITHUB_ID + '?tab=repositories'
    get_repository(profile_link)

    print('Downloading...')
    download_zip()

    print('Finished!')


if __name__ == '__main__':
    main()
