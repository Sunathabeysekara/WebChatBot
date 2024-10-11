# -*- coding: utf-8 -*-
"""webchatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Zck_OnnfRfGNBt1inm7nmW-mxW_NCAZ5

chat bot to read from blogs and sites to retrival information by user query by user using NLP,AI, and pinecorn

selenium to extract content data
deeplake to store
pinecone to get result as nlp
"""

!pip install -q deeplake pinecone selenium

#configuring selenium to retrive information from the site
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from google.colab import drive
import json
drive.mount('/content/drive')

# Set up Chrome options for headless mode and run in google chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in (headless mode) background without GUI
options.add_argument('--no-sandbox')  # Required for Colab
#options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

# Create the driver object to chrome
driver = webdriver.Chrome(options=options)

#to get the web site URL to
url = input("Enter the URL: ")

# Open the website
driver.get(url)

# Print the title of the webpage to verify obtained the link correctly
print(driver.title)
#https://builtin.com/artificial-intelligence

"""returned the topic correcly url linked correcly"""

# Extracting if topic is in the paragraph tags
paragraphs = driver.find_elements(By.TAG_NAME, 'p')

# Extract and print the text from each paragraph
extracted_paragraphs = [paragraph.text for paragraph in paragraphs]
print("Extracted Paragraphs:")
for paragraph in extracted_paragraphs:
    print(paragraph)


# Find all <a> tags (links)
links = driver.find_elements(By.TAG_NAME, 'a')
extracted_links = [link.get_attribute('href') for link in links if link.get_attribute('href')]
print("Extracted Links:")
for link in extracted_links:
    print(link)

# Extract the URLs (href) from each link


driver.quit()
# Organize the extracted data into a dictionary for JSON storage
data = {
    "paragraphs": extracted_paragraphs,
    "links": extracted_links
}
drive_file_path = '/content/drive/My Drive/Colab Notebooks//web_data/web_data.json'

# Save the extracted data to a JSON file
with open(drive_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"Data saved successfully to: {drive_file_path}")

from transformers import pipeline

# Step 2: Load the JSON data
json_file_path = '/content/drive/My Drive/Colab Notebooks/web_data/web_data.json'
with open(json_file_path, 'r') as f:
    data = json.load(f)



paragraphs = data.get('paragraphs', [])
links = data.get('links', [])

documents = paragraphs

# Step 3: Process the data (Assuming your JSON structure has a 'paragraphs' key)
#documents = [entry['paragraph'] for entry in data]  # Adjust based on your JSON structure

# Step 4: Use a Language Model
qa_pipeline = pipeline("question-answering")

# Example question
question = "what are the topics covers in site?"

# Step 5: Get answers from the documents
for document in documents:
    result = qa_pipeline(question=question, context=document)
    print(f"Answer: {result['answer']} (Score: {result['score']})")

