from picamera2 import Picamera2
from openai import OpenAI
from gtts import gTTS
import requests
import base64
import cv2
import os


picam2 = Picamera2()
conf = picam2.create_still_configuration(main={'size': (1080,720), 'format':'RGB888'})
picam2.configure(conf)
picam2.start()

while True:
    question = (input("What would you like to know? ")).lower()
    
    if question == 'stop':
        break
    elif question == 'help':
        client = OpenAI(api_key=KEY)

        ok = False
        while not ok:
            try:
                os.system("pacmd set-card-profile bluez_card.B0_3F_64_27_83_89 handsfree_head_unit")
            except:
                print('err setting handsfree mode.')
            else:
                ok = True

        os.system("sudo hcitool cmd 0x3F 0x01C 0x01 0x02 0x00 0x01 0x01")

        print("Now you are supposed to talk...")

        os.system("timeout 5 parecord -v audio_command.wav")

        audio_file = open("audio_command.wav", "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
            language="en"
        )

        print(transcription)

        picture_magic_words = ("front of me", "image", "picture", "photo")

        take_picture = False
        for word in picture_magic_words:
            if word in transcription:
                take_picture = True
                break

        if take_picture == True:
            array = picam2.capture_array('main')
            cv2.imwrite("image.jpeg", array)

            image_path = "./image.jpeg"

            def encode_image(image_path):
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode('utf-8')

            base64_image = encode_image(image_path)

            payload =  {"model": "gpt-4-vision-preview",
                "messages": [
                 {"role": "system",
                  "content": [{"type": "text",
                               "text": "Your goal is to help a blind person providing valuable answers using between 15 and 25 words. Provide information even if the image is blurry, and don't mention it."}],
                 },
                  {
                    "role": "user",
                    "content": [
                      {
                        "type": "text",
                        "text": f"{transcription}"
                      },
                      {
                        "type": "image_url",
                        "image_url": {
                          "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                      }
                    ]
                  }
                ],
                "max_tokens": 500
              }

            headers = {"Authorization": f"Bearer KEY",
                        "Content-Type": "application/json"}


            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)
            r = response.json()

            print(r["choices"][0]["message"]["content"])

            # The text that you want to convert to audio
            mytext = r["choices"][0]["message"]["content"]

            # Language in which you want to convert
            language = 'en'

            myobj = gTTS(text=mytext, lang=language, tld='us', slow=False)

            # Saving the converted audio in a mp3 file named
            myobj.save("description.wav")
            os.system("paplay description.wav")
        else:
            payload = {"model": "gpt-3.5-turbo",
                       "messages": [
                           {"role": "system",
                            "content": [{"type": "text",
                                         "text": "You are a smart person and have to respond to every question using between 10 and 15 words."}],
                            },
                           {
                               "role": "user",
                               "content": [
                                   {
                                       "type": "text",
                                       "text": f"{transcription}"
                                   }
                               ]
                           }
                       ],
                       "max_tokens": 500
                       }

            headers = {"Authorization": f"Bearer KEY",
                       "Content-Type": "application/json"}

            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)
            r = response.json()

            print(r["choices"][0]["message"]["content"])

            # The text that you want to convert to audio
            mytext = r["choices"][0]["message"]["content"]


            # Language in which you want to convert
            language = 'en'

            myobj = gTTS(text=mytext, lang=language, tld='us', slow=False)

            # Saving the converted audio in a mp3 file named
            myobj.save("description.wav")
            os.system("paplay description.wav")
picam2.stop()
