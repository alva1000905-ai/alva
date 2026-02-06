import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

components.html(
    """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body {
        margin: 0;
        overflow: hidden;
        background: #0b0b0b;
    }
    canvas {
        display: block;
        touch-action: none;
    }
</style>
</head>
<body>
<canvas id="game"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

let level = 1;
let score = 0;

let ball = {
    x: canvas.width / 2,
    y: canvas.height - 80,
    r: 12,
    vx: 0,
    vy: 0
};

let dragging = false;
let startX = 0;
let startY = 0;

let obstacles = [];

function generateLevel() {
    obstacles = [];
    for (let i = 0; i < level + 3; i++) {
        obstacles.push({
            x: Math.random() * (canvas.width - 100) + 50,
            y: Math.random() * (canvas.height / 2),
            w: 60,
            h: 20
        });
    }
}

generateLevel();

function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height - 80;
    ball.vx = 0;
    ball.vy = 0;
}

canvas.addEventListener("pointerdown", e => {
    dragging = true;
    startX = e.clientX;
    startY = e.clientY;
});

canvas.addEventListener("pointermove", e => {
    if (!dragging) return;
});

canvas.addEventListener("pointerup", e => {
    dragging = false;
    const dx = startX - e.clientX;
    const dy = startY - e.clientY;
    ball.vx = dx * 0.08;
    ball.vy = dy * 0.08;
});

function update() {
    ball.x += ball.vx;
    ball.y += ball.vy;

    ball.vx *= 0.99;
    ball.vy *= 0.99;

    if (ball.x < ball.r || ball.x > canvas.width - ball.r) {
        ball.vx *= -1;
    }
    if (ball.y < ball.r) {
        ball.vy *= -1;
    }

    for (let o of obstacles) {
        if (
            ball.x > o.x &&
            ball.x < o.x + o.w &&
            ball.y > o.y &&
            ball.y < o.y + o.h
        ) {
            score += 10;
            ball.vy *= -1;
        }
    }

    if (ball.y > canvas.height + 50) {
        resetBall();
    }

    if (score >= level * 50) {
        level++;
        generateLevel();
        resetBall();
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#111";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#00ffcc";
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#ff4757";
    for (let o of obstacles) {
        ctx.fillRect(o.x, o.y, o.w, o.h);
    }

    ctx.fillStyle = "#ffffff";
    ctx.font = "20px Arial";
    ctx.fillText("Score: " + score, 20, 30);
    ctx.fillText("Level: " + level, 20, 60);

    if (dragging) {
        ctx.strokeStyle = "#00ffcc";
        ctx.beginPath();
        ctx.moveTo(ball.x, ball.y);
        ctx.lineTo(startX, startY);
        ctx.stroke();
    }
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
""",
    height=900,
)
