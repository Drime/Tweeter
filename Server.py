import SimpleHTTPServer, BaseHTTPServer
import socket
import thread
import Twitter
import time
import Settings

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

if __name__=="__main__":

    #Create an HTTP server to host the .LLM files
    httpd = StoppableHTTPServer(("127.0.0.1",8080), SimpleHTTPServer.SimpleHTTPRequestHandler)
    thread.start_new_thread(httpd.serve, ())


    #The loop for retrieving tweets
    while True:
        print("Collecting tweets!")

        #Retrieves the messages container.
        tweets = Twitter.get_tweets()

        #Do something for every tweet in the container.
        for tweet in tweets:
            print(tweet)

        time.sleep(Settings.tweet_loop)

    httpd.stop()
