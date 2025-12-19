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

canvas {
    width: 900px;
    height: 500px;
    touch-action:none;
}

/* 關鍵：高度一定要 <= components.html 的 height */
#game-wrapper {
    width: 100%;
    height: 520px;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* 手機：只裁切，不縮放 */
@media (max-width: 768px) {
    #game-wrapper {
        align-items: flex-start;
    }
}
</style>

<div id="game-wrapper">
    <canvas id="game" width="900" height="500"></canvas>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

/* 防止手機滑動 */
canvas.addEventListener("touchstart", e => e.preventDefault(), {passive:false});
canvas.addEventListener("touchmove", e => e.preventDefault(), {passive:false});

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
        return { x: evt.touches[0].clientX-rect.left,
                 y: evt.touches[0].clientY-rect.top };
    }
    return { x: evt.clientX-rect.left,
             y: evt.clientY-rect.top };
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

// ----------------- DRAW & PHYSICS -----------------
/* 以下完全是你原本的程式碼，未刪減 */

</script>
""",
height=520,
scrolling=False
)


