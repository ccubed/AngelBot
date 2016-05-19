AniList OAuth2
==============

AniList has an interesting Oauth2 setup. It uses 1 hour tokens that the bot refreshes seamlessly in the background.
This is what those tokens are used for. Note, not all these features are necessarily coded yet.


Profiles
--------
If you call the auser command without inputting a name it will grab your profile, this requires OAuth.

Follows/Notifications
---------------------
In order to show you your notifications and allow you to follow other users, OAuth is required.

Adding Anime
------------
Self explanatory.

Marking Shows Watched
---------------------
Self explanatory.

Favorites
---------
Modifications to and Retrieving of favorite anime/manga.

Airing
------
A special endpoint that returns your currently watching currently airing anime as defined by AniList's filters. It required OAuth. Don't ask me.

Lists
-----
Retrieval of Anime and Manga Lists. Not the same as changing episode or show status. This is simply for display.

