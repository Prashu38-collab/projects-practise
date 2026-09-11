const choiceButtons =
    document.querySelectorAll(".choice-button");

const playerChoiceDisplay =
    document.querySelector("#player-choice");

const computerChoiceDisplay =
    document.querySelector("#computer-choice");

const result =
    document.querySelector("#result");

const message =
    document.querySelector("#message");

const playerScore =
    document.querySelector("#player-score");

const computerScore =
    document.querySelector("#computer-score");

const drawScore =
    document.querySelector("#draw-score");

const resetButton =
    document.querySelector("#reset-button");


let scores = {
    player: 0,
    computer: 0,
    draw: 0
};


const emojis = {
    rock: "🪨",
    paper: "📄",
    scissors: "✂️"
};


choiceButtons.forEach(button => {

    button.addEventListener("click", async () => {

        const choice =
            button.dataset.choice;

        await playGame(choice);

    });

});


async function playGame(playerChoice) {

    try {

        result.textContent = "Computer is thinking...";

        message.textContent = "";

        playerChoiceDisplay.textContent =
            emojis[playerChoice];

        computerChoiceDisplay.textContent =
            "❓";


        const response = await fetch("/play", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                choice: playerChoice
            })

        });


        const data = await response.json();


        if (!response.ok) {

            throw new Error(data.error);

        }


        computerChoiceDisplay.textContent =
            emojis[data.computer];


        updateGame(data.winner);

        updateScores();

    }

    catch (error) {

        console.error(error);

        result.textContent =
            "Something went wrong";

        message.textContent =
            error.message;

    }

}


function updateGame(winner) {

    if (winner === "player") {

        result.textContent = "You Win! 🎉";

        message.textContent =
            "Nice move! You beat the computer.";

        scores.player++;

    }

    else if (winner === "computer") {

        result.textContent = "Computer Wins 🤖";

        message.textContent =
            "The computer got you this round.";

        scores.computer++;

    }

    else {

        result.textContent = "It's a Draw 🤝";

        message.textContent =
            "Both players chose the same thing.";

        scores.draw++;

    }

}


function updateScores() {

    playerScore.textContent =
        scores.player;

    computerScore.textContent =
        scores.computer;

    drawScore.textContent =
        scores.draw;

}


resetButton.addEventListener("click", resetGame);


function resetGame() {

    scores = {
        player: 0,
        computer: 0,
        draw: 0
    };


    playerChoiceDisplay.textContent =
        "❓";

    computerChoiceDisplay.textContent =
        "❓";


    result.textContent =
        "Make your move";


    message.textContent =
        "Choose rock, paper, or scissors below.";


    updateScores();

}