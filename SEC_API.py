# In this project, we are going to scrape company filings data from the SEC, specifically, SEC Edgar
# *** EDGAR: (Electronic Data Gathering, Analysis, and Retrieval system) which is
# a comprehensive database, used by The U.S. Securities and Exchange Commission, designed to enable the electronic
# submission, retrieval, and analysis of financial and corporate data from publicly traded entities.

#***I have used the help of ChatGPT for areas of the code I had struggled with. This goes the same for every project
# I have created.

# Companies publicly traded in the United States are required to file various reports and disclosures with the SEC.
# These companies trading on major stock exchanges like the New York Stock Exchange and NASDAQ Stock Exchange are notably large
# accelerated filer companies with a market capitalization of $700 million or more.
# Consider the example of Steven Cohen, who contributed $10 million of his own money to S.A.C Capital
# and grew it to more than $12 billion in capital for the hedge fund, back in 1972!

# Fast-forward to more recent times: after getting in trouble, Steven Cohen let go of outside capital,
# thus relinquishing one of the world's most successful hedge funds in history.
# He then transformed his fund into the family office known as Point72 Asset Management,
# which is currently valued at around $30 billion as of August 22, 2024, as reported by Forbes at
# https://www.forbes.com/profile/steve-cohen/

# Scraping company filings data from the SEC for free using Python is really cool.

# In response to the inquiry, there are several prominent cybersecurity companies with large market capitalization
# merit examination. Specifically, Palo Alto Networks and Fortinet,
# two leading cybersecurity firms, collectively possess a staggering market capitalization of at least $90 billion.

# The SEC provides easy programmatic access to EDGAR data through its APIs. In this project, we will utilize
# the EDGAR Tools Library, a Python library developed by Dwight Gunning and available in a public repository,
# to access this data.

from edgar import * # From the EDGAR library we want to import everything: the Company function, the
# set_identity function to see which company data we want to parse and then, using set_library,
# we are going to set an identity; as well as the xbrl package as we are working wil xbrl data.

#***from edgar.xbrl import xbrldata.XBRLData # Calling the XBRLData class to parse xbrl documents

import requests
#***from bs4 import BeautifulSoup # pip install beautifulsoup

# Tell the SEC who you are:
set_identity("Caela Mills caela.cm04@gmail.com") # Setting an identity means entering a name and email. It is a
# rule from the SEC API that the user identity of the client machine must be recognized by the Edgar Rest machine.

# To query the SEC application programming interface, we can specify the company and provide either its stock ticker
# symbol or its Central Index Key code. In this case, I will use the company's ticker symbol,
# which corresponds to its name listed on the NASDAQ exchange.

# Define the companies using their NASDAQ ticker symbols.
palo_altos_networks = Company("PANW")
fortinet = Company("FTNT")

# These statements retrieve the most recent financial (or "financials") information for both companies:
palo_altos_networks_financials = palo_altos_networks.financials
print("\nPalo Alto Networks Financials:")
print(palo_altos_networks_financials) # This statement presents the financial information in the form of
# a balance sheet.
fortinet_financials = fortinet.financials
print("\nFortinet Financials:")
print(fortinet_financials) # This statement presents the financial information in the form of
# a balance sheet.

# These statements retrieve the former aliases both companies adopted from the past:
# Retrieve and print former names if available
try:
    palo_altos_networks_former_names = palo_altos_networks.former_names
    print("\nPalo Alto Networks Former Names:")
    print(palo_altos_networks_former_names)
except Exception as e:
    print(f"Error retrieving former names for Palo Alto Networks: {e}")

try:
    fortinet_former_names = fortinet.former_names
    print("\nCheck Fortinet Former Names:")
    print(fortinet_former_names)
except Exception as e:
    print(f"Error retrieving former names for Fortinet: {e}")

# Suppose we wanted to retrieve their 10-Q filings of their company filings, in other words,
# their quarterly earnings data, all we hwave to do is enter the following statements:
try:
    filings = palo_altos_networks.get_filings(form="10-Q")
    filings_df = filings.to_pandas() # The variable filings_df is getting these 10-Q filings as a pandas dataframe.
    print("\nPalo Alto Networks 10-Q Filings:") # We know there are 36 rows by 13 columns worth of information (0-35).
    print(filings_df) # Here we say print (or "display") all of our 10-Q filings.
except Exception as e:
    print(f"Error retrieving 10-Q filings for Palo Alto Networks: {e}")

try:
    filings = fortinet.get_filings(form="10-Q")
    filings_df = filings.to_pandas()
    print("\nFortinet 10-Q Filings:") # We know there are 44 rows by 13 columns worth of information (0-43).
    print(filings_df)
except Exception as e:
    print(f"Error retrieving 10-Q filings for Fortinet: {e}")

# Suppose you wanted to get raw data. You can get it but using this specific method.
# Focusing on one filing: the latest 10-Q filings of data, then we would do the following:

try:
    latest_10q = filings.latest() # Assign the variable 'latest_10q' to the retrieved filings and using the latest()
    # method, and our program will display the latest (or most recent) 10-Q filings.
    tenq = latest_10q.obj()

    # From our 10-Qs, we have different types of data that we can display: we have text data or "items," and we have
    # financial numerical data.

    # Display the list of items available
    print("\nAvailable items in the 10-Q filings:")
    print(tenq.items) # This displays the list of items available in each 10-Q filing.
except Exception as e:
    print(f"Error processing items in the 10-Q filings: {e}")


# Access a specific item like Item 2
# Use dictionary-like access to view stored items.
print(tenq["Item 2"])

def fetch_and_display_item(ticker, item_name):
    try:
        # Fetch 10-Q filings
        company = Company(ticker)
        filings = company.get_filings(form="10-Q")

        if not filings:
            print(f"No 10-Q filings available for {ticker}.")
            return

        # Retrieve the latest 10-Q filing
        latest_filing = filings[0]  # Assuming the first in the list is the latest

        # Access specific item; make sure to refer to the documentation of the library
        item = getattr(latest_filing, item_name, "Item not found")
        print(f"\n{item_name} Data for {ticker}:")
        print(item)

    except Exception as e:
        print(f"Error processing latest 10-Q filing for {ticker}: {e}")

# # Using the xbrl object, we can assign this to our latest 10-Q filing object and with a xbrl method to
# # extract XBRL data.
# xbrl = latest_10q.xbrl()
# # Check available attributes and methods of the XBRL data object
# print("\nAvailable attributes in XBRL object:")
# print(dir(xbrl)) # The dir() method will return the attributes and methods of the object inside its scope,
# # that being, 'xbrl.'

try:
    # Using the xbrl object, we can assign this to our latest 10-Q filing object and with a xbrl method to
    # extract XBRL data.
    xbrl = latest_10q.xbrl()

    # Check available attributes and methods of the XBRL data object
    print("\nAvailable attributes in XBRL object:")
    print(dir(xbrl)) # The dir() method will return the attributes and methods of the object inside its scope,
    # that being, 'xbrl.'

    # Show xbrl data with attribute 'parse.()' or 'parse_raw' or parse_obj or 'extract'
    # xbrl.parse('XBRL Data') or parse_raw

    # I am having trouble accessing XBRL Data but that will be rectified later...
    if hasattr(xbrl, 'parse_obj'):
        xbrl_data_extracted = xbrl.parse_obj
        print("\nThe required 'parse_obj' attribute is not available in the XBRL object.")
        print(xbrl_data_extracted)
    else:
        print("\nMethod 'parse_obj' not found in the XBRL object.")

except Exception as e:
    print(f"\nError accessing or printing XBRL Data: {e}")

# --Output--
# Extracted XBRL Data:
# <bound method BaseModel.parse_obj of <class 'edgar.xbrl.xbrldata.XBRLData'>>
# ----------------------------------------------------------------------------------------------------------------------
# The next kind of forms that I want to look at are the 8-K annual reports.
# The 8-Ks reports are like special disclosures that these cybersecurity firms have to make regarding their business.
# Form 8-K is a fundamental disclosure document mandated by the SEC for publicly traded entities,
# including cybersecurity companies.
# It serves to report critical events that shareholders ought to be informed of.
# Unlike the comprehensive annual 10-K or quarterly 10-Q reports detailing a company's financial performance and
# operations, the 8-K concentrates on specific, frequently time-critical information.

try:
    filings = palo_altos_networks.get_filings(form="8-K")
    filings_df = filings.to_pandas()
    print("\nPalo Alto Networks 8-K Filings:") # We know there are 112 rows by 13 columns worth of information (0-111).
    print(filings_df)
except Exception as e:
    print(f"Error retrieving 8-K filings for Palo Alto Networks: {e}")

try:
    filings = fortinet.get_filings(form="8-K")
    filings_df = filings.to_pandas()
    print("\nFortinet 8-K Filings:") # We know there are 121 rows by 13 columns worth of information (0-120).
    print(filings_df)
except Exception as e:
    print(f"Error retrieving 8-K filings for Fortinet: {e}")


try:
    latest_8k = filings.latest() # Assign the variable 'latest_10q' to the retrieved filings and using the latest()
    # method, and our program will display the latest (or most recent) 10-Q filings.
    eightk = latest_8k.obj()

    # From our 10-Qs, we have different types of data that we can display: we have text data or "items," and we have
    # financial numerical data.

    # Display the list of items available
    print("\nAvailable items in the 8-K filings:")
    print(eightk.items) # This displays the list of items available in each 10-Q filing.
except Exception as e:
    print(f"Error processing items in the 8-K filings: {e}")

try:
    # Inspect the available attributes and methods of the eightk object
    print("\nAttributes and methods of the eightk object:")
    print(dir(eightk))  # List all attributes and methods

    # Access the content of "Item 9.01" based on available methods
    if hasattr(eightk, '__getitem__'):
        item_901_content = eightk.__getitem__('Item 9.01')
        print("\nContent of Item 9.01:")
        print(item_901_content)  # Print the content of Item 9.01
        press_release_count = item_901_content.lower().count('press release')
        print(f"\nNumber of press releases in Item 9.01: {press_release_count}") # How many press releases are there?
    else:
        print("Method '__getitem__' not found in the 8-K object.")

except Exception as e:
    print(f"Error accessing or printing Item 9.01: {e}")


# Is there a way I could access the exhibit 99.1 press release document in Python?
# The answer: Yes. The required functionality can be achieved through the use of libraries such as
# requests for handling HTTP requests and BeautifulSoup for parsing HTML.

# ***Parsing is the analysis of symbolic sequences in a sting of text based on a particular formal grammar.

# If these libraries are not currently installed, they can be acquired through the installation process.


# URL of the SEC EDGAR search results page for a specific company and date
# Replace with the actual URL for the Form 8-K filing you're interested in retrieving.


def download_document(cik, filing_number, document_name, save_path):
    base_url = "https://www.sec.gov/Archives/edgar/data"
    url = f"{base_url}/{cik}/{filing_number}/{document_name}"

    try:
        print(f"Attempting to download document from: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        with open(save_path, 'htm') as file:
            file.write(response.content)
        print(f"Document downloaded successfully: {save_path}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - URL: {url}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err} - URL: {url}")
    except Exception as e:
        print(f"An unexpected error occurred: {e} - URL: {url}")

# CIK and Filing Numbers
# The Actual Values obtained from SEC EDGAR - get rid of the 3 zeros in front the "000"
palo_alto_cik = "1327567"  # CIK for Palo Alto Networks | This is factually correct
fortinet_cik = "1262039"  # CIK for Fortinet | This is factually correct

# Filing Information for the Most Recent 8-K Filing
palo_alto_filing_number = "000132756724000023"  # Filing number for Palo Alto | This is factually correct -- from
# "001-35594" to "000132756724000023"
fortinet_filing_number = "000126203924000034"  # Filing number for Fortinet | This is factually correct -- from
# "001-34511" to "000126203924000034"

# The Actual Document Names with their Actual Values for the Most Recent 8-K Filing
palo_alto_document_name = "ex991q424earningsrelease.htm"  # Document name for Palo Alto Networks -- from "panw-20240819.htm"
fortinet_document_name = "ftntq2-2024ex991corrected.htm"  # Document name for Fortinet -- from "ftnt-20240806.htm"

# Save paths -- do not use 'file:///' as a prefix
# How do you save a .htm file to a file path (when downloaded) to your pc in Python code?
palo_alto_save_path = "C:/Users/Administrator/Downloads/palo_alto_networks_document.htm" # From "./palo_alto_networks_document.htm" to
# "file:///C:/Users/Administrator/Downloads/palo_alto_networks_document.htm"
fortinet_save_path = "C:/Users/Administrator/Downloads/fortinet_document.htm" # From "./fortinet_document.htm" to "file:///C:/Users/Administrator/Downloads/fortinet_document.htm"

# Download documents
download_document(palo_alto_cik, palo_alto_filing_number, palo_alto_document_name, palo_alto_save_path)
download_document(fortinet_cik, fortinet_filing_number, fortinet_document_name, fortinet_save_path)


# How can you tell when a global business is going to devalue their currency?



