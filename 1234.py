import streamlit as st
st.set_page_config(page_title="Golf Game", layout="wide")

import streamlit.components.v1 as components

components.html(
"""
<style>
body {
    margin: 0;
    overflow: hidden;
    background: #2ba84a;
}
</style>

<canvas id="game" width="900" height="500" style="width:100%;touch-action:none;"></canvas>

<script>

// ----------------------------------------------------
// CANVAS SETUP
// ----------------------------------------------------
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// ----------------------------------------------------
// GAME STATE
// ----------------------------------------------------
let level = 1;
let score = 0;

let ball = {
    x: 150,
    y: 250,
    vx: 0,
    vy: 0,
    r: 12
};

let hole = {
    x: 750,
    y: 250,
    r: 18
};

let friction = 0.985;
let stickyFriction = 0.90;   // bottom zone friction

let obstacles = [];

// ----------------------------------------------------
// OBSTACLE GENERATION
// ----------------------------------------------------
function generateObstacles() {
    obstacles = [];
    let count = Math.min(3 + level, 8);

    for (let i = 0; i < count; i++) {
        let w = 40 + Math.random()*100;
        let h = 20 + Math.random()*60;
        let x = 150 + Math.random()*650;
        let y = 50 + Math.random()*350;

        obstacles.push({ x, y, w, h });
    }
}

// ----------------------------------------------------
// LEVEL GENERATION
// ----------------------------------------------------
function newLevel() {
    ball.x = 150;
    ball.y = 250;
    ball.vx = 0;
    ball.vy = 0;

    hole.x = 200 + Math.random()*600;
    hole.y = 80 + Math.random()*300;

    generateObstacles();

    level++;
}

// ----------------------------------------------------
// INPUT HANDLING (Drag for direction + power)
// ----------------------------------------------------
let dragStart = null;
let dragging = false;
let dragEnd = null;

function getPos(evt) {
    let rect = canvas.getBoundingClientRect();
    if (evt.touches) {
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

function startDrag(evt) {
    dragStart = getPos(evt);
    dragging = true;
}

function moveDrag(evt) {
    if (dragging) dragEnd = getPos(evt);
}

function endDrag(evt) {
    if (!dragging) return;

    dragEnd = dragEnd || dragStart;

    // stronger pull factor
    let dx = dragStart.x - dragEnd.x;
    let dy = dragStart.y - dragEnd.y;

    ball.vx = dx * 0.12;   // increased from 0.07
    ball.vy = dy * 0.12;

    dragging = false;
    dragStart = null;
    dragEnd = null;
}


// EVENT REGISTRATION
canvas.addEventListener("mousedown", startDrag);
canvas.addEventListener("mousemove", moveDrag);
canvas.addEventListener("mouseup", endDrag);

canvas.addEventListener("touchstart", startDrag);
canvas.addEventListener("touchmove", moveDrag);
canvas.addEventListener("touchend", endDrag);

// ----------------------------------------------------
// DRAW FUNCTIONS
// ----------------------------------------------------
function drawBackground() {
    ctx.fillStyle = "#3ebd59";
    ctx.fillRect(0,0,900,500);

    // sticky zone at bottom
    ctx.fillStyle = "#2e8b47";
    ctx.fillRect(0,420,900,80);

    ctx.fillStyle = "rgba(0,0,0,0.06)";
    for (let i=0;i<200;i++){
        let x = Math.random()*900;
        let y = Math.random()*500;
        ctx.fillRect(x,y,4,10);
    }
}

function drawHole() {
    ctx.save();
    ctx.translate(hole.x, hole.y);

    ctx.fillStyle = "#000";
    ctx.beginPath();
    ctx.ellipse(0, 0, hole.r, hole.r*0.6, 0, 0, Math.PI*2);
    ctx.fill();

    ctx.restore();
}

function drawObstacles() {
    ctx.fillStyle = "#654321";
    for (let o of obstacles) {
        ctx.fillRect(o.x, o.y, o.w, o.h);
    }
}

function drawBall() {
    ctx.save();
    ctx.translate(ball.x, ball.y);

    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(0, 0, ball.r, 0, Math.PI*2);
    ctx.fill();

    // shadow
    ctx.fillStyle = "rgba(0,0,0,0.25)";
    ctx.beginPath();
    ctx.ellipse(4, 6, ball.r*0.6, ball.r*0.3, 0, 0, Math.PI*2);
    ctx.fill();

    ctx.restore();
}

function drawHUD() {
    ctx.fillStyle = "white";
    ctx.font = "32px Arial Black";
    ctx.fillText("Score: " + score + "    Level: " + level, 20, 40);
}

// ----------------------------------------------------
// COLLISION WITH OBSTACLES
// ----------------------------------------------------
function collideObstacles() {
    for (let o of obstacles) {
        if (
            ball.x + ball.r > o.x &&
            ball.x - ball.r < o.x + o.w &&
            ball.y + ball.r > o.y &&
            ball.y - ball.r < o.y + o.h
        ) {
            // bounce back
            if (ball.x < o.x || ball.x > o.x + o.w) ball.vx *= -0.8;
            if (ball.y < o.y || ball.y > o.y + o.h) ball.vy *= -0.8;
        }
    }
}

// ----------------------------------------------------
// GAME PHYSICS
// ----------------------------------------------------
function physics() {
    ball.x += ball.vx;
    ball.y += ball.vy;

    // sticky bottom zone
    if (ball.y > 420) {
        ball.vx *= stickyFriction;
        ball.vy *= stickyFriction;
    } else {
        ball.vx *= friction;
        ball.vy *= friction;
    }

    // walls
    if (ball.x < ball.r) { ball.x = ball.r; ball.vx *= -0.7; }
    if (ball.x > 900-ball.r) { ball.x = 900-ball.r; ball.vx *= -0.7; }
    if (ball.y < ball.r) { ball.y = ball.r; ball.vy *= -0.7; }
    if (ball.y > 500-ball.r) { ball.y = 500-ball.r; ball.vy *= -0.7; }

    collideObstacles();

    // hole detection
    let dx = ball.x - hole.x;
    let dy = ball.y - hole.y;
    if (Math.sqrt(dx*dx + dy*dy) < hole.r) {
        score++;
        newLevel();
    }
}

// ----------------------------------------------------
// MAIN LOOP
// ----------------------------------------------------
generateObstacles();
function loop() {
    ctx.clearRect(0,0,900,500);

    drawBackground();
    drawHole();
    drawObstacles();
    drawBall();
    drawHUD();

    if (!dragging) physics();

    requestAnimationFrame(loop);
}
loop();

</script>
""",
height=520,
scrolling=False)
