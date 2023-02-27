print('STEP 1: TEXT EXTRACTION')

"""
Importing the necessary information including title and text of the given articles URL ID
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd

# Load the input file
df = pd.read_excel('Input.xlsx')

# Define the directory where the extracted text files will be stored
directory = 'extracted_text'

# Create the directory if it does not exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Loop through each row in the dataframe
for index, row in df.iterrows():
    try:
        # Get the URL and URL_ID for the current row
        url = row['URL']
        url_id = row['URL_ID']

        # Send a request to the URL and get the HTML response
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title and text
        title = soup.find('title').text
        text = ' '.join(map(lambda p: p.text, soup.find_all('p')))

        # Remove any unwanted characters from the title and text
        title = re.sub(r'[^\x00-\x7F]+', ' ', title)
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)

        # Concatenate the title and text
        content = title + '\n' + text

        # Write the extracted text to a file
        with open(f'{directory}/{url_id}.txt', 'w', encoding='utf-8') as f:
            f.write(content)
    except:
        # If there is any error, print a message
        print(f'Error extracting text from URL_ID: {url_id}')

    print("URL", index + 1, "Scanned")

print('Text extraction completed!')


print('STEP 2: CHECKING IMPORTED FILES')

"""
To know if the files are imported properly and check the names
"""

import os

folder_path = path = r"C:\Users\Gaurav\Data Science - Analysis\BlackCoffr Internship\extracted_text"

files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

files.sort(key=lambda x: int(x.split('.')[0]))

print(files)

print('STEP 3: STOPWORDS LISTING')

"""
List of all the stopwords mentioned in the mutliple text files converted into one list named stopwords
"""

import os

# Define the path to the stopwords folder
stopwords_folder_path = "StopWords/"

# Get a list of all the stopword files in the folder
stopword_files = [file for file in os.listdir(stopwords_folder_path) if file.endswith(".txt")]

# Initialize an empty list to store the stopwords
stopwords = []

# Loop through each stopword file
for stopword_file in stopword_files:
    # Open the stopword file
    with open(os.path.join(stopwords_folder_path, stopword_file), 'r') as f:
        # Read the contents of the file
        contents = f.read()

        # Split the contents into words
        words = contents.split()

        # Add the words to the stopwords list
        stopwords.extend(words)

# Remove duplicates from the stopwords list
stopwords_list = list(set(stopwords))

print(stopwords_list)

print('STEP 4: CREATING MASTER DICTIONARY - POSITIVE TEXT AND NEGATIVE TEXT')

"""
Master Dictionary with keys as positive and negative and the respective words that were mentioned in the text file
"""

# Define the positive and negative words lists
positive_words = []
negative_words = []

with open("MasterDictionary/positive-words.txt", "r") as file:
    positive_words = [word.strip() for word in file.readlines() if word.strip().lower() not in stopwords_list]

with open("MasterDictionary/negative-words.txt", "r") as file:
    negative_words = [word.strip() for word in file.readlines() if word.strip().lower() not in stopwords_list]

# Define the master dictionary
master_dict = {"positive": positive_words, "negative": negative_words}

print(master_dict)


print("DATA ANALYSIS STEP")

"""
Extraction done and now doing data analysis in the below cell from textblob import TextBlob
"""

from textblob import TextBlob
import os
import pandas as pd
import textstat
import nltk
from nltk.tokenize import word

# Location of the text files
folder_path = 'extracted_text'

# List of all text files in the folder
file_list = os.listdir(folder_path)

# Create an empty list to store the output data
output_data = []

# Loop through each text file in the file_list
for file_name in file_list:
    print("Text File:", file_name, "Scanned")

    # Read the contents of the text file
    with open(os.path.join(folder_path, file_name), 'r') as file:
        text = file.read()

    # Check if the text is not None or empty
    if text is not None and text.strip() != '':

        # Removing pre-defined stopwords
        words = text.split()
        words = [word for word in words if word.lower() not in stopwords_list]
        text = ' '.join(words)

        # Tokenize the text
        tokens = word(text)

        # Remove the stop words from the tokens
        tokens = [word for word in tokens if word.lower() not in stopwords_list]

        # Calculate the positive score
        positive_score = 0
        for word in tokens:
            if word.lower() in master_dict["positive"]:
                positive_score += 1

        # Calculate the negative score
        negative_score = 0
        for word in tokens:
            if word.lower() in master_dict["negative"]:
                negative_score += 1

        # Calculate the polarity score
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

        # Calculate the subjectivity score
        subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)

        # Create a TextBlob object with the article text
        text_blob = TextBlob(text)

        # Compute the sentiment scores
        # positive_score = text_blob.sentiment.polarity
        # negative_score = 1 - positive_score
        # polarity_score = text_blob.sentiment.polarity
        # subjectivity_score = text_blob.sentiment.subjectivity

        # Compute the average sentence length
        avg_sentence_length = sum(len(sentence.words) for sentence in text_blob.sentences) / len(text_blob.sentences)

        # Compute the percentage of complex words
        complex_word_count = len([word for word in text_blob.words if len(word) >= 5])
        percentage_of_complex_words = complex_word_count / len(text_blob.words)

        # Compute the FOG index
        fog_index = 0.4 * (avg_sentence_length + percentage_of_complex_words)

        # Compute the average number of words per sentence
        avg_number_of_words_per_sentence = len(text_blob.words) / len(text_blob.sentences)

        # Compute the word count
        word_count = len(text_blob.words)

        # Compute the syllables per word
        syllables_per_word = sum(textstat.syllable_count(word) for word in text_blob.words) / len(text_blob.words)

        # Compute the personal pronouns count
        personal_pronouns = len(
            [word for word in text_blob.words if word.lower() in ['i', 'me', 'my', 'mine', 'myself']])

        # Compute the average word length
        avg_word_length = sum(len(word) for word in text_blob.words) / len(text_blob.words)

        # Append the computed data to the output data list
        output_data.append([positive_score, negative_score, polarity_score, subjectivity_score,
                            avg_sentence_length, percentage_of_complex_words, fog_index,
                            avg_number_of_words_per_sentence,
                            complex_word_count, word_count, syllables_per_word, personal_pronouns, avg_word_length])

output_df = pd.DataFrame(output_data, columns=['POSITIVE_SCORE', 'NEGATIVE_SCORE', 'POLARITY_SCORE', 'SUBJECTIVITY_SCORE', 'AVG_SENTENCE_LENGTH', 'PERCENTAGE_OF_COMPLEX_WORDS', 'FOG_INDEX', 'AVG_NUMBER_OF_WORDS_PER_SENTENCE', 'COMPLEX_WORD_COUNT', 'WORD_COUNT', 'SYLLABLE_PER_WORD', 'PERSONAL_PRONOUNS', 'AVG_WORD_LENGTH'])
output_df.head()


print("CONCATENATING THE TWO DATAFRAMES TO GET THE FINAL RESULTING DATAFRAME")
"""
Now joining the df and output_df with each other to have the same format as of output_data_structure
"""

df = pd.read_excel('Input.xlsx')

output_ds = pd.concat([df, output_df], axis=1)
output_ds.head()


print("SAVING THE OUTPUT AS 'Output Data Structure'")
"""
Saving the excel file locally as "Output Data Structure"
"""

output_ds.to_excel("Output Data Structure.xlsx", index=False)
