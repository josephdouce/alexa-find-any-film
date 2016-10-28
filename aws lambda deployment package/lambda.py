"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import requests
import datetime as dt
# change this from mykeys to keys
from mykeys import alexa_skill_id

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        #'reprompt': {
        #    'outputSpeech': {
        #        'type': 'PlainText',
        #        'text': reprompt_text
        #    }
        #},
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to films." \
                    "Please tell me the location of your desired cinema."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me the location of your desired cinema."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying find any film..." \
                    "Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_session_attributes(location, from_date):
    """ Sets the attributes in the session
    """

    return {
        "location": location,
        "date": from_date,
        }


#def get_location_id(location):


#def get_locaion_listings(venue_id, date):


#def amazon_yes_intent():


#def amazon_no_intent():


def whats_playing_intent(intent, session):
    """ Gets the values from the session and prepares the speech to reply to the
    user.
    """

    card_title = ""
    session_attributes = {}
    movies = []
    should_end_session = True

    if 'value' in intent['slots']['location']:
        location = intent['slots']['location']['value']
        if 'value' in intent['slots']['date']:
            from_date = intent['slots']['date']['value']
        else:
            from_date = dt.datetime.today().strftime("%Y-%m-%d")
        r_location = requests.get('http://moviesapi.herokuapp.com/cinemas/find/' + location).json()
        if r_location == []:
            venue_id = "10539"
        else:
            venue_id = r_location[0]['venue_id']
        r_movies = requests.get('http://findanyfilm.com/api/screenings/by_venue_id/venue_id/' + venue_id + "date_from/" + from_date).json()
        for movie_id in r_movies[venue_id]['films']:
            movies.append(r_movies[venue_id]['films'][movie_id]['film_data']['film_title'])
        create_session_attributes(location, from_date)
        card_title = r_movies[venue_id]['name']
        speech_output = "Films showing at " + r_movies[venue_id]['name'] + " on the " + from_date + " are..." + ', '.join(movies)
        reprompt_text = "Is that everything?"
    else:
        speech_output = "I'm not sure what you would like to do" \
                        "Please try again."
        reprompt_text = "I'm not sure what you would like to do"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "whatsPlayingIntent":
        return whats_playing_intent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    # elif intent_name == "AMAZON.YesIntent":
    #     return amazon_yes_intent()
    # elif intent_name == "AMAZON.NoIntent":
    #     return amazon_no_intent()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if event['session']['application']['applicationId'] != \
        alexa_skill_id:
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
