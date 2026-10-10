import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Streamlit Snake Game",
    page_icon="🐍",
    layout="centered"
)

st.title("🐍 Game Rắn Săn Mồi trên Streamlit")
st.write("Sử dụng các phím mũi tên (**↑ ↓ ← →**) hoặc **W, A, S, D** để điều khiển.")

snake_game_code = """
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
        .score-container {
            display: flex; justify-content: space-between;
            width: 400px; margin-bottom: 12px;
            font-size: 18px; font-weight: 600;
        }
        canvas {
            border: 2px solid #262730; border-radius: 8px;
            background-color: #16213e; box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
            outline: none;
        }
        .hint { margin-top: 10px; color: #888; font-size: 13px; }
    </style>
</head>
<body>

<div class="score-container">
    <div>Điểm: <span id="score" style="color: #00fff5;">0</span></div>
    <div>Kỷ lục: <span id="high-score" style="color: #ff4b4b;">0</span></div>
</div>

<canvas id="snakeCanvas" width="400" height="400" tabindex="1"></canvas>
<div class="hint">Click vào khung game nếu phím điều khiển không phản hồi</div>

<script>
    const canvas = document.getElementById("snakeCanvas");
    const ctx = canvas.getContext("2d");
    const scoreElement = document.getElementById("score");
    const highScoreElement = document.getElementById("high-score");

    canvas.focus();

    const gridSize = 20;
    const tileCount = canvas.width / gridSize;

    let snake = [];
    let food = { x: 0, y: 0 };
    let dx = gridSize;
    let dy = 0;
    let score = 0;
    let highScore = 0;
    let gameInterval = null;
    let isGameOver = false;
    let changingDirection = false;

    function initGame() {
        snake = [
            { x: 10 * gridSize, y: 10 * gridSize },
            { x: 9 * gridSize, y: 10 * gridSize },
            { x: 8 * gridSize, y: 10 * gridSize }
        ];
        score = 0;
        dx = gridSize;
        dy = 0;
        isGameOver = false;
        scoreElement.textContent = score;
        generateFood();
        
        if (gameInterval) clearInterval(gameInterval);
        gameInterval = setInterval(gameLoop, 100);
    }

    function generateFood() {
        food.x = Math.floor(Math.random() * tileCount) * gridSize;
        food.y = Math.floor(Math.random() * tileCount) * gridSize;

        snake.forEach(part => {
            if (part.x === food.x && part.y === food.y) {
                generateFood();
            }
        });
    }

    function gameLoop() {
        if (isGameOver) return;

        changingDirection = false;
        clearCanvas();
        drawFood();
        moveSnake();
        drawSnake();
        checkCollision();
    }

    function clearCanvas() {
        ctx.fillStyle = "#16213e";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function drawSnake() {
        snake.forEach((part, index) => {
            ctx.fillStyle = index === 0 ? "#ff4b4b" : "#4e54c8";
            ctx.strokeStyle = "#16213e";
            ctx.fillRect(part.x, part.y, gridSize, gridSize);
            ctx.strokeRect(part.x, part.y, gridSize, gridSize);
        });
    }

    function moveSnake() {
        const head = { x: snake[0].x + dx, y: snake[0].y + dy };
        snake.unshift(head);

        if (head.x === food.x && head.y === food.y) {
            score += 10;
            scoreElement.textContent = score;
            if (score > highScore) {
                highScore = score;
                highScoreElement.textContent = highScore;
            }
            generateFood();
        } else {
            snake.pop();
        }
    }

    function checkCollision() {
        const head = snake[0];

        if (head.x < 0 || head.x >= canvas.width || head.y < 0 || head.y >= canvas.height) {
            endGame();
        }

        for (let i = 1; i < snake.length; i++) {
            if (head.x === snake[i].x && head.y === snake[i].y) {
                endGame();
            }
        }
    }

    function endGame() {
        isGameOver = true;
        clearInterval(gameInterval);

        ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#ff4b4b";
        ctx.font = "bold 28px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 20);

        ctx.fillStyle = "#fff";
        ctx.font = "16px sans-serif";
        ctx.fillText(`Điểm của bạn: ${score}`, canvas.width / 2, canvas.height / 2 + 15);
        ctx.fillText("Nhấn phím bất kỳ để chơi lại", canvas.width / 2, canvas.height / 2 + 55);
        ctx.textAlign = "start";
    }

    window.addEventListener("keydown", handleKeyPress);

    function handleKeyPress(e) {
        if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "].includes(e.key)) {
            e.preventDefault();
        }

        if (isGameOver) {
            initGame();
            return;
        }

        if (changingDirection) return;

        const key = e.key;
        const goingUp = dy === -gridSize;
        const goingDown = dy === gridSize;
        const goingRight = dx === gridSize;
        const goingLeft = dx === -gridSize;

        if ((key === "ArrowLeft" || key === "a" || key === "A") && !goingRight) {
            dx = -gridSize;
            dy = 0;
            changingDirection = true;
        }
        if ((key === "ArrowUp" || key === "w" || key === "W") && !goingDown) {
            dx = 0;
            dy = -gridSize;
            changingDirection = true;
        }
        if ((key === "ArrowRight" || key === "d" || key === "D") && !goingLeft) {
            dx = gridSize;
            dy = 0;
            changingDirection = true;
        }
        if ((key === "ArrowDown" || key === "s" || key === "S") && !goingUp) {
            dx = 0;
            dy = gridSize;
            changingDirection = true;
        }
    }

    function drawFood() {
        ctx.fillStyle = "#00fff5";
        ctx.beginPath();
        ctx.arc(food.x + gridSize / 2, food.y + gridSize / 2, gridSize / 2 - 2, 0, Math.PI * 2);
        ctx.fill();
    }

    initGame();
</script>

</body>
</html>
"""

components.html(snake_game_code, height=500)
