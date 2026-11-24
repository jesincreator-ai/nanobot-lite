"""MicroPython-friendly Nanobot Lite routing core for ESP32-WROOM."""
RULES = {
 'stop': ('stop','halt','freeze','நிறுத்து','நிறுத்துங்கள்','නවත්වන්න'),
 'greeting': ('hello','hi','hey','வணக்கம்','ஹலோ','ආයුබෝවන්','හෙලෝ'),
 'help': ('help','உதவி','උදව්'),
 'status': ('status','battery','நிலை','மின்கலம்','තත්ත්වය','බැටරි'),
 'forward': ('move forward','go forward','forward','முன்னே போ','ඉදිරියට යන්න'),
 'back': ('move back','go back','backward','பின்னால் போ','පස්සට යන්න'),
 'left': ('turn left','இடது','වමට'),
 'right': ('turn right','வலது','දකුණට'),
 'search': ('search','find','தேடு','සොයන්න'),
}

def route(text):
    s = str(text or '').lower().strip()
    for intent, terms in RULES.items():
        if any(t.lower() in s for t in terms):
            return {'intent': intent, 'confidence': 0.95 if intent == 'stop' else 0.85,
                   'needs_confirmation': intent in ('forward','back','left','right'),
                   'reply': 'Recognized: ' + intent}
    return {'intent':'chat','confidence':0.35,'needs_confirmation':False,'reply':'No local rule matched.'}

def search_sd(query, path='/sd/billi/knowledge.json', max_hits=3):
    """Search SD JSON array of {title,text,language,source} objects."""
    try:
        import json
        with open(path,'r') as f: docs=json.load(f)
        q=str(query).lower().strip(); hits=[]
        for d in docs:
            hay=(str(d.get('title',''))+' '+str(d.get('text',''))).lower()
            if q and q in hay: hits.append(d)
            if len(hits)>=max_hits: break
        return hits
    except Exception: return []

if __name__ == '__main__':
    while True:
        try:
            text=input('BILLI> '); decision=route(text); print(decision)
            if decision['intent']=='search': print(search_sd(text))
        except KeyboardInterrupt: break
