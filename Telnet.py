import telnetlib
import Settings

def update_display(filename):

    filename = "twitter_test"

    #Connect to the display
    try:

        #Connect to the server
        display = telnetlib.Telnet(Settings.inova_host)

        try:
            #Enter username
            display.read_until("LED_DISPLAY_1 login: ")
            display.write(Settings.inova_user.encode('ascii') + "\r\n")

            print('USERNAME ACCEPTED')

            try:
                #Enter password
                display.read_until("Password: ")
                display.write(Settings.inova_password.encode('ascii') + "\r\n")

                print('PASSWORD ACCEPTED')

            except:

                print('PASSWORD FAILED')

            #Do something on the display.
            try:

                #go the the message folder.
                display.write("cd /inova/local_msgs" + "\r\n")

                #Remove the file if it exists.
                display.write("rm "+filename+".llm" + "\r\n")

                #Download the file with wget.
                display.write("wget http://" + Settings.server_ip + "/" + filename+".llm" + "\r\n")

                print('COMMANDS DELIVERED')

                display.write('exit' + "\r\n")

            except:

                print('FAILED TO RUN COMMANDS')

        except:

            print 'FAILED TO LOGIN'

        #Collect and discard session data
        sess = display.read_all()
        print(sess)

        #Close the connection
        display.close()
        print('CONNECTION CLOSED')

    except:
        print'CONNECTION FAILED'