#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from google.appengine.api import memcache
from google.appengine.ext import db
from hmdb import Planet
from hmdb import Player
from hmdb import Fleet


class Updater:
    def __init__(self, raw_data=None):
        self.__raw_data_list = raw_data.split('&')[1:]
        self.__chunk_list = []
        self.gcounter = 0
        self.pcounter = 0
#        self.__tmp_fleet = None
#        self.__tmp_planet = None

    def chop(self, size):
        """
        Splits the data list in <lenght> elements long lists
        """
        n_chunks = len(self.__raw_data_list)/size
        for i in range(n_chunks):
            self.__chunk_list.append(self.__raw_data_list[i*size:i*size+size])
        self.__chunk_list.append(self.__raw_data_list[(i+1)*size:])

    def getChunkList(self):
        """
        returns the list of chunks
        """
        return self.__chunk_list

    def update(self, chunk):
        """
        Parses the chunk given as first argument, and updates the database
        with the extracted values
        """
        first_planet = True
        first_fleet = True
#        if self.__tmp_fleet:
#            fleet = self.__tmp_fleet
#            first_fleet = False
#        if self.__tmp_planet:
#            planet = self.__tmp_planet
#            first_planet = False
        tmp_fleet = memcache.get("tmp_fleet")
        tmp_planet = memcache.get("tmp_planet")
        if tmp_fleet:
            fleet = tmp_fleet
            first_fleet = False
        if tmp_planet:
            planet = tmp_planet
            first_planet = False
        for info in chunk:
            self.gcounter += 1
            value = info.split('=')[1]
# Planet
            if info.startswith('planet'):
                self.pcounter += 1
                qf = Fleet.gql('WHERE location_name = :1', value.lower())
                db.delete(qf.fetch(50))
                if not first_planet:
                    planet.put()
                planet = Planet(key_name='_'.join(['planet', value.lower()]),
                                name=value)
                first_planet = False
# Stasis
            elif info.startswith('stasis'):
                    planet.stasis = value
# Fleet ID
            elif info.startswith('fleetid'):
                if not first_fleet:
                    fleet.put()
                fleet = Fleet(key_name='_'.join(['fleet', value]),
                              location=planet,
                              location_name=planet.name.lower())
                first_fleet = False
# Fleet race
            elif info.startswith('frace'):
                    fleet.race = value
# Fleet owner
            elif info.startswith('owner'):
                tmpq = db.GqlQuery("SELECT * FROM Player WHERE name = :1", value)
                player = tmpq.get()
                if not player:
                    player = Player(key_name='_'.join(['player', value.lower()]),
                                    name=value)
                    player.put()
                fleet.owner = player
                fleet.owner_name = value.lower()
# Defend
            elif info.startswith('defend'):
                    fleet.defend = value
# Camouflage
            elif info.startswith('camouf'):
                    fleet.camo = value
# Mass bombing
            elif info.startswith('bombing'):
                    fleet.bombing = value
# Scouts
            elif info.startswith('scou'):
                fleet.scouts = value
# Cruisers
            elif info.startswith('crui'):
                fleet.cruisers = value
# Bombers
            elif info.startswith('bomb'):
                fleet.bombers = value
# Destroyers
            elif info.startswith('dest'):
                fleet.destroyers = value
# Carried armies
            elif info.startswith('carmies'):
                fleet.carmies = value
# Ground armies
            elif info.startswith('garmies'):
                fleet.garmies = value
        planet.put()
        fleet.put()
        memcache.set_multi({
            "fleet": fleet,
            "planet": planet},
            key_prefix="tmp_", time=200)
#        self.__tmp_fleet = fleet
#        self.__tmp_planet = planet


def main():
    pass

if __name__ == '__main__':
    sys.exit(main())