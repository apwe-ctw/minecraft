from __future__ import annotations
from enum import Enum
from typing import Optional


class ActionType(Enum):
    ADD = 'add'
    SUBTRACT = 'sub'
    SET = 'set'

    @staticmethod
    def value_from(name: str) -> Optional[ActionType]:
        return next(filter(
            lambda i: i.value == name,
            (i for i in ActionType)
        ))


class Sprite(Enum):
    BIRD = 'assets/bird.gif'
    CAKE = 'assets/cake.gif'
    ELEPHANT = 'assets/elephant.gif'
    FISH = 'assets/fish.gif'
    GAME = 'assets/game.gif'
    HEARTBEAT = 'assets/heartbeat.gif'
    PONY = 'assets/pony.gif'
    SHEEP = 'assets/sheep.gif'
    SNOW_FIGHT = 'assets/snow-fight.gif'
    STARWARS = 'assets/starwars.gif'
    NONE = ''


class Fund(Enum):
    HONG_KONG_ETF = ('Hong Kong ETF', 13.5)
    FREEDOM_FUND = ('Freedom Fund', 35)
    UNION_SP500_INDEX = ('Union SP500 Index Fund', 25)
    YU_LENG_1000_ETF = ('Yu Leng 100 ETF', 15)
    TANG_5000_ETF = ('Tang 5000 Trust ETF', 18)
    Niki_8864_T=('Niki 8864 T', 27)

    @property
    def returns(self):
        return self.value[1]

    @property
    def name(self):
        return self.value[0]

    @staticmethod
    def value_from(name: str) -> Optional[Fund]:
        return next(filter(
            lambda i: i.name == name,
            (i for i in Fund)
        ))
