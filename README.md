# USC Webreg Scraper
I created this webscraper in order to be used to help Makers with advertising. You give it a text file with all the class codes that you want information from and the program will give you a CSV file with all sections and information from those sections available on WebReg.

## How to Use
First clone the repo and open it in VS Code. Then, go to the top right and click where it says select another kernel. Create a virtual environment. Put all the classes you want the information for into a file called "Classes.txt". If you want to make sure there's no duplicates and sort it into alphabetical order, run ClassesSorter.ipynb After that, just run SeleniumClassScraper.ipynb, the first part and then the second part. It will create a CSV called Classes.csv which will have all the data. Then, you can just import it into Google Sheets or Excel and do whatever you want with it.
