{
  "intents": [
    {
      "intent": "whatsPlayingIntent",
      "slots": [
        {
            "name": "location",
            "type": "LOCATIONS"
        },
        {
            "name": "date",
            "type": "AMAZON.DATE"
        }

      ]
    },
    {
      "intent": "moreInformationIntent",
      "slots": [
        {
            "name": "film",
            "type": "FILMS"
        }
      ]
    },
    {
      "intent": "AMAZON.HelpIntent"
    },
    {
      "intent": "AMAZON.StopIntent"
    },
    {
      "intent": "AMAZON.YesIntent"
    },
    {
      "intent": "AMAZON.NoIntent"
    },
    {
      "intent": "AMAZON.CancelIntent"
    }
  ]
}
