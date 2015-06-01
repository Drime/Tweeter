# Build the required data for the llm_writer
def build_llm(tweets):

    # Separator between tweet-messages
        tweet = ' | '

        # Selector
        i = 1

        # If total tweet length is less then 200 characters an other tweet is added (1 tweet is max 140 characters).
        while len(tweet) < 200 and i < tweets.total:

            try:
                # Always display a 'storing' if present.
                if tweets.storingen >= i:

                    # Append the storing to tweet, apply [STORING] notifier in front.
                    tweet += "[STORING]" + str(tweets.storingtweets[i] + " | ")

                # If no more 'storing' available use normal tweets.
                else:

                    # Append the (normal) tweet
                    tweet += str(tweets.normaltweets[i] + " | ")

            except:
                # If fail continue to next tweet.
                tweet

            # Increase the selector (next tweet)
            i += 1

        # Build the LLM file for the display and host it locally.
        write_llm(tweet, str(tweets.total), str(tweets.storingen))

# Write the LLM file
def write_llm(tweet, tweets, storing):
    # The resulting file to be transported to the display.
    with open("llm/twitter_test.llm", "w") as fout:

        # Open read-only to avoid tempering.
        with open("display_template", "r") as fin:
            for line in fin:
                if '%storing%' in line:
                    fout.write(line.replace('%storing%', storing))
                elif '%tweet%' in line:
                    fout.write(line.replace('%tweet%', tweet))
                elif '%tweets%' in line:
                    fout.write(line.replace('%tweets%', tweets))
                else:
                    # Write the normal line.
                    fout.write(line)
