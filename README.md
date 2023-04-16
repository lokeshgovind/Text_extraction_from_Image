# Text_extraction_from_Image
----
### ABOUT:
Extracting text from the Image using easyOCR and Creating a user-friendly webpage to display the extracted data using streamlit and python
***
----
#### why is this helpful?
Using this code we can extract the details of the digital card and helping the users to store the extracted data in a database 
****
#### Task:
`import necessary modules`
- [x] easyocr
- [x] sreamlit
- [x] pandas
- [x] re

### **How it works** ?
1.Extracting the text data from image using the  `reader.readtext` function of easyocr.

2.Getting the necessary informations from the card using **regular expression**:

     + Cardholder Name
     + Cardholder Designation
     * Email
     + website link
     + Address

