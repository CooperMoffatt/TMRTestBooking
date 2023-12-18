import csv
import datetime
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


options = Options()
options.add_argument("--enable-chrome-browser-cloud-management")

driver = webdriver.Chrome(options=options)

def inTheWay(): # Stuff in the way of the booking
    # Navigate to the website
    driver.get(
        "https://www.service.transport.qld.gov.au/SBSExternal/public/WelcomeDrivingTest.xhtml"
    )

    # Find the element by id
    button = driver.find_element("id", "j_id_60:aboutThisServiceForm:continueButton")
    button.click()

    # Terms of use Bypass
    TermsButton = driver.find_element(
        "id", "termsAndConditions:TermsAndConditionsForm:acceptButton"
    )
    TermsButton.click()

    # License Number
    licenseNumber = driver.find_element("id", "CleanBookingDEForm:dlNumber")
    licenseNumber.send_keys("ENTER DRIVERS LICENSE NUMBER")

    # Name
    name = driver.find_element("id", "CleanBookingDEForm:contactName")
    name.send_keys("ENTER NAME HERE")

    # Phone
    phone = driver.find_element("id", "CleanBookingDEForm:contactPhone")
    phone.send_keys("ENTER PHONE")


    # Menu
    menu = driver.find_element("id", "CleanBookingDEForm:productType_label")
    menu.click()

    menuFind = driver.find_element("id", "CleanBookingDEForm:productType_1")
    menuFind.click()

    # Continue
    continueButton = driver.find_element(
        "id", "CleanBookingDEForm:actionFieldList:confirmButtonField:confirmButton"
    )
    continueButton.click()


    # Confirming details
    time.sleep(1)
    confirmButton = driver.find_element(
        "id", "BookingConfirmationForm:actionFieldList:confirmButtonField:confirmButton"
    )
    confirmButton.click()

    print("Signed in with details")
    time.sleep(1)


def loganSite2(): # selecting SCQ South Brisbane site
    # selecting SCQ South Brisbane
    GClist = driver.find_element("id", "BookingSearchForm:region")
    GClist.click()
    GCFind = driver.find_element("id", "BookingSearchForm:region_13")
    GCFind.click()
    # selecting confirm
    confirm = driver.find_element(
        "id", "BookingSearchForm:actionFieldList:confirmButtonField:confirmButton"
    )
    confirm.click()
    print("Selected SCQ South Brisbane")
    time.sleep(1)




def scrapTable():
    url = driver.current_url
    response = requests.get(url)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the table in the parsed HTML
    table = soup.find("table", {"role": "grid"})

    # Find all rows in the table body
    rows = table.find("tbody").find_all("tr")

    data = []
    # Iterate over each row
    for row in rows:
        # Find each cell in the row
        cells = row.find_all("td")

        # Extract the text from the cells
        booking_time = cells[1].text.strip()
        location = cells[2].text.strip()

        # Store the data in a dictionary and append it to the list
        data.append({"booking_time": booking_time, "location": location})
    print("Scraped data: ")
    print(data)
    print("Exporting to csv file")
    with open("C:/Users/Koopa/Documents/Python Programs/TMRTestBooking/data.csv", "w", newline="") as file:
        # Create a CSV writer
        writer = csv.writer(file)

        # Write the headers to the CSV file
        writer.writerow(["booking_time", "location"])
        
        # Iterate over the data
        for row in data:
            # Write the data to the CSV file
            writer.writerow([row["booking_time"], row["location"]])
            

def checkingCancelations():
    print("Checking for cancelations")
    now = datetime.datetime.now()
    in_14_days = now + datetime.timedelta(days=14)
    booking_found = False

    with open("C:/Users/Koopa/Documents/Python Programs/TMRTestBooking/data.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            booking_time = datetime.datetime.strptime(row[0], '%A, %d %B %Y %I:%M %p')
            if now <= booking_time <= in_14_days:
                print(f"Booking available: {booking_time} at {row[1]}")
                booking_found = True
                
    if not booking_found:
        print("No bookings available")
    


inTheWay()

loganSite2()

scrapTable()

checkingCancelations()


time.sleep(10)
