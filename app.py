import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Cute Whack-a-Mole",
    page_icon="🐹",
    layout="centered"
)

cute_game_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0; padding: 0;
            background-color: #fcf6f5; color: #3d3a39;
            font-family: 'Plus Jakarta Sans', sans-serif;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh;
        }
        h1 {
            color: #d87c69;
            margin-bottom: 5px;
            font-size: 26px;
        }
        .subtitle {
            color: #8c7b78;
            font-size: 14px;
            margin-bottom: 15px;
        }
        .info-container {
            display: flex; justify-content: space-between;
            width: 360px; margin-bottom: 15px;
            font-size: 18px; font-weight: 700;
            background: #ffffff;
            padding: 12px 20px;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(233, 180, 169, 0.2);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            width: 360px;
            height: 360px;
            background-color: #faedcd;
            padding: 16px;
            border-radius: 24px;
            box-shadow: 0 10px 25px rgba(212, 163, 89, 0.2);
        }
        .hole {
            background-color: #fefae0;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 44px;
            cursor: pointer;
            user-select: none;
            box-shadow: inset 0 6px 12px rgba(0,0,0,0.06);
            transition: transform 0.1s, background-color 0.2s;
        }
        .hole:active {
            transform: scale(0.92);
        }
        .hole.mole {
            background-color: #ffb4a9;
            transform: scale(1.05);
            animation: pop 0.15s ease;
        }
        @keyframes pop {
            0% { transform: scale(0.8); }
            100% { transform: scale(1.05); }
        }
        .btn-start {
            margin-top: 20px;
            padding: 12px 28px;
            font-size: 16px;
            font-weight: 800;
            background-color: #e07a5f;
            color: #ffffff;
            border: none;
            border-radius: 16px;
            cursor: pointer;
            box-shadow: 0 6px 15px rgba(224, 122, 95, 0.4);
            transition: background-color 0.2s, transform 0.1s;
        }
        .btn-start:hover {
            background-color: #d87c69;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>

<h1>🐹 Đập Chuột Kẹo Ngọt 🍬</h1>
<div class="subtitle">Chạm nhanh tay vào những chú chuột đáng yêu nhé!</div>

<div class="info-container">
    <div>Điểm: <span id="score" style="color: #e07a5f;">0</span></div>
    <div>Thời gian: <span id="timer" style="color: #f4a261;">30</span>s</div>
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

<button class="btn-start" id="startBtn" onclick="startGame()">Bắt Đầu Chơi 🌸</button>

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

        let speed = Math.max(400, 1000 - (score * 20));
        moleTimer = setTimeout(showMole, speed);
    }

    holes.forEach(hole => {
        hole.addEventListener('click', () => {
            if (!isPlaying) return;
            if (hole === activeHole) {
                score += 10;
                scoreDisplay.textContent = score;
                activeHole.classList.remove('mole');
                activeHole.textContent = '✨';
                setTimeout(() => {
                    if(activeHole === hole) {
                        activeHole.textContent = '';
                    }
                }, 150);
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
        startBtn.textContent = 'Chơi Lại 🌸';
        alert(`Hết giờ rồi! Tổng số điểm dễ thương của bạn là: ${score}`);
    }
</script>

</body>
</html>
"""

components.html(cute_game_code, height=600)
