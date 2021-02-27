import sounddevice as sd
import soundfile as sf
import tkinter as tk
import threading
import os
import time
import keyboard
from audio2numpy import open_audio
import numpy as np

if os.path.exists("sound_configs.txt"):
    print('sound config exist')
    with open("sound_configs.txt",'r') as f:
        sounds = [line.split('\t') for line in f.read().split('\n')]
    print('sound config loaded')
    print(sounds[0])
    if sounds and len(sounds[0]) < 4:
        sounds = []
        print('something went wrong with sound config')
else:
    sounds = []

testbool = False

def set_testbool():
    global testbool
    testbool = True

# stop the current sound from playing
def stop_sound():
    sd.stop()

# set sound hotkey and volume
def set_attributes():
    global sounds
    sounds[int(box2.get())][2] = box.get()
    with open("sound_configs.txt",'w+') as f:
        f.writelines(['\t'.join(sound)+'\n' for sound in sounds])
    get_sounds()

def clear_attributes():
    global sounds
    sounds[int(box2.get())][2] = 'NA'
    with open("sound_configs.txt",'w+') as f:
        f.writelines(['\t'.join(sound)+'\n' for sound in sounds])
    get_sounds()

# get list of all sound devices
# @return the list of sound devices
def get_sound_devices():
    device_list = sd.devicelist()
    return device_list

def get_sounds():
    global sounds
    files = os.listdir("sounds")
    for file in files:
        try:
            if len(sounds) == 0 or file not in np.array(sounds).T[1]:
                sounds.append([str(len(sounds)), file, 'NA', '100'])
        except:
            pass
    txt.configure(state='normal')
    txt.delete('1.0', tk.END)
    txt.insert('1.0', '\n'.join([f'{sound[0]}\t{sound[1][:20].ljust(20)}\t{sound[2]}' for sound in sounds]))
    txt.configure(state='disabled')
    with open("sound_configs.txt",'w+') as f:
        f.writelines(['\t'.join(sound)+'\n' for sound in sounds])
    #print(sounds)

def play_audio(i=-1):
    global sounds
    if i == -1:
        i = int(box2.get())
    #sd.stop()
    try:
        data, fs = sf.read(f'sounds/{sounds[i][1]}', dtype='float32')
    except:
        data, fs = open_audio(f'sounds/{sounds[i][1]}')
    sd.play(data, fs, device=13)
    status = sd.wait()

def get_key_press():
    global sounds
    global testbool
    while True:
        if testbool:
            play_audio(int(box2.get()))
            testbool = False
            print('true')
            time.sleep(0.5)
        for i, combo in enumerate(sounds):
            try:
                if keyboard.is_pressed(combo[2]):
                    print("true")
                    play_audio(i)
                    time.sleep(0.5)
            except:
                pass
        time.sleep(0.01)

master = tk.Tk()

hotkeyvar = tk.StringVar()
filenvar = tk.StringVar()

inputmenu = tk.Frame(master)
label = tk.Label(inputmenu, text='Hotkey:')
label2 = tk.Label(inputmenu, text='Sound ID:')
box = tk.Entry(inputmenu, textvariable = hotkeyvar)
box2 = tk.Entry(inputmenu, textvariable = filenvar)
btn = tk.Button(inputmenu, text = 'test', command=set_testbool)
btn2 = tk.Button(inputmenu, text = 'refresh', command=get_sounds)
btn3 = tk.Button(inputmenu, text = 'set', command=set_attributes)
btn4 = tk.Button(inputmenu, text = 'clear', command=clear_attributes)
btn5 = tk.Button(inputmenu, text = 'stop', command=stop_sound)

textoutput = tk.Frame(master)
txt = tk.Text(textoutput, width=50)
txt.configure(state='disabled')
scrollb = tk.Scrollbar(textoutput, command=txt.yview)
txt['yscrollcommand'] = scrollb.set

label.grid(row=0,column=0)
label2.grid(row=0,column=1)
box.grid(row=1,column=0)
box2.grid(row=1,column=1)
btn.grid(row=0, rowspan=1, column=2, sticky='nsew')
btn2.grid(row=1, rowspan=1, column=2, sticky='nsew')
btn3.grid(row=0, rowspan=1, column=3, sticky='nsew')
btn4.grid(row=1, rowspan=1, column=3, sticky='nsew')
btn5.grid(row=0, rowspan=1, column=4, sticky='nsew')
inputmenu.pack(side='top')

txt.grid(row=0, column=0, sticky='nsew')
scrollb.grid(row=0, column=1, sticky='nsew')
textoutput.pack()

get_sounds()
#sounds_thread = threading.Thread(target=get_sounds)
keylogger_thread = threading.Thread(target=get_key_press)
#sounds_thread.start()
keylogger_thread.start()

master.mainloop()