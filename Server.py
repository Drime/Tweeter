import SimpleHTTPServer
import BaseHTTPServer
import socket
import thread
import time

import Twitter
import Settings
import Update
import LLM
import Audio


# The HTTP server which will be started in a separated thread.
class StoppableHTTPServer(BaseHTTPServer.HTTPServer):
    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)
        self.socket.settimeout(1)
        self.run = True

    def get_request(self):
        while self.run:
            try:
                sock, addr = self.socket.accept()
                sock.settimeout(None)
                return (sock, addr)
            except socket.timeout:
                pass

    def stop(self):
        self.run = False

    def serve(self):
        while self.run:
            self.handle_request()


if __name__ == "__main__":

    # Create an HTTP server to host the .LLM files
    httpd = StoppableHTTPServer(("0.0.0.0", Settings.server_port), SimpleHTTPServer.SimpleHTTPRequestHandler)
    thread.start_new_thread(httpd.serve, ())

    # Set a 'storing' counter for audio clips.
    storing_c = 0

    # Wash, Rinse, Repeat.
    while True:

        print("Collecting tweets!")

        # Retrieves the messages container.
        tweets = Twitter.get_tweets()

        # Create the llm file
        LLM.build_llm(tweets)

        # Send a message to the display to retrieve the LLM file.
        Update.update_display(Settings.filename)

        # Play audio when a 'storing' is discovered.
        if storing_c < tweets.storingen:

            # Play the audio file.
            Audio.storing()

            # Set the counter to the 'storing' level.
            storing_c = tweets.storingen

        # Wait for a set amount of time.
        time.sleep(Settings.tweet_loop)

    # Stops the HTTP server that is serving llm files.
    httpd.stop()
