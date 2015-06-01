import telnetlib
import Settings
import time

# Connect to the display with telnet.
def update_display(filename):

    # Connect to the display
    try:

        # Connect to the server
        display = telnetlib.Telnet(Settings.inova_host)

        try:
            # Enter username
            display.read_until("LED_DISPLAY_1 login: ")
            display.write(Settings.inova_user.encode('ascii') + "\r\n")

            print('USERNAME ACCEPTED')

            try:
                # Enter password
                display.read_until("Password: ")
                display.write(Settings.inova_password.encode('ascii') + "\r\n")

                print('PASSWORD ACCEPTED')

            except:

                print('PASSWORD FAILED')

            # Do something on the display.
            try:

                # cd to the the message folder.
                display.write("cd /inova/local_msgs" + "\r\n")

                # Wait for 1 second
                time.sleep(1)

                # Remove the file if it exists.
                display.write("rm " + filename + ".llm" + "\r\n")

                # Wait for 1 second
                time.sleep(1)

                # Download the file with wget.
                display.write("wget http://" + Settings.server_ip + ':' + str(
                    Settings.server_port) + "/llm/" + filename + ".llm" + "\r\n")

                # Logout from the display.
                display.write('logout' + "\r\n")

            except:

                print('FAILED TO RUN COMMANDS')

        except:

            print 'FAILED TO LOGIN'

        # Collect and discard session data (required)
        sess = display.read_all()
        print(sess)

        # Close the connection
        display.close()
        print('CONNECTION CLOSED')

    except:
        print'CONNECTION FAILED'
