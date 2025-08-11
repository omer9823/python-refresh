let ws;
const statusArea = document.getElementById('status-area');
const startBtn = document.getElementById('start');
const hitBtn = document.getElementById('hit');
const standBtn = document.getElementById('stand');
const splitBtn = document.getElementById('split');
const doubleBtn = document.getElementById('double');
const dealerCards = document.getElementById('dealer-cards');
const playerHandsWrapper = document.getElementById('player-hands');
const advisorBasic = document.getElementById('advisor-basic');
const advisorCount = document.getElementById('advisor-count');
const advisorTrueCount = document.getElementById('advisor-truecount');
const balanceElem = document.getElementById('balance');
const betValueElem = document.getElementById('bet-value');
const chips = document.querySelectorAll('.chip');

let balance = 1000;
let bet = 25;

function setButtons({ start, hit, stand, split, double }) {
    startBtn.disabled = !start;
    hitBtn.disabled = !hit;
    standBtn.disabled = !stand;
    splitBtn.disabled = !split;
    doubleBtn.disabled = !double;
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

function renderPlayerHands(player_hands, activeIndex) {
    playerHandsWrapper.innerHTML = '';
    player_hands.forEach((hand, idx) => {
        const block = document.createElement('div');
        block.className = 'hand-block' + (idx === activeIndex ? ' active' : '');

        const header = document.createElement('div');
        header.className = 'hand-header';
        header.innerHTML = `<span>Hand ${idx + 1}/${player_hands.length}</span><span>Total: ${hand.total}${hand.is_blackjack ? ' (Blackjack)' : ''}${hand.is_bust ? ' (Bust)' : ''}</span>`;
        block.appendChild(header);

        const row = document.createElement('div');
        row.className = 'cards-row';
        renderCards(row, hand.cards);
        block.appendChild(row);

        playerHandsWrapper.appendChild(block);
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

function updateFromState(data) {
    // Dealer and hands
    renderCards(dealerCards, data.dealer_hand.cards || []);
    renderPlayerHands(data.player_hands || [], data.active_hand_index || 0);

    // Advisor
    advisorBasic.textContent = "Basic Strategy: " + (data.basic_advice ? data.basic_advice.toUpperCase() : '-');
    advisorCount.textContent = "Count-Adjusted: " + (data.count_advice ? data.count_advice.toUpperCase() : '-');
    advisorTrueCount.textContent = "True Count: " + (data.true_count !== undefined && data.true_count !== null ? data.true_count : '0.0');

    // Status
    let msg = data.message || '';
    if (data.round_over && Array.isArray(data.final_results)) {
        const resultsText = data.final_results.map((r, i) => `Hand ${i + 1}: ${resultMessage(r)}`).join(' | ');
        msg = (msg ? msg + ' ' : '') + resultsText;
    }
    statusArea.textContent = msg;

    // Buttons
    if (data.round_over) {
        setButtons({ start: true, hit: false, stand: false, split: false, double: false });
    } else {
        setButtons({
            start: false,
            hit: true,
            stand: true,
            split: !!data.can_split,
            double: !!data.can_double,
        });
    }
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
    if (parseInt(chip.getAttribute('data-bet')) === 25) {
        chip.classList.add('selected');
    }
});

updateBalanceAndBet();

startBtn.onclick = function() {
    if (!ws || ws.readyState !== 1) {
        ws = new WebSocket('ws://localhost:8000/ws/game');
        ws.onopen = () => {
            ws.send(JSON.stringify({ action: 'start' }));
            setButtons({ start: false, hit: true, stand: true, split: false, double: false });
        };
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            updateFromState(data);
        };
        ws.onerror = () => {
            statusArea.textContent = "WebSocket connection error";
            setButtons({ start: true, hit: false, stand: false, split: false, double: false });
        };
        ws.onclose = () => {
            setButtons({ start: true, hit: false, stand: false, split: false, double: false });
        };
    } else {
        ws.send(JSON.stringify({ action: 'start' }));
        setButtons({ start: false, hit: true, stand: true, split: false, double: false });
    }
};

hitBtn.onclick = function() {
    if (ws && ws.readyState === 1) {
        ws.send(JSON.stringify({ action: 'hit' }));
    }
};

standBtn.onclick = function() {
    if (ws && ws.readyState === 1) {
        ws.send(JSON.stringify({ action: 'stand' }));
    }
};

splitBtn.onclick = function() {
    if (ws && ws.readyState === 1) {
        ws.send(JSON.stringify({ action: 'split' }));
    }
};

doubleBtn.onclick = function() {
    if (ws && ws.readyState === 1) {
        ws.send(JSON.stringify({ action: 'double' }));
    }
};