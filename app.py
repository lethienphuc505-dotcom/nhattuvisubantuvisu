import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Streamlit Whack-a-Mole",
    page_icon="🐹",
    layout="centered"
)

st.write("Nhấn vào các ô có chú chuột xuất hiện để ghi điểm trước khi hết giờ!")

whack_game_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0; padding: 0;
            background-color: #0e1117; color: #fff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }
        .info-container {
            display: flex; justify-content: space-between;
            width: 340px; margin-bottom: 15px;
            font-size: 18px; font-weight: 600;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            width: 340px;
            height: 340px;
            background-color: #16213e;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
        }
        .hole {
            background-color: #0f3460;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            cursor: pointer;
            user-select: none;
            transition: background-color 0.1s;
        }
        .hole.mole {
            background-color: #e94560;
        }
        .btn-start {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            background-color: #00fff5;
            color: #0e1117;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        .btn-start:hover {
            background-color: #00cccc;
        }
    </style>
</head>
<body>

<div class="info-container">
    <div>Điểm: <span id="score" style="color: #00fff5;">0</span></div>
    <div>Thời gian: <span id="timer" style="color: #ff4b4b;">30</span>s</div>
</div>

<div class="grid" id="grid">
    <div class="hole" data-id="0"></div>
    <div class="hole" data-id="1"></div>
    <div class="hole" data-id="2"></div>
    <div class="hole" data-id="3"></div>
    <div class="hole" data-id="4"></div>
    <div class="hole" data-id="5"></div>
    <div class="hole" data-id="6"></div>
    <div class="hole" data-id="7"></div>
    <div class="hole" data-id="8"></div>
</div>

<button class="btn-start" id="startBtn" onclick="startGame()">Bắt đầu chơi</button>

<script>
    const holes = document.querySelectorAll('.hole');
    const scoreDisplay = document.getElementById('score');
    const timerDisplay = document.getElementById('timer');
    const startBtn = document.getElementById('startBtn');

    let score = 0;
    let timeLeft = 30;
    let gameTimer = null;
    let moleTimer = null;
    let activeHole = null;
    let isPlaying = false;

    function startGame() {
        if (isPlaying) return;
        isPlaying = true;
        score = 0;
        timeLeft = 30;
        scoreDisplay.textContent = score;
        timerDisplay.textContent = timeLeft;
        startBtn.style.display = 'none';

        gameTimer = setInterval(() => {
            timeLeft--;
            timerDisplay.textContent = timeLeft;
            if (timeLeft <= 0) {
                endGame();
            }
        }, 1000);

        showMole();
    }

    function randomHole() {
        const index = Math.floor(Math.random() * holes.length);
        const hole = holes[index];
        if (hole === activeHole) {
            return randomHole();
        }
        return hole;
    }

    function showMole() {
        if (!isPlaying) return;
        
        if (activeHole) {
            activeHole.classList.remove('mole');
            activeHole.textContent = '';
        }

        activeHole = randomHole();
        activeHole.classList.add('mole');
        activeHole.textContent = '🐹';

        let speed = Math.max(400, 1000 - (score * 20)); // Càng về sau chuột hiện càng nhanh
        moleTimer = setTimeout(showMole, speed);
    }

    holes.forEach(hole => {
        hole.addEventListener('click', () => {
            if (!isPlaying) return;
            if (hole === activeHole) {
                score += 10;
                scoreDisplay.textContent = score;
                activeHole.classList.remove('mole');
                activeHole.textContent = '';
                activeHole = null;
            }
        });
    });

    function endGame() {
        isPlaying = false;
        clearInterval(gameTimer);
        clearTimeout(moleTimer);
        if (activeHole) {
            activeHole.classList.remove('mole');
            activeHole.textContent = '';
        }
        startBtn.style.display = 'block';
        startBtn.textContent = 'Chơi Lại';
        alert(`Hết giờ! Tổng số điểm của bạn là: ${score}`);
    }
</script>

</body>
</html>
"""

components.html(whack_game_code, height=520)
