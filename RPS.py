# Predict the opponent's next move from what followed the same recent
# sequence of rounds earlier in the match, then play the move that beats it.

BEATS = {"R": "P", "P": "S", "S": "R"}  # value beats key
N = 2  # how many past rounds form the pattern we look up


def player(prev_play, state={"rounds": [], "table": {}, "my_last": ""}):
    # An empty prev_play means a new match: wipe everything learned so far.
    if prev_play == "":
        state["rounds"] = []
        state["table"] = {}
        state["my_last"] = ""
    else:
        # Record the round that just finished as "my move + their move".
        rounds = state["rounds"]
        if len(rounds) >= N:
            # The N rounds before this one were followed by prev_play.
            key = "".join(rounds[-N:])
            counts = state["table"].setdefault(key, {"R": 0, "P": 0, "S": 0})
            counts[prev_play] += 1
        rounds.append(state["my_last"] + prev_play)

    # Look up what the opponent usually does after the last N rounds.
    guess = "R"
    if len(state["rounds"]) >= N:
        counts = state["table"].get("".join(state["rounds"][-N:]))
        if counts:
            guess = max(counts, key=counts.get)

    move = BEATS[guess]
    state["my_last"] = move
    return move