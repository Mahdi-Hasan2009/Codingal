import * as THREE from 'three';

// --- SETTINGS ---
const LANE_WIDTH = 3;
const SPEED = 0.4;
let currentLane = 1; // 0, 1, 2
let score = 0;
let isGameOver = false;

// --- SCENE SETUP ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87CEEB); // Sky Blue
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 10, 7.5);
scene.add(light);
scene.add(new THREE.AmbientLight(0x404040));

// --- PLAYER ---
const player = new THREE.Mesh(
    new THREE.BoxGeometry(1, 1, 1),
    new THREE.MeshStandardMaterial({ color: 0xff0000 })
);
player.position.y = 0.5;
scene.add(player);

// --- TRACK ---
const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(10, 5000),
    new THREE.MeshStandardMaterial({ color: 0x333333 })
);
floor.rotation.x = -Math.PI / 2;
scene.add(floor);

// --- OBSTACLES ---
const obstacles = [];
function spawnObstacle() {
    if (isGameOver) return;
    const geometry = new THREE.BoxGeometry(2, 2, 2);
    const material = new THREE.MeshStandardMaterial({ color: 0x555555 });
    const obs = new THREE.Mesh(geometry, material);
    
    obs.position.z = player.position.z - 60;
    obs.position.x = (Math.floor(Math.random() * 3) - 1) * LANE_WIDTH;
    obs.position.y = 1;
    
    scene.add(obs);
    obstacles.push(obs);
}
setInterval(spawnObstacle, 1500);

// --- CONTROLS ---
window.addEventListener('keydown', (e) => {
    if (isGameOver) return;
    if (e.key === "ArrowLeft" && currentLane > 0) currentLane--;
    if (e.key === "ArrowRight" && currentLane < 2) currentLane++;
});

// --- GAME LOOP ---
function animate() {
    if (isGameOver) return;
    requestAnimationFrame(animate);

    // Forward Motion
    player.position.z -= SPEED;
    camera.position.set(0, 5, player.position.z + 10);
    camera.lookAt(0, 0, player.position.z - 10);

    // Lane Movement
    const targetX = (currentLane - 1) * LANE_WIDTH;
    player.position.x += (targetX - player.position.x) * 0.15;

    // Score
    score++;
    document.getElementById('score').innerText = Math.floor(score / 10);

    // Collision Detection
    obstacles.forEach(obs => {
        const dist = player.position.distanceTo(obs.position);
        if (dist < 1.5) {
            isGameOver = true;
            document.getElementById('game-over').style.display = 'block';
        }
    });

    renderer.render(scene, camera);
}

animate();