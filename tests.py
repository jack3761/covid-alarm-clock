import web_server
import weather_update
import news_filter
import covid_update

key_words = ['covid']

def test_covid_update():
    assert type(covid_update.get_covid_data()) is dict, "it's not a dictionary"

def test_news_filter():
    assert type(news_filter.get_news()) is list, "it's not a list"
    
def test_weather_update():
    assert len(weather_update.get_weather()) == 3, "there is missing information"
    
def test_process_alarm():
    alarm_details = {'alarm_time' : '10:34', 'alarm_weather' : True, 'alarm_news' : False}
    covid = web_server.get_covid_data()
    #a text-to-speech announcement should also be playing
    assert web_server.process_alarm(alarm_details) == covid + "." + " Weather update: " + weather_update.get_weather() + ".", 'This was the wrong announcement'
    
