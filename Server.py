import SimpleHTTPServer, BaseHTTPServer
import socket
import thread
import Twitter
import time
import Settings
import Update
import LLM

#The HTTP server which will be started in a seperated thread.
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
    httpd = StoppableHTTPServer(("0.0.0.0",8080), SimpleHTTPServer.SimpleHTTPRequestHandler)
    thread.start_new_thread(httpd.serve, ())





    #The loop for retrieving tweets
    while True:

        print("Collecting tweets!")

        #Retrieves the messages container.
        tweets = Twitter.get_tweets()


        tweet = ' | '
        i = 1

        while len(tweet) < 200 and i < tweets.total:


            try:
                if tweets.storingen >= i:
                    tweet += "[STORING]" + str(tweets.storingentweets[i] + " | ")

                else:

                    tweet += str(tweets.normaltweets[i] + " | ")
                i += 1
            except:
                i += 1
        print('tweet is long: ' + str(len(tweet)))


        LLM.create_llm(tweet, str(tweets.total), str(tweets.storingen))

        print(Update.update_display("twitter_test"))

        time.sleep(Settings.tweet_loop)

    #Stops the HTTP server that is serving llm files.
    httpd.stop()
