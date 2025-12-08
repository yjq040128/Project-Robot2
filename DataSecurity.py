from microbit import *
import radio
import music

radio.config(group=1)
radio.on()

current_face = -1
registered_faces = [False, False, False]
security_level = 1  # 1:低, 2:中, 3:高
access_count = 0

def check_security(face_id):

    if security_level == 1:
        return True
    elif security_level == 2:
        return registered_faces[face_id]
    elif security_level == 3:

        if registered_faces[face_id] and access_count < 10:
            return True
    return False

def show_face_secure(face_id):

    if face_id < 0 or face_id > 2:
        display.show(Image.CONFUSED)
        sleep(500)
        display.clear()
        return

    if check_security(face_id):

        display.show(str(face_id))


        notes = ['C4:2', 'D4:2', 'E4:2']
        music.play(notes[face_id])

        if security_level == 3:
            global access_count
            access_count += 1
    else:

        display.show(Image.NO)
        music.play(['C2:4'])

    sleep(1000)
    display.clear()

def parse_face_data(data):

    if data and len(data) >= 2 and data[0] == 'Y':
        try:
            face_num = int(data[1])
            if 0 <= face_num <= 2:
                return face_num
        except:
            pass
    return -1

display.show("SEC")
sleep(1000)
display.clear()

while True:

    if button_a.is_pressed():
        if 0 <= current_face <= 2:
            registered_faces[current_face] = True
            display.show(Image.YES)
            sleep(500)
            display.clear()
        sleep(300)


    if button_b.is_pressed():
        security_level = (security_level % 3) + 1
        display.show(str(security_level))
        sleep(500)
        display.clear()
        sleep(300)


    data = radio.receive()
    if data:
        face_num = parse_face_data(data)

        if face_num != current_face:
            current_face = face_num
            show_face_secure(face_num)

    sleep(100)
