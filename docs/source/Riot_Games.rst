Riot Games
==========
**NOTE:** This does not function yet. I am waiting for Riot to approve my usage of the API.



This is an API for looking up information on League of Legends matches, players and champions. First some legal stuff.

Legalese
--------
I am legally required to tell you that:
    AngelBot isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.

Privacy Policy
--------------
I am also, per my agreement with Riot, legally required to tell you that I don't store any of your information on my app except for your discord user ID or Oauth token at most. Your user ID is easily obtainable by anyone with developer mode turned on. Your oauth tokens are encrypted (:doc:`Security`) and I don't have any intention of decrypting them for anyone. If someone did ask me for someone's token I would send them a nice cat meme back. I like cat meme's, don't you? If they got uppity and persistent I would simply delete your data and let you know who was asking after it before sending them a cease and desist from a lawyer, because I ain't got time for that shit. Do you? No? I didn't think so. So that's my privacy policy. If you want a TLDR version, then here goes.

**TLDR PRIVACY POLICY:** I don't store nothing, I don't have nothing and no you can't have it even if I did. So go away. Charles Click 2016 @ vertinext.com. Questions or Concerns can be addressed to CharlesClick@vertinext.com.

Features
--------
islolup
    Return the status for every shard in every region. Includes any known incidents.

lolstatus [region]
    Return the status for a specific region. Region should be one of na1 (North America), eu (Europe West), eun1 (EU Nordic and East), la1 (Latin America North), la2 (Latin America South), oc1 (Oceania), jp1 (Japan)

lolfree
    Return the current free rotation heros.

lolfreatures
    **NA Only**: Return the currently featured games, their team makeup, game mode, map and currently elapsed time.

lolrecent [summoner]
    **NA Only**: Return a list of recent games and whether or not they were a win or loss for summoner. Summoner can be a name or ID.

lolstats [summoner]
    **NA Only**: Return a summary of ranked and unranked stats for a summoner for the current season. Summoner can be a name or id.