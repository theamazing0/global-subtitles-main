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

#* Imports Required Dependencies
# Make Sure You Have Installed These from requirements.txt

import pyaudio
import websockets
import asyncio
import base64
import json
from configure import assemblyai_key
import settings
from datetime import datetime
import sys
import os

# Gets System Time For Transcription File
timedate = datetime.now()
# Gets Home Directory Path
homeDirectoryPath = os.path.expanduser('~')

# Configures Stream
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

# API URL For AssemblyAI API
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

# Used Internally To Communicate With AssemblyAI
async def send_receive():
    print('     INFO: Connecting websocket to url ${URL}')
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", assemblyai_key),),
        ping_interval=5,
        ping_timeout=20
    ) as _ws:
        await asyncio.sleep(0.1)
        print("     INFO: Receiving SessionBegins ...")
        session_begins = await _ws.recv()
        print("     INFO: Sending messages ...")

        async def send():
            while True:
                try:
                    # Sends Audio Data To API
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data), })
                    print("     INFO: Sent Audio Data To AssemblyAI")
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "     ERROR: Not a websocket 4008 error"
                # Checks If Application Is Still Running
                if settings.running == True: # If True
                    await asyncio.sleep(0.01) # Schedules Repeat Of Send Audio Data Loop
                else: # If Not
                    sys.exit() # Terminates Application

        async def receive():
            global homeDirectoryPath
            global timedate
            while True:
                try:
                    # Recieve Audio Data
                    result_str = await _ws.recv()
                    print("     INFO: Recieved Text From API- "+ json.loads(result_str)['text'])
                    mySubtitle = (json.loads(result_str)['text'])
                    # If Transcription Is Enabled
                    if json.loads(result_str)['message_type'] == 'FinalTranscript':
                        if settings.transcriptionEnabled == "Enabled":
                            # Adds To Transcription File
                            fileName = homeDirectoryPath + \
                                "/globalsubtitles_transcription_" + \
                                str(timedate)
                            file = open(fileName, "a")
                            file.write(mySubtitle + "\n")
                            file.close()
                    # Displays Subtitle Based On User Configuration
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
