'''

 ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗     
██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║     
██║  ███╗██║     ██║   ██║██████╔╝███████║██║     
██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║     
╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗
 ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝                                      

███████╗██╗   ██╗██████╗ ████████╗██╗████████╗██╗     ███████╗███████╗
██╔════╝██║   ██║██╔══██╗╚══██╔══╝██║╚══██╔══╝██║     ██╔════╝██╔════╝
███████╗██║   ██║██████╔╝   ██║   ██║   ██║   ██║     █████╗  ███████╗
╚════██║██║   ██║██╔══██╗   ██║   ██║   ██║   ██║     ██╔══╝  ╚════██║
███████║╚██████╔╝██████╔╝   ██║   ██║   ██║   ███████╗███████╗███████║
╚══════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝   ╚═╝   ╚══════╝╚══════╝╚══════╝

Made with ❤️ for Coding By Samvid & Navadeep
!!! Make Sure You Have Specified API Keys In app/configure.py Before Running !!!
!!! Make Sure You Have Installed All Dependencies In requirements.txt !!!
Read the LICENSE file for License
Read README.md for information about the project
Run app/app.py with Python 3.10.1 to Start Applet

'''

# from distutils.command.config import config
# from logging.handlers import TimedRotatingFileHandler
import pyaudio
import websockets
import asyncio
import base64
import json
from configure import assemblyai_key
# import tkinter as tk
import settings
from datetime import datetime
import os
import sys

timedate = datetime.now()


FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
# starts recording
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


async def send_receive():
    print(f'Connecting websocket to url ${URL}')
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", assemblyai_key),),
        ping_interval=5,
        ping_timeout=20
    ) as _ws:
        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")
        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data), })
                    print("Sent Something To AssemblyAI API")
                    await _ws.send(json_data)
                    # if settings.running == True:
                    #     print("funcs.py loop continuing to run")
                    #     await asyncio.sleep(0.01)
                    #     return True
                    # else:
                    #     print("funcs.py loop IS ENDING, Is Running: " +
                    #           str(settings.running))
                    #     sys.exit()
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                if settings.running == True:
                    print("funcs.py loop continuing to run")
                    await asyncio.sleep(0.01)
                else:
                    print("funcs.py loop IS ENDING, Is Running: " +
                    str(settings.running))
                    sys.exit()
            # if settings.running == True:
            #     print("funcs.py loop continuing to run")
            #     return True
            # else:
            #     print("funcs.py loop IS ENDING, Is Running: " +
            #     str(settings.running))
            #     sys.exit()

        async def receive():
            global homeDirectoryPath
            global timedate
            while True:
                try:
                    result_str = await _ws.recv()
                    print("from funcs.py: " + str(json.loads(result_str)))
                    mySubtitle = (json.loads(result_str)['text'])
                    if json.loads(result_str)['message_type'] == 'FinalTranscript':
                        if settings.transcriptionEnabled == "Enabled":
                            fileName = homeDirectoryPath + \
                                "/globalsubtitles_transcription_" + \
                                str(timedate)
                            file = open(fileName, "a")
                            file.write(mySubtitle + "\n")
                            file.close()
                        # print("Final Transcript: "+json.loads(result_str)['text'])
                    # print(subtitle)
                    # subtitleLabel = subtitleLbl
                    # subtitleLabel['text'] = subtitle
                    splitSubtitle = mySubtitle.split()
                    wordCount = len(splitSubtitle)
                    if wordCount > settings.wordcount:
                        removable = wordCount-settings.wordcount
                        del splitSubtitle[:removable]
                        joinedString = ' '.join(
                            [str(item) for item in splitSubtitle])
                        settings.subtitleVar = joinedString
                    else:
                        settings.subtitleVar = mySubtitle
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())
