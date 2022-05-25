#This is wrapperClass built on the top of api calls to make it user independent
#Can be used by many user

import json
import requests

from functions import questionsAnswers, setTime

class CalendlyMoe:
    def __init__(self,moe_app_key,moe_auth_live,calendly_auth,event):
        event_decoded = json.loads(event['body'])
        self.moe_app_key = moe_app_key
        self.moe_auth_live = moe_auth_live
        self.calendly_auth = calendly_auth
        self.event_decoded = event_decoded
        self.moe_headers = {
            "Authorization": "Basic"+" "+moe_auth_live,
            "Content-Type": "application/json",
            "MOE-APPKEY": moe_app_key
            }
        self.cal_headers = {
            "Authorization": "Bearer"+" "+calendly_auth ,
            "Content-Type": "application/json"
            }

        self.test_moe_user_api_endpoint = "https://api-02.moengage.com/v1/customer/"+moe_app_key

        self.test_moe_event_api_endpoint = "https://api-02.moengage.com/v1/event/"+moe_app_key

    #I have make invitee.created and invitee.canceled common because everthing is same apart from event
    def createOperations(self):
        event = self.event_decoded["event"]
        cancel_url = self.event_decoded["payload"]["cancel_url"]
        event_url = self.event_decoded["payload"]["event"]
        event_created_at = self.event_decoded["payload"]["created_at"]
        invitee_email = self.event_decoded["payload"]["email"]
        invitee_name = self.event_decoded["payload"]["name"]
        invitee_first_name = self.event_decoded["payload"]["first_name"]
        invitee_last_name = self.event_decoded["payload"]["last_name"]
        mobile = self.event_decoded["payload"]["text_reminder_number"]
        reschedule_url = self.event_decoded["payload"]["reschedule_url"]
        reschedule_status = self.event_decoded["payload"]["rescheduled"]
        status = self.event_decoded["payload"]["status"]
        uri = self.event_decoded["payload"]["uri"]
        timezone = self.event_decoded["payload"]["timezone"]
        tracking_utm_campaign = self.self.event_decoded["payload"]["tracking"]["utm_campaign"]
        tracking_utm_source = self.event_decoded["payload"]["tracking"]["utm_source"]
        tracking_utm_medium = self.event_decoded["payload"]["tracking"]["utm_medium"]
        tracking_utm_content = self.event_decoded["payload"]["tracking"]["utm_content"]
        tracking_utm_term = self.event_decoded["payload"]["tracking"]["utm_term"]
        tracking_salesforce_uuid = self.event_decoded["payload"]["tracking"]["salesforce_uuid"]

        # breaking invitee_name into first_name and last_name
        first_name = invitee_name.split(' ', 1)[0]
        last_name = invitee_name.split(' ', 1)[-1]


        # Getting all the questions and answers in attributes by calling a function questionsAnswers from functions.py file
        quesAns_Attributes = questionsAnswers(self.event_decoded)

        

        
        
        # calling MoEngage User API for user creation/update        
        print("Making Request Body")
        request_body = {
            "type" : "customer",
            "customer_id": invitee_email,
            "attributes": {
                "first_name": first_name,
                "last_name": last_name,
                "name": invitee_name,
                "email": invitee_email,
                "mobile": mobile,
                }
            }
        
        req = json.dumps(request_body)

        print("Calling MoE User API")
        
        r = requests.post(url=self.test_moe_user_api_endpoint, data=req, headers=self.moe_headers)
        
        print(r.text)
        
        # Pushing invitee.create /invitee.canceled event 
        
        print("Get request for event information")
        
        event_info = requests.get(event_url, headers = self.cal_headers)
        
        if event_info.status_code == 200:
            
            event_info_text = json.loads(event_info.text)
            event_name = event_info_text["resource"]["name"]
            event_start_time = event_info_text["resource"]["start_time"]
            total_invitees = event_info_text["resource"]["invitees_counter"]["total"]
            event_guests = event_info_text["resource"]["event_guests"]
            user_uri = event_info_text["resource"]["event_memberships"][0]["user"]

            time_attributes = setTime(timezone,event_start_time)

            user_info = requests.get(user_uri, headers = self.cal_headers)
            
            user_info_text = json.loads(user_info.text)
            
            print("Making event response body")

            event_attributes = {
                                "event_name": event_name,
                                "cancel_url": cancel_url,
                                "event_url": event_url,
                                "event_created_at" : event_created_at,
                                "uri" : uri,
                                "status": status,
                                "reschedule_url": reschedule_url,
                                "reschedule_status": reschedule_status,
                                "timezone": timezone,
                                "local_event_start_time": time_attributes["local_event_start_time"],
                                "PST_event_start_time":time_attributes["pst_event_start_time"], 
                                "IST_event_start_time":time_attributes["ist_event_start_time"], 
                                "UTC_event_start_time": time_attributes["utc_event_start_time"],
                                "total_invitees": total_invitees,
                                "event_guests": event_guests,
                                "calendly_member_email": user_info_text["resource"]["email"],
                                "calendly_member_name": user_info_text["resource"]["name"],
                                "tracking_salesforce_uuid" : tracking_salesforce_uuid,
                                "utm_campaign": tracking_utm_campaign,
                                "utm_source": tracking_utm_source,
                                "utm_medium": tracking_utm_medium,
                                "utm_content": tracking_utm_content,
                                "utm_term": tracking_utm_term,
            }

            i = 0
            while i < len(quesAns_Attributes["questions"]):
                event_attributes[quesAns_Attributes["questions"][i]] = quesAns_Attributes["answers"][i]
                i +=1
            
            event_response = {
                    "type": "event",
                    "customer_id": invitee_email,
                    "actions": [{
                            "action": event,
                            "attributes": event_attributes
                        }
                    ]
                    }

            # Pushing the Event into MoEngage
            
            print("Pushing Event into MoE")
            
            event_response_json = json.dumps(event_response)
            eventpush = requests.post(url=self.test_moe_event_api_endpoint, data=event_response_json, headers=self.moe_headers)
            
            print(eventpush.status_code)

        else :
            print("Couldn't get the event information. The API error is " + event_info.text)
                
