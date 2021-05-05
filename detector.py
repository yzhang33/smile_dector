from cv2 import cv2
import os
import re
from rivescript import RiveScript
from tkinter import Tk, Label, Entry, Button, StringVar
import tweepy 
from dotenv import load_dotenv
import random
import emoji
import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
import requests

# haar_frontface_xml = pkg_resources.resource_filename(
# 'cv2', 'data/haarcascades/haarcascade_frontalface_default.xml')
# haar_eye_xml = pkg_resources.resource_filename(
# 'cv2', 'data/haarcascades/haarcascade_frontalface_default.xml')
# haar_smile_xml = pkg_resources.resource_filename(
# 'cv2', 'data/haarcascades/haarcascade_frontalface_default.xml')

face_cascade = cv2.CascadeClassifier('/home/youming/Documents/smile_detector/cascade/haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('/home/youming/Documents/smile_detector/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('/home/youming/Documents/smile_detector/cascade/haarcascade_smile.xml')
#twitter 
load_dotenv()
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET') 
access_token = os.getenv('ACCESS_TOKEN') 
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')  
api_key = os.getenv('GIPHY_API')  
#count smiles so far
smile_count=[]
smile_emoji=[
    "\U0001F600",
    "\U0001F603",
    "\U0001F604",
    "\U0001F601",
    "\U0001F606",
    "\U0001F605",
    "\U0001F923",
    "\U0001F602",
    "\U0001F642",
    "\U0001F643",
    "\U0001F609",
    "\U0001F60A",
    "\U0001F607",
    "\U0001F970",
    "\U0001F60D",
    "\U0001F929",
    "\u263A",
    "\U0001F972",
    "\U0001F60B",
    "\U0001F61B",
    "\U0001F92A",
    "\U0001F911",
    "\U0001F917",
    "\U0001F924",
    "\U0001F920",
    "\U0001F60E"
]
# create an instance of the API class
api_instance = giphy_client.DefaultApi()
q = 'smile' # str | Search query term or prhase.
limit = 100 # int | The maximum number of records to return. (optional) (default to 25)
offset = 0 # int | An optional results offset. Defaults to 0. (optional) (default to 0)
rating = 'g' # str | Filters results by specified rating. (optional)
lang = 'en' # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

class SmileBot:
    def __init__(self, master):
        self.master = master

        self.master.geometry('600x400')
        self.master['bg'] = '#ffbf00'
        
        self.e1 = Entry(self.master)
        self.e1.pack(pady=30)
        self.label = Label(self.master, text='', pady=20, bg='#ffbf00')
        self.label.pack()
        
        Button(self.master,text="Send", padx=10, 
                pady=5,command=self.receive).pack()
        self.bot = RiveScript(utf8=True,debug=False)

    def receive(self):
        tk_input = self.e1.get()

        self.bot.unicode_punctuation = re.compile(r'[.,!?;:]')
        self.bot.load_directory("eg/brain")
        self.bot.sort_replies()

        #input text for rivescript
        input_text = tk_input
        input_text = input_text.encode("utf-8").strip()

        reply_text = self.response(input_text)
        self.label.config(text=reply_text)

    def response(self,text):
        text = text.decode("utf-8")
        print(text)
        reply = self.bot.reply("localuser",text)
        reply_text = reply.encode("utf-8").strip()
        return reply_text
        
def gif_download(gif_url):
    '''
    Takes the URL of an Image/GIF and downloads it
    '''
    gif_data = requests.get(gif_url).content
    with open('image.gif', 'wb') as handler:
        handler.write(gif_data)
        handler.close()

def get_gif():
    try: 
        # Search Endpoint
        api_response = api_instance.gifs_search_get(api_key, q, limit=limit, offset=offset, rating=rating, lang=lang, fmt=fmt)
        url = (random.choice(api_response.__dict__['_data']).__dict__['_images'].__dict__['_downsized_large'].__dict__['_url'])
        return url
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

def tweet_smile(mode):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    if mode == 1:
        smile_string =""
        for s in smile_count:
            smile_string += s+" "
        api.update_status(emoji.emojize("Smiles I've seen\n"+smile_string+"\n"))
    if mode == 2:
        url = get_gif()
        gif_download(url)
        message= "Keep smiling @yzhang69 " + "#smile\n"
        api.update_with_media('image.gif',status=message)

    # print(tweettopublish)

def Mbox():
    root = Tk()
    root.title('Chat with SmileMan')
    my_gui = SmileBot(root)
    root.mainloop()

def detect(gray, frame):
    smile = False
    face = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x_face, y_face, w_face, h_face) in face:
        cv2.rectangle(frame, (x_face, y_face), (x_face+w_face, y_face+h_face), (255, 130, 0), 2)
        ri_grayscale = gray[y_face:y_face+h_face, x_face:x_face+w_face]
        ri_color = frame[y_face:y_face+h_face, x_face:x_face+w_face] 
        smile = smile_cascade.detectMultiScale(ri_grayscale, 1.7, 20)
        for (x_smile, y_smile, w_smile, h_smile) in smile: 
            cv2.rectangle(ri_color,(x_smile, y_smile),(x_smile+w_smile, y_smile+h_smile), (20, 0, 255), 2)
            smile = True
    return frame,smile

def main():
    #fram count
    frame_count = 0
    video_capture = cv2.VideoCapture(0)
    while True:
        # Captures video_capture frame by frame
        _, frame = video_capture.read() 

        # To capture image in monochrome                    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  

        # calls the detect() function    
        canvas, smile = detect(gray, frame) 
        # found smile 
        if smile and frame_count % 60 == 0:
            smile_count.append(random.choice(smile_emoji))
            Mbox()
        # idel time tweet something
        if smile == ():
            if frame_count % 200 == 0:
                if len(smile_count) > 0:
                    tweet_smile(1)
                    print("tweeting")
            if frame_count != 0 and frame_count % 120 == 0:
                tweet_smile(2)
                print("tweeting gif")

        # Displays the result on camera feed                     
        cv2.imshow('Video', canvas) 

        # The control breaks once q key is pressed                        
        if cv2.waitKey(1) & 0xff == ord('q'):               
            break
        frame_count += 1

    # Release the capture once all the processing is done.
    video_capture.release()                                 
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()

