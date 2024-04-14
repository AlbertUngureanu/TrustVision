import random
def encrypt_data(message):
    ascii_characters = ''.join(chr(i) for i in range(33, 127))
    #print(ascii_characters)

    pad = random.randrange(1, 10)
    fb = random.randrange(1, 3)

    print("fb = " + str(fb) + " pad = " + str(pad))

    fb = int(fb)
    pad = int(pad)

    initial_fb = fb

    encrypted_data = ""

    for i in range(len(message)):
        if fb % 2 == 1:
            encrypted_data += ascii_characters[(ascii_characters.index(message[i]) + pad) % len(ascii_characters)]
            #print((ascii_characters.index(message[i]) + pad) % len(ascii_characters))
            #print("i = " + str(i) + " Encrypted data: " + encrypted_data)
        else:
            new_index = (ascii_characters.index(message[i]) - pad)
            if new_index < 0:
                encrypted_data += ascii_characters[new_index]
            else:
                encrypted_data += ascii_characters[new_index % len(ascii_characters)]
            #print("new index: " + str(new_index))
            #print("i = " + str(i) + " Encrypted data: " + encrypted_data)

        #print(encrypted_data)
        fb += 1

    encrypted_data += str(pad)
    encrypted_data += str(initial_fb)

    return encrypted_data

def decrypt_data(encrypted_data):
    ascii_characters = ''.join(chr(i) for i in range(33, 127))
    #print(ascii_characters)

    fb = encrypted_data[-1:]
    pad = encrypted_data[len(encrypted_data) - 2]

    print("fb = " + str(fb) + " pad = " + str(pad))

    fb = int(fb)
    pad = int(pad)

    decrypted_data = ""

    for i in range(len(encrypted_data)-2):
        if fb % 2 == 0:
            decrypted_data += ascii_characters[(ascii_characters.index(encrypted_data[i]) + pad) % len(ascii_characters)]
            #print((ascii_characters.index(message[i]) + pad) % len(ascii_characters))
            #print("i = " + str(i) + " Decrypted data: " + decrypted_data)
        else:
            new_index = (ascii_characters.index(encrypted_data[i]) - pad)
            if new_index < 0:
                decrypted_data += ascii_characters[new_index]
            else:
                decrypted_data += ascii_characters[new_index % len(ascii_characters)]
            #print("new index: " + str(new_index))
            #print("i = " + str(i) + " Decrypted data: " + decrypted_data)

        #print(encrypted_data)
        fb += 1


    return decrypted_data

message = "M!@uV1@t@?!"

encrypted_mess = encrypt_data(message)
print("Encrypted message: " + encrypted_mess)

decrypted_mess = decrypt_data(encrypted_mess)
print("Decrypted message: " + decrypted_mess)