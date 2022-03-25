
# Smart Alarm Clock project

## Introduction

This project contains python modules used to run a web server that allows a user to read personalised notifications and set alarms with text to speech covid, news and weather updates.

## Prerequisites

The main module used in this project is web_server.py which imports modules covid_update.py, news_filter.py, time_conversions.py and weather_update.py which are all included in the file. API keys are required for the news_filter and weather_update modules which can be added in the config file. 

## Installation

Modules pyttsx3, sched, time, json, requests and flask are all required to run the code. All of these can be installed with a pip install, eg: pip install pyttsx3
Additionally, the covid_update module requires the install of the module uk_covid19 with a pip install. The manual for this module can be found here https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/

## Getting Started

Additions to the config.json must be made before running the code. The config file is seperated into three dictionaries; news, weather and misc. Both the news and weather dictionaries require an API key to run. The news key can be found for free at https://newsapi.org/ and the weather one at openweathermap.org. The news dictionary in config.json has an optional key "news_key_words" that is an empty list. If you wish, you can add key words as strings to this list and the news_filter module will filter out articles that don't contain these key words. In the weather dictionary there is a "weather_city" key which requires a string input for the name of a city in the UK to collect weather information from. The last two keys are found in the misc dictionary. "image" refers to the file name of an image found in the static folder. If you wish to change the image used, move an image into the static folder and change the value of this key to the name of the image file. "refresh_time" refers to the amount of seconds taken to refresh the notifications automatically. It is currently set to 1800 seconds which is 30 minutes but can be changed to whatever is preferred.

With the config.json set up, the code should run. Once the server is up, it can be reached at the local address 127.0.0.1:5000/ where the HTML template should show up with an alarm column, notifications column and the option to set alarms in the centre. Notifications should already appear and when closed should be replaced with a new one and alarms should show up on the left column if they are set for this day. They are set with a label and the option for news updates, weather updates or both. When the time of the alarm is reached, a text to speech announcement is made with the requested information. Alarms can be cancelled with the x in the corner of their box on the page.

## Testing

In the program there are functions to test different features; tts_request and index_test which can be called by adding their function names to the  URL with a / . These should demonstrate these features. There are additional tests in the tests.py module that check to ensure that suitable data is being received from the external modules. There is also a test for the process_alarm function to ensure that it creates a suitable announcement and that the text to speech works in this setting.

## Developer Documentation

When the program is loaded, it schedules the function to set alarms for the day by calculating the delay until midnight so that it can set that days alarms when the time comes. This function then sets another schedule for itself in a days time. The first notifications are also set up as well as a log file. A few global variables are set up also. The app variable is set up for Flask in order to maintain the web server as well as the schedular that is used throughout the program for functions mentioned previously as well as to set alarms. The alarms, alarm_notifications and regular notifications are also set up as global variables as lists as it's required for these to be frequently accessed by different functions throughout the running of the program. 

#### Index

Once the web page is loaded up with the address the index function is run, which uses the alarm.html template to run the page and display the alarms and notifications. This is then responding to user inputs such as setting alarms or deleting alarms and notifications. When this happens, the appropriate function is called.

#### Schedule_event

Schedule event is responding to inputs for setting up alarms. This is checking the different inputs on the html and storing their values in a dictionary. This dictionary is then added to the alarm list and alarm_notification list. If the alarm is for the current date, the alarm is scheduled then by calculating its delay, and when it's time calling the process_alarm function.

#### process_alarm

The process_alarm function takes in the information from the dictionary and forms a string so that it can be read out using the text to speech. This always starts with an update on covid cases following weather and news, dependent on whether the user selected that when setting the alarm.

#### 'get' functions

In the module there are many functions that get data required in multiple use cases. The get_current_time and get_current_date functions use the time module to form a string representing the current time and date to be used as a comparison to alarms later. There are also functions to gather data from the covid, weather and news modules that use the corresponding API's and store the data in a useful way to be interacted with throughout the program. These are predominantly used within the filter_notifications function.

#### filter_notifications

The filter_notifications function is used to collect the data from the different API's and load them into the notifications to be displayed. It also schedules itself to be called after the refresh time determined in the config file has been reached, providing updated data to the notifications.

#### 'delete' functions

The delete functions are called in the index and use the inputs from the URL to determine which alarm or notification is to be removed. For the alarm, it checks against the alarms in both the alarm and alarm_notification lists and if they are the same one as the input, they are removed from both. The delete notifications function is similar except when the notification is deleted, it is replaced with a news update until the list is empty. These are then refreshed using the filter_notifications function once the refresh time is reached.

## Details

Author - Jack Purkiss

