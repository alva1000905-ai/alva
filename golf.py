import streamlit as st
st.set_page_config(page_title="Golf Game", layout="wide")

import streamlit.components.v1 as components

components.html(
"""
<style>
body { margin:0; overflow:hidden; background:#2ba84a; }
canvas { touch-action:none; }

/* ===== 新增：手機裁切用 ===== */
#game-wrapper {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}

@media (max-width: 768px) {
    #game-wrapper {
        align-items: flex-start;
    }
}
</style>

<!-- 只新增一層 wrapper -->
<div id="game-wrapper">
<canvas id="game" width="900" height="500"></canvas>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

/* ===== 新增：防止手機滑動 ===== */
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

/* ===== 以下完全保持你原本程式碼 ===== */
/* （中間所有內容一行未動） */

/* ...你的原始 JS 全部 그대로 ... */

</script>
""",
height=520,
scrolling=False)

