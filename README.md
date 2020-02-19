# poker challenge
In this poker challenge, you will compete against other bachelor students in a mode similar to cash game.
You will start each round with a stack of 200 and we will sum up your total win/loss over all of the played hands.
If we simulate 100 hands with 3 players participation your maximum win over the 100 hands is equal to:
100 hands * 2 opponents * 200 stack = 40'000.
Your maximum loss is equal to: 100 hands * 200 stack = -20'000

The ranking is given by the sum of your win/loss compared to your opponents.

We reset the stack at the beginning of every round so that every player has to participate in all played poker hands.

We set the small blind to 1, the big blind to 2 and the initial stack to 200.

The evaluation will be carried out in parallel to save time. Take this into account when thinking about capturing statistics over your opponents' behavior.
It is planned to evaluate 1 million poker hands, but this is not fixed yet.

Have fun participating in this challenge 👩‍💻👨‍💻💸🎉 and do not forget to do literature research 📚🤓.

# Issues
If you have an issue or need help then open an issue on GitHub. We will get back to you.

# Poker engine
We used the [PyPokerEngine](https://github.com/ishikota/PyPokerEngine) as a base implementation. We fixed some issues and improved the performance. The forked PyPokerEngine is available [here](https://github.com/YanickSchraner/PyPokerEngine).

# Create your bot
To create your own but you have to extend the `BasePokerPlayer` class. There are 3 example baseline implementations given in the baseline directory.

You have to implement 7 methods. One is just used as a string representation of your bot, the `declare_action` is used to specify your next action. There are 5 methods used to provide your bot with messages from the table. You do not have to use them, but they may be useful.

Make sure that your implementation is located in the `agent` module, otherwise the evaluation on AICrowd will fail.

Below you find a minimal implementation of the `BasePokerPlayer`:
```
class MyBot(BasePokerPlayer):
    """
    Documentation for callback arguments given here:
    https://github.com/ishikota/PyPokerEngine/blob/master/AI_CALLBACK_FORMAT.md
    """

    def __str__(self):
        return "MyBot"

    def declare_action(self, valid_actions: List[Dict[str, Union[int, str]]], hole_card: List[str],
                       round_state: Dict[str, Union[int, str, List, Dict]]) -> Tuple[Union[int, str], Union[int, str]]:
        """
        Define what action the player should execute.
        :param valid_actions: List of dictionary containing valid actions the player can execute.
        :param hole_card: Cards in possession of the player encoded as a list of strings.
        :param round_state: Dictionary containing relevant information and history of the game.
        :return: action: str specifying action type. amount: int action argument.
        """
        return 'call', 0

    def receive_game_start_message(self, game_info: Dict[str, Union[int, Dict, List]]) -> None:
        """
        Called once the game started.
        :param game_info: Dictionary containing game rules, # of rounds, initial stack, small blind and players at the table.
        """
        pass

    def receive_round_start_message(self, round_count: int, hole_card: List[str],
                                    seats: List[Dict[str, Union[str, int]]]) -> None:
        """
        Called once a round starts.
        :param round_count: Round number, in Cash Game always 1.
        :param hole_card: Cards in possession of the player.
        :param seats: Players at the table.
        """
        pass

    def receive_street_start_message(self, street: str, round_state: Dict[str, Union[int, str, List, Dict]]) -> None:
        """
        Gets called at every stage (preflop, flop, turn, river, showdown).
        :param street: Game stage
        :param round_state: Dictionary containing the round state
        """
        pass

    def receive_game_update_message(self, action: Dict[str, Union[str, int]],
                                    round_state: Dict[str, Union[int, str, List, Dict]]) -> None:
        """
        Gets called after every action made by any of the players.
        :param action: Dict containing the player uuid and the executed action
        :param round_state: Dictionary containing the round state
        """
        pass

    def receive_round_result_message(self, winners: List[Dict[str, Union[int, str]]],
                                     hand_info: [List[Dict[str, Union[str, Dict]]]],
                                     round_state: Dict[str, Union[int, str, List, Dict]]) -> None:
        """
        Called at the end of the round.
        :param winners: List of the round winners containing the stack and player information.
        :param hand_info: List containing a Dict for every player at the table describing the players hand this round.
        :param round_state: Dictionary containing the round state
        """
        pass
```


**Very important**: Keep your wall time to decide for action short, otherwise we will not be able to evaluate 1 million poker hands in a reasonable time. At the moment this is a soft limit, but we may enforce it in the future. Aim for a max. time of 0.04 seconds per call of `declare_action`.

# Baselines
Take a look at our provided baselines in the baselines directory. You can evaluate your implementation against them.
We may provide more elaborated baselines in the future.
You can use the `ConsolePlayer` to join the poker table yourself and play against the baselines or your implementation.

# Evaluation on AICrowd
To load your poker bot you have to add an entry to the `evaluation_config.json` file:
In the `players` section you have to add an entry like `<ModuleName>`: `<ClassName>` (ModuleName = Python file name without .py)

Example:
```
{
  "players": {
    "MyBot": "MyBotPlayer"
  },
  "baselines": {
    "BaselinePokerPlayer": "BaselinePlayer",
    "CallBaselinePokerPlayer": "CallBaselinePlayer",
    "RandomPokerPlayer": "RandomPlayer"
  },
  "n_evaluations": 100000,
  "small_blind": 1,
  "log_file_location": "./logs"
}
```

You do not have to change the other config parameters.

# Allowed frameworks
To run the evaluation we have to be able to execute all provided implementation on our server automatically. As we do not want to fight with versioning issues and installation of frameworks we have to restrict the use of frameworks.
Please make sure that your bot can run using only the dependencies listed below:
- Python 3.6
- Tensorflow 2.1
- Pytorch 1.4
- scikit-learn 0.22.1

If you still want to use other dependencies then open an issue on GitHub with a reason why and for what purpose.

# Run evaluation local
To run the evaluation on your environment you can use the `runEvaluation.py` file.
On line #8 you can specify how many hands you want to evaluate and how many players should sit at the table. You can register / place your own player at the table using `config.register_player("Name", YourClass())`. The empty seats will be filled up with available baseline implementations. You can participate in the evaluation through the ConsolePlayer by registering it `config.register_player("Console", ConsolePlayer())`.
You may register as many players in your local evaluation as you wish.
