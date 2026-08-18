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

In my project, qr code generator i understand how python module qr code easily generates qr code for us we just need one varible lets say data for the content to qr code and how we change the color to green by creating an instance of qr class and fillcolor=green and backcolor=white
