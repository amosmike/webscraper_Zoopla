from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from time import sleep
from time import time
from cookie_accepter2 import load_and_accept_cookies

URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
driver = webdriver.Safari() 

load_and_accept_cookies(URL, driver, sleep)

sleep(1)

driver.switch_to.default_content()

def get_links(driver: webdriver.Safari) -> list:

    prop_container = driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div[2]/main/div[2]/div[2]') #Gets Xpath of all properties on page ## Make sure XPath is still valid 
    prop_list = prop_container.find_elements_by_xpath('./div')
    print("PROPERTY LIST BELOW")
    print(prop_list)
    link_list = []

    for property in prop_list: # Takes the big list of <div>s to different properties individually 
        a_tag = property.find_element_by_tag_name('a')
        link = a_tag.get_attribute('href')
        link_list.append(link) # Gets each link and puts it into link_list
        
    print(f'There are {len(link_list)} properties on page ' +  str(i+1))
    #print(link_list)

    return link_list

# get_links(driver)

big_list = []
    # driver = load_and_accept_cookies(URL, driver, sleep) # Do we need this??? 

for i in range(2):
    
    # Need to get links from page 1/start page
    big_list.extend(get_links(driver)) # Call the function we just created and extend the big list with the returned list ## replaced extend with append ?## 
    ###

    ## Click the next button. Don't forget to use sleeps, so the website doesn't suspect
    next_button = driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div[2]/main/div[2]/div[3]/ul/li[7]/a')
    next_button.click()
    sleep(3)

    try:
        close_popup = driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/button')
        close_popup.click()
        print("Popup removed, page: " + str(i+2))

    except:
        print("No popups page: " + str(i+1)) #pass # If there is no cookies button, we won't find it, so we can pass
        pass # If there is no cookies button, we won't find it, so we can pass

    print("Page: " + str(i+1) + " complete")
    sleep(2)

print(big_list)

dict_properties = {'Price': [], 'Address': [], 'Bedrooms': [], 'Description': []}
count = 0

for link in big_list:

    driver.get(link)
    ## TO DO: Visit all the links, and extract the data. Don't forget to use sleeps, so the website doesn't suspect
    try:
        price = driver.find_element_by_xpath('//*[@id="main-content"]/div[1]/div[1]/div/div[2]/div[2]/p').text
    except:
        price = "UNKNOWN"

    address = driver.find_element_by_xpath('//*[@id="listing-summary-details-heading"]/div[2]/address').text

    bedrooms = driver.find_element_by_xpath('//*[@id="listing-summary-details-heading"]/div[1]').text

    span_tag = driver.find_element_by_xpath('//*[@id="main-content"]/div[1]/section[2]/div[2]/div/div/div/span')
    description = span_tag.text

    dict_properties['Price'].append(price)
    dict_properties['Address'].append(address)
    dict_properties['Bedrooms'].append(bedrooms)
    dict_properties['Description'] = description

    count += 1
    print("Finished link " + str(count))
    sleep(2)


driver.quit() # Close the browser when you finish
print(dict_properties)
