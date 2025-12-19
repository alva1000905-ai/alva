import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Golf Game", layout="wide")

components.html(
"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<style>
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: #2ba84a;
    overflow: hidden;
}

#container {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

canvas {
    background: #2ba84a;
    touch-action: none;
}
</style>
</head>

<body>
<div id="container">
    <canvas id="game"></canvas>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const DESIGN_WIDTH = 900;
const DESIGN_HEIGHT = 500;

let scale = 1;
let offsetX = 0;
let offsetY = 0;

// ================= RESIZE (比例正確的核心) =================
function resizeCanvas() {
    const sw = window.innerWidth;
    const sh = window.innerHeight;

    scale = Math.min(sw / DESIGN_WIDTH, sh / DESIGN_HEIGHT);

    const displayWidth = DESIGN_WIDTH * scale;
    const displayHeight = DESIGN_HEIGHT * scale;

    offsetX = (sw - displayWidth) / 2;
    offsetY = (sh - displayHeight) / 2;

    canvas.style.width = displayWidth + "px";
    canvas.style.height = displayHeight + "px";

    const dpr = window.devicePixelRatio || 1;
    canvas.width = displayWidth * dpr;
    canvas.height = displayHeight * dpr;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

// ================= GAME STATE =================
let level = 1;
let score = 0;

let ball = { x:150, y:250, vx:0, vy:0, r:12 };
let hole = { x:750, y:250, r:18 };

let friction = 0.985;
let stickyFriction = 0.90;

let obstacles = [];
let dragging = false;
let dragStart = null;
let dragEnd = null;

// ================= INPUT（修正偏移 + 比例） =================
function getPos(evt){
    const rect = canvas.getBoundingClientRect();
    let x, y;

    if(evt.touches){
        x = evt.touches[0].clientX - rect.left;
        y = evt.touches[0].clientY - rect.top;
    } else {
        x = evt.clientX - rect.left;
        y = evt.clientY - rect.top;
    }

    return {
        x: x / scale,
        y: y / scale
    };
}

function startDrag(e){
    e.preventDefault();
    const p = getPos(e);
    const dx = p.x - ball.x;
    const dy = p.y - ball.y;
    if(Math.hypot(dx,dy) < ball.r + 5){
        dragging = true;
        dragStart = p;
    }
}

function moveDrag(e){
    if(dragging){
        e.preventDefault();
        dragEnd = getPos(e);
    }
}

function endDrag(e){
    if(!dragging) return;
    e.preventDefault();

    dragEnd = dragEnd || dragStart;
    ball.vx = (dragStart.x - dragEnd.x) * 0.12;
    ball.vy = (dragStart.y - dragEnd.y) * 0.12;

    dragging = false;
    dragStart = dragEnd = null;
}

canvas.addEventListener("mousedown", startDrag);
canvas.addEventListener("mousemove", moveDrag);
canvas.addEventListener("mouseup", endDrag);

canvas.addEventListener("touchstart", startDrag, {passive:false});
canvas.addEventListener("touchmove", moveDrag, {passive:false});
canvas.addEventListener("touchend", endDrag, {passive:false});

// ================= OBSTACLES =================
function generateObstacles(){
    obstacles = [];
    let count = Math.min(3 + level, 8);
    for(let i=0;i<count;i++){
        let w = 20, h = 60 + Math.random()*80;
        let x = 100 + Math.random()*650;
        let y = 80 + Math.random()*280;
        obstacles.push({x,y,w,h});
    }
}

// ================= LEVEL =================
function newLevel(){
    ball.x = 150; ball.y = 250;
    ball.vx = ball.vy = 0;
    hole.x = 200 + Math.random()*600;
    hole.y = 100 + Math.random()*250;
    generateObstacles();
    level++;
}

// ================= DRAW =================
function draw(){
    ctx.clearRect(0,0,DESIGN_WIDTH,DESIGN_HEIGHT);

    ctx.fillStyle="#3ebd59";
    ctx.fillRect(0,0,DESIGN_WIDTH,DESIGN_HEIGHT);

    ctx.fillStyle="#2e8b47";
    ctx.fillRect(0,420,DESIGN_WIDTH,80);

    ctx.fillStyle="#654321";
    obstacles.forEach(o=>ctx.fillRect(o.x,o.y,o.w,o.h));

    ctx.fillStyle="#000";
    ctx.beginPath();
    ctx.arc(hole.x,hole.y,hole.r,0,Math.PI*2);
    ctx.fill();

    ctx.fillStyle="#fff";
    ctx.beginPath();
    ctx.arc(ball.x,ball.y,ball.r,0,Math.PI*2);
    ctx.fill();

    ctx.fillStyle="#fff";
    ctx.font="24px Arial Black";
    ctx.fillText(`Score: ${score}  Level: ${level}`,20,35);

    if(dragging && dragEnd){
        ctx.strokeStyle="red";
        ctx.lineWidth=3;
        ctx.beginPath();
        ctx.moveTo(ball.x,ball.y);
        ctx.lineTo(dragEnd.x,dragEnd.y);
        ctx.stroke();
    }
}

// ================= PHYSICS =================
function physics() {

    // ---------- 預測下一位置 ----------
    let nextX = ball.x + ball.vx;
    let nextY = ball.y + ball.vy;

    const left   = ball.r;
    const right  = DESIGN_WIDTH - ball.r;
    const top    = ball.r;
    const bottom = 420 - ball.r;

    // ---------- X 方向牆壁 ----------
    if (nextX < left) {
        nextX = left;
        if (ball.vx < 0) ball.vx *= -0.8;
    }
    else if (nextX > right) {
        nextX = right;
        if (ball.vx > 0) ball.vx *= -0.8;
    }

    // ---------- Y 方向牆壁 ----------
    if (nextY < top) {
        nextY = top;
        if (ball.vy < 0) ball.vy *= -0.8;
    }
    else if (nextY > bottom) {
        nextY = bottom;
        if (ball.vy > 0) ball.vy *= -0.8;
    }

    // ---------- 套用位置 ----------
    ball.x = nextX;
    ball.y = nextY;

    // ---------- 摩擦力（最後才做） ----------
    ball.vx *= friction;
    ball.vy *= friction;

    // ---------- 小速度歸零（防抖動） ----------
    if (Math.abs(ball.vx) < 0.02) ball.vx = 0;
    if (Math.abs(ball.vy) < 0.02) ball.vy = 0;

    // ---------- 進洞 ----------
    const dx = ball.x - hole.x;
    const dy = ball.y - hole.y;
    if (Math.hypot(dx, dy) < hole.r) {
        score++;
        newLevel();
    }
}


// ================= LOOP =================
generateObstacles();
function loop(){
    if(!dragging) physics();
    draw();
    requestAnimationFrame(loop);
}
loop();
</script>
</body>
</html>
""",
height=600,
scrolling=False
)

