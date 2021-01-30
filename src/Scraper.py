#%%
from selenium import webdriver
# import Action chains  
from selenium.webdriver.common.action_chains import ActionChains
# import KEYS 
from selenium.webdriver.common.keys import Keys
import time
# research filters
job_position = "data science"
location = "heidelberg"
radius = "50"

class Scaper:
    def __init__(self, location, job_title, job_type, radius, list_forbidden_words) -> None:
        # selenium options
        print("Initializing the scraper..")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument("--test-type")
        # self.options.headless = True # do not open the browser 
        self.options.binary_location = "/usr/bin/brave-browser-stable" # set path to browser file
        self.driver = webdriver.Chrome(executable_path="/home/fedmag/Projects/JobsAggregator/lib/chromedriver", options=self.options)
        self.action = ActionChains(self.driver)
        # scaper options
        self.location = location
        self.job_title = job_title
        self.job_type = job_type
        self.radius = radius
        self.forbidden_words = list_forbidden_words
        print("..scraper initialized!")

    # functions
    def glassdoor_print_offer(self, offer,i): 
        self.action.key_down(Keys.ESCAPE).perform() # avoid the 'create profile' popup
        offer.click()
        time.sleep(1.5) # after the click the page needs to load the offer
        desc = self.driver.find_element_by_class_name("jobDescriptionContent")
        links = self.driver.find_elements_by_link_text("Jetzt bewerben") # this always returns a list
        link = links[0]
        if  ("deutsch-") not in desc.text.lower():
            print("---------------------------------")
            print("Post title: {} - {}".format(offer.text, i+1))
            print(link.get_attribute('href'))
            print("---------------------------------")
            print(desc.text)
            print("\n =============")
    
    def scrape_glassdoor(self):
        print("Scraping GLASSDOOR: \n")
        website = "https://www.glassdoor.de/"
        self.driver.get(website)
        
        time.sleep(5)
        offers = self.driver.find_elements_by_class_name("jobInfoItem") # retrieving the list of jobs
        # dealing with the cookie button
        try:
            self.driver.find_element_by_id("onetrust-accept-btn-handler").click() # if the cookies button is there click it
        except:
            print("Cookie button did not appear!")
        for i, offer in enumerate(offers):
            self.glassdoor_print_offer(offer,i)  
        self.driver.close()

# %%
scraper = Scaper("heidelberg", "data-science", "internship", "50", [])
scraper.scrape_glassdoor()
# %%
https://www.glassdoor.de/Job/heidelberg-data-science-jobs-SRCH_IL.0,8_IC2598197_KO9,13.htm?jobType=internship
https://www.glassdoor.de/Job/heidelberg-data-science-jobs-SRCH_IL.0,10_IC2563483_KO11,23.htm
https://www.glassdoor.de/Job/heidelberg-data-science-jobs-SRCH_IL.0,10_IC2563483_KO11,23.htm?jobType=internship