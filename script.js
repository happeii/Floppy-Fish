
//board
let board;
let boardWidth = 360;
let boardHeight = 640;
let context;

//fish
let fishWidth = 34; //width/height ratio = 408/228 = 17/12
let fishHeight = 24;
let fishX = boardWidth/8;
let fishY = boardHeight/2;
let fishImg;

let fish = {
    x : fishX,
    y : fishY,
    width : fishWidth,
    height : fishHeight
}

//corals
let coralArray = [];
let coralWidth = 64; //width/height ratio = 384/3072 = 1/8
let coralHeight = 512;
let coralX = boardWidth;
let coralY = 0;

let topcoralImg;
let bottomcoralImg;

//physics
let velocityX = -2; //corals moving left speed
let velocityY = 0; //fish jump speed
let gravity = 0.2;

let gameOver = false;
let score = 0;

window.onload = function() {
    board = document.getElementById("board");
    board.height = boardHeight;
    board.width = boardWidth;
    context = board.getContext("2d"); //used for drawing on the board

    //draw flappy fish
    // context.fillStyle = "green";
    // context.fillRect(fish.x, fish.y, fish.width, fish.height);

    //load images
    fishImg = new Image();
    fishImg.src = "./assets/fish.png";
    fishImg.onload = function() {
        context.drawImage(fishImg, fish.x, fish.y, fish.width, fish.height);
    }

    topcoralImg = new Image();
    topcoralImg.src = "./assets/coraldown.png";

    bottomcoralImg = new Image();
    bottomcoralImg.src = "./assets/coralup.png";

    requestAnimationFrame(update);
    setInterval(placecorals, 1500); //every 1.5 seconds
    document.addEventListener("keydown", movefish);
}

function update() {
    requestAnimationFrame(update);
    if (gameOver) {
        return;
    }
    context.clearRect(0, 0, board.width, board.height);

    //fish
    velocityY += gravity;
    // fish.y += velocityY;
    fish.y = Math.max(fish.y + velocityY, 0); //apply gravity to current fish.y, limit the fish.y to top of the canvas
    context.drawImage(fishImg, fish.x, fish.y, fish.width, fish.height);

    if (fish.y > board.height) {
        gameOver = true;
    }

    //corals
    for (let i = 0; i < coralArray.length; i++) {
        let coral = coralArray[i];
        coral.x += velocityX;
        context.drawImage(coral.img, coral.x, coral.y, coral.width, coral.height);

        if (!coral.passed && fish.x > coral.x + coral.width) {
            score += 0.5; //0.5 because there are 2 corals! so 0.5*2 = 1, 1 for each set of corals
            coral.passed = true;
        }

        if (detectCollision(fish, coral)) {
            gameOver = true;
        }
    }

    //clear corals
    while (coralArray.length > 0 && coralArray[0].x < -coralWidth) {
        coralArray.shift(); //removes first element from the array
    }

    //score
    context.fillStyle = "white";
    context.font="45px sans-serif";
    context.fillText(score, 5, 45);

    if (gameOver) {
        context.fillText("GAME OVER", 5, 90);
    }
}

function placecorals() {
    if (gameOver) {
        return;
    }

    //(0-1) * coralHeight/2.
    // 0 -> -128 (coralHeight/4)
    // 1 -> -128 - 256 (coralHeight/4 - coralHeight/2) = -3/4 coralHeight
    let randomcoralY = coralY - coralHeight/4 - Math.random()*(coralHeight/2);
    let openingSpace = board.height/4;

    let topcoral = {
        img : topcoralImg,
        x : coralX,
        y : randomcoralY,
        width : coralWidth,
        height : coralHeight,
        passed : false
    }
    coralArray.push(topcoral);

    let bottomcoral = {
        img : bottomcoralImg,
        x : coralX,
        y : randomcoralY + coralHeight + openingSpace,
        width : coralWidth,
        height : coralHeight,
        passed : false
    }
    coralArray.push(bottomcoral);
}

function movefish(e) {
    if (e.code == "Space" || e.code == "ArrowUp" || e.code == "KeyW" || e.button == 1) {
        //jump
        velocityY = -6;

        //reset game
        if (gameOver) {
            fish.y = fishY;
            coralArray = [];
            score = 0;
            gameOver = false;
        }
    }
}

function detectCollision(a, b) {
    return a.x < b.x + b.width &&   //a's top left corner doesn't reach b's top right corner
           a.x + a.width > b.x &&   //a's top right corner passes b's top left corner
           a.y < b.y + b.height &&  //a's top left corner doesn't reach b's bottom left corner
           a.y + a.height > b.y;    //a's bottom left corner passes b's top left corner
}