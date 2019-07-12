import json 
import io
import ast
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from Queue import Queue, Full

def parse_audio(path):
    global global_path
    global_path = path
    audio = path+'/recording.mp3'
    CHUNK = 1024
    # Note: It will discard if the websocket client can't consumme fast enough
    # So, increase the max size as per your choice
    BUF_MAX_SIZE = CHUNK * 10

    speech_to_text = SpeechToTextV1(
    iam_apikey='9e0ri-mtT_R8DicTjLTNkRe9T1WJFxHdkFBYobAmlxp2',
    url='https://gateway-wdc.watsonplatform.net/speech-to-text/api/v1/recognize'
    )

    speech_to_text.disable_SSL_verification()
    jsonresult=""
    q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))

    class MyRecognizeCallback(RecognizeCallback):

        def __init__(self):
            RecognizeCallback.__init__(self)

        def on_data(self, data):
            q.put(data)

        def on_error(self, error):
            print('Error received: {}'.format(error))

        def on_inactivity_timeout(self, error):
            print('Inactivity timeout: {}'.format(error))



    myRecognizeCallback = MyRecognizeCallback()

    #read input audio file 
    with open(audio,'rb') as audio_file:
        audio_source = AudioSource(audio_file)
        speech_to_text.recognize_using_websocket(
            audio=audio_source,
            content_type='audio/mp3',
            recognize_callback=myRecognizeCallback,
            model='en-US_BroadbandModel',
            speaker_labels=True)

    # write to raw transcript 
    with open(global_path+'/sample.json','w+') as f :
        while not q.empty():
            f.write(json.dumps(q.get()))


def convert():
    with io.open(global_path+"/sample.json",encoding='utf-8') as f:
        d = json.load(f)

    final_conv=[]
    old_speaker=None
    conversation=""
    new_index=0

    for k1,v1 in d.items():  #v1 is list , int , list 
        if k1=="speaker_labels":
            for index in range(len(v1)):
                each_value=v1[index] 
                if (each_value['speaker']!=old_speaker and old_speaker!=None) :
                    # print "new user"
                    conversation="Speaker "+str(old_speaker)+ " : "
                    
                    for new_k1,new_v1 in d.items():
                        # print new_v1
                        if new_k1=='results':
                            if isinstance(new_v1,list):
                                for v2 in new_v1:  
                                    # print v2
                                    for k3,v3 in v2['alternatives'][0].items():
                                        if isinstance(v3,list):
                                            # print v3
                                            for each in v3:
                                                # print from_,to_
                                                if each[1]<= from_ and each[2]<= to_:
                                                    conversation+= each[0]+' '
                                                    v3.remove(each)
                                                    

                    final_conv.append( conversation)
                    old_speaker=each_value['speaker']                             
                else:
                    old_speaker=each_value['speaker']
                    from_=each_value['from']
                    to_=each_value['to']

    return final_conv










