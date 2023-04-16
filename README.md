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

     - First nested list item 👍
     - Cardholder Designation 👍
     - Email 👍
     - website link 👍
     - Address 👍
3.create a **webpage** to display the extracted data using **streamlit**.

4.Have the dropdowns so that the users can view the card details.

5.Show the extracted details in the **TABLE** format using **pandas**
```
data_list=[[company_name,name2,designation,email,website2,numbers2,address,pincode]] 
df=pd.DataFrame(data_list,columns=["Company Name","Cardholder Name","Designation",'Email',"Website","Contact Number","Address",'Pincode'])
st.dataframe(df)
```
6.### Inserting the card details in **mySQL** database:
```
data = (company_name,name2,designation,email,website2,numbers2,address,pincode,image_data)
                    sql = "insert into image_details(company_name, name, designation, email, website, contact_number, address, pincode,image) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
 cursor.execute(sql, data)
 connector.commit()
 
 ```
