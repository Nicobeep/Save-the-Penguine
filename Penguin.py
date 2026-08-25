import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="Save the Penguin",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# GAME
# ============================================================

GAME_HTML = r"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<style>

/* ============================================================
   PAGE
   ============================================================ */

html,
body {

    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    background: transparent;

    font-family: Arial, sans-serif;

}


/* ============================================================
   RESPONSIVE GAME CONTAINER
   ============================================================ */

#game-container {

    position: relative;

    width: 100vw;
    height: 100vh;

    overflow: hidden;

}


/*
    The actual game keeps its original
    1000 × 750 coordinate system.

    JavaScript scales it to fill
    the available browser space.
*/

#game {

    position: absolute;

    width: 1000px;
    height: 750px;

    left: 50%;
    top: 50%;

    transform-origin: center center;

    overflow: hidden;

    background: rgb(35, 135, 210);

    border-radius: 12px;

    user-select: none;

    cursor: pointer;

}


/* ============================================================
   WORLD
   ============================================================ */

#world {

    position: absolute;

    width: 1000px;
    height: 750px;

    left: 0;
    top: 0;

}


/* ============================================================
   WATER
   ============================================================ */

.water-wave {

    position: absolute;

    width: 35px;
    height: 12px;

    border-top:
        2px solid
        rgba(100, 190, 235, 0.75);

    border-radius: 50%;

    pointer-events: none;

}


/* ============================================================
   HUD
   ============================================================ */

#hud {

    position: absolute;

    left: 20px;
    top: 18px;

    z-index: 1000;

    color: white;

    text-shadow:
        1px 1px 3px
        rgba(0,0,0,0.35);

    pointer-events: none;

}


#score {

    font-size: 30px;

    font-weight: bold;

}


#instructions {

    margin-top: 6px;

    font-size: 18px;

}


#controls {

    margin-top: 4px;

    font-size: 16px;

}


#physics {

    position: absolute;

    bottom: 15px;
    left: 20px;

    color: white;

    font-size: 16px;

    z-index: 1000;

    text-shadow:
        1px 1px 3px
        rgba(0,0,0,0.35);

}


/* ============================================================
   ICE
   ============================================================ */

.ice {

    position: absolute;

    width: 55px;
    height: 55px;

    box-sizing: border-box;

    background:
        rgb(175, 230, 250);

    border:
        3px solid
        rgb(70, 155, 195);

    border-radius: 8px;

    transform-origin: center center;

    z-index: 20;

    cursor: pointer;

}


.ice:hover {

    box-shadow:
        0 0 0 4px
        rgba(245,205,60,0.9);

}


.ice.pillar {

    cursor: not-allowed;

}


.ice.falling {

    pointer-events: none;

}


/* ============================================================
   CONNECTIONS
   ============================================================ */

.connection {

    position: absolute;

    height: 3px;

    background:
        rgb(70,155,195);

    transform-origin:
        left center;

    z-index: 5;

    pointer-events: none;

}


/* ============================================================
   PILLAR INDICATORS
   ============================================================ */

.pillar-indicator {

    position: absolute;

    width: 10px;
    height: 10px;

    border-radius: 50%;

    background:
        rgb(25,100,150);

    transform:
        translate(-50%, -50%);

    z-index: 10;

    pointer-events: none;

}


/* ============================================================
   PENGUIN
   ============================================================ */

#penguin {

    position: absolute;

    width: 44px;
    height: 52px;

    transform:
        translate(-50%, -50%);

    z-index: 500;

    pointer-events: none;

}


.penguin-body {

    position: absolute;

    width: 44px;
    height: 44px;

    left: 0;
    top: 0;

    background:
        rgb(25,30,35);

    border-radius: 50%;

}


.penguin-belly {

    position: absolute;

    width: 26px;
    height: 27px;

    left: 9px;
    top: 15px;

    background:
        rgb(240,245,245);

    border-radius: 50%;

}


.eye {

    position: absolute;

    width: 9px;
    height: 9px;

    top: 10px;

    background: white;

    border-radius: 50%;

}


.eye.left {

    left: 8px;

}


.eye.right {

    right: 8px;

}


.pupil {

    position: absolute;

    width: 4px;
    height: 4px;

    top: 13px;

    background:
        rgb(25,30,35);

    border-radius: 50%;

}


.pupil.left {

    left: 11px;

}


.pupil.right {

    right: 11px;

}


.beak {

    position: absolute;

    left: 16px;
    top: 20px;

    width: 0;
    height: 0;

    border-left:
        6px solid transparent;

    border-right:
        6px solid transparent;

    border-top:
        9px solid
        rgb(255,165,45);

}


.foot {

    position: absolute;

    width: 22px;
    height: 7px;

    top: 39px;

    background:
        rgb(255,165,45);

    border-radius: 50%;

}


.foot.left {

    left: -2px;

}


.foot.right {

    right: -2px;

}


/* ============================================================
   RESTART BUTTON
   ============================================================ */

#restart-button {

    position: absolute;

    right: 20px;
    top: 20px;

    z-index: 1200;

    border: none;

    border-radius: 8px;

    padding:
        10px 18px;

    background:
        rgba(255,255,255,0.94);

    color:
        rgb(22,76,106);

    font-weight: bold;

    font-size: 16px;

    cursor: pointer;

}


#restart-button:hover {

    background: white;

    transform:
        scale(1.04);

}


/* ============================================================
   GAME OVER
   ============================================================ */

#game-over {

    position: absolute;

    inset: 0;

    background:
        rgba(0,0,0,0.52);

    z-index: 2000;

    display: none;

    align-items: center;

    justify-content: center;

    flex-direction: column;

    color: white;

}


#game-over-message {

    font-size: 42px;

    font-weight: bold;

    text-shadow:
        2px 2px 4px
        rgba(0,0,0,0.5);

}


#game-over-message.win {

    color:
        rgb(60,210,100);

}


#game-over-message.lose {

    color:
        rgb(225,60,60);

}


#restart-message {

    margin-top: 16px;

    font-size: 20px;

}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 600px) {

    #score {

        font-size: 25px;

    }

    #instructions {

        font-size: 15px;

    }

    #controls {

        font-size: 13px;

    }

    #physics {

        font-size: 13px;

    }

}

</style>

</head>


<body>


<div id="game-container">

    <div id="game">

        <div id="world"></div>


        <!-- ==================================================
             HUD
             ================================================== -->

        <div id="hud">

            <div id="score">
                Ice Broken: 0
            </div>

            <div id="instructions">
                Click ice blocks to break them
            </div>

            <div id="controls">
                R = Restart
            </div>

        </div>


        <div id="physics">
            1 hit = normal&nbsp;&nbsp;&nbsp;2 hits = falls
        </div>


        <!-- ==================================================
             RESTART
             ================================================== -->

        <button id="restart-button">
            Restart
        </button>


        <!-- ==================================================
             GAME OVER
             ================================================== -->

        <div id="game-over">

            <div id="game-over-message"></div>

            <div id="restart-message">
                Press R or click Restart
            </div>

        </div>

    </div>

</div>


<script>

/* ============================================================
   CONSTANTS
   ============================================================ */

const WIDTH = 1000;
const HEIGHT = 750;

const CENTER_X = WIDTH / 2;
const CENTER_Y = HEIGHT / 2;

const GRAVITY = 900;

const ICE_THICKNESS = 20;
const ICE_SIZE = 55;

const PENGUIN_RADIUS = 22;

const PLATFORM_HEIGHT = 180;

const FALL_LIMIT = -250;


/* ============================================================
   ELEMENTS
   ============================================================ */

const game =
    document.getElementById("game");

const gameContainer =
    document.getElementById(
        "game-container"
    );

const world =
    document.getElementById("world");

const scoreElement =
    document.getElementById("score");

const gameOverElement =
    document.getElementById(
        "game-over"
    );

const gameOverMessage =
    document.getElementById(
        "game-over-message"
    );

const restartButton =
    document.getElementById(
        "restart-button"
    );


/* ============================================================
   STATE
   ============================================================ */

let blocks = [];

let connections = [];

let pillars = [];

let penguin = null;

let iceBroken = 0;

let gameOver = false;

let won = false;

let lastTime =
    performance.now();


/* ============================================================
   RESPONSIVE SCALING
   ============================================================

   The actual game is still 1000 × 750.

   We scale that entire game to fit
   the available browser window.

   This means the game gets larger on
   large monitors and smaller on phones.
   ============================================================ */

function resizeGame() {

    const availableWidth =
        window.innerWidth;

    const availableHeight =
        window.innerHeight;


    const horizontalPadding = 8;

    const verticalPadding = 8;


    const scaleX =
        (
            availableWidth -
            horizontalPadding
        ) / WIDTH;


    const scaleY =
        (
            availableHeight -
            verticalPadding
        ) / HEIGHT;


    let scale =
        Math.min(
            scaleX,
            scaleY
        );


    /*
        Don't make the game tiny.

        On a normal desktop this will
        usually be around 1.0–1.4.
    */

    scale =
        Math.max(
            0.55,
            scale
        );


    game.style.transform =
        `translate(-50%, -50%) scale(${scale})`;

}


window.addEventListener(
    "resize",
    resizeGame
);

resizeGame();


/* ============================================================
   RANDOM
   ============================================================ */

function randomUniform(min, max) {

    return (
        min +
        Math.random() *
        (max - min)
    );

}


/* ============================================================
   WORLD → SCREEN
   ============================================================ */

function worldToScreen(x, y) {

    return {

        x:
            CENTER_X + x,

        y:
            CENTER_Y + y

    };

}


/* ============================================================
   ICE BLOCK
   ============================================================ */

class IceBlock {

    constructor(
        x,
        y,
        row,
        col
    ) {

        this.x = x;

        this.y = y;

        this.row = row;

        this.col = col;

        this.size =
            ICE_SIZE;

        this.z =
            PLATFORM_HEIGHT;

        this.vz = 0;

        this.angle = 0;

        this.angularVelocity = 0;

        this.mass = 1;

        this.alive = true;

        this.supported = false;

        this.connections = [];

        this.damage = 0;


        this.element =
            document.createElement(
                "div"
            );


        this.element.className =
            "ice";


        this.element.dataset.row =
            row;


        this.element.dataset.col =
            col;


        world.appendChild(
            this.element
        );


        this.element.addEventListener(
            "click",
            (event) => {

                event.stopPropagation();

                if (!gameOver) {

                    breakIce(this);

                }

            }
        );

    }


    update(dt) {

        if (!this.alive) {

            return;

        }


        /* ====================================================
           SUPPORTED
           ==================================================== */

        if (this.supported) {

            this.vz = 0;


            const difference =
                PLATFORM_HEIGHT -
                this.z;


            this.z +=
                difference *
                Math.min(
                    1,
                    15 * dt
                );


            this.angularVelocity *=
                0.90;

        }


        /* ====================================================
           FALLING
           ==================================================== */

        else {

            this.vz -=
                GRAVITY * dt;


            this.z +=
                this.vz * dt;


            this.angularVelocity *=
                0.995;


            this.angle +=
                this.angularVelocity * dt;

        }


        if (this.supported) {

            this.angle +=
                this.angularVelocity * dt;

        }


        /* ====================================================
           REMOVE AFTER FALLING
           ==================================================== */

        if (
            this.z <
            FALL_LIMIT
        ) {

            this.alive = false;

            this.element.remove();

            return;

        }


        this.render();

    }


    render() {

        if (!this.alive) {

            return;

        }


        const position =
            worldToScreen(
                this.x,
                this.y
            );


        const scale =
            Math.max(
                0.75,
                Math.min(
                    1.25,
                    1 +
                    this.z * 0.001
                )
            );


        const size =
            ICE_SIZE * scale;


        this.element.style.left =
            `${
                position.x -
                size / 2
            }px`;


        this.element.style.top =
            `${
                position.y -
                size / 2
            }px`;


        this.element.style.width =
            `${size}px`;


        this.element.style.height =
            `${size}px`;


        this.element.style.transform =
            `rotate(${
                -this.angle *
                180 /
                Math.PI
            }deg)`;

    }


    destroyElement() {

        if (
            this.element
        ) {

            this.element.remove();

        }

    }

}


/* ============================================================
   CONNECTION
   ============================================================ */

class Connection {

    constructor(a, b) {

        this.a = a;

        this.b = b;

        this.alive = true;


        this.element =
            document.createElement(
                "div"
            );


        this.element.className =
            "connection";


        world.appendChild(
            this.element
        );

    }


    render() {

        if (
            !this.alive ||
            !this.a.alive ||
            !this.b.alive
        ) {

            this.element.style.display =
                "none";

            return;

        }


        const a =
            worldToScreen(
                this.a.x,
                this.a.y
            );


        const b =
            worldToScreen(
                this.b.x,
                this.b.y
            );


        const dx =
            b.x - a.x;


        const dy =
            b.y - a.y;


        const length =
            Math.sqrt(
                dx * dx +
                dy * dy
            );


        const angle =
            Math.atan2(
                dy,
                dx
            ) *
            180 /
            Math.PI;


        this.element.style.display =
            "block";


        this.element.style.left =
            `${a.x}px`;


        this.element.style.top =
            `${a.y - 1.5}px`;


        this.element.style.width =
            `${length}px`;


        this.element.style.transform =
            `rotate(${angle}deg)`;

    }

}


/* ============================================================
   SUPPORT PILLAR
   ============================================================ */

class SupportPillar {

    constructor(block) {

        this.block = block;

        this.x = block.x;

        this.y = block.y;

        this.height =
            PLATFORM_HEIGHT;


        this.element =
            document.createElement(
                "div"
            );


        this.element.className =
            "pillar-indicator";


        world.appendChild(
            this.element
        );


        this.render();

    }


    supports() {

        return this.block.alive;

    }


    render() {

        const position =
            worldToScreen(
                this.x,
                this.y
            );


        this.element.style.left =
            `${position.x}px`;


        this.element.style.top =
            `${position.y}px`;

    }

}


/* ============================================================
   PENGUIN
   ============================================================ */

class Penguin {

    constructor(x, y) {

        this.x = x;

        this.y = y;


        this.z =
            PLATFORM_HEIGHT +
            ICE_THICKNESS +
            PENGUIN_RADIUS;


        this.vz = 0;

        this.mass = 1.5;

        this.alive = true;

        this.support = null;


        this.element =
            document.createElement(
                "div"
            );


        this.element.id =
            "penguin";


        this.element.innerHTML = `

            <div class="penguin-body"></div>

            <div class="penguin-belly"></div>

            <div class="eye left"></div>

            <div class="eye right"></div>

            <div class="pupil left"></div>

            <div class="pupil right"></div>

            <div class="beak"></div>

            <div class="foot left"></div>

            <div class="foot right"></div>

        `;


        world.appendChild(
            this.element
        );

    }


    findSupport() {

        let best = null;

        let bestDistance =
            Infinity;


        for (
            const block of blocks
        ) {

            if (!block.alive) {

                continue;

            }


            const dx =
                this.x -
                block.x;


            const dy =
                this.y -
                block.y;


            const distance =
                Math.sqrt(
                    dx * dx +
                    dy * dy
                );


            if (
                distance <
                block.size * 0.60
            ) {

                if (
                    distance <
                    bestDistance
                ) {

                    best =
                        block;

                    bestDistance =
                        distance;

                }

            }

        }


        return best;

    }


    update(dt) {

        if (!this.alive) {

            return;

        }


        this.vz -=
            GRAVITY * dt;


        const support =
            this.findSupport();


        if (support) {

            const iceTop =
                support.z +
                ICE_THICKNESS / 2;


            const penguinBottom =
                this.z -
                PENGUIN_RADIUS;


            if (
                penguinBottom <=
                    iceTop &&
                this.vz < 0
            ) {

                this.z =
                    iceTop +
                    PENGUIN_RADIUS;


                this.vz = 0;


                this.support =
                    support;

            }

        }
        else {

            this.support = null;

        }


        this.z +=
            this.vz * dt;


        if (
            this.z < -40
        ) {

            this.alive =
                false;

        }


        this.render();

    }


    render() {

        if (!this.alive) {

            this.element.style.display =
                "none";

            return;

        }


        this.element.style.display =
            "block";


        const position =
            worldToScreen(
                this.x,
                this.y
            );


        const scale =
            Math.max(
                0.7,
                Math.min(
                    1.25,
                    1 +
                    this.z * 0.001
                )
            );


        this.element.style.left =
            `${position.x}px`;


        this.element.style.top =
            `${position.y}px`;


        this.element.style.transform =
            `translate(-50%, -50%)
             scale(${scale})`;

    }

}


/* ============================================================
   CREATE LEVEL
   ============================================================ */

function createLevel() {

    blocks = [];

    connections = [];

    pillars = [];


    const rows = 7;

    const cols = 10;

    const spacing = 60;


    const startX =
        -(
            (cols - 1) *
            spacing
        ) / 2;


    const startY =
        -(
            (rows - 1) *
            spacing
        ) / 2;


    const grid = [];


    /* ========================================================
       ICE BLOCKS
       ======================================================== */

    for (
        let row = 0;
        row < rows;
        row++
    ) {

        const rowBlocks = [];


        for (
            let col = 0;
            col < cols;
            col++
        ) {

            let x =
                startX +
                col * spacing;


            let y =
                startY +
                row * spacing;


            x +=
                randomUniform(
                    -2,
                    2
                );


            y +=
                randomUniform(
                    -2,
                    2
                );


            const block =
                new IceBlock(
                    x,
                    y,
                    row,
                    col
                );


            rowBlocks.push(
                block
            );


            blocks.push(
                block
            );

        }


        grid.push(
            rowBlocks
        );

    }


    /* ========================================================
       FOUR CORNER PILLARS
       ======================================================== */

    const cornerBlocks = [

        grid[0][0],

        grid[0][cols - 1],

        grid[rows - 1][0],

        grid[rows - 1][cols - 1]

    ];


    for (
        const block of
        cornerBlocks
    ) {

        pillars.push(
            new SupportPillar(
                block
            )
        );


        block.element.classList.add(
            "pillar"
        );

    }


    /* ========================================================
       CONNECTIONS
       ======================================================== */

    for (
        let row = 0;
        row < rows;
        row++
    ) {

        for (
            let col = 0;
            col < cols;
            col++
        ) {

            const current =
                grid[row][col];


            if (
                col <
                cols - 1
            ) {

                const connection =
                    new Connection(
                        current,
                        grid[row][col + 1]
                    );


                connections.push(
                    connection
                );


                current.connections.push(
                    connection
                );


                grid[row][col + 1]
                    .connections
                    .push(
                        connection
                    );

            }


            if (
                row <
                rows - 1
            ) {

                const connection =
                    new Connection(
                        current,
                        grid[row + 1][col]
                    );


                connections.push(
                    connection
                );


                current.connections.push(
                    connection
                );


                grid[row + 1][col]
                    .connections
                    .push(
                        connection
                    );

            }

        }

    }


    /* ========================================================
       PENGUIN
       ======================================================== */

    const centerRow =
        Math.floor(
            Math.random() *
            (rows - 2)
        ) + 1;


    const centerCol =
        Math.floor(
            Math.random() *
            (cols - 2)
        ) + 1;


    const center =
        grid[
            centerRow
        ][
            centerCol
        ];


    penguin =
        new Penguin(
            center.x,
            center.y
        );

}


/* ============================================================
   STRUCTURAL SUPPORT
   ============================================================ */

function updateStructuralSupport() {

    for (
        const block of blocks
    ) {

        block.supported =
            false;

    }


    const queue = [];


    for (
        const pillar of pillars
    ) {

        const block =
            pillar.block;


        if (
            block.alive
        ) {

            block.supported =
                true;


            queue.push(
                block
            );

        }

    }


    while (
        queue.length > 0
    ) {

        const current =
            queue.shift();


        for (
            const connection
            of current.connections
        ) {

            if (
                !connection.alive
            ) {

                continue;

            }


            if (
                !connection.a.alive ||
                !connection.b.alive
            ) {

                continue;

            }


            const neighbor =
                connection.a === current
                    ? connection.b
                    : connection.a;


            if (
                !neighbor.supported
            ) {

                neighbor.supported =
                    true;


                queue.push(
                    neighbor
                );

            }

        }

    }

}


/* ============================================================
   PILLAR CHECK
   ============================================================ */

function isPillarBlock(block) {

    return pillars.some(
        pillar =>
            pillar.block === block
    );

}


/* ============================================================
   ADJACENT BLOCKS
   ============================================================ */

function getAdjacentBlocks(block) {

    const adjacent = [];


    const ADJACENT_DISTANCE =
        70;


    const ALIGNMENT_TOLERANCE =
        15;


    for (
        const other of blocks
    ) {

        if (
            other === block ||
            !other.alive
        ) {

            continue;

        }


        if (
            isPillarBlock(other)
        ) {

            continue;

        }


        const dx =
            Math.abs(
                other.x -
                block.x
            );


        const dy =
            Math.abs(
                other.y -
                block.y
            );


        const horizontal =
            dx <
                ADJACENT_DISTANCE &&
            dy <
                ALIGNMENT_TOLERANCE;


        const vertical =
            dy <
                ADJACENT_DISTANCE &&
            dx <
                ALIGNMENT_TOLERANCE;


        if (
            horizontal ||
            vertical
        ) {

            adjacent.push(
                other
            );

        }

    }


    return adjacent;

}


/* ============================================================
   START FALLING
   ============================================================ */

function startFalling(block) {

    if (
        !block.alive
    ) {

        return;

    }


    block.supported =
        false;


    if (
        block.vz >= 0
    ) {

        block.vz =
            -50;

    }


    if (
        Math.abs(
            block.angularVelocity
        ) < 0.2
    ) {

        block.angularVelocity =
            randomUniform(
                -3,
                3
            );

    }


    block.element.classList.add(
        "falling"
    );

}


/* ============================================================
   BREAK ICE
   ============================================================ */

function breakIce(block) {

    if (
        !block ||
        !block.alive ||
        gameOver
    ) {

        return;

    }


    /* ========================================================
       PILLARS CANNOT BE DESTROYED
       ======================================================== */

    if (
        isPillarBlock(block)
    ) {

        return;

    }


    /* ========================================================
       FIND ADJACENT BLOCKS FIRST
       ======================================================== */

    const adjacentBlocks =
        getAdjacentBlocks(
            block
        );


    /* ========================================================
       DIRECT CLICK
       ======================================================== */

    block.alive =
        false;


    block.supported =
        false;


    block.destroyElement();


    iceBroken++;


    updateScore();


    /* ========================================================
       REMOVE CONNECTIONS
       ======================================================== */

    for (
        const connection
        of connections
    ) {

        if (
            connection.a === block ||
            connection.b === block
        ) {

            connection.alive =
                false;

        }

    }


    /* ========================================================
       COLLATERAL DAMAGE
       ======================================================== */

    for (
        const neighbor
        of adjacentBlocks
    ) {

        if (
            !neighbor.alive
        ) {

            continue;

        }


        if (
            isPillarBlock(
                neighbor
            )
        ) {

            continue;

        }


        neighbor.damage++;


        /* ====================================================
           SECOND HIT → FALL
           ==================================================== */

        if (
            neighbor.damage >= 2
        ) {

            startFalling(
                neighbor
            );


            for (
                const connection
                of connections
            ) {

                if (
                    connection.a === neighbor ||
                    connection.b === neighbor
                ) {

                    connection.alive =
                        false;

                }

            }

        }

    }


    /* ========================================================
       STRUCTURAL SUPPORT
       ======================================================== */

    updateStructuralSupport();


    /* ========================================================
       UNSUPPORTED ICE FALLS
       ======================================================== */

    for (
        const ice of blocks
    ) {

        if (
            !ice.alive
        ) {

            continue;

        }


        if (
            !ice.supported
        ) {

            startFalling(
                ice
            );

        }

    }

}


/* ============================================================
   SCORE
   ============================================================ */

function updateScore() {

    scoreElement.innerText =
        `Ice Broken: ${iceBroken}`;

}


/* ============================================================
   GAME OVER
   ============================================================ */

function showGameOver() {

    gameOver =
        true;


    gameOverElement.style.display =
        "flex";


    if (won) {

        gameOverMessage.innerText =
            "PENGUIN SAVED!";


        gameOverMessage.className =
            "win";

    }
    else {

        gameOverMessage.innerText =
            "PENGUIN FELL!";


        gameOverMessage.className =
            "lose";

    }

}


/* ============================================================
   RESET
   ============================================================ */

function resetGame() {

    gameOver =
        false;


    won =
        false;


    iceBroken =
        0;


    updateScore();


    gameOverElement.style.display =
        "none";


    world.innerHTML =
        "";


    createLevel();


    updateStructuralSupport();


    for (
        const block of blocks
    ) {

        block.render();

    }


    for (
        const connection
        of connections
    ) {

        connection.render();

    }


    for (
        const pillar
        of pillars
    ) {

        pillar.render();

    }


    penguin.render();

}


/* ============================================================
   UPDATE
   ============================================================ */

function update(dt) {

    if (
        gameOver
    ) {

        return;

    }


    updateStructuralSupport();


    /* ========================================================
       ICE
       ======================================================== */

    for (
        const block of blocks
    ) {

        block.update(
            dt
        );

    }


    /* ========================================================
       CONNECTIONS
       ======================================================== */

    for (
        const connection
        of connections
    ) {

        connection.render();

    }


    /* ========================================================
       PENGUIN
       ======================================================== */

    penguin.update(
        dt
    );


    /* ========================================================
       LOSE
       ======================================================== */

    if (
        !penguin.alive
    ) {

        won =
            false;


        showGameOver();

        return;

    }


    /* ========================================================
       WIN
       ======================================================== */

    const aliveCount =
        blocks.filter(
            block =>
                block.alive
        ).length;


    if (
        penguin.alive &&
        aliveCount <= 20
    ) {

        won =
            true;


        showGameOver();

    }

}


/* ============================================================
   GAME LOOP
   ============================================================ */

function gameLoop(timestamp) {

    let dt =
        (
            timestamp -
            lastTime
        ) / 1000;


    dt =
        Math.min(
            dt,
            0.02
        );


    lastTime =
        timestamp;


    update(dt);


    requestAnimationFrame(
        gameLoop
    );

}


/* ============================================================
   RESTART BUTTON
   ============================================================ */

restartButton.addEventListener(
    "click",
    function(event) {

        event.stopPropagation();

        resetGame();

    }
);


/* ============================================================
   KEYBOARD
   ============================================================ */

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "r" ||
            event.key === "R"
        ) {

            resetGame();

        }

    }
);


/* ============================================================
   WATER WAVES
   ============================================================ */

function createWaterWaves() {

    for (
        let y = 10;
        y < HEIGHT;
        y += 45
    ) {

        for (
            let x = 10;
            x < WIDTH;
            x += 70
        ) {

            const wave =
                document.createElement(
                    "div"
                );


            wave.className =
                "water-wave";


            wave.style.left =
                `${x}px`;


            wave.style.top =
                `${y}px`;


            wave.style.opacity =
                String(
                    0.25 +
                    Math.random() *
                    0.5
                );


            game.appendChild(
                wave
            );

        }

    }

}


/* ============================================================
   START
   ============================================================ */

createWaterWaves();

resetGame();

resizeGame();

requestAnimationFrame(
    gameLoop
);

</script>

</body>

</html>
"""


# ============================================================
# DISPLAY GAME
# ============================================================

components.html(
    GAME_HTML,
    height=1000,
    scrolling=False,
)
