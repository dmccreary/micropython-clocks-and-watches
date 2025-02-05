// MicroSim Template with region drawing parameters
let canvasWidth = 730;  // increased to fit 4 digits
let drawHeight = 200;
let controlHeight = 50;
let canvasHeight = drawHeight + controlHeight;
let leftMargin = 0;
let topMargin = 100;
let margin = 25;
let defaultTextSize = 36;

let segmentMapping = [
  [1, 1, 1, 1, 1, 1, 0], // 0
  [0, 1, 1, 0, 0, 0, 0], // 1
  [1, 1, 0, 1, 1, 0, 1], // 2
  [1, 1, 1, 1, 0, 0, 1], // 3
  [0, 1, 1, 0, 0, 1, 1], // 4
  [1, 0, 1, 1, 0, 1, 1], // 5
  [1, 0, 1, 1, 1, 1, 1], // 6
  [1, 1, 1, 0, 0, 0, 0], // 7
  [1, 1, 1, 1, 1, 1, 1], // 8
  [1, 1, 1, 1, 0, 1, 1]  // 9
];

function setup() {
    const canvas = createCanvas(canvasWidth, canvasHeight);
    var mainElement = document.querySelector('main');
    canvas.parent(mainElement);
    textSize(defaultTextSize);
}

function draw() {
    // Background
    fill('aliceblue');
    stroke('sliver');
    strokeWeight(1);
    rect(0, 0, canvasWidth, drawHeight);
    fill('white');
    rect(0, drawHeight, canvasWidth, controlHeight);

    // Get current time
    let now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();

    // Convert to 12-hour format
    let ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // convert 0 to 12

    // Split digits
    let h1 = Math.floor(hours / 10);
    let h2 = hours % 10;
    let m1 = Math.floor(minutes / 10);
    let m2 = minutes % 10;

    let digitSize = 60;
    let spacing = digitSize * 3;

    // Draw four digits

    // Draw hours
    if (h1 !== 0) { // Only show first hour digit if not zero
        drawDigit(h1, leftMargin, topMargin, digitSize);
    }
    drawDigit(h2, leftMargin + spacing, topMargin, digitSize);
    
    // Draw colon
    fill('navy');
    noStroke();
    circle(leftMargin + spacing * 1.5, topMargin - digitSize/2, 15);
    circle(leftMargin + spacing * 1.5, topMargin + digitSize/2, 15);
    
    // Draw minutes
    drawDigit(m1, leftMargin + spacing * 2, topMargin, digitSize);
    drawDigit(m2, leftMargin + spacing * 3, topMargin, digitSize);

    // Draw AM/PM
    noStroke();
    textSize(defaultTextSize);
    fill('navy');
    text(ampm, leftMargin + spacing * 3.5, drawHeight-margin-10);
}

function drawDigit(digit, x, y, size) {
    let segmentOn = segmentMapping[digit];
    strokeWeight(size/4);  // Adjust segment thickness based on size
    stroke('navy');
    // Horizontal segments
    let horizontal = [0, 3, 6];
    for (let i of horizontal) {
        if (segmentOn[i]) {
            if (i==0) yOffset = 0;
            if (i==3) yOffset = size*2;
            if (i==6) yOffset = size;
            line(x - size, y+yOffset-size, x + size, y+yOffset-size);
        }
    }

    // Vertical segments
    let vertical = [1, 2, 4, 5];
    for (let i of vertical) {
        if (segmentOn[i]) {
            if (i==1 || i==5) {startY = y-size; endY = y}
            if (i==2 || i==4) {startY = y; endY = y + size;}
            if (i==4 || i==5) {xOffset = -size;}
            if (i==1 || i==2) {xOffset = +size;}
            xpos = x + xOffset;
            line(xpos, startY, xpos, endY);
        }
    }
}