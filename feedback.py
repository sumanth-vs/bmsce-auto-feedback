from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import chromedriver_autoinstaller

WEBCAMPUS_URL = 'https://webcampus.bmsce.in/student'
FEEDBACK_BASE_URL = 'https://webcampus.bmsce.in/student/feedbackFaculty/'

def screamErrorAndQuit(msg):
    print(f'ERROR: {msg}')
    exit(1)

def autoFeedback(user_usn, user_pass, rating):
    # Gets the latest version of Chrome Driver and
    # adds it to the path automatically
    print("Installing chrome-driver...")
    chromedriver_autoinstaller.install()
    print("Done.")

    # set webdriver to browser you intend to run this on
    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()    

    driver.get(WEBCAMPUS_URL)

    usn_field = driver.find_element(By.ID, 'usn')
    usn_field.send_keys(user_usn)

    pass_field = driver.find_element(By.ID, 'password')
    pass_field.send_keys(user_pass)

    signin_btn = driver.find_element(
        By.XPATH, '/html/body/div/div/div/form/div/div/button')
    signin_btn.click()

    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "page-profile"))
        )
    except:
        driver.quit()
        screamErrorAndQuit('Wrong login details!')
    print('Signed in.')

    feedback_page_url = ''
    view_btns = driver.find_elements(By.PARTIAL_LINK_TEXT, 'View')
    for view_btn in view_btns:
        if FEEDBACK_BASE_URL in view_btn.get_attribute('href'):
            feedback_page_url = view_btn.get_attribute('href')

    driver.get(feedback_page_url)
    print('In feedback page.')

    feedback_urls = []
    course_btns = driver.find_elements(By.PARTIAL_LINK_TEXT, 'Give Feedback')
    for course_btn in course_btns:
        feedback_urls.append(course_btn.get_attribute('href'))

    feedback_count = len(feedback_urls)
    print('Found', str(feedback_count), 'courses that need feedback.')
    if feedback_count > 0:
        print('Submitting feedback...')
        for feedback_url in feedback_urls:

            driver.get(feedback_url)

            breadcrumb = driver.find_element(By.CLASS_NAME, 'breadcrumb')
            course_name = breadcrumb.find_elements(By.TAG_NAME, 'li')[-1].text

            feedback_form = driver.find_element(By.ID, 'js_dataTable1')
            rows = feedback_form.find_elements(By.CSS_SELECTOR, 'tbody tr')

            # rows 0-7 -> selection; row 8 -> custom feedback message; row 9 -> submit btn
            for row in rows[:-2]:
                cols = row.find_elements(By.TAG_NAME, 'td')
                # cols 0,1 -> s.no, competency; cols 2-6 -> excellent, vgood, good, fair, poor

                radio_btn = cols[1+rating]
                radio_btn.click()

            feedback_form.find_element(By.ID, 'submit_feedback').click()
            print('-- Feedback for', course_name, 'submitted.')

        print("And we're done.")
    else:
        print('Nothing to do :/')

    driver.quit()


def main():
    print(
    """

    ██████╗ ███╗   ███╗███████╗ ██████╗███████╗    ███████╗███████╗███████╗██████╗ ██████╗  █████╗  ██████╗██╗  ██╗
    ██╔══██╗████╗ ████║██╔════╝██╔════╝██╔════╝    ██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
    ██████╔╝██╔████╔██║███████╗██║     █████╗      █████╗  █████╗  █████╗  ██║  ██║██████╔╝███████║██║     █████╔╝ 
    ██╔══██╗██║╚██╔╝██║╚════██║██║     ██╔══╝      ██╔══╝  ██╔══╝  ██╔══╝  ██║  ██║██╔══██╗██╔══██║██║     ██╔═██╗ 
    ██████╔╝██║ ╚═╝ ██║███████║╚██████╗███████╗    ██║     ███████╗███████╗██████╔╝██████╔╝██║  ██║╚██████╗██║  ██╗
    ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝╚══════╝    ╚═╝     ╚══════╝╚══════╝╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                                                                                                                  

    """)

    print('Attempting sign in.')
    user_usn = input('-- Enter USN: ')
    user_pass = getpass('-- Enter Password: ')
    rating = int(input(
    """--  Choose a Rating
    1. Excellent
    2. Very Good
    3. Good
    4. Fair
    5. Poor
    """))
    if rating not in [1, 2, 3, 4, 5]:
      screamErrorAndQuit("Invalid Rating")

    autoFeedback(user_usn.upper(), user_pass, rating)


if __name__ == "__main__":
    main()
