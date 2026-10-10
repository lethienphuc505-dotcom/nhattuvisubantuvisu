import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Space Shooter with Menu",
    page_icon="🚀",
    layout="centered"
)

space_menu_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0; padding: 0;
            background-color: #0b0f19; color: #fff;
            font-family: 'Plus Jakarta Sans', sans-serif;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh;
            overflow: hidden;
        }
        .container {
            position: relative;
            width: 400px; height: 500px;
            border: 2px solid #1f2937; border-radius: 16px;
            background-color: #050811;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            overflow: hidden;
        }
        .menu-screen {
            position: absolute; width: 100%; height: 100%;
            background: rgba(5, 8, 17, 0.92);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            z-index: 10;
            transition: opacity 0.3s ease;
        }
        .menu-screen.hidden {
            opacity: 0; pointer-events: none;
        }
        h1 { color: #00fff5; font-size: 26px; margin-bottom: 5px; text-shadow: 0 0 15px rgba(0,255,245,0.6); text-align: center; }
        .subtitle { color: #8892b0; font-size: 13px; margin-bottom: 25px; text-align: center; }
        
        .menu-btn {
            width: 200px; padding: 12px 0;
            margin: 8px 0; font-size: 16px; font-weight: 800;
            background: linear-gradient(135deg, #00fff5, #7000ff);
            color: #fff; border: none; border-radius: 14px;
            cursor: pointer; box-shadow: 0 4px 15px rgba(0,255,245,0.3);
            transition: transform 0.1s, filter 0.2s;
        }
        .menu-btn:hover { filter: brightness(1.1); transform: translateY(-2px); }
        .menu-btn:active { transform: scale(0.95); }
        .menu-btn.mode-btn {
            background: linear-gradient(135deg, #fb8500, #ffb703);
            color: #0b0f19;
            box-shadow: 0 4px 15px rgba(251,133,0,0.3);
        }
        
        .hud {
            position: absolute; top: 12px; left: 16px; right: 16px;
            display: flex; justify-content: space-between;
            font-size: 15px; font-weight: bold; z-index: 5;
        }
        canvas { outline: none; }
    </style>
</head>
<body>

<div class="container" id="gameContainer">
    <!-- MÀN HÌNH MENU -->
    <div class="menu-screen" id="menuScreen">
        <h1>🚀 KHÔNG CHIẾN 🌌</h1>
        <div class="subtitle" id="modeText">Chế độ hiện tại: DỄ (Chill)</div>
        
        <button class="menu-btn" onclick="startGame()">CHƠI NGAY ▶</button>
        <button class="menu-btn mode-btn" onclick="toggleMode()">ĐỔI CHẾ ĐỘ ⚙️</button>
    </div>

    <!-- HUD TRONG GAME -->
    <div class="hud">
        <div>Điểm: <span id="score" style="color: #00fff5;">0</span></div>
        <div>Mạng: <span id="lives" style="color: #ff4b4b;">❤️❤️❤️</span></div>
    </div>

    <canvas id="gameCanvas" width="400" height="500" tabindex="1"></canvas>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreElement = document.getElementById("score");
    const livesElement = document.getElementById("lives");
    const menuScreen = document.getElementById("menuScreen");
    const modeText = document.getElementById("modeText");

    let score = 0;
    let lives = 3;
    let isPlaying = false;
    let gameInterval = null;
    let currentMode = 'easy'; // 'easy' hoặc 'hard'

    let player = {
        x: 180,
        y: 430,
        width: 40,
        height: 35,
        speed: 5,
        dx: 0
    };

    let bullets = [];
    let enemies = [];
    let stars = [];

    for(let i=0; i<45; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2 + 1,
            speed: Math.random() * 1 + 0.3
        });
    }

    function toggleMode() {
        if (currentMode === 'easy') {
            currentMode = 'hard';
            modeText.textContent = "Chế độ hiện tại: KHÓ (Thử Thách 🔥)";
            modeText.style.color = "#ff4b4b";
        } else {
            currentMode = 'easy';
            modeText.textContent = "Chế độ hiện tại: DỄ (Chill 🌸)";
            modeText.style.color = "#00fff5";
        }
    }

    function startGame() {
        menuScreen.classList.add("hidden");
        isPlaying = true;
        score = 0;
        lives = 3;
        bullets = [];
        enemies = [];
        player.x = 180;
        scoreElement.textContent = score;
        updateLivesDisplay();
        
        canvas.focus();

        if (gameInterval) clearInterval(gameInterval);
        gameInterval = setInterval(gameLoop, 1000 / 60);
    }

    function updateLivesDisplay() {
        let hearts = "";
        for(let i=0; i<lives; i++) hearts += "❤️";
        livesElement.textContent = hearts;
    }

    function gameLoop() {
        update();
        draw();
    }

    function update() {
        player.x += player.dx;
        if (player.x < 0) player.x = 0;
        if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;

        for (let i = bullets.length - 1; i >= 0; i--) {
            bullets[i].y -= 10;
            if (bullets[i].y < 0) bullets.splice(i, 1);
        }

        // Tần suất và tốc độ kẻ địch thay đổi theo chế độ chọn
        let spawnRate = currentMode === 'easy' ? 0.018 : 0.035;
        let enemySpeedMin = currentMode === 'easy' ? 1.2 : 2.2;
        let enemySpeedMax = currentMode === 'easy' ? 2.2 : 3.8;

        if (Math.random() < spawnRate) {
            enemies.push({
                x: Math.random() * (canvas.width - 40),
                y: -40,
                width: 36,
                height: 32,
                speed: enemySpeedMin + Math.random() * (enemySpeedMax - enemySpeedMin)
            });
        }

        for (let i = enemies.length - 1; i >= 0; i--) {
            enemies[i].y += enemies[i].speed;

            if (
                player.x < enemies[i].x + enemies[i].width &&
                player.x + player.width > enemies[i].x &&
                player.y < enemies[i].y + enemies[i].height &&
                player.y + player.height > enemies[i].y
            ) {
                enemies.splice(i, 1);
                lives--;
                updateLivesDisplay();
                if (lives <= 0) endGame();
                continue;
            }

            if (enemies[i].y > canvas.height) {
                enemies.splice(i, 1);
            }
        }

        for (let i = bullets.length - 1; i >= 0; i--) {
            for (let j = enemies.length - 1; j >= 0; j--) {
                if (
                    bullets[i].x > enemies[j].x &&
                    bullets[i].x < enemies[j].x + enemies[j].width &&
                    bullets[i].y > enemies[j].y &&
                    bullets[i].y < enemies[j].y + enemies[j].height
                ) {
                    bullets.splice(i, 1);
                    enemies.splice(j, 1);
                    score += 10;
                    scoreElement.textContent = score;
                    break;
                }
            }
        }

        stars.forEach(star => {
            star.y += star.speed;
            if (star.y > canvas.height) star.y = 0;
        });
    }

    function draw() {
        ctx.fillStyle = "#050811";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#ffffff";
        stars.forEach(star => {
            ctx.fillRect(star.x, star.y, star.size, star.size);
        });

        // Tàu người chơi
        let px = player.x;
        let py = player.y;
        
        ctx.fillStyle = "#00fff5";
        ctx.beginPath();
        ctx.moveTo(px + 20, py);
        ctx.lineTo(px + 5, py + 25);
        ctx.lineTo(px + 35, py + 25);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = "#7000ff";
        ctx.fillRect(px, py + 18, 8, 12)
