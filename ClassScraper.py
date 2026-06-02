from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
import lxml
import csv
import sys
import argparse

# Initialize the parser object
parser = argparse.ArgumentParser(description="Parsing Safari option and Input and Output file parameters")

# Define Safari flag and optional input and output files
parser.add_argument('-s', '--Safari', action='store_true', help="Use Safari instead of Chrome for Selenium")
parser.add_argument('-i', '--input', type=str, default="Classes", help="Specify path for input file, not inclluding file extension")
parser.add_argument('-o', '--output', type=str, default="Classes", help="Specify path for output file, not including file extension")

args = parser.parse_args()

with webdriver.Safari() if args.Safari else webdriver.Chrome() as driver:
    try:
        # opens file with all the classes, codes should be like they are in the USC thing
        with open(f"{args.input}.txt", 'r') as file:
            #getting to usc schedule page 
            driver.get("https://my.usc.edu")

            # was trying to sign in through selenium but realized it would be significantly easier with manual sign-in

            #waits until you're at the myUSC page after manually signing in
            while(driver.title.find("myUSC")==-1):
                True
            #goes to webreg
            driver.get("https://my.usc.edu/portal/oasis/webregbridge.php")
            #goes to the current semester
            driver.find_element(By.ID, "termLink1").click()
            assert "WebReg" in driver.title
            data = []
            content = file.read()
            #gets all the class codes
            codes = content.splitlines()
            for code in codes:
                # print(code)
                # splits the class code with the department code
                department = code[0:code.find("-")]
                # goes to the department site
                driver.get(f"https://webreg.usc.edu/Courses?Program={department}")
                # gets the html of the site and then searches it for the div of the class
                soup = BS(driver.page_source, 'lxml')
                class_div = soup.find("div", id="courseBin_"+code)
                # if it can find the class
                if(class_div):
                    # gets all the sections of the current class
                    sections = class_div.find_all("div", class_="section")
                    # formats each class into a dictionary entry of fields matching to values
                    for section in sections:
                        fields = section.text.splitlines()
                        goodInfo = []
                        for i in fields:
                            i = i.strip()
                            if i != "":
                                goodInfo.append(i)
                        print(goodInfo)
                        entry = {"Class:": code.strip()}
                        i = 1
                        while(i < len(goodInfo) - 1):
                            if(goodInfo[i].find(":") != len(goodInfo[i]) - 1):
                                entry[goodInfo[i-1]] = goodInfo[i]
                                i+=1
                            i+=1
                        print(entry)
                        data.append(entry)
            # writes the data into a csv
        with open(f"{args.output}.csv", 'w') as csvfile:
            fields = ["Class:", "Section:", "Session:", "Type:", "Units:", "Registered:", "Time:", "Days:", "Instructor:", "Location:"]
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=fields)

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            writer.writerows(data)
        
    except OSError as e:
        print(f"Error: The file '{args.input}.txt' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
