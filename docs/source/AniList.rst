AniList
=======
**Module version:** Official Release 1.0

Have you ever wanted to look up anime details while on discord? No? Oh well I have, so I made a module to do that. Since I intend to some day also support hummingbird.me, I have prefaced these commands with an a in addition to the server prefix you define or the $. The hummingbird commands will be prefixed with an h. This is to be able to discern which service the commands will use because otherwise they're basically going to look exactly the same.

**NOTE:** Anilist makes no guarantees about adult content. I also don't filter by that tag. Even if I did filter they don't even make a guarantee that all adult content is appropriately marked adult. So case in point: This can return NSFW/Adult content, you have been warned.

**Note 2:** I had to write a preprocessor for the anilist profiles due to the HTML content messing with discord formatting. If you notice any profiles that either A) Mess up discord formatting or B) come out weird put in an issue about at it https://github.com/ccubed/AngelBot/issues . Be sure to include the username or user id.

That's it folks. As of now the features available in this module are the core feature set. Anything added past now will be by request or if I think it should be!

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

apeople [query]
    Searches AniList for users with names that match query

afollow [uid/name]
    **OAUTH Required**: Name needs to reduce down to one uid to work. Follows a user on AniList.

anilist [uid/name]
    Grab 20 random completed titles from a user's anime list. If there are less than 20, display the list.

amangalist [uid/name]
    Grab 20 random completed titles from a user's manga list. If there are less than 20, display the list.

awatch [id/name]
    **OAUTH Required**: Mark an anime as plan to watch on your anime list. Useful if you're on discord and someone pops up an anime that you want to look at later.

aread [id/name]
    **OAUTH Required**: Mark a manga as plan to read on your manga list. Useful if you're on discord and someone pops up an interesting manga that you want to check out.

anext [a or m]:[id or name]
    **OAUTH Required**: The first parameter should be an a if you're modifying anime or m if you're modifying manga. The second should be the name or ID of the anime or manga you want to add an episode watched/chapter read to. This will handle marking items completed as well if you've watched/read the last item.

awatching [uid/name]
    Grab 20 random titles from a user's now watching anime. If 20 or less, display the list.

areading [uid/name]
    Grab 20 random titles from a user's now reading manga. If 20 or less, display the list.