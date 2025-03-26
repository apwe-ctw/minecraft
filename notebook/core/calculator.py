from dataclasses import dataclass
from datetime import datetime

from core.utils import Fund, Sprite, ActionType

import time
import random
import RPi.GPIO as GPIO

@dataclass
class Calculator:
    initial_deposit: float = 0
    contribution_amount: float = 0
    investment_timespan: int = 0
    fund: Fund = Fund.HONG_KONG_ETF
    future_balance: float = 0
    contribution_period: int = 12
    compound_period: int = 12
    sprite: Sprite = Sprite.HEARTBEAT
    goal: float = 1000000

        
    def set_lights(self):
        """
        Set the lights up!
        """
        LED = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED, GPIO.OUT) 

        GPIO.output(LED, True)
        time.sleep(10.0)

        GPIO.cleanup() 
        return None
    
    def get_sprite(self):
        """
        Used to retrieve the sprite displayed when target investment reached
        """
        return self.sprite.value

    def get_funds(self):
        """
        Used to retrieve a list of available funds
        :return:
        """
        return [i.value for i in Fund]

    def get_selected_fund(self):
        """
        Retrieves the current fund selected by the user
        """
        return {"name": self.fund.name, "returns": self.fund.returns}

    def get_amount(self, field: str):
        """
        Used to retrieve values from the calculator. E.g. initial deposit
        :param field: name of the field
        :return:
        """
        return getattr(self, field)

    def change_fund(self, name: str):
        """
        Change the fund selected for the calculation
        :param name: Name of the fund
        :return:
        """
        self.fund = Fund.value_from(name)

    def change_amount(self, field: str, value, action_string: str):
        """
        Used to change a property on the calculator. E.g. initial deposit, contribution amount e.t.c
        :param field: calculator property
        :param value: Any
        :param action_string: ADD | SUBTRACT | SET
        :return: the updated field value
        """
        action = ActionType.value_from(action_string)
        change = getattr(self, field)

        if action == ActionType.ADD:
            change += value
        elif action == ActionType.SUBTRACT:
            change -= value
        elif action == ActionType.SET:
            change = value

        if change >= 0:
            setattr(self, field, change)
            return change
        return getattr(self, field)

    def calculate_future_values(self):
        """
        Calculates the future value
        """
        current_year = datetime.now().year
        labels = [year for year in range(current_year, current_year + int(self.investment_timespan))]
        principal_dataset = {
            "label": 'Total Principal',
            "backgroundColor": 'rgb(0, 123, 255)',
            "data": []
        }
        earnings_dataset = {
            "label": "Total Earnings",
            "backgroundColor": 'rgb(23, 162, 184)',
            "data": []
        }

        self.future_balance = 0

        for time in range(1, self.investment_timespan + 1):
            principal = self.initial_deposit + (self.contribution_amount * self.contribution_period * time)
            earnings = 0
            balance = principal
            estimated_return = self.fund.returns / 100

            if estimated_return:
                gains = (1 + estimated_return / self.compound_period) ** (self.compound_period * time)
                compound_earnings = self.initial_deposit * gains
                contribution_earnings = self.contribution_amount * (gains - 1) / (estimated_return / self.contribution_period)
                earnings = compound_earnings + contribution_earnings - principal
                balance = compound_earnings + contribution_earnings

            self.future_balance = balance
            principal_dataset['data'].append(round(principal, 2))
            earnings_dataset['data'].append(round(earnings, 2))

        return {
            "labels": labels,
            "datasets": [principal_dataset, earnings_dataset],
        }
