import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="3D Whack-a-Mole",
    page_icon="🐹",
    layout="centered"
)

game_3d_code = """
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
            overflow: hidden;
        }
        .header {
            text-align: center;
            margin-bottom: 5px;
        }
        h1 { color: #00fff5; font-size: 22px; margin: 0; }
        .info-container {
            display: flex; justify-content: space-between;
            width: 380px; margin: 10px 0;
            font-size: 16px; font-weight: bold;
            background: rgba(255, 255, 255, 0.05);
            padding: 8px 16px; border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        #canvas-container {
            width: 380px; height: 320px;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
            background: #111827;
        }
        .btn-start {
            margin-top: 12px;
            padding: 10px 24px;
            font-size: 15px; font-weight: bold;
            background: linear-gradient(135deg, #00fff5, #7000ff);
            color: #fff; border: none; border-radius: 12px;
            cursor: pointer; box-shadow: 0 4px 15px rgba(0,255,245,0.3);
            transition: transform 0.1s;
        }
        .btn-start:active { transform: scale(0.95); }
    </style>
    <!-- Nhúng thư viện Three.js 3D từ CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div class="header">
    <h1>🐹 Game Đập Chuột 3D 🎮</h1>
</div>

<div class="info-container">
    <div>Điểm: <span id="score" style="color: #00fff5;">0</span></div>
    <div>Thời gian: <span id="timer" style="color: #ff4b4b;">30</span>s</div>
</div>

<div id="canvas-container"></div>

<button class="btn-start" id="startBtn" onclick="startGame()">Bắt Đầu Chơi 3D</button>

<script>
    let scene, camera, renderer;
    let holes = [];
    let moles = [];
    let score = 0;
    let timeLeft = 30;
    let gameTimer = null;
    let moleTimer = null;
    let activeIndex = -1;
    let isPlaying = false;

    // Khởi tạo không gian 3D Three.js
    function init3D() {
        const container = document.getElementById('canvas-container');
        
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x111827);

        camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 7, 7);
        camera.lookAt(0, 0, 0);

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        // Ánh sáng
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0xffffff, 1);
        pointLight.position.set(5, 10, 5);
        scene.add(pointLight);

        // Tạo 9 hố và 9 chú chuột 3D dạng lưới 3x3
        const spacing = 1.6;
        for (let x = -1; x <= 1; x++) {
            for (let z = -1; z <= 1; z++) {
                // Tạo hố (Hình trụ màu tối)
                const holeGeo = new THREE.CylinderGeometry(0.6, 0.6, 0.3, 32);
                const holeMat = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.8 });
                const hole = new THREE.Mesh(holeGeo, holeMat);
                hole.position.set(x * spacing, 0, z * spacing);
                scene.add(hole);
                holes.push(hole);

                // Tạo chuột 3D (Hình cầu/Khối cầu dẹt màu hồng cam đáng yêu ẩn bên trong hố)
                const moleGeo = new THREE.SphereGeometry(0.4, 32, 32);
                const moleMat = new THREE.MeshStandardMaterial({ color: 0xf472b6, roughness: 0.4 });
                const mole = new THREE.Mesh(moleGeo, moleMat);
                mole.position.set(x * spacing, -0.5, z * spacing); // Ẩn bên dưới
                scene.add(mole);
                moles.push(mole);
            }
        }

        // Bắt sự kiện click chuột trên màn hình 3D
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        renderer.domElement.addEventListener('click', (event) => {
            if (!isPlaying) return;
            const rect = renderer.domElement.getBoundingClientRect();
            mouse.x = ((event.clientX - rect.left) / container.clientWidth) * 2 - 1;
            mouse.y = -((event.clientY - rect.top) / container.clientHeight) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(moles);

            if (intersects.length > 0) {
                const clickedMole = intersects[0].object;
                const index = moles.indexOf(clickedMole);
                if (index === activeIndex) {
                    score += 10;
                    document.getElementById('score').textContent = score;
                    hideMole(activeIndex);
                    activeIndex = -1;
                }
            }
        });

        animate();
    }

    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }

    function startGame() {
        if (isPlaying) return;
        isPlaying = true;
        score = 0;
        timeLeft = 30;
        document.getElementById('score').textContent = score;
        document.getElementById('timer').textContent = timeLeft;
        document.getElementById('startBtn').style.display = 'none';

        gameTimer = setInterval(() => {
            timeLeft--;
            document.getElementById('timer').textContent = timeLeft;
            if (timeLeft <= 0) {
                endGame();
            }
        }, 1000);

        showRandomMole();
    }

    function showRandomMole() {
        if (!isPlaying) return;

        if (activeIndex !== -1) {
            hideMole(activeIndex);
        }

        activeIndex = Math.floor(Math.random() * moles.length);
        
        // Hiệu ứng chuột trồi lên 3D
        let currentY = -0.5;
        const targetY = 0.2;
        const riseInterval = setInterval(() => {
            currentY += 0.1;
            if (currentY >= targetY) {
                currentY = targetY;
                clearInterval(riseInterval);
            }
            moles[activeIndex].position.y = currentY;
        }, 20);

        let speed = Math.max(500, 1200 - (score * 25));
        moleTimer = setTimeout(showRandomMole, speed);
    }

    function hideMole(index) {
        if (index === -1) return;
        moles[index].position.y = -0.5; // Kéo chuột thụt xuống hố
    }

    function endGame() {
        isPlaying = false;
        clearInterval(gameTimer);
        clearTimeout(moleTimer);
        if (activeIndex !== -1) {
            hideMole(activeIndex);
            activeIndex = -1;
        }
        document.getElementById('startBtn').style.display = 'block';
        document.getElementById('startBtn').textContent = 'Chơi Lại 3D';
        alert(`Trò chơi kết thúc! Tổng điểm 3D của bạn là: ${score}`);
    }

    window.onload = init3D;
</script>

</body>
</html>
"""

components.html(game_3d_code, height=520)
