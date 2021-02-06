# project1-sap258

# Requirements:
For this project we need to install Flask, os and requests library.
We can install them by using the command "npm install".
Create a Spotify developers account: https://developer.spotify.com/ and create an app.
Create a Guthub account if you don't have one already.
Create a repository on Github with any name.


# After finishing the requirements, follow these steps:
1. First we need to import these libraries into our code.
2. After importing them we can make a separate file called ".env"
3. In this file we need to store our "Client ID" and "Client Secret" keys which are in your spotify app.
4. We can now import those keys using os library. This way we are hiding the keys so that no one can see them.
5. Now we have to make a POST request to the spotify server using these keys to get the access token.
6. After getting the access token we can get artist top tracks.
7. Now we can choose a random track and send it to our html file to display it on a webpage. 

# Some of the issues I had for this project are:
1. Json response was hard to trace through and this website is really useful: https://jsonformatter.curiousconcept.com/.
2. CSS file was not updating and doing a hard refresh(ctrl5) fixed the problem.
3. When I was sending the request to the server to get the track preview of the song. For this request the server needs an access token and the track id. For some reason I was getting an error form the server when I passed the id in the parameters. So I added the id in the url and that seems to fix the issue. 

# Some of the known issues of this project:
If the server does not have a track preview then it will display an empty track. Some of the tracks have no preview of the song so in that case the page will display an empty track. 
The artist ids are hardcoded so if the id are changed by spotify then this program will not work. 

# How can I improve this project:
Instead of hardcoding the ids of the artist we can get user input of which artist they want to listen to and then request the server for the tracks. This will give users accessibility to who they want to listen to. 
Displaying more information about the song or artist. We can also use look up related articles about the song or artist using the new york times api. 
