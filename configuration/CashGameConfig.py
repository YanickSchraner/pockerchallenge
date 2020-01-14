import os
from datetime import datetime
from typing import Dict
import locale

from baseline.BaselinePokerPlayer import BaselinePlayer
from baseline.CallBaselinePokerPlayer import CallBaselinePlayer
from baseline.RandomPokerPlayer import RandomPlayer

from pypokerengine.api.game import setup_config, start_poker

locale.setlocale(locale.LC_ALL, '')


class CashGameConfig():

    def __init__(self, initial_stack: int = 100, small_blind_amount: int = 1, min_table_size: int = 2,
                 evaluations: int = 1000000, log_file_location: str = './logs'):
        now = datetime.strftime(datetime.now(), "%d.%m.%Y-%H:%M:%S")
        self.log_file_location = os.path.join(log_file_location, f"evaluation_{now}.json")
        self.initial_stack = initial_stack
        self.config = setup_config(max_round=evaluations, initial_stack=initial_stack, small_blind_amount=small_blind_amount)
        self.min_table_size = min_table_size
        self.evaluations = evaluations
        self.player_final_stack = {}
        self.baselines = [BaselinePlayer, CallBaselinePlayer, RandomPlayer]

    def run_evaluation(self, verbose: int = 0) -> Dict[str, int]:
        self._fill_up_with_baseline_player()
        game_result = start_poker(self.config, verbose=verbose, cashgame=True, log_file_location=self.log_file_location)
        for player in game_result['players']:
            self.player_final_stack[player['name']] = player['cashgame_stack']
        self.player_final_stack = {k: v for k, v in
                                   sorted(self.player_final_stack.items(), key=lambda item: item[1], reverse=True)}
        for rank, (name, stack) in enumerate(self.player_final_stack.items()):
            print(f"{rank + 1:2}. Player: {name:>25}, Stack: {stack:n}")
        return self.player_final_stack


    def register_player(self, name: str, algorithm: BaselinePlayer):
        self.config.register_player(name=name, algorithm=algorithm)


    def _get_config(self):
        self._fill_up_with_baseline_player()
        return self.config


    def _fill_up_with_baseline_player(self):
        for i in range(max(self.min_table_size - len(self.config.players_info), 1)):
            player = self.baselines[i % len(self.baselines)]()
            self.config.register_player(name=f"{str(player)}{i}", algorithm=player)
