#Open the twitter template
def create_llm(tweet, tweets, storing):

    #The resulting file to be transported to the display.
    with open("llm/twitter_test.llm", "w") as fout:

        #Open read-only to avoid tempering.
        with open("display_template", "r") as fin:
            for line in fin:
                if '%storing%' in line:
                    fout.write(line.replace('%storing%', storing))
                elif '%tweet%' in line:
                    fout.write(line.replace('%tweet%', tweet))
                elif '%tweets%' in line:
                    fout.write(line.replace('%tweets%', tweets))
                else:
                   #Write the normal line.
                   fout.write(line)