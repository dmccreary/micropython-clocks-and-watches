let canvasWidth = 400;
let drawHeight = 250;
let controlHeight = 40;
let canvasHeight = drawHeight + controlHeight;
let defaultTextSize = 12;
let timeTextSize = 24;
let margin = 50;
let showTextTime = false;
let showValues = false;
let button;
let valButton;
let circleSize = 30;
let columnSpacing = 60;

function setup() {
  const canvas = createCanvas(canvasWidth, canvasHeight);
  var mainElement = document.querySelector('main');
  canvas.parent(mainElement);
  
  button = createButton("Show Text Time");
  button.position(10, drawHeight + 10);
  button.mousePressed(toggleTextTime);
  
  valButton = createButton("Show Values");
  valButton.position(120, drawHeight + 10);
  valButton.mousePressed(toggleValues);
}

function getBinaryDigits(num, length) {
  return num.toString(2).padStart(length, '0').split('').map(Number);
}

function drawBinaryColumn(x, y, bits, values, label, color) {
  // Draw label at top
  fill('black');
  textSize(defaultTextSize);
  textAlign(CENTER);
  text(label, x, y + 50);
  
  // Draw binary circles from bottom to top
  for (let i = 0; i < bits.length; i++) {
    let yPos = y - (i * (circleSize + 10)); // Stack from bottom up
    fill(bits[bits.length - 1 - i] ? color : 'lightgray');
    circle(x, yPos, circleSize);
    
    if (showValues) {
      fill('white');
      textSize(defaultTextSize);
      textAlign(CENTER, CENTER);
      text(values[bits.length - 1 - i], x, yPos);
    }
  }
  
  // Draw decimal value at bottom
  fill('black');
  textSize(defaultTextSize);
  textAlign(CENTER);
  let decimalValue = parseInt(bits.join(''), 2);
  text(decimalValue, x, y + 30);
}

function draw() {
  stroke('silver');
  strokeWeight(1);
  fill('aliceblue');
  rect(0,0, canvasWidth, drawHeight);
  fill('white');
  rect(0,drawHeight, canvasWidth, controlHeight);
  
  // Get current time
  let now = new Date();
  let hours = now.getHours();
  let minutes = now.getMinutes();
  let seconds = now.getSeconds();
  
  // Calculate individual digits
  let hoursTens = Math.floor(hours / 10);
  let hoursOnes = hours % 10;
  let minutesTens = Math.floor(minutes / 10);
  let minutesOnes = minutes % 10;
  let secondsTens = Math.floor(seconds / 10);
  let secondsOnes = seconds % 10;
  
  // Get binary arrays for each digit
  let hoursTensBinary = getBinaryDigits(hoursTens, 2);
  let hoursOnesBinary = getBinaryDigits(hoursOnes, 4);
  let minutesTensBinary = getBinaryDigits(minutesTens, 3);
  let minutesOnesBinary = getBinaryDigits(minutesOnes, 4);
  let secondsTensBinary = getBinaryDigits(secondsTens, 3);
  let secondsOnesBinary = getBinaryDigits(secondsOnes, 4);
  
  // Starting positions
  let startX = margin;
  let startY = drawHeight - margin - 50;
  
  // Draw each column
  drawBinaryColumn(startX, startY, hoursTensBinary, [2, 1], 'Hr Tens', 'blue');
  drawBinaryColumn(startX + columnSpacing, startY, hoursOnesBinary, [8, 4, 2, 1], 'Hr Ones', 'blue');
  drawBinaryColumn(startX + columnSpacing * 2, startY, minutesTensBinary, [4, 2, 1], 'Min Tens', 'green');
  drawBinaryColumn(startX + columnSpacing * 3, startY, minutesOnesBinary, [8, 4, 2, 1], 'Min Ones', 'green');
  drawBinaryColumn(startX + columnSpacing * 4, startY, secondsTensBinary, [4, 2, 1], 'Sec Tens', 'purple');
  drawBinaryColumn(startX + columnSpacing * 5, startY, secondsOnesBinary, [8, 4, 2, 1], 'Sec Ones', 'purple');
  
  // Display textual time if toggled
  if (showTextTime) {
    fill('black');
    textAlign(CENTER);
    textSize(timeTextSize);
    text(
      `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`,
      canvasWidth / 2,
      drawHeight - 15
    );
  }
}

function toggleTextTime() {
  showTextTime = !showTextTime;
  button.html(showTextTime ? "Hide Text Time" : "Show Text Time");
}

function toggleValues() {
  showValues = !showValues;
  valButton.html(showValues ? "Hide Values" : "Show Values");
}