import pyaudio
import websockets
import asyncio
import base64
import json
from configure import auth_key
import tkinter as tk

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
        extra_headers=(("Authorization", auth_key),),
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
                    json_data = json.dumps({"audio_data": str(data)})
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                await asyncio.sleep(0.01)

            return True

        async def receive():
            while True:
                try:
                    result_str = await _ws.recv()
                 #    print(json.loads(result_str)['text'])
                    subtitle = (json.loads(result_str)['text'])
                    print(subtitle)
                    app.subtitleLbl['text'] = subtitle
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())

# # * Start The Proccess


# def subtitle():
#     print('subtitle loop started')
#     subtitleWindow = tk.Tk()
#     subtitleWindow.title('Global Subtitles')
#     subtitleWindow.wait_visibility(subtitleWindow)
#     subtitleWindow.attributes('-topmost', True, '-alpha', 0.3)
#     startWindow.destroy()  # subtitleWindow.mainloop()
#     asyncio.run(send_receive())

# # * Tkinter Implementation


# startWindow = tk.Tk()
# startWindow.title('Welcome')
# startWindow.resizable(width=False, height=False)

# titleFrame = tk.Frame(master=startWindow)
# titleFrame.columnconfigure(0, minsize=500)

# titleLbl = tk.Label(text='Global Subtitles', font=(
#     'Times New Roman', '48'), master=titleFrame)
# titleFrame.grid(row=0, column=0)
# titleLbl.grid(row=0, column=0)

# buttonFrame = tk.Frame(master=startWindow)
# buttonFrame.columnconfigure(2)
# startBtn = tk.Button(master=buttonFrame, text='Start', font=(
#     'Times New Roman', '30'), command=subtitle)

# buttonFrame.grid(row=1, column=0)
# startBtn.grid(row=0, column=0, padx=50)

# # asyncio.run(send_receive())

# startWindow.mainloop()

# # * -------------------------
