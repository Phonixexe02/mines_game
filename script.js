const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const messageDiv = document.getElementById('message');
const levelSpan = document.getElementById('level');
const timeSpan = document.getElementById('time');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const resetBtn = document.getElementById('reset-btn');
const menuBtn = document.getElementById('menu-btn');
const minesSelect = document.getElementById('mines-select');
const gameOverPopup = document.getElementById('game-over-popup');
const restartBtn = document.getElementById('restart-btn');
const coinsSpan = document.getElementById('coins');

let size = 6;
let numMines = 5;
let grid = [];
let mines = new Set();
let revealed = new Set();
let level = 1;
let coins = 0;
let gameOver = false;
let paused = false;
let startTime;
let timerInterval;

const BOX_SIZE = 40;
const MARGIN = 2;

function createGrid() {
    grid = Array(size).fill().map(() => Array(size).fill(' '));
    mines.clear();
    while (mines.size < numMines) {
        const row = Math.floor(Math.random() * size);
        const col = Math.floor(Math.random() * size);
        const key = `${row},${col}`;
        if (!mines.has(key)) {
            mines.add(key);
            grid[row][col] = 'M';
        }
    }
}

function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let row = 0; row < size; row++) {
        for (let col = 0; col < size; col++) {
            const x = col * (BOX_SIZE + MARGIN) + MARGIN;
            const y = row * (BOX_SIZE + MARGIN) + MARGIN;
            const key = `${row},${col}`;

            ctx.fillStyle = revealed.has(key) ? (grid[row][col] === 'M' ? '#ff0000' : '#00ff00') : '#cccccc';
            ctx.fillRect(x, y, BOX_SIZE, BOX_SIZE);
            ctx.strokeRect(x, y, BOX_SIZE, BOX_SIZE);

            ctx.fillStyle = '#000';
            ctx.font = '20px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            const text = revealed.has(key) ? (grid[row][col] === 'M' ? 'M' : 'E') : '*';
            ctx.fillText(text, x + BOX_SIZE / 2, y + BOX_SIZE / 2);
        }
    }
}

function handleClick(x, y) {
    if (gameOver || paused) return;

    const col = Math.floor(x / (BOX_SIZE + MARGIN));
    const row = Math.floor(y / (BOX_SIZE + MARGIN));
    const key = `${row},${col}`;

    if (row < 0 || row >= size || col < 0 || col >= size || revealed.has(key)) return;

    revealed.add(key);

    if (grid[row][col] === 'M') {
        gameOver = true;
        gameOverPopup.style.display = 'flex';
        clearInterval(timerInterval);
    } else {
        if (revealed.size === size * size - numMines) {
            level++;
            coins += 10;
            levelSpan.textContent = `Level: ${level}`;
            coinsSpan.textContent = `Coins: ${coins}`;
            size = 5 + level;
            canvas.width = size * (BOX_SIZE + MARGIN) + MARGIN;
            canvas.height = size * (BOX_SIZE + MARGIN) + MARGIN;
            revealed.clear();
            createGrid();
            messageDiv.textContent = 'Level Complete!';
            setTimeout(() => {
                messageDiv.textContent = '';
                startTimer();
            }, 2000);
        }
    }
    drawGrid();
}

function startTimer() {
    let timeLeft = 180;
    timeSpan.textContent = `Time: ${timeLeft}s`;
    timerInterval = setInterval(() => {
        if (!paused && !gameOver) {
            timeLeft--;
            timeSpan.textContent = `Time: ${timeLeft}s`;
            if (timeLeft <= 0) {
                gameOver = true;
                gameOverPopup.style.display = 'flex';
                clearInterval(timerInterval);
            }
        }
    }, 1000);
}

function startGame() {
    numMines = parseInt(minesSelect.value);
    size = 5 + level;
    canvas.width = size * (BOX_SIZE + MARGIN) + MARGIN;
    canvas.height = size * (BOX_SIZE + MARGIN) + MARGIN;
    revealed.clear();
    gameOver = false;
    paused = false;
    messageDiv.textContent = '';
    coinsSpan.textContent = `Coins: ${coins}`;
    createGrid();
    drawGrid();
    startTimer();
}

function togglePause() {
    paused = !paused;
    pauseBtn.textContent = paused ? 'Resume' : 'Pause';
}

function resetGame() {
    level = 1;
    coins = 0;
    levelSpan.textContent = `Level: ${level}`;
    coinsSpan.textContent = `Coins: 0`;
    clearInterval(timerInterval);
    timeSpan.textContent = 'Time: 0s';
    startGame();
}

// Event listeners
canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    handleClick(x, y);
});

// Touch support for mobile
canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const touch = e.touches[0];
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    handleClick(x, y);
});

startBtn.addEventListener('click', () => {
    document.getElementById('menu').style.display = 'none';
    document.getElementById('game-info').style.display = 'flex';
    document.getElementById('game-canvas').style.display = 'block';
    document.getElementById('controls').style.display = 'block';
    document.getElementById('message').style.display = 'block';
    startGame();
});
pauseBtn.addEventListener('click', togglePause);
resetBtn.addEventListener('click', resetGame);
restartBtn.addEventListener('click', () => {
    gameOverPopup.style.display = 'none';
    resetGame();
});

menuBtn.addEventListener('click', () => {
    document.getElementById('menu').style.display = 'block';
    document.getElementById('game-info').style.display = 'none';
    document.getElementById('game-canvas').style.display = 'none';
    document.getElementById('controls').style.display = 'none';
    document.getElementById('message').style.display = 'none';
    document.getElementById('game-over-popup').style.display = 'none';
    level = 1;
    coins = 0;
    clearInterval(timerInterval);
    gameOver = false;
    paused = false;
});

// Initialize
// Game starts on Start Game button click