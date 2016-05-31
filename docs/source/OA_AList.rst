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

Lists
-----
Modifications to Anime and Manga lists of any kind required OAuth. Used for adding new Anime and Manga and changing status, review. ratings, etc.

