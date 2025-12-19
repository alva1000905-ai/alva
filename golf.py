import streamlit as st
st.set_page_config(page_title="Golf Game", layout="wide")

import streamlit.components.v1 as components

components.html(
"""
<style>
body {
    margin:0;
    overflow:hidden;
    background:#2ba84a;
}

/* 容器負責裁切 */
#game-wrapper {
    width: 100vw;
    height: 100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    overflow:hidden;
}

/* 手機：限制可視大小（裁切，不縮放） */
@media (max-width: 768px) {
    #game-wrapper {
        align-items:flex-start;
        padding-top:10px;
    }
    canvas {
        transform: translateY(-40px);
    }
}

canvas {
    width: 900px;
    height: 500px;
    touch-action:none;
}
</style>

<div id="game-wrapper">
    <canvas id="game" width="900" height="500"></canvas>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// ----------------- GAME STATE -----------------
let level = 1;
let score = 0;

let ball = { x:150, y:250, vx:0, vy:0, r:12 };
let hole = { x:750, y:250, r:18 };

let friction = 0.985;
let stickyFriction = 0.90;

let obstacles = [];

let dragStart = null;
let dragging = false;
let dragEnd = null;

// ----------------- OBSTACLES -----------------
function generateObstacles() {
    obstacles = [];
    let count = Math.min(3 + level, 8);
    for(let i=0;i<count;i++){
        let w = 15 + Math.random()*10;
        let h = 50 + Math.random()*80;
        let x = 50 + Math.random()*800;
        let y = 50 + Math.random()*400;

        let dx = x + w/2 - hole.x;
        let dy = y + h/2 - hole.y;
        if(Math.sqrt(dx*dx + dy*dy) < hole.r + Math.max(w,h)){
            i--;
            continue;
        }
        obstacles.push({x,y,w,h});
    }
}

// ----------------- LEVEL -----------------
function newLevel() {
    ball.x = 150; ball.y = 250;
    ball.vx = 0; ball.vy = 0;
    hole.x = 200 + Math.random() * 600;
    hole.y = 80 + Math.random() * 300;
    generateObstacles();
    level++;
}

// ----------------- INPUT -----------------
function getPos(evt){
    let rect = canvas.getBoundingClientRect();
    if(evt.touches){
        return {
            x: evt.touches[0].clientX - rect.left,
            y: evt.touches[0].clientY - rect.top
        };
    }
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}

function startDrag(evt){
    let pos = getPos(evt);
    let dx = pos.x - ball.x;
    let dy = pos.y - ball.y;
    if(Math.sqrt(dx*dx + dy*dy) < ball.r + 5){
        dragStart = pos;
        dragging = true;
    }
}

function moveDrag(evt){
    if(dragging) dragEnd = getPos(evt);
}

function endDrag(evt){
    if(!dragging) return;
    dragEnd = dragEnd || dragStart;
    let dx = dragStart.x - dragEnd.x;
    let dy = dragStart.y - dragEnd.y;
    ball.vx = dx * 0.12;
    ball.vy = dy * 0.12;
    dragging = false;
    dragStart = null;
    dragEnd = null;
}

canvas.addEventListener("mousedown", startDrag);
canvas.addEventListener("mousemove", moveDrag);
canvas.addEventListener("mouseup", endDrag);

canvas.addEventListener("touchstart", startDrag, {passive:false});
canvas.addEventListener("touchmove", moveDrag, {passive:false});
canvas.addEventListener("touchend", endDrag, {passive:false});

// ----------------- DRAW -----------------
function drawBackground(){
    ctx.fillStyle = "#3ebd59";
    ctx.fillRect(0,0,900,500);
    ctx.fillStyle = "#2e8b47";
    ctx.fillRect(0,420,900,80);
}

function drawHole(){
    ctx.save();
    ctx.translate(hole.x,hole.y);
    ctx.fillStyle="#006400";
    ctx.beginPath(); ctx.arc(0,0,hole.r+5,0,Math.PI*2); ctx.fill();
    ctx.fillStyle="#000";
    ctx.beginPath(); ctx.arc(0,0,hole.r,0,Math.PI*2); ctx.fill();
    ctx.restore();
}

function drawObstacles(){
    ctx.fillStyle="#654321";
    obstacles.forEach(o=>ctx.fillRect(o.x,o.y,o.w,o.h));
}

function drawBall(){
    ctx.fillStyle="white";
    ctx.beginPath();
    ctx.arc(ball.x,ball.y,ball.r,0,Math.PI*2);
    ctx.fill();
}

function drawHUD(){
    ctx.fillStyle="white";
    ctx.font="28px Arial Black";
    ctx.fillText("Score: "+score+"   Level: "+level,20,35);
}

// ----------------- PHYSICS（安全不穿牆） -----------------
function physics(){
    let nextX = ball.x + ball.vx;
    let nextY = ball.y + ball.vy;

    const left = ball.r;
    const right = 900 - ball.r;
    const top = ball.r;
    const bottom = 420 - ball.r;

    if(nextX < left){ nextX = left; if(ball.vx < 0) ball.vx *= -0.8; }
    if(nextX > right){ nextX = right; if(ball.vx > 0) ball.vx *= -0.8; }
    if(nextY < top){ nextY = top; if(ball.vy < 0) ball.vy *= -0.8; }
    if(nextY > bottom){ nextY = bottom; if(ball.vy > 0) ball.vy *= -0.8; }

    ball.x = nextX;
    ball.y = nextY;

    ball.vx *= friction;
    ball.vy *= friction;

    if(Math.abs(ball.vx) < 0.02) ball.vx = 0;
    if(Math.abs(ball.vy) < 0.02) ball.vy = 0;

    let dx = ball.x - hole.x;
    let dy = ball.y - hole.y;
    if(Math.sqrt(dx*dx+dy*dy) < hole.r){
        score++;
        newLevel();
    }
}

// ----------------- LOOP -----------------
generateObstacles();
function loop(){
    ctx.clearRect(0,0,900,500);
    drawBackground();
    drawHole();
    drawObstacles();
    drawBall();
    drawHUD();
    if(!dragging) physics();
    requestAnimationFrame(loop);
}
loop();
</script>
""",
height=520,
scrolling=False
)

