import time

from configuration.CashGameConfig import CashGameConfig

if __name__ == '__main__':
    start = time.time()
    config = CashGameConfig(evaluations=1000)
    config.run_evaluation()
    end = time.time()
    time_taken = end - start
    print('Evaluation Time: ', time_taken)
