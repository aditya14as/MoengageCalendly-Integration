#User will create and object of class CalendlyMoe by providing all the required key
#and call a method createdOperations() to perform all the operations

from wrapperClass import CalendlyMoe
import os

moe_app_key = os.environ.get('MoeAppKeyLive')
moe_auth_live = os.environ.get('MoeAuthLive')
calendly_auth = os.environ.get('CalendlyAuth')

#event fetched by the webhook url in json formate

#Below are the example of event, I have leave many field blank also event can of of either invitee.created or invitee.canceled
#If headers and url of event is common then we can also initialise this part in class so that user don't have to worry about
event = {
    "event": "invitee.created"
}
#Argumets should be in this orientations -> CalendlyMoe(Moengage_app_key, Moengage_auth_live, Calendly_auth)
user1 = CalendlyMoe(moe_app_key,moe_auth_live,calendly_auth)

#calling method to create all the operations
user1.createOperations()