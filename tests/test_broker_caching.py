holding = ""

def match(msg_obj):
    return msg_obj.target == "caching"

def process(txq, msg_obj):
    if not holding:
        holding = msg_obj.msg
    else:
        txq.put(holding)