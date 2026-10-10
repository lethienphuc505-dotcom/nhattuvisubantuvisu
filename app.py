import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Cute 3D Whack-a-Mole",
    page_icon="🐹",
    layout="centered"
)

game_3d_cute_mouse = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0; padding: 0;
            background-color: #1a1c29; color: #fff;
            font-family: 'Plus Jakarta Sans', sans-serif;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            overflow: hidden;
        }
        .header { text-align: center; margin-bottom: 5px; }
        h1 { color: #ffb703; font-size: 22px; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        .info-container {
            display: flex; justify-content: space-between;
            width: 380px; margin: 8px 0;
            font-size: 16px; font-weight: bold;
            background: rgba(255, 255, 255, 0.08);
            padding: 8px 16px; border-radius: 14px;
            box-shadow: inset 0 2px 4px rgba(255,255,255,0.1);
        }
        #canvas-container {
            width: 380px; height: 320px;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 12px 35px rgba(0,0,0,0.5);
            background: #212538;
            border: 2px solid rgba(255,255,255,0.05);
        }
        .btn-start {
            margin-top: 12px;
            padding: 10px 28px;
            font-size: 15px; font-weight: bold;
            background: linear-gradient(135deg, #fb8500, #ffb703);
            color: #1a1c29; border: none; border-radius: 14px;
            cursor: pointer; box-shadow: 0 6px 20px rgba(251,133,0,0.4);
            transition: transform 0.1s, filter 0.2s;
        }
        .btn-start:hover { filter: brightness(1.1); }
        .btn-start:active { transform: scale(0.95); }
    </style>
    <!-- Thư viện Three.js 3D -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div class="header">
    <h1>🐹 Đập Chuột 3D Hoạt Hình 🌸</h1>
</div>

<div class="info-container">
    <div>Điểm: <span id="score" style="color: #ffb703;">0</span></div>
    <div>Thời gian: <span id="timer" style="color: #ef476f;">30</span>s</div>
</div>

<div id="canvas-container"></div>

<button class="btn-start" id="startBtn" onclick="startGame()">Bắt Đầu Chơi 🎮</button>

<script>
    let scene, camera, renderer;
    let moleGroups = [];
    let score = 0;
    let timeLeft = 30;
    let gameTimer = null;
    let moleTimer = null;
    let activeIndex = -1;
    let isPlaying = false;

    function init3D() {
        const container = document.getElementById('canvas-container');
        
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x212538);

        camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 7.5, 7.5);
        camera.lookAt(0, -0.2, 0);

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        // Ánh sáng dịu nhẹ phong cách hoạt hình
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(5, 12, 7);
        scene.add(dirLight);

        // Tạo 9 hố đất và 9 chú chuột 3D đáng yêu
        const spacing = 1.6;
        for (let x = -1; x <= 1; x++) {
            for (let z = -1; z <= 1; z++) {
                // 1. Hố đất hình trụ màu tối có viền miệng hố
                const holeGeo = new THREE.CylinderGeometry(0.58, 0.52, 0.35, 32);
                const holeMat = new THREE.MeshStandardMaterial({ color: 0x11131a, roughness: 0.9 });
                const hole = new THREE.Mesh(holeGeo, holeMat);
                hole.position.set(x * spacing, -0.05, z * spacing);
                scene.add(hole);

                // 2. Nhóm mô hình chuột hoạt hình 3D
                const moleGroup = new THREE.Group();

                // Thân chuột (Màu xám sáng mịn màng)
                const bodyGeo = new THREE.SphereGeometry(0.35, 32, 32);
                bodyGeo.scale(1, 1.15, 1);
                const bodyMat = new THREE.MeshStandardMaterial({ color: 0xc5d3e8, roughness: 0.5 });
                const body = new THREE.Mesh(bodyGeo, bodyMat);
                body.position.y = 0.05;
                moleGroup.add(body);

                // Má hồng phúng phính
                const cheekGeo = new THREE.SphereGeometry(0.1, 16, 16);
                const cheekMat = new THREE.MeshStandardMaterial({ color: 0xffb5a7, roughness: 0.4 });
                const leftCheek = new THREE.Mesh(cheekGeo, cheekMat);
                leftCheek.position.set(-0.22, -0.02, 0.22);
                moleGroup.add(leftCheek);
                const rightCheek = leftCheek.clone();
                rightCheek.position.x = 0.22;
                moleGroup.add(rightCheek);

                // Tai trái & Tai phải (Màu hồng bên trong)
                const earGeo = new THREE.SphereGeometry(0.14, 16, 16);
                const earMat = new THREE.MeshStandardMaterial({ color: 0x93a4b8, roughness: 0.5 });
                const leftEar = new THREE.Mesh(earGeo, earMat);
                leftEar.position.set(-0.28, 0.38, -0.05);
                moleGroup.add(leftEar);
                const rightEar = leftEar.clone();
                rightEar.position.x = 0.28;
                moleGroup.add(rightEar);

                // Mắt chuột (Mắt bi tròn đen bóng)
                const eyeGeo = new THREE.SphereGeometry(0.05, 16, 16);
                const eyeMat = new THREE.MeshStandardMaterial({ color: 0x2b2d42, roughness: 0.1 });
                const leftEye = new THREE.Mesh(eyeGeo, eyeMat);
                leftEye.position.set(-0.13, 0.12, 0.28);
                moleGroup.add(leftEye);
                const rightEye = leftEye.clone();
                rightEye.position.x = 0.13;
                moleGroup.add(rightEye);

                // Mũi chuột hồng xinh
                const noseGeo = new THREE.SphereGeometry(0.06, 16, 16);
                const noseMat = new THREE.MeshStandardMaterial({ color: 0xff5964, roughness: 0.3 });
                const nose = new THREE.Mesh(noseGeo, noseMat);
                nose.position.set(0, 0.04, 0.33);
                moleGroup.add(nose);

                // Vị trí ẩn bên dưới hố
                moleGroup.position.set(x * spacing, -0.9, z * spacing);
                scene.add(moleGroup);
                moleGroups.push(moleGroup);
            }
        }

        // Bắt sự kiện click chuột
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        renderer.domElement.addEventListener('click', (event) => {
            if (!isPlaying) return;
            const rect = renderer.domElement.getBoundingClientRect();
            mouse.x = ((event.clientX - rect.left) / container.clientWidth) * 2 - 1;
            mouse.y = -((event.clientY - rect.top) / container.clientHeight) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(scene.children, true);
            
            if (intersects.length > 0) {
                for (let i = 0; i < moleGroups.length; i++) {
                    if (isDescendant(intersects[0].object, moleGroups[i])) {
                        if (i === activeIndex) {
                            score += 10;
                            document.getElementById('score').textContent = score;
                            
                            // Hiệu ứng thụt xuống nhanh khi bị đập trúng
                            hideMole(activeIndex);
                            activeIndex = -1;
                        }
                        break;
                    }
                }
            }
        });

        animate();
    }

    function isDescendant(child, parent) {
        let node = child.parent;
        while (node != null) {
            if (node == parent) return true;
            node = node.parent;
        }
        return false;
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

        activeIndex = Math.floor(Math.random() * moleGroups.length);
        
        // Hiệu ứng chuột trồi lên mượt mà
        let currentY = -0.9;
        const targetY = -0.15;
        const riseInterval = setInterval(() => {
            currentY += 0.12;
            if (currentY >= targetY) {
                currentY = targetY;
                clearInterval(riseInterval);
            }
            moleGroups[activeIndex].position.y = currentY;
        }, 15);

        let speed = Math.max(450, 1100 - (score * 25));
        moleTimer = setTimeout(showRandomMole, speed);
    }

    function hideMole(index) {
        if (index === -1) return;
        moleGroups[index].position.y = -0.9;
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
        document.getElementById('startBtn').textContent = 'Chơi Lại 🎮';
        alert(`Hết giờ rồi! Tổng số điểm của bạn là: ${score}`);
    }

    window.onload = init3D;
</script>

</body>
</html>
"""

components.html(game_3d_cute_mouse, height=520)
