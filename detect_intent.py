import dialogflow_v2beta1 as dialogflow
import uuid
from contingency_planning import Rail_Line_Name
from contingency_planning import Line
from predict_delay import predict_delay
from mongoConnector import mongoConnector
from pymongo import ASCENDING, DESCENDING
from datetime import datetime
import get_train_fares
from os import environ


class df_intent_detect:
    def __init__(self):
        environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/georgemarkham/Documents/MSc/AI/train-chatbot-deployment/train-chatbot/client_secret.json"
        # environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/gmarkham/train-chatbot/client_secret.json"
        self.session_client = session_client = dialogflow.SessionsClient()
        self.session = session_client.session_path("trainchatbot", str(uuid.uuid4()))
        self.language_code = "en"
        self.db = mongoConnector("mongodb://127.0.0.1:27017/", "train_data")


    def detect_intent_and_reply(self, text, sender_id):
        print("-*"*50)
        print("\n"*2)
        print(sender_id)
        print("\n")
        print(text)
        print("\n"*2)
        print("-*"*50)
        if sender_id != "360181248095549":
            text_input = dialogflow.types.TextInput(text=text, language_code=self.language_code)
            query_input = dialogflow.types.QueryInput(text=text_input)
            response = self.session_client.detect_intent(session=self.session, query_input=query_input)

            if self.db.findOne("customers", {"sender_id": sender_id}) == None:
                self.db.store("customers", {
                    "sender_id": sender_id, 
                    "trains": []
                    })

            action = response.query_result.action
            print(action)
            if action == "book_ticket.book_ticket-yes":
                    print("-*"*50)
                    print(response.query_result.output_contexts[0])
                    print("-*"*50)
                    try:
                        from_stn = response.query_result.output_contexts[0].parameters['location_from']['city']
                    except:
                        from_stn = response.query_result.output_contexts[0].parameters['location_from']['subadmin-area']
                    try:
                        to_stn = response.query_result.output_contexts[0].parameters['location_to']['city']
                    except:
                        to_stn = response.query_result.output_contexts[0].parameters['location_to']['subadmin-area']

                    time = response.query_result.output_contexts[0].parameters['depart_time']
                    date = response.query_result.output_contexts[0].parameters['depart_date']
                    trains = get_train_fares.get_train_fares(from_stn, to_stn, date, time)
                    cheapest_train = trains[0]
                    self.db.findOneAndUpdate("customers", {"sender_id": sender_id}, {"$push": {"trains": cheapest_train}})
                    return "The cheapest ticket from " + from_stn + " to " + to_stn + " is at " + str(cheapest_train['time']) + " and costs £" + str(cheapest_train['cost']) + ". Here's the link: " + cheapest_train['url']
            if action == "train_delay.train_delay-yes":
                try:
                    current_delay = int(response.query_result.output_contexts[0].parameters['current_delay'])
                    try:
                        from_stn = response.query_result.output_contexts[0].parameters['location_from']['city']
                    except:
                        from_stn = response.query_result.output_contexts[0].parameters['location_from']['subadmin-area']
                    try:
                        to_stn = response.query_result.output_contexts[0].parameters['location_to']['city']
                    except:
                        to_stn = response.query_result.output_contexts[0].parameters['location_to']['subadmin-area']

                    intended_arrival = response.query_result.output_contexts[0].parameters['intended_arrival']
                    day, month, year, date, time = self.fmt_intended_arrival(intended_arrival)
                    predictor = predict_delay()
                    return "We think you're going to be " + str(predictor.predict(current_delay, day, month, year, date, time, from_stn, to_stn)) + " minutes late"
                except:
                    print(response.query_result.output_contexts[0])
                    return "We're having some problems, check back in a bit"
            if action == "contingency_planning.contingency_planning-yes":
                try:
                    line_name = response.query_result.output_contexts[0].parameters['line_name']
                    engine = Rail_Line_Name()
                    engine.reset()
                    engine.declare(Line(line_name=str(line_name).lower()))
                    engine.run()
                    return engine.response
                except:
                    print(response.query_result.output_contexts[0])
                    return "We're having some problems, check back in a bit"
            if response.query_result.intent.display_name == "next-train-query":
                try:
                    customer = self.db.findOne("customers", {"sender_id": sender_id})
                    trains = customer['trains']
                    if len(trains) > 0:
                        # sorted_trains = trains.sort([("date", ASCENDING), ("time", ASCENDING)])
                        # sorted_trains[0]
                        sorted_trains = sorted(sorted(trains, key=lambda x: x['time'], reverse=False), key=lambda x: x['time'], reverse=False)
                        i = 0
                        train_dt = datetime.strptime(str(sorted_trains[i]['date']) + " " + str(sorted_trains[i]['time']) , "%d%m%y %H%M")
                        while i < len(sorted_trains) and train_dt < datetime.now():
                            train_dt = datetime.strptime(str(sorted_trains[i]['date']) + " " + str(sorted_trains[i]['time']) , "%d%m%y %H%M")
                            i = i+1
                        if i < len(sorted_trains):
                            train_time = str(sorted_trains[i]['time'])[:2] + ":" + str(sorted_trains[i]['time'])[2:]
                            train_date = str(sorted_trains[i]['date'])[:2] + "/" + str(sorted_trains[i]['date'])[2:4] + "/" + str(sorted_trains[i]['date'])[4:]
                            train_from = str(sorted_trains[i]['from'])
                            train_to = str(sorted_trains[i]['to'])
                            return "Your next train is at " + train_time + " on " + train_date + ". Going from " + train_from + " to " + train_to + ". Have a great trip!"
                        else:
                            return "It appears you don't have any trips planned! Remember you can always book a trip with us, just ask!"

                    else:
                        return "We don't seem to have any data about trains you're interested in. If you'd like to book a train ticket all you need to do is ask!"

                except:
                    print(response.query_result.output_contexts[0])
                    return "We're having some problems, check back in a bit"
            else:
                return response.query_result.fulfillment_text
            
        else:
            return ""
    def fmt_intended_arrival(self, dt):
        dt_arr = dt.split("T")
        date_arr = dt_arr[0].split("-")
        time_arr = dt_arr[1].split(":")
        return int(date_arr[2]), int(date_arr[1]), int(date_arr[0][2:]), int(str(date_arr[2] + date_arr[1] + date_arr[0][2:])), int(str(time_arr[0] + time_arr[1]))

if __name__ == "__main__":
    df = df_intent_detect()
    while True:
        msg = input()
        print(df.detect_intent_and_reply(msg, "1"))