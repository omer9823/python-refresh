let ws;
const statusArea = document.getElementById('status-area');
const startBtn = document.getElementById('start');
const hitBtn = document.getElementById('hit');
const standBtn = document.getElementById('stand');
const dealerCards = document.getElementById('dealer-cards');
const playerCards = document.getElementById('player-cards');
const advisorBasic = document.getElementById('advisor-basic');
const advisorCount = document.getElementById('advisor-count');
const advisorTrueCount = document.getElementById('advisor-truecount');
const balanceElem = document.getElementById('balance');
const betValueElem = document.getElementById('bet-value');
const chips = document.querySelectorAll('.chip');

let balance = 1000;
let bet = 25;

function setButtons(start, hit, stand) {
    startBtn.disabled = !start;
    hitBtn.disabled = !hit;
    standBtn.disabled = !stand;
}

function getSuitSymbol(suit) {
    switch (suit) {
        case 'Hearts': return '♥';
        case 'Diamonds': return '♦';
        case 'Clubs': return '♣';
        case 'Spades': return '♠';
        default: return '';
    }
}

function renderCards(container, cards) {
    container.innerHTML = '';
    cards.forEach(card => {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card';
        cardDiv.innerHTML = `
            <div>${card.rank}</div>
            <div class="suit">${getSuitSymbol(card.suit)}</div>
        `;
        container.appendChild(cardDiv);
    });
}

function resultMessage(result) {
    if (result === "dealer") return "Dealer wins!";
    if (result === "player") return "You win!";
    if (result === "push") return "Push (tie)!";
    if (result === "bust") return "You busted!";
    if (result === "none" || !result) return "";
    return result;
}

function showStatus(data) {
    if (data.error) {
        statusArea.textContent = "Error: " + data.error;
        return;
    }
    renderCards(playerCards, data.player_hand.cards);
    renderCards(dealerCards, data.dealer_hand.cards);
    advisorBasic.textContent = "Basic Strategy: " + (data.basic_advice ? data.basic_advice.toUpperCase() : '-');
    advisorCount.textContent = "Count-Adjusted: " + (data.count_advice ? data.count_advice.toUpperCase() : '-');
    advisorTrueCount.textContent = "True Count: " + (data.true_count !== undefined && data.true_count !== null ? data.true_count : '0.0');
    let output = "";
    if (data.result && data.result !== "none") {
        output += resultMessage(data.result) + " ";
    }
    if (data.message) {
        output += data.message;
    }
    statusArea.textContent = output;
}

function updateBalanceAndBet() {
    balanceElem.textContent = `$${balance}`;
    betValueElem.textContent = `$${bet}`;
}

chips.forEach(chip => {
    chip.addEventListener('click', function() {
        chips.forEach(c => c.classList.remove('selected'));
        chip.classList.add('selected');
        bet = parseInt(chip.getAttribute('data-bet'));
        updateBalanceAndBet();
    });
    // Default select $25
    if (parseInt(chip.getAttribute('data-bet')) === 25) {
        chip.classList.add('selected');
    }
});

updateBalanceAndBet();

startBtn.onclick = function() {
    if (!ws || ws.readyState !== 1) {
        ws = new WebSocket('ws://localhost:8000/ws/game');
        ws.onopen = () => {
            ws.send(JSON.stringify({action: 'start'}));
            setButtons(false, true, true);
        };
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            showStatus(data);
            if (data.result && data.result !== 'none') {
                setButtons(true, false, false);
            }
        };
        ws.onerror = (event) => {
            statusArea.textContent = "WebSocket connection error";
            setButtons(true, false, false);
        };
        ws.onclose = (event) => {
            setButtons(true, false, false);
        };
    } else {
        ws.send(JSON.stringify({action: 'start'}));
        setButtons(false, true, true);
    }
};

hitBtn.onclick = function() {
    if (ws && ws.readyState === 1) {
        ws.send(JSON.stringify({action: 'hit'}));
    }
};

standBtn.onclick = function() {
    if (ws && ws.readyState === 1) {
        ws.send(JSON.stringify({action: 'stand'}));
    }
};