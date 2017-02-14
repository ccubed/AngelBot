Overwatch
=========

This module allows you to grab stats for battletags across the US or EU region. You can write battletags as name#ID or name-ID. The API expects name-ID but we're used to name#ID.
* OWAPI now does multiregion automatically and AngelBot supports it.

Features
--------

ow <battletag>
    Pull stats for a battletag. Can be EU or US.

owheroes <battletag>
    This endpoint has changed. It now returns heroes and win rates, but no other data. This now returns any played hero on a battletag with a win rate greater than 0%.
