// Canvas dimensions
let drawHeight = 400;
let controlHeight = 50;
let canvasHeight = drawHeight + controlHeight;
let aspectRatio = 1.91; // Open Graph standard
let canvasWidth = canvasHeight * aspectRatio;
let margin = 50;

// UI elements
let zoomSlider;

// Drawing constants
const boxHeight = 60;
const boxWidth = 200;
const smallBoxWidth = 80;
const componentSpacing = 100;

function setup() {
  const canvas = createCanvas(canvasWidth, canvasHeight);
  var mainElement = document.querySelector('main');
  canvas.parent(mainElement);
  
  // Create zoom level slider
  zoomSlider = createSlider(1, 10, 1, 1);
  zoomSlider.position(140, drawHeight + 15);
  zoomSlider.size(canvasWidth - 3*margin);
  
  textSize(16);
  textAlign(CENTER, CENTER);
  rectMode(CENTER);
}

function drawBox(x, y, w, h, label, text_size = 16, color = 'lightgray') {
  fill(color);
  stroke(0);
  strokeWeight(2);
  rect(x, y, w, h, 5);
  
  fill(0);
  noStroke();
  textSize(text_size);
  text(label, x, y);
}

function drawArrow(x1, y1, x2, y2, label = '') {
  stroke(0);
  strokeWeight(2);
  
  // Draw line
  line(x1, y1, x2, y2);
  
  // Draw arrowheads
  push();
  translate(x2, y2);
  rotate(atan2(y2 - y1, x2 - x1));
  fill(0);
  triangle(-10, -5, 0, 0, -10, 5);
  pop();
  
  push();
  translate(x1, y1);
  rotate(atan2(y2 - y1, x2 - x1));
  fill(0);
  triangle(10, -5, 0, 0, 10, 5);
  pop();
  
  // Draw label
  if (label) {
    fill(0);
    noStroke();
    text(label, (x1 + x2)/2, (y1 + y2)/2 - 10);
  }
}

function draw() {
  // Draw background regions
  rectMode(CORNER);
  fill('aliceblue');
  stroke('green');
  rect(0, 0, canvasWidth, drawHeight);
  fill('whitegray');
  rect(0, drawHeight, canvasWidth, controlHeight);
  rectMode(CENTER);

  // Get current zoom level
  let zoomLevel = zoomSlider.value();
  
  // Calculate center position
  let centerX = canvasWidth/2;
  let centerY = drawHeight/2;
  
  switch(zoomLevel) {
    case 1:
      drawBox(centerX, centerY, canvasWidth * .8, drawHeight * .8, 'Clock', 48);
      break;
      
    case 2:
      drawBox(centerX, centerY - componentSpacing, canvasWidth*.7, drawHeight*.4, 'Display', 36);
      drawBox(centerX, centerY + componentSpacing, canvasWidth*.7, drawHeight*.4, 'Microcontroller', 36);
      break;
      
    case 3:
      drawBox(centerX, centerY - componentSpacing, canvasWidth*.7, drawHeight*.3, 'Display', 24);
      drawArrow(centerX, centerY - componentSpacing/2, centerX, centerY + componentSpacing/2, 'SPI Bus', 24);
      drawBox(centerX, centerY + componentSpacing, canvasWidth*.7, drawHeight*.3, 'Microcontroller', 24);
      break;
      
    case 4:
      drawBox(centerX, centerY - componentSpacing, boxWidth, boxHeight, 'Display', 24);
      drawArrow(centerX, centerY - componentSpacing/2, centerX, centerY + componentSpacing/2, 'SPI Bus', 24);
      drawBox(centerX, centerY + componentSpacing, boxWidth, boxHeight, 'Microcontroller', 24);
      drawBox(centerX + boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'RTC', 24);
      break;
      
    case 5:
      drawBox(centerX, centerY - componentSpacing, boxWidth, boxHeight, 'Display', 24);
      drawArrow(centerX, centerY - componentSpacing/2, centerX, centerY + componentSpacing/2, 'SPI Bus', 24);
      drawBox(centerX, centerY + componentSpacing, boxWidth, boxHeight, 'Microcontroller', 24);
      drawBox(centerX + boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'RTC', 24);
      drawArrow(centerX + boxWidth/2, centerY + componentSpacing, 
                centerX + boxWidth, centerY + componentSpacing, 'I2C Bus', 24);
      break;
      
    case 6:
      drawBox(centerX, centerY - componentSpacing, boxWidth, boxHeight, 'Display', 24);
      drawArrow(centerX, centerY - componentSpacing/2, centerX, centerY + componentSpacing/2, 'SPI Bus', 24);
      drawBox(centerX, centerY + componentSpacing, boxWidth, boxHeight, 'Microcontroller', 24);
      drawBox(centerX + boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'RTC', 24);
      drawArrow(centerX + boxWidth/2, centerY + componentSpacing, 
                centerX + boxWidth, centerY + componentSpacing, 'I2C Bus', 24);
      drawBox(centerX - boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'Buttons', 24);
      break;
      
    case 7:
      drawBox(centerX, centerY - componentSpacing, boxWidth, boxHeight, 'Display', 24);
      drawArrow(centerX, centerY - componentSpacing/2, centerX, centerY + componentSpacing/2, 'SPI Bus', 24);
      drawBox(centerX, centerY + componentSpacing, boxWidth, boxHeight, 'Microcontroller', 24);
      drawBox(centerX + boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'RTC', 24);
      drawArrow(centerX + boxWidth/2, centerY + componentSpacing, 
                centerX + boxWidth, centerY + componentSpacing, 'I2C Bus', 24);
      drawBox(centerX - boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'Buttons', 24);
      drawBox(centerX, centerY + componentSpacing * 2, boxWidth * 1.5, boxHeight/2, 'Power', 'gold');
      break;
      
    case 8:
      drawBox(centerX, centerY - componentSpacing, boxWidth, boxHeight, 'Display', 24);
      drawArrow(centerX, centerY - componentSpacing/2, centerX, centerY + componentSpacing/2, 'SPI Bus', 24);
      drawBox(centerX, centerY + componentSpacing, boxWidth, boxHeight, 'Microcontroller', 24);
      drawBox(centerX + boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'RTC', 24);
      drawArrow(centerX + boxWidth/2, centerY + componentSpacing, 
                centerX + boxWidth, centerY + componentSpacing, 'I2C Bus', 24);
      drawBox(centerX - boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'Buttons', 24);
      drawBox(centerX - boxWidth, centerY, smallBoxWidth, boxHeight, 'Speaker', 24);
      drawBox(centerX, centerY + componentSpacing * 2, boxWidth * 1.5, boxHeight/2, 'Power', 24, 'gold');
      break;
      
    case 9:
      drawBox(centerX, centerY - componentSpacing, boxWidth, boxHeight, 'Display', 24);
      drawArrow(centerX, centerY - componentSpacing/2, centerX, centerY + componentSpacing/2, 'SPI Bus', 24);
      
      // Microcontroller with cores
      drawBox(centerX, centerY + componentSpacing, boxWidth, boxHeight, 'Microcontroller', 24);
      drawBox(centerX - 50, centerY + componentSpacing - 15, smallBoxWidth, boxHeight/2, 'Core 1', 24, 'lavender');
      drawBox(centerX - 50, centerY + componentSpacing + 15, smallBoxWidth, boxHeight/2, 'Core 2', 24, 'lavender');
      
      drawBox(centerX + boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'RTC', 24);
      drawArrow(centerX + boxWidth/2, centerY + componentSpacing, 
                centerX + boxWidth, centerY + componentSpacing, 'I2C Bus', 24);
      drawBox(centerX - boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'Buttons', 24);
      drawBox(centerX - boxWidth, centerY, smallBoxWidth, boxHeight, 'Speaker', 24);
      drawBox(centerX, centerY + componentSpacing * 2, boxWidth * 1.5, boxHeight/2, 'Power', 24, 'gold');
      break;
      
    case 10:
      drawBox(centerX, centerY - componentSpacing, boxWidth, boxHeight, 'Display', 24);
      drawArrow(centerX, centerY - componentSpacing/2, centerX, centerY + componentSpacing/2, 'SPI Bus', 24);
      
      // Microcontroller with cores and PIO
      drawBox(centerX, centerY + componentSpacing, boxWidth, boxHeight, 'Microcontroller', 24);
      drawBox(centerX - 50, centerY + componentSpacing - 15, smallBoxWidth, boxHeight/2, 'Core 1', 24, 'lavender');
      drawBox(centerX - 50, centerY + componentSpacing + 15, smallBoxWidth, boxHeight/2, 'Core 2', 24, 'lavender');
      drawBox(centerX + 50, centerY + componentSpacing, smallBoxWidth, boxHeight/1.5, 'PIO', 24, 'lavender');
      
      drawBox(centerX + boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'RTC');
      drawArrow(centerX + boxWidth/2, centerY + componentSpacing, 
                centerX + boxWidth, centerY + componentSpacing, 'I2C Bus', 24);
      drawBox(centerX - boxWidth, centerY + componentSpacing, smallBoxWidth, boxHeight, 'Buttons', 24);
      drawBox(centerX - boxWidth, centerY, smallBoxWidth, boxHeight, 'Speaker', 24);
      drawBox(centerX, centerY + componentSpacing * 2, boxWidth * 1.5, boxHeight/2, 'Power', 24, 'gold');
      break;
  }
  
  // Draw slider label
  fill('black');
  textSize(20);
  text("Zoom Level: " + zoomLevel, 70, drawHeight + 25);
}