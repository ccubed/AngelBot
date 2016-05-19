AniList
=======

Have you ever wanted to look up anime details while on discord? No? Oh well I have, so I made a module to do that. Since I intend to some day also support hummingbird.me, I have prefaced these commands with an a in addition to the server prefix you define or the $. The hummingbird commands will be prefixed with an h. This is to be able to discern which service the commands will use because otherwise they're basically going to look exactly the same.

**NOTE:** Anilist makes no guarantees about adult content. I also don't filter by that tag. Even if I did filter they don't even make a guarantee that all adult content is appropriately marked adult. So case in point: This can return NSFW/Adult content, you have been warned.

**Note 2:** I had to write a preprocessor for the anilist profiles due to the HTML content messing with discord formatting. It can take a little bit of time for a user profile to return because of that.

aanime [name or id]
    Search for an anime based on name or id.

acharacter [name or id]
    Search for a character.

amanga [name or id]
    Search for a manga.

acurrent
    Return the ten most popular currently airing anime on AniList.

awaifu [name or id]
    A fun command. Just outputs your waifu and a message declaring your undying devotion.

ahusbando [name or id]
    Equal Opportunity! Declare your devotion for your husbando! Complete with pic.

auser
    **OAUTH Required**: Pulls your user details

asuer [username or id]
    Pulls the details of another user

anotifications
    **OAUTH Required**: Pulls up to 10 notifications off your profile