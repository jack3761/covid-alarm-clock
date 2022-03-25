import pyttsx3
import sched
import time
import covid_update
import news_filter
import weather_update
import time_conversions
import json
import requests
import logging
from flask import Flask, request, render_template

app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
alarms = []
alarm_notifications = []
notifications = [] 

@app.route('/')
@app.route('/index')
def index():
    """Main host of the HTML page that calls the other functions to interact with user inputs"""
    #check if the user has set an alarm and schedule it if so
    schedule_event()
    #check if the user has removed an alarm and delete it if so
    delete_alarm()
    #check if the user has deleted a notification and delete it if so
    delete_notifications()
    
    with open('config.json', 'r') as f:
        x = json.load(f)["misc"]
        alarm_image = x["image"]
    logging.info('html opened')
    #form the HTMl page
    return render_template('alarm.html', title='Daily update', image = alarm_image, notifications=notifications, alarms = alarm_notifications)

def delete_alarm() ->None:
    """Deletes alarm based on the 'alarm_item' variable found in the URL input"""
    alarm_to_delete = request.args.get("alarm_item")
    #check if the alarm has the same name as the one to be deleted
    for alarm in alarm_notifications:
        if alarm['title'] == alarm_to_delete:
            #remove the alarm from the alarm notifications and the alarm list
            alarm_notifications.remove(alarm)
            alarms.remove(alarm)
    if alarm_to_delete:
        logging.info('Event: ' + alarm_to_delete + " alarm cancelled")
            
def delete_notifications() ->None:
    """Deletes notification based on the 'notif' variable found in the URL input"""
    notif_to_delete = request.args.get("notif")
    #check if the notification has the same name as the one to be deleted
    for notif in notifications:
        if notif['title'] == notif_to_delete:
            #remove the notification from the list
            notifications.remove(notif)
            try:
                #add a news article to the notifications to replace the missing one
                notifications.append({'title' : 'News', 'content' : news.pop(0)})
            except IndexError:
                #when the list of news articles have run out return an error to the log file
                logging.error('IndexError when trying to append to notifications')
    if notif_to_delete:
        logging.info('Event: ' + notif_to_delete + " notification dismissed")
          
@app.route('/index_test')
def index_test():
    """Test function to demonstrate the display of the html template"""
    notifications = filter_notifications()
    logging.info('index test run')
    return render_template('alarm.html', title='Daily update', notifications=notifications,  alarms = alarm_notifications)

@app.route('/tts_request') 
def tts_request(announcement="Text to speech example announcement!") ->str:
    """Test function to check that the text to speech is working appropriately"""
    engine = pyttsx3.init()
    engine.say(announcement)
    engine.runAndWait()
    logging.info('tts test run')
    return "Hello text-to-speech example"

def schedule_event() ->None:
    """Use the inputs from the html to set an alarm"""
    s.run(blocking=False)
    #set up the alarm_details dictionary with all of the inputs from the html
    alarm_details = {}
    alarm_details['alarm_time'] = request.args.get("alarm")    
    alarm_details['alarm_label'] = request.args.get("two")    
    if request.args.get("news") == "news":
        alarm_details['alarm_news'] = True
    else:
        alarm_details['alarm_news'] = False    
    if request.args.get("weather") == "weather":
        alarm_details['alarm_weather'] = True
    else:
        alarm_details['alarm_weather'] = False        
    
    if alarm_details['alarm_time']:
        current_date = get_current_date()
        current_time = get_current_time()
        alarm_details['alarm_date'] = alarm_details['alarm_time'][0:10]
        alarm_details['alarm_time'] = alarm_details['alarm_time'][11:]
        
        #add the alarm to the alarm list and alarm notifications
        alarms.append(alarm_details)
        create_alarm_notification(alarm_details)
        logging.info('Event: Alarm added to list')
        
        #if it's the same date then schedule the alarm
        if alarm_details['alarm_date'] == current_date:
            delay = time_conversions.hhmm_to_seconds(alarm_details['alarm_time']) - time_conversions.hhmm_to_seconds(current_time) 
            s.enter(int(delay), 1, process_alarm, (alarm_details,))
            logging.info('Event: Alarm scheduled')
    

def process_alarm(alarm_details:dict) ->str:
    """Forms and reads out the announcement to be made when the alarm is scheduled"""
    
    #read out the alarm time
    announcement = alarm_details['alarm_time'] + " announcement"
    engine = pyttsx3.init()
    engine.say(announcement)
    engine.runAndWait()
    
    covid_data = get_covid_data()
    
    #form the informational announcement dependant on users input on weather and news
    announcement = covid_data + "."
    
    if alarm_details['alarm_weather']:
        announcement = announcement + " Weather update: " + get_weather_update() + "."
    
    if alarm_details['alarm_news']:
        announcement = announcement + " News update: " + get_news_update().pop(0)
        
    engine.say(announcement)
    engine.runAndWait()
    alarms.remove(alarm_details)
    alarm_notifications.remove(alarm_details['alarm_label'])
    logging.info(alarm_details['alarm_time'] + " alarm announced")    
    return announcement
        
def get_current_time() ->str:
    """Forms a string to represent the current time using the time module"""
    current_time = str(time.gmtime()[3]) + ':' + str(time.gmtime()[4])
    return current_time
    
def get_current_date() ->str:
    """Forms a string to represent the current date using the time module"""
    if len(str(time.gmtime()[2])) == 1:
        current_date = str(time.gmtime()[0]) + '-' + str(time.gmtime()[1]) + '-0' + str(time.gmtime()[2])
    else:
        current_date = str(time.gmtime()[0]) + '-' + str(time.gmtime()[1]) + '-' + str(time.gmtime()[2])
    return current_date

def get_weather_update() ->str:
    """Collects weather data from the weather API in the weather_update module"""
    weather_data = weather_update.get_weather()
    weather = "It is " + str(weather_data[0]) + " degrees with " + str(weather_data[1]) + " in " + str(weather_data[2])
    logging.info('Weather information updated')
    return weather

def get_covid_data() ->str:
    """Collects covid data from the covid API in the covid_update module"""
    covid_data = covid_update.get_covid_data()
    for day in covid_data['data']:
        if day['cases']['daily']:
            daily_cases = str(day['cases']['daily'])
            total_cases = str(day['cases']['cumulative'])
            cases_date = day['date']
            break
        else:
            pass
    for day in covid_data['data']:        
        if day['deaths']['daily']:
            daily_deaths = str(day['deaths']['daily'])
            total_deaths = str(day['deaths']['cumulative'])
            deaths_date = day['date']
            break
        else:
            pass
    
    message = 'As of ' + cases_date + ' there have been ' + daily_cases + ' daily cases and ' + total_cases + " total cases. As of " + deaths_date + ' there have been ' + daily_deaths + ' daily deaths and ' + total_deaths + " total deaths"
    logging.info('Covid data updated')
    return message

def get_news_update() ->list:
    """Collects the news articles from the API in the news_filter module"""
    news_titles = news_filter.get_news()
    logging.info('News articles updated')
    return news_titles
    
def filter_notifications(include_covid:bool, include_weather:bool, news_articles:int) ->None:
    """Forms the automatic notifications based off of the three data sources"""
    #find the time in seconds the notifications should be refreshed automatically
    with open('config.json', 'r') as f:
        x = json.load(f)["misc"]
        refresh_time = x["refresh_time"]
    #call the function again in the given time
    s.enter(refresh_time, 1, filter_notifications,(True, True, 2))
    notifications.clear()
    covid_data = get_covid_data()
    global news
    news = get_news_update()
    weather = get_weather_update()
    #add the relevent information to the notifications list
    if include_covid:
        notifications.append({'title' : 'Covid update', 'content' : covid_data})
    if include_weather:
        notifications.append({'title' : 'Weather', 'content' : weather})
    for i in range(news_articles):
        notifications.append({'title' : 'News', 'content' : news.pop(i - 1)})
    logging.info('Event: Notifications filtered')


def schedule_daily_alarms() ->int:
    """At midnight each day schedule the alarms for the following day"""
    delay = time_conversions.hhmm_to_seconds("24:00")
    s.enter(int(delay), 1, schedule_daily_alarms,())
    current_date = get_current_date()
    #schedule all alarms that have the same date as this day
    for alarm in alarms:
        if alarm['alarm_date'] == current_date:
            delay = time_conversions.hhmm_to_seconds(alarm['alarm_time']) - time_conversions.hhmm_to_seconds(current_time) 
            s.enter(int(delay), 1, process_alarm, (alarm,))
    logging.info('Event: Daily alarms scheduled')
    
def delay_to_midnight():
    """Calculates the delay between the current time and midnight"""
    current_time = get_current_time()
    delay = time_conversions.hhmm_to_seconds("24:00") - time_conversions.hhmm_to_seconds(current_time)
    return delay
    
def create_alarm_notification(alarm_details:dict) ->None:
    """Creates the visuals for the alarms on the HTML template"""
    news = alarm_details["alarm_news"]
    weather = alarm_details["alarm_weather"]
    date = alarm_details["alarm_date"]
    alarm_title = alarm_details["alarm_label"]
    alarm_content = str(alarm_details["alarm_time"]) + " alarm"
    #show the relevent information about the alarm based on user inputs
    if news == True and weather == True:
        alarm_content = alarm_content + " with news and weather update"
    elif news == True and weather == False:
        alarm_content = alarm_content + " with news update"
    elif news == False and weather == True:
        alarm_content = alarm_content + " with weather update"
    
    alarm_content = alarm_content + " on " + date
    
    alarm_notifications.append({'title' : alarm_title, 'content' : alarm_content})
    
if __name__ == '__main__':
    s.enter(delay_to_midnight(), schedule_daily_alarms,())
    filter_notifications(True, True, 2)
    logging.basicConfig(filename='sys.log', encoding='utf-8', level=logging.DEBUG)
    app.run()