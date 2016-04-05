Events
======

Introduction
============

This is an events module for the bot. It allows you to schedule raids, trials, roulettes and other various events. It also supports signups. As of this writing it doesn't support timezones because python, but that is being worked on.

Commands
========
$events
    Show a listing of all upcoming events

$raid [name] at [date] for [stage]
    Add an event for raid [name] at [date] for [stage]. [date] should have the format YYYY-MM-DD HH:MM. [stage] should be 1 for raids without multiple stages or whatever stage it is.
    Example: $raid Alexander Midas Savage at 2016-04-20 18:00 for 5

$roulette [name] at [date]
    Add an event for roulette [name] at [date]. [date] should have the format YYYY-MM-DD HH:MM.
    Example: $roulette Leveling at 2016-04-20 18:00

$trial [name] at [date] for [mode]
    Add an event for trial [name] at [date] for [mode]. [name] should be the name of the enemy, not the name of the trial. [date] shoudl be in the format YYYY-MM-DD HH:MM. [mode] should be normal, hard or extreme.
    Example: $trial Shiva at 2016-04-20 18:00 for Extreme

$other [name] at [date]
    Add an event that has nothing to do with any of hte other types. [name] should describe the event. [date] should..well, I've said that enough.
    Example: $other Wedding of Sora and Riku at 2016-04-20 16:00

$join [id] as [role] with [class]
    Join event [id] as [role] and note you're going as [class]. [role] should be 'DPS', 'Tank' or 'Healer.' [class] should be the name of your class.
    Example: $join 1 as DPS with Ninja

$wn [id]
     Who's needed for this [id]. Will return a breakdown of what roles are still needed.

$who [id]
    Who's going to [id]. Shows current signups. If the type isn't other, will also breakdown the classes and roles.