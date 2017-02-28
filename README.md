# APIwrapper
wrapper API that communicates with the BuzzFeed API that lets you query for articles in a slightly removed way


● How to compile / execute your code 

● How you tested your code (we love tests!) 

● Any design decisions that you made that we should know about 

● Any interesting algorithms/packages/etc. you used



Wrote this with python 2.7 on ubuntu 14.04.

Need to have Bottle Python Web Framework installed.

	sudo pip install bottle

I also used requests, json, and urllib.


main.py is executable. 
If it is not for some reason, type ch +x main.py into terminal.

Type ./main.py into the terminal. If that doesn't work, change the first line in main.py from "#!/usr/bin/python" to wherever your python interpreter is located.

Once it is running, open "localhost:8080/index" in a webbrowser.

In the terminal, fill out the prompts. After typing in the feed name, it should take a few seconds to load. After selecting 2 or 3, it should take several seconds to load.

Links to the articles that fit the parameters should be on localhost:8080/index.

If you want to test the program again without restarting it in the terminal, just refresh the webpage.

I created a class for feeds and a class for buzzes.

I had a problem with duplicates appearing in the json. I looked through it and there's duplicates on the webpages. I sorted out the duplicates at the initialization of the feed by using a dictionary and overloading the "equal to" operator in the buzz object so when it compared buzzes, it would compare it by the uri since each buzz must have a unique uri to be a unique article. I also overloaded the "less than" and the "greater than or equal to" operators to sort the buzz objects into alphabetical order (based on title), so it would be easier to see duplicates.

