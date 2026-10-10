import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Space Shooter Game",
    page_icon="🚀",
    layout="centered"
)

space_shooter_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700&display=swap" rel="stylesheet">
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
        h1 { color: #00fff5; font-size: 22px; margin-bottom: 5px; text-shadow: 0 0 10px rgba(0,255,245,0.5); }
        .subtitle { color: #8892b0; font-size: 13px; margin-bottom: 12px; }
        .info-container {
            display: flex; justify-content: space-between;
            width: 400px; margin-bottom: 10px;
            font-size: 16px; font-weight: bold;
            background: rgba(255, 255, 255, 0.05);
            padding: 8px 16px; border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        canvas {
            border: 2px solid #1f2937; border-radius: 14px;
            background-color: #050811;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            outline: none;
            cursor: pointer;
        }
        .btn-start {
            margin-top: 15px;
            padding: 10px 24px;
            font-size: 15px; font-weight: bold;
            background: linear-gradient(135deg, #00fff5, #7000ff);
            color: #fff; border: none; border-radius: 12px;
            cursor: pointer; box-shadow: 0 4px 15px rgba(0,255,245,0.3);
            transition: transform 0.1s;
        }
        .btn-start:active { transform: scale(0.95); }
    </style>
</head>
<body>

<h1>🚀 Không Chiến Không Gian (Dễ Chơi) 🌌</h1>
<div class="subtitle">Dùng phím mũi tên Trái/Phải để di chuyển, Phím Cách (Space) để bắn!</div>

<div class="info-container">
    <div>Điểm: <span id="score" style="color: #00fff5;">0</span></div>
    <div>Mạng: <span id="lives" style="color: #ff4b4b;">❤️❤️❤️</span></div>
</div>

<canvas id="gameCanvas" width="400" height="420" tabindex="1"></canvas>

<button class="btn-start" id="startBtn" onclick="startGame()">Bắt Đầu Chơi 🎮</button>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreElement = document.getElementById("score");
    const livesElement = document.getElementById("lives");

    let score = 0;
    let lives = 3;
    let isPlaying = false;
    let gameInterval = null;

    let player = {
        x: 180,
        y: 360,
        width: 40,
        height: 35,
        speed: 4.5, // Giảm tốc độ di chuyển của tàu để dễ kiểm soát hơn
        dx: 0
    };

    let bullets = [];
    let enemies = [];
    let stars = [];

    for(let i=0; i<40; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2 + 1,
            speed: Math.random() * 1 + 0.3
        });
    }

    function startGame() {
        isPlaying = true;
        score = 0;
        lives = 3;
        bullets = [];
        enemies = [];
        player.x = 180;
        scoreElement.textContent = score;
        updateLivesDisplay();
        document.getElementById("startBtn").style.display = "none";
        
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

        // Tăng tốc độ đạn bay để bắn trúng mượt hơn
        for (let i = bullets.length - 1; i >= 0; i--) {
            bullets[i].y -= 10;
            if (bullets[i].y < 0) bullets.splice(i, 1);
        }

        // Giảm tần suất xuất hiện kẻ địch (cho thưa ra để dễ thở)
        if (Math.random() < 0.018) {
            enemies.push({
                x: Math.random() * (canvas.width - 40),
                y: -40,
                width: 36,
                height: 32,
                speed: 1.2 + Math.random() * 1.0 // Giảm tốc độ rơi của địch xuống chậm hơn hẳn
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
        ctx.fillRect(px, py + 18, 8, 12);
        ctx.fillRect(px + 32, py + 18, 8, 12);

        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(px + 20, py + 12, 4, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#ffb703";
        ctx.fillRect(px + 14, py + 25, 4, 6 + Math.random() * 4);
        ctx.fillRect(px + 22, py + 25, 4, 6 + Math.random() * 4);

        // Đạn
        ctx.fillStyle = "#ffb703";
        bullets.forEach(b => {
            ctx.fillRect(b.x - 2, b.y, 4, 12);
        });

        // Tàu địch
        enemies.forEach(e => {
            let ex = e.x;
            let ey = e.y;

            ctx.fillStyle = "#ff4b4b";
            ctx.beginPath();
            ctx.moveTo(ex + 18, ey + 32);
            ctx.lineTo(ex, ey + 5);
            ctx.lineTo(ex + 36, ey + 5);
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle = "#b7094c";
            ctx.fillRect(ex + 4, ey + 10, 28, 6);

            ctx.fillStyle = "#00fff5";
            ctx.beginPath();
            ctx.arc(ex + 18, ey + 18, 4, 0, Math.PI * 2);
            ctx.fill();
        });
    }

    function endGame() {
        isPlaying = false;
        clearInterval(gameInterval);
        
        ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#ff4b4b";
        ctx.font = "bold 26px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 25);

        ctx.fillStyle = "#fff";
        ctx.font = "16px sans-serif";
        ctx.fillText(`Tổng điểm: ${score}`, canvas.width / 2, canvas.height / 2 + 10);
        
        document.getElementById("startBtn").style.display = "block";
        document.getElementById("startBtn").textContent = "Chơi Lại 🚀";
        ctx.textAlign = "start";
    }

    window.addEventListener("keydown", (e) => {
        if (!isPlaying) return;
        if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") player.dx = -player.speed;
        if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") player.dx = player.speed;
        if (e.key === " " || e.key === "ArrowUp") {
            bullets.push({ x: player.x + player.width / 2, y: player.y });
            e.preventDefault();
        }
    });

    window.addEventListener("keyup", (e) => {
        if ((e.key === "ArrowLeft" || e.key === "a" || e.key === "A") && player.dx < 0) player.dx = 0;
        if ((e.key === "ArrowRight" || e.key === "d" || e.key === "D") && player.dx > 0) player.dx = 0;
    });

    canvas.addEventListener("click", () => {
        canvas.focus();
    });

    draw();
</script>

</body>
</html>
"""

components.html(space_shooter_code, height=530)
