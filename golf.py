import streamlit as st
st.set_page_config(page_title="Golf Game", layout="wide")

import streamlit.components.v1 as components

components.html(
"""
<style>
body { margin:0; overflow:hidden; background:#2ba84a; }

#game-wrapper{
    width:100%;
    height:100%;
    display:flex;
    justify-content:center;
    align-items:flex-start;
}

canvas { 
    touch-action:none; 
    transform-origin: top left;
}
</style>

<div id="game-wrapper">
    <canvas id="game" width="900" height="500"></canvas>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// ----------------- RESPONSIVE SCALE -----------------
function resizeGame(){
    const screenW = window.innerWidth;
    const screenH = window.innerHeight;

    const scaleW = screenW / 900;
    const scaleH = screenH / 500;

    const scale = Math.min(scaleW, scaleH, 1);
    canvas.style.transform = `scale(${scale})`;
}

window.addEventListener("resize", resizeGame);
resizeGame();

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
    ball.x = 150; ball.y = 250; ball.vx = 0; ball.vy = 0;
    hole.x = 200 + Math.random() * 600;
    hole.y = 80 + Math.random() * 300;
    generateObstacles();
    level++;
}

// ----------------- INPUT -----------------
function getPos(evt){
    let rect = canvas.getBoundingClientRect();
    let scaleX = canvas.width / rect.width;
    let scaleY = canvas.height / rect.height;

    if(evt.touches){
        return { 
            x: (evt.touches[0].clientX - rect.left) * scaleX,
            y: (evt.touches[0].clientY - rect.top) * scaleY
        };
    }
    return { 
        x: (evt.clientX - rect.left) * scaleX,
        y: (evt.clientY - rect.top) * scaleY
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

canvas.addEventListener("touchstart", startDrag);
canvas.addEventListener("touchmove", moveDrag);
canvas.addEventListener("touchend", endDrag);

// ----------------- DRAW -----------------
function drawBackground(){
    ctx.fillStyle = "#3ebd59";
    ctx.fillRect(0,0,900,500);
    ctx.fillStyle = "#2e8b47";
    ctx.fillRect(0,420,900,80);
    ctx.fillStyle="rgba(0,0,0,0.06)";
    for(let i=0;i<100;i++){
        let x=Math.random()*900; let y=Math.random()*500;
        ctx.fillRect(x,y,2,6);
    }
}

function drawHole(){
    ctx.save(); 
    ctx.translate(hole.x,hole.y);
    ctx.fillStyle="#006400";
    ctx.beginPath(); ctx.arc(0,0,hole.r+5,0,Math.PI*2); ctx.fill();
    ctx.fillStyle="#000";
    ctx.beginPath(); ctx.arc(0,0,hole.r,0,Math.PI*2); ctx.fill();
    ctx.strokeStyle="red"; ctx.lineWidth=2;
    ctx.beginPath(); ctx.moveTo(0,-hole.r-15); ctx.lineTo(0,0); ctx.stroke();
    ctx.fillStyle="red";
    ctx.beginPath(); ctx.moveTo(0,-hole.r-15); ctx.lineTo(8,-hole.r-8); ctx.lineTo(0,-hole.r-1); ctx.closePath(); ctx.fill();
    ctx.restore();
}

function drawObstacles(){
    ctx.fillStyle="#654321";
    for(let o of obstacles) ctx.fillRect(o.x,o.y,o.w,o.h);
}

function drawBall(){
    ctx.save(); ctx.translate(ball.x,ball.y);
    ctx.fillStyle="white"; ctx.beginPath(); ctx.arc(0,0,ball.r,0,Math.PI*2); ctx.fill();
    ctx.fillStyle="rgba(0,0,0,0.25)";
    ctx.beginPath(); ctx.ellipse(4,6,ball.r*0.6,ball.r*0.3,0,0,Math.PI*2); ctx.fill();
    ctx.restore();
}

function drawHUD(){
    ctx.fillStyle="white"; ctx.font="32px Arial Black";
    ctx.fillText("Score: "+score+"    Level: "+level,20,40);
}

// ----------------- POWER BAR -----------------
function drawPowerBar(){
    if(dragging && dragEnd){
        let dx = dragStart.x - dragEnd.x;
        let dy = dragStart.y - dragEnd.y;
        let power = Math.min(Math.sqrt(dx*dx + dy*dy), 150);
        ctx.fillStyle="rgba(255,0,0,0.6)";
        ctx.fillRect(ball.x - 50, ball.y - 30, power * 0.6, 10);
        ctx.strokeStyle="#fff";
        ctx.strokeRect(ball.x - 50, ball.y - 30, 150*0.6, 10);
    }
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

// ----------------- COLLISION -----------------
function collideObstacles(){
    for(let o of obstacles){
        if(ball.x+ball.r>o.x && ball.x-ball.r<o.x+o.w &&
           ball.y+ball.r>o.y && ball.y-ball.r<o.y+o.h){
            if(ball.x<o.x || ball.x>o.x+o.w) ball.vx*=-0.8;
            if(ball.y<o.y || ball.y>o.y+o.h) ball.vy*=-0.8;
        }
    }
}

// ----------------- PHYSICS -----------------
function physics(){
    ball.x += ball.vx; ball.y += ball.vy;

    let margin = ball.r + 5;
    if(ball.x < margin){ ball.x = margin; ball.vx*=-0.7; }
    if(ball.x > 900 - margin){ ball.x = 900 - margin; ball.vx*=-0.7; }
    if(ball.y < margin){ ball.y = margin; ball.vy*=-0.7; }
    if(ball.y > 420 - margin){ ball.y = 420 - margin; ball.vy*=-0.7; }

    if(ball.y > 420){ ball.vx *= 0.90; ball.vy *= 0.90; }
    else { ball.vx *= 0.985; ball.vy *= 0.985; }

    collideObstacles();

    let dx = ball.x - hole.x; let dy = ball.y - hole.y;
    if(Math.sqrt(dx*dx+dy*dy) < hole.r){ score++; newLevel(); }
}

// ----------------- MAIN LOOP -----------------
generateObstacles();
function loop(){
    ctx.clearRect(0,0,900,500);
    drawBackground(); 
    drawHole(); 
    drawObstacles();
    drawBall(); 
    drawHUD(); 
    drawAimLine();
    drawPowerBar();
    if(!dragging) physics();
    requestAnimationFrame(loop);
}
loop();
</script>
""",
height=520,
scrolling=False
)


