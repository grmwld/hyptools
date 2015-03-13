# Introduction #

This tool allows several users to send the information about the foreign planets they have fleets on.
Any other player can then search for a planet or a player, and learn what is the situation on that planet even if he has no fleets on it. That is basic info sharing.

# How does it work #

If a player with fleets on a planet can see every other fleets on that planet, that would be just great if his allies had a way to know the "planet status" without the first player having to actively copy past the info.
That's what hivemind does. It fetches info about fleets present on foreign planets (not owned ones for security reasons) and stores the data about present fleets on each of these planets in a database. Then any member with the required authorisation can perform a search on the database by player name or planet name, and learn where a player is present, or who is present on a given planet.

# Authorisation #

For now, the authorisation to use the tool is handled by Sopo.
Authentication is made through the HAPI.