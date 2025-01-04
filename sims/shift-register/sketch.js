// Sample MicroSim Sketch Template for 2D Geometry
// MicroSim Template for 2D geometry with region drawing parameters
// Use for an instructor standing in front of a "smart white board" with controls on the bottom
// Author: Dan McCreary
// Version geometry-1

// The width of the entire canvas
let canvasWidth = 700;
// The top drawing region above the interactive controls
let drawWidth = canvasWidth;
let drawHeight = 400;
// The control region is where we place sliders, buttons, etc.
let controlHeight = 60;
// The total height = drawing region + control region
let canvasHeight = drawHeight + controlHeight;

// margin around the active plotting region
let margin = 25;
// the left margin area needs to hold the width of the text label and value
let sliderLeftMargin = 130;

// Chip Location 
let chipWidth = 100;
let chipHeight = 240;
let centerX = canvasWidth / 4;
let centerY = drawHeight / 2;
let rightPinXStart = centerX + chipWidth/2;
let pinLength = 20;
let rightPinXEnd = rightPinXStart + pinLength;


// larger text so students in the back of the room can read the labels
let defaultTextSize = 16;

// Variables for UI elements
let dataInRadio;
let nextClockButton;
let latchButton;

// Internal signals
let dataIn = false;
let clock = false;  // Will toggle on each press of NEXT CLOCK
let latch = false;  // Will toggle on press of LATCH button

// 74HC594 has an internal shift register and an output register
// We'll store them as arrays of 8 bits (booleans)
let shiftRegister = [false, false, false, false, false, false, false, false];
let outputRegister = [false, false, false, false, false, false, false, false];

// For storing a short timeline of states
// Each element will be an object like:
// { dataIn: bool, clock: bool, latch: bool, outputs: [bool,bool,...] }
let timeline = [];
// Limit how many history steps we keep
let maxTimelineSteps = 12;

function setup() {
  // Create the main canvas
  const canvas = createCanvas(canvasWidth, canvasHeight);
  // If you want to place this in a <main> container in HTML:
  var mainElement = document.querySelector('main');
  if (mainElement) {
    canvas.parent(mainElement);
  }

  textSize(16);

  // Radio button for Data In (ON/OFF)
  dataInRadio = createRadio();
  dataInRadio.option('OFF', 'OFF');
  dataInRadio.option('ON', 'ON');
  dataInRadio.selected('OFF');
  dataInRadio.changed(() => {
    dataIn = (dataInRadio.value() === 'ON');
  });
  // Position it somewhere near the bottom left
  dataInRadio.position(10, drawHeight + 5);

  // NEXT CLOCK button
  nextClockButton = createButton('NEXT CLOCK');
  nextClockButton.position(120, drawHeight + 10);
  nextClockButton.mousePressed(doNextClock);

  // LATCH button
  latchButton = createButton('LATCH');
  latchButton.position(240, drawHeight + 10);
  latchButton.mousePressed(doLatch);

}

function draw() {
  // ---------------------------
  // 1. Draw background regions
  // ---------------------------
  // Make the background drawing region a very light blue
  fill('aliceblue');
  // Draw a thin light gray outline for the region borders
  stroke('silver');
  rect(0, 0, canvasWidth, drawHeight);

  // Make the background of the controls area white
  fill('white');
  rect(0, drawHeight, canvasWidth, controlHeight);

  // ---------------------------
  // 2. Draw the 74HC594 "chip"
  // ---------------------------

  // Draw the chip body
  fill('lightgray');
  stroke('black');
  rectMode(CENTER);
  // rounded corner 10 for nice look
  rect(centerX, centerY, chipWidth, chipHeight, 10);

  // Label the chip
  fill('black');
  noStroke();
  textAlign(CENTER, CENTER);
  textSize(18);
  text("74HC594", centerX, centerY);

  // ---------------------------
  // 3. Label the pins
  // ---------------------------
  
  // Input
  textSize(defaultTextSize);
  textAlign(LEFT, CENTER);

  // Left side pins: DATA IN, CLOCK, LATCH
  let leftPinX = centerX - chipWidth/2 - 70; 
  let pinSpacing = 30;
  let topPinY = centerY - pinSpacing;
  
  text("DATA IN", leftPinX, topPinY);
  text("CLOCK",   leftPinX, topPinY + pinSpacing);
  text("LATCH",   leftPinX, topPinY + 2*pinSpacing);

  // Right side pins: OUT1 to OUT8
  for (let i = 0; i < 8; i++) {
    let y = centerY - (3.5 * pinSpacing) + i*pinSpacing;
    textAlign(LEFT, CENTER);
    text(`OUT ${i+1}`, rightPinXEnd + 5, y);
  }

  // ---------------------------
  // 4. Draw lines showing how signals connect
  //    (purely cosmetic to show connections)
  // ---------------------------
  stroke('black');
  strokeWeight(1);

  // Data In line to chip
  line(leftPinX + 60, topPinY, centerX - chipWidth/2, topPinY);
  // Clock line
  line(leftPinX + 60, topPinY + pinSpacing, centerX - chipWidth/2, topPinY + pinSpacing);
  // Latch line
  line(leftPinX + 60, topPinY + 2*pinSpacing, centerX - chipWidth/2, topPinY + 2*pinSpacing);

  // Output lines from chip
  for (let i = 0; i < 8; i++) {
    let y = centerY - (3.5 * pinSpacing) + i*pinSpacing;
    line(rightPinXStart, y, rightPinXEnd, y);
  }

  // ---------------------------
  // 5. Timeline display (on right side of the draw region)
  // ---------------------------
  // We'll draw a small rectangle region on the far right and list up to maxTimelineSteps states
  // back to standard (x,y,w,h)
  rectMode(CORNER);
  let timelineX = canvasWidth/2; 
  let timelineY = margin;
  let timelineW = canvasWidth/2 - margin*2; 
  let timelineH = drawHeight - margin*4;

  noFill();
  stroke('green');
  rect(timelineX, 50, timelineW, timelineH);

  fill('black');
  noStroke();
  textSize(14);
  textAlign(LEFT, TOP);
  text("Timeline", timelineX + 5, timelineY + 5);

  // Each step is about 15-20 px tall
  let stepHeight = 15;
  for (let i = 0; i < timeline.length; i++) {
    let state = timeline[i];
    let y = timelineY + 25 + i*stepHeight;
    // Create a compact text representation
    let bits = state.outputs.map(b => b ? '1' : '0').join('');
    // let lineTxt = `${i}: D=${state.dataIn?1:0} C=${state.clock?1:0} L=${state.latch?1:0} Out=${bits}`;
    let lineTxt = `${i}: D=${state.dataIn?1:0} L=${state.latch?1:0} Out=${bits}`;
    text(lineTxt, timelineX + 5, y);
  }

  // ---------------------------
  // 6. Optional text about current states in the main region
  // ---------------------------
  fill('black');
  textSize(16);
  textAlign(CENTER, TOP);
  let statusStr = "DATA IN: " + (dataIn ? "HIGH" : "LOW");
  // statusStr += " | CLOCK: " + (clock ? "HIGH" : "LOW");
  statusStr += " | LATCH: " + (latch ? "HIGH" : "LOW");
  text(statusStr, width/2, drawHeight - 30);

  // 7. Show output bits next to the OUT pins (just a small circle or text)
  textAlign(LEFT, CENTER);
  for (let i = 0; i < 8; i++) {
    let y = centerY - (3.5 * pinSpacing) + i*pinSpacing;
    fill(outputRegister[i] ? 'red' : 'white');
    stroke('black');
    circle(rightPinXEnd + 65, y, 10);
  }
}

// This function is called each time the user presses NEXT CLOCK
function doNextClock() {
  // Toggle clock line: Low -> High -> shift -> Low
  clock = !clock;
  // If we just went HIGH, that is the "rising edge" – shift the data in
  if (clock) {
    shiftInBit(dataIn);
  }
  // If we want a single button press to do a quick pulse, we can immediately toggle back to low
  // so visually it won't remain high. This simulates a single clock pulse on each press.
  setTimeout(() => {
    clock = !clock;
    updateTimeline(); 
  }, 100);  
}

// Shift in the bit to the shiftRegister
function shiftInBit(bitValue) {
  // shift right: the MSB is lost, the new bit goes into index 0 or index 7
  // 74HC594 typically shifts from bit 0 -> bit1 -> ... -> bit7.  
  // We'll assume bit0 is "rightmost" for display. You can invert if you prefer.
  
  // Move everything one position to the left
  for (let i = shiftRegister.length - 1; i > 0; i--) {
    shiftRegister[i] = shiftRegister[i-1];
  }
  // Insert the new bit at index 0
  shiftRegister[0] = bitValue;
}

// This function is called each time the user presses the LATCH button
function doLatch() {
  latch = !latch;
  if (latch) {
    // On rising edge of latch, we copy shiftRegister to outputRegister
    outputRegister = shiftRegister.slice();
  }
  updateTimeline();
  // Optionally set latch low again quickly (to simulate a pulse)
  setTimeout(() => {
    latch = !latch;
    updateTimeline();
  }, 150);
}

// Record the current dataIn, clock, latch, and output register to the timeline
function updateTimeline() {
  // Create an object for the new state
  let newState = {
    dataIn: dataIn,
    clock: clock,
    latch: latch,
    outputs: outputRegister.slice() // copy
  };
  timeline.push(newState);

  // If we exceed the maxTimelineSteps, remove the oldest
  while (timeline.length > maxTimelineSteps) {
    timeline.shift();
  }
}
