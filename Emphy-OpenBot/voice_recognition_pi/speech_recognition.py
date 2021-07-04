import speech_recognition as sr
from subprocess import call

cmd_beg= 'espeak '
cmd_end= ' 2>/dev/null' # To dump the std errors to /dev/null

r = sr.Recognizer()
m = sr.Microphone(device_index=2)


try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                cmd = (u"You said {}".format(value).encode("utf-8"))
                print(cmd)
                cmd = cmd.replace(' ', '_')
                print("Now speak")
                call([cmd_beg+cmd+cmd_end], shell=True)
            else:  # this version of Python uses unicode for strings (Python 3+)
                cmd = ("You said {}".format(value))
                print(cmd)
                cmd = cmd.replace(' ', '_')
                call([cmd_beg+cmd+cmd_end], shell=True)
        except sr.UnknownValueError:
            cmd = "Oops Did not catch that"
            print(cmd)
            cmd = cmd.replace(' ', '_')
            call([cmd_beg+cmd+cmd_end], shell=True)
        except sr.RequestError as e:
            cmd = ("Uh oh Could not request results from Google Speech Recognition service; {0}".format(e))
            print(cmd)
            cmd = cmd.replace(' ', '_')
            call([cmd_beg+cmd+cmd_end], shell=True)

except KeyboardInterrupt:
    pass