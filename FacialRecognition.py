from microbit import *
import radio
import music

radio.config(group=1)
radio.on()

current_face = -1

def show_face(face_id):

    if 0 <= face_id <= 2:
        display.show(str(face_id))

        if face_id == 0:
            music.play(['C4:2'])
        elif face_id == 1:
            music.play(['D4:2'])
        elif face_id == 2:
            music.play(['E4:2'])
        sleep(1000)
        display.clear()
    else:
        display.show(Image.CONFUSED)
        sleep(500)
        display.clear()

def parse_face_data(data):

    if len(data) >= 2 and data[0] == 'Y':
        try:
            face_num = int(data[1])
            if 0 <= face_num <= 2:
                return face_num
        except:
            pass
    return -1

display.show("FACE")
sleep(1000)
display.clear()

while True:

    data = radio.receive()

    if data:
        face_num = parse_face_data(data)

        if face_num != current_face:
            current_face = face_num
            show_face(face_num)

    sleep(100)
