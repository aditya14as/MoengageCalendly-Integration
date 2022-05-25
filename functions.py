import datetime
import pytz

#Functions for setting date and time
def setTime(timezone,event_start_time):
    # Converting event start time to different timezones
        if timezone == "Asia/Calcutta":
            revised_timezone = "Asia/Kolkata"

        else :
            revised_timezone = timezone
                
        event_start_time_timestamp = datetime.datetime.strptime(event_start_time,'%Y-%m-%dT%H:%M:%S.%fZ')

        utc_event_start_time = datetime.datetime.strptime(event_start_time,'%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y:%m:%d %H:%M:%S")


        local_event_start_time = event_start_time_timestamp.astimezone(pytz.timezone(revised_timezone)).strftime("%Y:%m:%d %H:%M:%S")

        print("PST time setting")

        pst_event_start_time = event_start_time_timestamp.astimezone(pytz.timezone('US/Pacific')).strftime("%Y:%m:%d %H:%M:%S")

        print("IST time setting")

        ist_event_start_time = event_start_time_timestamp.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%Y:%m:%d %H:%M:%S")

        time_attributes = {
            "utc_event_start_time" : utc_event_start_time,
            "local_event_start_time" : local_event_start_time,
            "pst_event_start_time" : pst_event_start_time,
            "ist_event_start_time" : ist_event_start_time
        }

        return time_attributes

#Function for fetching all the questions and answers
def questionsAnswers(event_decoded):
        l = len(event_decoded["payload"]["questions_and_answers"])
        questions = [event_decoded["payload"]["questions_and_answers"][i]["question"] for i in range(l)]
        answers = [event_decoded["payload"]["questions_and_answers"][i]["answer"] for i in range(l)]
        quesAns_Attributes = {
            "questions" : questions,
            "answers" : answers
        }
        return quesAns_Attributes