from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

choices = ["rock", "paper", "scissors"]


def determine_winner(player, computer):
    if player == computer:
        return "draw"

    if (
        (player == "rock" and computer == "scissors")
        or (player == "paper" and computer == "rock")
        or (player == "scissors" and computer == "paper")
    ):
        return "player"

    return "computer"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/play", methods=["POST"])
def play():
    data = request.get_json()

    player_choice = data.get("choice")

    if player_choice not in choices:
        return jsonify({
            "error": "Invalid choice"
        }), 400

    computer_choice = random.choice(choices)

    winner = determine_winner(
        player_choice,
        computer_choice
    )

    return jsonify({
        "player": player_choice,
        "computer": computer_choice,
        "winner": winner
    })


if __name__ == "__main__":
    app.run(debug=True)