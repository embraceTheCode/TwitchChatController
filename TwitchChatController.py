#06/04/2021 Carlos Astengo Macias

# Documentation:
# Twitch IRC connection: https://dev.twitch.tv/docs/irc/guide
# Python socket: https://docs.python.org/3/library/socket.html#functions
# Pyautogui: https://pyautogui.readthedocs.io/en/latest/keyboard.html
# Get OAuth key: https://twitchapps.com/tmi/

import socket
import pyautogui

#Twitch address and port found in documentation
address = "irc.twitch.tv"
port = 6667

#User credentials
oauthKey = ""
nickname = ""
channelName = ""

#Starts connection with irc and sends credentials
irc = socket.socket()
irc.connect((address, port)) 
irc.send(("PASS " + oauthKey + "\n" + "NICK " + nickname + "\n" + "JOIN #" + channelName + "\n").encode())

def main():

    #Presses given key once
    def PressButton(button):
        pyautogui.keyDown(button)
        pyautogui.keyUp(button)

    #Checks if the message contains a valid input
    def ValidateInput(controllerInput):
        controllerInput = controllerInput.lower()
        if "up" in controllerInput:
            PressButton(controllerInput)
        elif "down" in controllerInput:
            PressButton(controllerInput)
        elif "left" in controllerInput:
            PressButton(controllerInput)
        elif "right" in controllerInput:
            PressButton(controllerInput)
        elif "attack" in controllerInput:
            PressButton("x")
        elif "jump" in controllerInput:
            PressButton("z")

    #Checks if the program has correctly connected by looking for the message ">"
    #According to the irc documentation when you see that message you have correctly connected
    def ConfirmConnection():
        isJoining = True
        while isJoining:
            reader = irc.recv(1024)
            reader = reader.decode()
            for line in reader.split("\n"):
                print(line)
                if ">" in line:
                    print("\n" + "Bot has successfully connected to the channel.")
                    isJoining = False

    #Splits the string to get the user that sent the message
    def GetUser(line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    #Splits the string to get the message the user sent
    def GetMesssage(line):
        try:
            message = (line.split(":", 2)[2])
        except:
            message = ""
        return message

    ConfirmConnection()

    while True:
        #Receives new messages from chat
        try:
            reader = irc.recv(1024)
            reader = reader.decode()
        except:
            reader = ""
        
        for line in reader.split("\r\n"):
            if(line == ""):
                continue
            
            #if the line contains PRIVMSG it means that it was sent by a user
            elif "PRIVMSG" in line:
                user = GetUser(line)
                message = GetMesssage(line)
                print(user + " : " + message)
                ValidateInput(message)

            #According to twitch documentation:
                # “About once every five minutes, the server will send you a PING :tmi.twitch.tv. 
                # To ensure that your connection to the server is not prematurely terminated, reply with PONG :tmi.twitch.tv.
            elif "PING" in line:
                print(line)
                message = "PONG tmi.twitch.tv\r\n".encode()
                irc.send(msgg)
                print(msgg)
                continue
        message = ""

main()