
def parseDateTime(start_time_range, end_time_range):

    start_dt = start_time_range.replace("-","/").replace("T", " ").split("delimiter")
    end_dt = end_time_range.replace("-","/").replace("T", " ").split("delimiter")

    final_date_time = start_dt + end_dt

    return final_date_time


def communicationType(input):
    call_sms_dict = {}
    if len(input) == 2 :
        call_sms_dict.update({'call':True, 'sms':True})
    elif input[0] ==  'call':
        call_sms_dict.update({'call':True,'sms':False})
    else:
        call_sms_dict.update({'call':False, 'sms':True})
    return call_sms_dict

def callDirection(input):
    incoming_outgoing_dict = {}
    if input=='Incoming/Outgoing' :
        incoming_outgoing_dict.update({'incoming':True, 'outgoing':True})
    elif input ==  'Incoming':
        incoming_outgoing_dict.update({'incoming':True,'outgoing':False})
    else:
        incoming_outgoing_dict.update({'incoming':False, 'outgoing':True})
    return incoming_outgoing_dict