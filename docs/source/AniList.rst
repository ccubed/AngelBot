AniList
=======

Have you ever wanted to look up anime details while on discord? No? Oh well I have, so I made a module to do that. Since I intend to some day also support hummingbird.me, I have prefaced these commands with an a in addition to the server prefix you define or the $. The hummingbird commands will be prefixed with an h. This is to be able to discern which service the commands will use because otherwise they're basically going to look exactly the same.

**NOTE:** Anilist makes no guarantees about adult content. I also don't filter by that tag. Even if I did filter they don't even make a guarantee that all adult content is appropriately marked adult. So case in point: This can return NSFW/Adult content, you have been warned.

**More Notes:**  Gonna be honest here, It's not that great. I'm not sure how the titles are indexed but it is not a partial match search, you need to kind of know the title which makes it slightly less useful.

**And More:** So today I found out that there are actually characters, manga, staff, etc, with blank names. So yeah, if you see an id with no name that's not an error, that's the data being returned.

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