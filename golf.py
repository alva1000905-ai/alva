import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Golf Game",
    layout="wide"
)

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

canvas {
    width: 100vw;
    height: 100vh;
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

// ================= DESIGN SIZE =================
const DESIGN_WIDTH = 900;
const DESIGN_HEIGHT = 500;

let scaleX = 1;
let scaleY = 1;

// ================= RESIZE =================
function resizeCanvas() {
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;

    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    scaleX = rect.width / DESIGN_WIDTH;
    scaleY = rect.height / DESIGN_HEIGHT;
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

// ================= OBSTACLES =================
function generateObstacles() {
    obstacles = [];
    let count = Math.min(3 + level, 8);
    for(let i=0;i<count;i++){
        let w = 15 + Math.random()*10;
        let h = 50 + Math.random()*80;
        let x = 50 + Math.random()*800;
        let y = 50 + Math.random()*350;

        let dx = x + w/2 - hole.x;
        let dy = y + h/2 - hole.y;
        if(Math.sqrt(dx*dx + dy*dy) < hole.r + Math.max(w,h)){
            i--;
            continue;
        }
        obstacles.push({x,y,w,h});
    }
}

// ================= LEVEL =================
function newLevel() {
    ball.x = 150;
    ball.y = 250;
    ball.vx = 0;
    ball.vy = 0;

    hole.x = 200 + Math.random() * 600;
    hole.y = 80 + Math.random() * 300;

    generateObstacles();
    level++;
}

// ================= INPUT =================
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
        x: x / scaleX,
        y: y / scaleY
    };
}

function startDrag(evt){
    evt.preventDefault();
    const pos = getPos(evt);
    const dx = pos.x - ball.x;
    const dy = pos.y - ball.y;
    if(Math.sqrt(dx*dx + dy*dy) < ball.r + 5){
        dragging = true;
        dragStart = pos;
    }
}

function moveDrag(evt){
    if(!dragging) return;
    evt.preventDefault();
    dragEnd = getPos(evt);
}

function endDrag(evt){
    if(!dragging) return;
    evt.preventDefault();

    dragEnd = dragEnd || dragStart;
    const dx = dragStart.x - dragEnd.x;
    const dy = dragStart.y - dragEnd.y;

    ball.vx = dx * 0.12;
    ball.vy = dy * 0.12;

    dragging = false;
    dragStart = null;
    dragEnd = null;
}

canvas.addEventListener("mousedown", startDrag);
canvas.addEventListener("mousemove", moveDrag);
canvas.addEventListener("mouseup", endDrag);

canvas.addEventListener("touchstart", startDrag, { passive:false });
canvas.addEventListener("touchmove", moveDrag, { passive:false });
canvas.addEventListener("touchend", endDrag, { passive:false });

// ================= DRAW =================
function drawBackground(){
    ctx.fillStyle = "#3ebd59";
    ctx.fillRect(0,0,DESIGN_WIDTH,DESIGN_HEIGHT);

    ctx.fillStyle = "#2e8b47";
    ctx.fillRect(0,420,DESIGN_WIDTH,80);
}

function drawHole(){
    ctx.save();
    ctx.translate(hole.x, hole.y);
    ctx.fillStyle="#006400";
    ctx.beginPath();
    ctx.arc(0,0,hole.r+5,0,Math.PI*2);
    ctx.fill();

    ctx.fillStyle="#000";
    ctx.beginPath();
    ctx.arc(0,0,hole.r,0,Math.PI*2);
    ctx.fill();

    ctx.strokeStyle="red";
    ctx.lineWidth=2;
    ctx.beginPath();
    ctx.moveTo(0,-hole.r-15);
    ctx.lineTo(0,0);
    ctx.stroke();
    ctx.restore();
}

function drawObstacles(){
    ctx.fillStyle="#654321";
    obstacles.forEach(o => ctx.fillRect(o.x,o.y,o.w,o.h));
}

function drawBall(){
    ctx.fillStyle="white";
    ctx.beginPath();
    ctx.arc(ball.x,ball.y,ball.r,0,Math.PI*2);
    ctx.fill();
}

function drawHUD(){
    ctx.fillStyle="white";
    ctx.font="24px Arial Black";
    ctx.fillText(`Score: ${score}   Level: ${level}`, 20, 35);
}

function drawAimLine(){
    if(dragging && dragEnd){
        ctx.strokeStyle="rgba(255,0,0,0.7)";
        ctx.lineWidth=3;
        ctx.beginPath();
        ctx.moveTo(ball.x,ball.y);
        ctx.lineTo(dragEnd.x,dragEnd.y);
        ctx.stroke();
    }
}

function drawPowerBar(){
    if(dragging && dragEnd){
        const dx = dragStart.x - dragEnd.x;
        const dy = dragStart.y - dragEnd.y;
        const power = Math.min(Math.sqrt(dx*dx + dy*dy), 150);
        ctx.fillStyle="rgba(255,0,0,0.6)";
        ctx.fillRect(ball.x - 50, ball.y - 30, power * 0.6, 10);
        ctx.strokeStyle="#fff";
        ctx.strokeRect(ball.x - 50, ball.y - 30, 90, 10);
    }
}

// ================= PHYSICS =================
function collideObstacles(){
    obstacles.forEach(o => {
        if(ball.x+ball.r>o.x && ball.x-ball.r<o.x+o.w &&
           ball.y+ball.r>o.y && ball.y-ball.r<o.y+o.h){
            ball.vx *= -0.8;
            ball.vy *= -0.8;
        }
    });
}

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


// ================= MAIN LOOP =================
generateObstacles();

function loop(){
    ctx.save();
    ctx.scale(scaleX, scaleY);

    ctx.clearRect(0,0,DESIGN_WIDTH,DESIGN_HEIGHT);

    drawBackground();
    drawHole();
    drawObstacles();
    drawBall();
    drawHUD();
    drawAimLine();
    drawPowerBar();

    if(!dragging) physics();

    ctx.restore();
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

