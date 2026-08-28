Here i will update my readme as a key lesson i learned for building every project. This repo is all about learning python through projects which help me to understand how things work.

CSV to JSON Converter

Key point I learned: 
DictReader reads the CSV file line by line and is an iterator. 
Therefore, if we want to store all the rows and access them later, we need to convert it into a list.

JSON to CSV Converter

JSON is not structured as rows and columns like CSV. Therefore, when converting JSON to CSV, we first need to create the header.
Since our JSON contains a list of dictionaries we can extract the keys from the dictionary at index 0 using data[0].keys(). 
These keys become the column headers in the CSV.

we use writeheader() to write the header 
writerows() to write all the data rows into the CSV file.

qr code generator

In my project, qr code generator i understand how python module qr code easily generates qr code for us we just need one varible lets say data for the content to qr code and how we change the color to green by creating an instance of qr class and fillcolor=green and backcolor=white

PDF text to audio:

In this project I understand the module pyttsx , it is an offline text to speech data that allows our programs to speak text out loud or save spoken audio to files. Pypdf2 is also used, it is used to manipulate pdf files here we will read the pdf. 
PDF file reader will help me to read pdf
numpages will help me to read out any pages from the book
Its so interesting that people have created so many modules for smooth software development. 

In study time analyser project first, I created
manifest.json — tells Chrome that this folder is an extension and defines its name, version, permissions, and background script.
background.js — runs in the background and will later detect browser activity.
The extension acts as a bridge between Chrome and Python, because Python cannot directly access Chrome's active tabs.

Step 2: we need to detect an active browser tab
V1:  We fetched from chrome.tabs.query and defined a function that gives the tab that is currently active in the current browser window.

chrome.tabs.query() gets information about the active tab.
tabs[0].title gives the page title.
tabs[0].url gives the page URL. 

Step 3 : We need to detect the tab changes

User changes tab ==> chrome provides an event chrome.tabs.onActivated that Tells when the user switches to another tab.
       |||
Chrome detects the change
       |||
Our code runs
       |||
Fetch new tab
       |||
Print title + URL

Step 4: Track Time Spent on Each Tab - we used datetime function 
step 5 : in step 5 we connect datetime function with chrome browser
step 6: Create Activity Records
step 7: connect with python







