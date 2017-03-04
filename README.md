# tornadoWS-with-tweepy
Combining Tornado WebSocket and Tweepy Streaming

To run:

<code> python wsapp.py </code>

<code> python -m SimpleHTTPServer 3000 </code>

In the browser:

localhost:3000

If the browser gives error modify index.html line 33: 

*  <code>ws://localhost:8888/ws</code> to <code>ws://yourIP:8888/ws</code>
  
*  in the browser change localhost with your internal address IP (yourIP:3000)

In the browser you will see the filtered tweets (tweets with #dataviz hashtag) coming from the server. New tweets are appended at the bottom of the list.





