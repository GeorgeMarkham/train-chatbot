from random import choice
from pyknow import *

class Line(Fact):
    """Info about the rail line."""
    pass
    
class Rail_Line_Name(KnowledgeEngine):
    @Rule(Line(line_name='east suffolk line'))
    def east_suffolk_line(self):
        self.response = "Walk"
            
    @Rule(Line(line_name='stansted express'))
    def stansted_express(self):
        self.response = "Reduce to 2 per hour but as last resort and must be formed of 8 coaches."
    
    @Rule(Line(line_name='west anglia outer'))
    def west_anglia_outer(self):
        self.response = "Skip stops between Bishops Stortford - Liverpool Street."
        
    @Rule(Line(line_name='west anglia inner'))
    def west_anglia_inner(self):
        self.response = "Skip stops, Round trips to cut out late running."
        
    @Rule(Line(line_name='romford - upminster'))
    def romford_upminster(self):
        self.response = "Round trips to cut out late running"
        
    @Rule(Line(line_name='southend to liverpool street'))
    def southend_to_liverpool_street(self):
        self.response = "Skip stops if required"
        
    @Rule(Line(line_name='southminster services'))
    def southminster_services(self):
        self.response = "Round trips to cut out late running"
        
    @Rule(Line(line_name='braintree line'))
    def braintree_line(self):
        self.response = "Implement a Witham to Braintree shuttle as soon as possible."
        
    @Rule(Line(line_name='clacton/colchester to liverpool street'))
    def clacton_colchester_to_liverpool_street(self):
        self.response = "Can run Colchester to Clacton shuttle with Thorpe to Walton shuttle."
    
    @Rule(Line(line_name='harwich town to liverpool street'))
    def harwich_town_to_liverpool_street(self):
        self.response = "Terminate at Harwich International."
    
    @Rule(Line(line_name='intercity norwich to liverpool street'))
    def intercity_norwich_to_liverpool_street(self):
        self.response = "Can be reduced to hourly xx00 from Nrw, xx30 from Lst"
    
    @Rule(Line(line_name='felixstowe line'))
    def felixstowe_line(self):
        self.response = "Round trips to cut out late running."
        
    @Rule(Line(line_name='cambridge to ipswich'))
    def cambridge_to_ipswich(self):
        self.response = "Consider turning at Nmk/BSE and using buses"
        
    @Rule(Line(line_name='peterborough line'))
    def peterborough_line(self):
        self.response = "In the event of severe late running consider terminating at Ely on Down services."

    @Rule(Line(line_name='norwich to yarmouth/lowestoft'))
    def norwich_to_yarmouth_lowestoft(self):
        self.response = "Alternative routing to Yarmouth. Able to divert Lowestoft services to Yarmouth and road passengers to/from Lowestoft"
        
    @Rule(Line(line_name='norwich to sheringham'))
    def norwich_to_sheringham(self):
        self.response = "Able to terminate Wroxham/North Walsham or Cromer"
        
    @Rule(Line(line_name='norwich to cambridge'))
    def norwich_to_cambridge(self):
        self.response = "Able to terminate Wymondham, Attleborough, Thetford or Ely. Passengers from Ely can transfer to/from FCC or Cross Country or Stagecoach East Midlands services."
        
if __name__ == "__main__":
    # THIS WILL WORK:
    engine = Rail_Line_Name()
    engine.reset()
    engine.declare(Line(line_name=input("Enter Rail Line Name. ").lower()))
    engine.run()
    print(engine.response)