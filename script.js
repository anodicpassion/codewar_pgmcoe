//based on an Example by @curran
window.requestAnimFrame = (function () { return window.requestAnimationFrame })();
var canvas = document.getElementById("space");
var c = canvas.getContext("2d");

var numStars = 1900;
var radius = '0.' + Math.floor(Math.random() * 9) + 1;
var focalLength = canvas.width * 2;
var warp = 0;
var centerX, centerY;

var stars = [], star;
var i;

var animate = true;

initializeStars();

function executeFrame() {

    if (animate)
        requestAnimFrame(executeFrame);
    moveStars();
    drawStars();
}

function initializeStars() {
    centerX = canvas.width / 2;
    centerY = canvas.height / 2;

    stars = [];
    for (i = 0; i < numStars; i++) {
        star = {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            z: Math.random() * canvas.width,
            o: '0.' + Math.floor(Math.random() * 99) + 1
        };
        stars.push(star);
    }
}

function moveStars() {
    for (i = 0; i < numStars; i++) {
        star = stars[i];
        star.z--;

        if (star.z <= 0) {
            star.z = canvas.width;
        }
    }
}

function drawStars() {
    var pixelX, pixelY, pixelRadius;

    // Resize to the screen
    if (canvas.width != window.innerWidth || canvas.width != window.innerWidth) {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        initializeStars();
    }
    if (warp == 0) {
        c.fillStyle = "rgba(0,10,20,1)";
        c.fillRect(0, 0, canvas.width, canvas.height);
    }
    c.fillStyle = "rgba(209, 255, 255, " + radius + ")";
    for (i = 0; i < numStars; i++) {
        star = stars[i];

        pixelX = (star.x - centerX) * (focalLength / star.z);
        pixelX += centerX;
        pixelY = (star.y - centerY) * (focalLength / star.z);
        pixelY += centerY;
        pixelRadius = 1 * (focalLength / star.z);

        c.fillRect(pixelX, pixelY, pixelRadius, pixelRadius);
        c.fillStyle = "rgba(209, 255, 255, " + star.o + ")";
        //c.fill();
    }
}


executeFrame();

function clg_name(){
    
}

function typeWriterEffect() {
    const text = "Code-War";
    const target = document.getElementById("type-write");
    let index = 0;
    let blinkCount = 0;

    function blinkCursor(times, callback) {
        let blinkInterval = setInterval(() => {
            target.innerHTML = (target.innerHTML.endsWith("|") ? target.innerHTML.slice(0, -1) : target.innerHTML + "|");
            blinkCount++;
            if (blinkCount >= times * 2) {
                clearInterval(blinkInterval);
                callback();
            }
        }, 400);
    }

    function typeText() {
        if (index < text.length) {
            if(index == text.length-1){
                target.innerHTML = text.slice(0, index + 1) + "";

            }
            else{
                target.innerHTML = text.slice(0, index + 1) + "|";
            }
            index++;
            setTimeout(typeText, 100);
        } else {
            blinkCount = 0;
            removeCursor();
            
            
            // blinkCursor(2, removeCursor);
        }
    }

    function removeCursor() {
        target.innerHTML = text;
        setTimeout(function () {
            
            $("#clg_name").fadeIn();
            $("#w").fadeIn(4000);

        }, 200);
        
    }

    blinkCursor(3, typeText);
}

function backgorund_blb_app(ini){
    var i = ini; 
    const increment_o = 0.05;
    function inc_o () {
        document.getElementById("splash").style.opacity = i;
        i = i - increment_o
        if (i > 1){
            console.log(i)
            setTimeout(inc_o, 20);
        }
        else{
            document.getElementById("splash").style.display = "none";
        }
    }
    inc_o();
}

window.addEventListener("load", function() {
    this.setTimeout(function () {
        backgorund_blb_app(1);
        typeWriterEffect(); 
    }, 100)
    
        
        
});

// document.addEventListener("DOMContentLoaded", 
//     function () {
//         typeWriterEffect(); 
        
//         backgorund_blb_app(1);
// });
