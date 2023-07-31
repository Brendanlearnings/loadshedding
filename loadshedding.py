import requests
import json 
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import datetime


if 'user' not in st.session_state:
    st.session_state.user = random_id_gen()
    now = datetime.now()
    st.session_state.timestamp = now.strftime('%Y-%m-%d %H:%M:%S.%f %z')

# Get token from json object 
with open('keys.json','r') as file:
    reader = json.load(file)
    token = reader['key']

def json_file_handler(mode:bool, file_name:str == None, data:str):
    '''This function reads and writes file according to the mode specified'''
    if mode == 0:
        with open(f'data/{file_name}.json','r') as read_file:
            reader = json.load(read_file)
            return reader 
    if mode == 1:
        with open(f'data/{file_name}.json','w') as write_file:
            writer = write_file.write(data)
            return f'Data written out to data/{file_name}' 

def status():
    '''This function gets me the current loadshedding stage/status'''
    url = "https://developer.sepush.co.za/business/2.0/status"
    payload = ""
    headers = {"token": f"{token}"}
    response = requests.request("GET", url, data=payload, headers=headers)
    status_obj = response.text
    json_file_handler(1,'current_stage',status_obj)


def area_search_text(text):
    url = f'https://developer.sepush.co.za/business/2.0/areas_search?text={text}'
    payload = ""
    headers = {"token": f"{token}"}
    response = requests.request("GET", url, data=payload, headers=headers)
    status_obj = response.text
    return json.dumps(status_obj)

def main():
    st.title('Loadshedding application to check current schedule for a location')
    st.text_input('Please enter your area:')

    



# Set up the directory for pages in app
pages = {
    "Information": details,
    "Contact details": contact_deets,
    "Merchandise": merch,
    "Events": events,
    "Additional": choices,
    "Checkout": checkout
}


# Create a menu with the page names
selection = st.sidebar.radio("Navigate to:", list(pages.keys()))

# Display the selected page with its corresponding function
pages[selection]()