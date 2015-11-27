#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otree_save_the_change.mixins import SaveTheChange

from otree.db import models
from otree.common_internal import get_models_module, get_players


class BaseGroup(SaveTheChange, models.Model):
    """Base class for all Groups.
    """

    _is_missing_players = models.BooleanField(default=False)

    id_in_subsession = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return str(self.pk)

    _players = []

    def _get_players(self, refresh_from_db=False):
        return get_players(
            self, order_by='id_in_group',
            refresh_from_db=refresh_from_db
        )

    def get_players(self):
        return self._get_players()

    def get_player_by_id(self, id_in_group):
        for p in self.get_players():
            if p.id_in_group == id_in_group:
                return p
        raise ValueError('No player with id_in_group {}'.format(id_in_group))

    def get_player_by_role(self, role):
        for p in self.get_players():
            if p.role() == role:
                return p
        raise ValueError('No player with role {}'.format(role))

    def set_players(self, players_list):
        for i, player in enumerate(players_list, start=1):
            player.group = self
            player.id_in_group = i
            player.save()
        # so that get_players doesn't return stale cache
        self._players = players_list
    #assigning position to player in group
    def set_players_by_position(self, players_list,minp,maxp):
        for index, player in enumerate(players_list, start=1):
            player.group = self
            # for single player check and set position id
            if(minp==maxp):
                l=1
                for p in self.get_players():
                    if int(p.id_in_group) == int(minp):
                        l=l+1                  
                if l==1:
                    player.id_in_group =int(minp)
                    player.save()
            else:
                for i in range(int(minp),int(maxp)+1):
                    l=1
                    for p in self.get_players():
                        if p.id_in_group == i:
                            l=l+1   
                    if l== 1:        
                        player.id_in_group =i
                        player.save()
                        break                 
        self._players = players_list
    #check position in group is available
    def check_availabilty(self, players_list,minp,maxp):
        #group is empty
        if len(players_list)==0:
            return 1

        for index, player in enumerate(players_list, start=1):
            player.group = self
            # for single player check and set position id
            if(minp==maxp):
                l=1
                for p in self.get_players():
                    if p.id_in_group == int(minp):
                        l=l+1  
                if l==1:
                    return 1
                else:
                    return 0
            #for session type or range type players
            else:
                for i in range(int(minp),int(maxp)+1):
                    l=1                    
                    for p in self.get_players():
                        if p.id_in_group == i:
                            l=l+1                       
                    if l== 1:     
                        return 1
                        break    
        # position in group is not available
        return 0    
        # self._players = players_list

    def in_previous_rounds(self):

        qs = type(self).objects.filter(
            session=self.session,
            id_in_subsession=self.id_in_subsession,
        )

        round_list = [
            g for g in qs if
            g.subsession.round_number < self.subsession.round_number
        ]

        if not len(round_list) == self.subsession.round_number - 1:
            raise ValueError(
                'This group is missing round history. '
                'You should not use this method if '
                'you are rearranging groups between rounds.'
            )

        round_list.sort(key=lambda grp: grp.subsession.round_number)

        return round_list

    def in_all_rounds(self):
        return self.in_previous_rounds() + [self]

    @property
    def _Constants(self):
        return get_models_module(self._meta.app_config.name).Constants
