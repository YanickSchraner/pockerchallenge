import time

from baseline.ConsolePokerPlayer import ConsolePlayer
from configuration.CashGameConfig import CashGameConfig

if __name__ == '__main__':
    start = time.time()
    config = CashGameConfig(evaluations=1000, min_table_size=6)
    # config.register_player("Console", ConsolePlayer())
    config.run_evaluation()
    end = time.time()
    time_taken = end - start
    print('Evaluation Time: ', time_taken)
