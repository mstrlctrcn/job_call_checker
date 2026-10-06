# job_call_checker
The purpose of this project is to check the websites for 3 different hiring halls (725, 538, 480) to gather information about all of their available calls and put it  into an easy to read format, thus saving me from navigating that information manually.

The scope expanded somewhat after beginning. After finding that I could harvest the data fairly easily, I opted to also text the data to myself on a set schedule. This worked for a while but problems arose with an update from the website and issues with the phone carrier and required some work to be re-done. 

I eventually settled on having the information emailed to me, to avoid carrier issues and was able to access an rss feed rather than the raw website to avoid 403 issues.

Currently the program works flawlessly. In the future I intend to add more data to the program, but until that data is posted for me to evaluate how to extract it, that portion is on hold. 

After discovering GitHub was able to run code on its own, I added a workflow so that the code self-executes on a set schedule and I receive a daily (excluding weekends) update on the job postings through my email now. Very pleased I was able to accomplish all this. It's a minor convenience, but it is confidence-building to know that I was able to make it happen.
