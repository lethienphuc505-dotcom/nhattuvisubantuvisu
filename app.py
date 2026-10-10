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
        }
        .hint { margin-top: 8px; color: #64748b; font-size: 12px; }
        .btn-start {
            margin-top: 15px;
            padding: 10px 24px;
            font-size: 15px; font-weight: bold;
            background: linear-gradient(135deg, #00fff5, #7000ff);
            color: #fff; border: none; border-radius: 12px;
            cursor: pointer; box-shadow: 0 4px 15px rgba(0,255,245,0.3);
        }
    </style>
</head>
<body>

<h1>🚀 Không Chiến Không Gian 🌌</h1>
<div class="subtitle">Dùng phím mũi tên Trái/Phải để di chuyển, phím Space để bắn!</div>

<div class="info-container">
    <div>Điểm: <span id="score" style="color: #00fff5;">0</span></div>
    <div>Mạng: <span id="lives" style="color: #ff4b4b;">❤️❤️❤️</span></div>
</div>

<canvas id="gameCanvas" width="400" height="450" tabindex="1"></canvas>
<div class="hint">Click vào khung game trước khi chơi bằng phím</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreElement = document.getElementById("score");
    const livesElement = document.getElementById("lives");

    canvas.focus();

    let score = 0;
    let lives = 3;
    let isPlaying = false;
    let gameInterval = null;

    // Phi thuyền của người chơi
    let player = {
        x: 180,
        y: 390,
        width: 40,
        height: 30,
        speed: 6,
        dx: 0
    };

    let bullets = [];
    let enemies = [];
    let stars = [];

    // Tạo hiệu ứng sao nền không gian
    for(let i=0; i<50; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2,
            speed: Math.random() * 1.5 + 0.5
        });
    }

    function startGame() {
        if (isPlaying) return;
        isPlaying = true;
        score = 0;
        lives = 3;
        bullets = [];
        enemies = [];
        scoreElement.textContent = score;
        updateLivesDisplay();
        
        if (gameInterval) clearInterval(gameInterval);
        gameInterval = setInterval(gameLoop, 1000 / 60); // 60 FPS
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
        // Di chuyển phi thuyền
        player.x += player.dx;
        if (player.x < 0) player.x = 0;
        if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;

        // Cập nhật đạn
        for (let i = bullets.length - 1; i >= 0; i--) {
            bullets[i].y -= 8;
            if (bullets[i].y < 0) {
                bullets.splice(i, 1);
            }
        }

        // Tạo kẻ địch ngẫu nhiên
        if (Math.random() < 0.03) {
            enemies.push({
                x: Math.random() * (canvas.width - 35),
                y: -40,
                width: 35,
                height: 35,
                speed: 2 + Math.random() * 2
            });
        }

        // Cập nhật kẻ địch
        for (let i = enemies.length - 1; i >= 0; i--) {
            enemies[i].y += enemies[i].speed;

            // Kiểm tra va chạm với phi thuyền
            if (
                player.x < enemies[i].x + enemies[i].width &&
                player.x + player.width > enemies[i].x &&
                player.y < enemies[i].y + enemies[i].height &&
                player.y + player.height > enemies[i].y
            ) {
                enemies.splice(i, 1);
                lives--;
                updateLivesDisplay();
                if (lives <= 0) {
                    endGame();
                }
                continue;
            }

            // Kẻ địch qua màn hình (mất máu)
            if (enemies[i].y > canvas.height) {
                enemies.splice(i, 1);
            }
        }

        // Kiểm tra đạn trúng kẻ địch
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

        // Cập nhật sao nền
        stars.forEach(star => {
            star.y += star.speed;
            if (star.y > canvas.height) star.y = 0;
        });
    }

    function draw() {
        ctx.fillStyle = "#050811";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Vẽ sao
        ctx.fillStyle = "#ffffff";
        stars.forEach(star => {
            ctx.fillRect(star.x, star.y, star.size, star.size);
        });

        // Vẽ phi thuyền người chơi (Hình tam giác khoa học viễn tưởng)
        ctx.fillStyle = "#00fff5";
        ctx.beginPath();
        ctx.moveTo(player.x + player.width / 2, player.y);
        ctx.lineTo(player.x, player.y + player.height);
        ctx.lineTo(player.x + player.width, player.y + player.height);
        ctx.closePath();
        ctx.fill();

        // Vẽ đạn
        ctx.fillStyle = "#ffb703";
        bullets.forEach(b => {
            ctx.fillRect(b.x - 2, b.y, 4, 10);
        });

        // Vẽ kẻ địch (Tiểu hành tinh / Tàu địch hình vuông đỏ)
        ctx.fillStyle = "#ff4b4b";
        enemies.forEach(e => {
            ctx.fillRect(e.x, e.y, e.width, e.height);
            // Trang trí thêm chi tiết tàu địch
            ctx.fillStyle = "#fff";
            ctx.fillRect(e.x + 10, e.y + 10, 15, 5);
            ctx.fillStyle = "#ff4b4b";
        });
    }

    function endGame() {
        isPlaying = false;
        clearInterval(gameInterval);
        
        ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#ff4b4b";
        ctx.font = "bold 26px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 20);

        ctx.fillStyle = "#fff";
        ctx.font = "16px sans-serif";
        ctx.fillText(`Tổng điểm: ${score}`, canvas.width / 2, canvas.height / 2 + 15);
        ctx.fillText("Nhấn nút Bắt Đầu để chơi lại", canvas.width / 2, canvas.height / 2 + 50);
        ctx.textAlign = "start";
    }

    // Điều khiển bàn phím
    window.addEventListener("keydown", (e) => {
        if (!isPlaying) return;
        if (e.key === "ArrowLeft" || e.key === "a") player.dx = -player.speed;
        if (e.key === "ArrowRight" || e.key === "d") player.dx = player.speed;
        if (e.key === " " || e.key === "ArrowUp") {
            bullets.push({ x: player.x + player.width / 2, y: player.y });
            e.preventDefault();
        }
    });

    window.addEventListener("keyup", (e) => {
        if ((e.key === "ArrowLeft" || e.key === "a") && player.dx < 0) player.dx = 0;
        if ((e.key === "ArrowRight" || e.key === "d") && player.dx > 0) player.dx = 0;
    });

    // Vẽ màn hình chờ ban đầu
    draw();
</script>

</body>
</html>
"""

components.html(space_shooter_code, height=550)
