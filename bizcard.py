# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import streamlit as st
import easyocr as ocr
import pandas as pd
import mysql.connector
import numpy as np
from PIL import Image
import re
import io
import os

#connecting IDE with mySQL database
connector= mysql.connector.connect(
    host ='localhost',
    user ='root',
    password ='123456',
    database ="text_extraction"
    )
cursor=connector.cursor()
#Title and header to display in streamlit
st.set_page_config(page_title="BizCard",layout="wide")
st.title("Data Science Project")
st.header("Easyocr-:red[Text Extraction From Image]")
st.markdown("### using `esayOCR`, `streamlit`")

#Dividing the webpage into two columns
left_column,right_column=st.columns(2)

with left_column:
    #users to upload image
    image=st.file_uploader("upload image",type=['jpg','png','jpeg'])
    if image is not None:
        upload_image=Image.open(image)
        def save_card(uploaded_file):
         filename = os.path.join("uploaded_files", uploaded_file.name)
         if not os.path.exists("uploaded_files"):
           os.makedirs("uploaded_files")
         with open(filename, "wb") as f:
           f.write(uploaded_file.getbuffer())
        save_card(image)
        
        #using easyOCR to extract text from Image
        @st.cache_resource
        def load_model():
            reader=ocr.Reader(['en'])
            return reader
        reader=load_model()
        result=reader.readtext(np.array(upload_image),paragraph=False)
        text=[]
        for i in result:
            text.append(i[1])
        data="".join(text)
        dup_data="".join(text)
        #To get email from the string of words using regular expression
        email=''
        for i in text:
            if re.search("[a-z]+[0-9]*@[a-zA-Z0-9]+.com", i):
                email+=i
                dup_data=dup_data.replace(email," ")
            else:
                continue
            
       #To get pincode     
        pincode=re.findall("\d{6,7}",dup_data)
        pincode=''.join(pincode)
        dup_data=dup_data.replace(pincode, ' ')
        
        #To get contact number/numbers
        numbers=re.findall(r"\+*\d{2,3}-\d{3,10}-\d{3,10}",dup_data)
        numbers2=''
        for i in numbers:
            numbers2+=i+" "
            dup_data=dup_data.replace(i, ' ')
         
        #To get website link
        website=re.findall(r"www\.*\s*[a-zA-Z0-9]+\.*com|WWW\.*\s*[a-zaA-Z0-9]+\.com|wwW\.*\s*[a-zA-Z0-9]+\.com", dup_data)
        website2=''
        for i in website:
            website2+=i
            dup_data=dup_data.replace(website2," ")
        
        #To extract street name
        street=re.findall(r'[0-9]{3}\s*[a-zA-Z0-9]+\s*',dup_data)
        street2=''
        for i in street:
            street2+=i
            dup_data=dup_data.replace(street2," ")
       
       #To get the state name which is default in this dataset
        state=re.findall(r"TamilNadu|tamilnadu|Tamilnadu",dup_data)
        state2="".join(state)
        dup_data=dup_data.replace(state2," ")
        
        
        stt=re.findall("St|st",dup_data)
        stt2=""
        for i in stt:
            stt2+=i
            dup_data=dup_data.replace(stt2," ")
        
        #Designation of the cardholder suitable only for this dataset
        desig_list = ['DATA MANAGER', 'CEO & FOUNDER','General Manager', 'Marketing Executive', 'Technical Manager']
        designation = ''
        for i in desig_list:
            if re.search(i, dup_data):
                designation += i
                dup_data = dup_data.replace(i, '')
                
        
        #Name of the cardholder
        split_data=dup_data.split(",")
        name=split_data[0]
        name2=''
        for n in name:
            name2+=n
        dup_data=dup_data.replace(name2," ")
        
        #To get company name
        company_list=['selva','GLOBAL', 'BORCELLEAIRLINES', 'Family Restaurant', 'Sun Electricals']
        company_name=''
        for name in company_list:
            if re.search(name,dup_data):
                if name=="selva":
                    i="selva digitals"
                    company_name+=i
                    dup_data=dup_data.replace(name," ")
                    dup_data=dup_data.replace(r"digitals"," ")
                elif name=="GLOBAL":
                    i="GLOBAL INSURANCE"
                    company_name+=i
                    dup_data=dup_data.replace(name," ")
                    dup_data=dup_data.replace(r"INSURANCE"," ")
                else:
                    company_name+=name
                    dup_data=dup_data.replace(company_name," ")
        final=''
        for let in dup_data:
            if let==',' or let==';' or let==':':
                continue
            else:
                final+=let      
        final=final.split()
        if len(final)>0:
            city=final[0]
            address=street2+" "+city+' '+state2    
        else:
            city="Erode"
            address=street2+' '+state2
            
        #options to be displayed in streamlit
        option=st.selectbox(label="**Card Details**",options=("Name","Designation",'email','website','contact number','company name',"street",'City','pincode',"state"))
        if option=='pincode':
            st.subheader(pincode)
        elif option=='contact number':
            st.subheader(numbers2)
        elif option=="email":
            st.subheader(email)
        elif option=='website':
            st.subheader(website2)
        elif option=='Designation':
            st.subheader(designation)
        elif option=="street":
            st.subheader(street2)
        elif option=="state":
            st.subheader(state2)
        elif option=='company name':
            st.subheader(company_name)
        elif option=="City":
            st.subheader(city)
        elif option=="Name":
            st.subheader(name2)
        saved_img = os.getcwd()+ "\\" + "uploaded_files"+ "\\"+ image.name
        #converting image to binary data
        def img_to_binary(file):
            # Convert image data to binary format
            with open(file, 'rb') as file:
                binaryData = file.read()
            return binaryData
        image_data =img_to_binary(saved_img)   
        st.write("##")
        
        #showing the extracted data in TABLE format
        if st.button("**Show Table**"):
            st.write("##")
            if len(final)>0:
                data_list=[[company_name,name2,designation,email,website2,numbers2,address,pincode]] 
                df=pd.DataFrame(data_list,columns=["Company Name","Cardholder Name","Designation",'Email',"Website","Contact Number","Address",'Pincode'])
                st.dataframe(df)
                
                #inserting the extracted data into mySQL
                if st.button("**Upload**") is not None:
                    data = (company_name,name2,designation,email,website2,numbers2,address,pincode,image_data)
                    sql = "insert into image_details(company_name, name, designation, email, website, contact_number, address, pincode,image) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
                    cursor.execute(sql, data)
                    connector.commit()
            else:
                data_list=[[company_name,name2,designation,email,website2,numbers2,address,pincode]] 
                df=pd.DataFrame(data_list,columns=["Company Name","Cardholder Name","Designation",'Email',"Website","Contact Number","Address",'Pincode'])
                st.dataframe(df)
                if st.button("**Upload**") is not None:
                    data = (company_name,name2,designation,email,website2,numbers2,address,pincode,image_data)
                    sql = "insert into image_details(company_name, name, designation, email, website, contact_number, address, pincode,image) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
                    cursor.execute(sql, data)
                    connector.commit()
                    
        #allowing the user to delete the uploaded data
        if st.button("**Delete Uploaded Data**") :
            cursor.execute("set sql_safe_updates=0")
            cursor.execute("delete from image_details where name='{}'".format(name2))
            connector.commit()
                    
#To show the image in streamlit app
if image is not None:
    with right_column:
        show_image=Image.open(image)
        st.image(show_image)
      
    