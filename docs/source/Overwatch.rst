Overwatch
=========

This module allows you to grab stats for battletags across the US or EU region. You can write battletags as name#ID or name-ID. The API expects name-ID but we're used to name#ID.

**NOTE**: Cross region works now. I'm no longer forcing US lookups since the timeouts related to the EU lookups on Blizzard's end seem to be gone.

Features
--------

ow <battletag>
    Pull stats for a battletag. Can be EU or US.

owheroes <battletag>
    Pull stats for top 5 most played heroes for a battletag

owhero <battletag>:<hero>
    Pull stats for a specific hero for a battletag. This is where the easter eggs are. See if you can find some of my funny names for the heroes. Also accepts IDs.
    Course you can also just go look at my source and find the names, but that's no fun.