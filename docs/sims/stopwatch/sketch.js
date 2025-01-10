// Stopwatch simulation using p5.js
let canvasWidth = 350;
let drawHeight = 240;
let controlHeight = 40;
let canvasHeight = drawHeight + controlHeight;
let defaultTextSize = 24;
let timeTextSize = 36;
let margin = 50;

// Stopwatch state
let isRunning = false;
let startTime = 0;
let elapsedTime = 0;
let lastTime = 0;

// Button states
let startStopButton;
let resetButton;
let lastButtonPress = 0;
const DEBOUNCE_TIME = 250;

function setup() {
  const canvas = createCanvas(canvasWidth, canvasHeight);
  var mainElement = document.querySelector('main');
  canvas.parent(mainElement);

  // Create start/stop button
  startStopButton = createButton("Start/Stop");
  startStopButton.position(10, drawHeight + 10);
  startStopButton.mousePressed(handleStartStop);

  // Create reset button
  resetButton = createButton("Reset");
  resetButton.position(100, drawHeight + 10);
  resetButton.mousePressed(handleReset);
}

function draw() {
  // Draw OLED display background (black)
  fill(0);
  stroke('silver');
  rect(0, 0, canvasWidth, drawHeight);

  // Controls region background
  fill('white');
  rect(0, drawHeight, canvasWidth, controlHeight);

  // Draw OLED display content
  drawOLEDContent();

  // Update elapsed time if running
  if (isRunning) {
    elapsedTime = lastTime + (millis() - startTime);
  }
}

function drawOLEDContent() {
  // Display title
  fill(255); // White text
  noStroke();
  textSize(16);
  textAlign(LEFT, TOP);
  text("stopwatch lab", 10, 10);

  // Display state
  textSize(14);
  text(isRunning ? "RUNNING" : "STOPPED", 10, 40);

  // Display time
  textSize(32);
  text(formatTime(elapsedTime), 10, 80);
}

function formatTime(ms) {
  let totalSeconds = floor(ms / 1000);
  let minutes = floor(totalSeconds / 60);
  let seconds = totalSeconds % 60;
  let milliseconds = floor((ms % 1000));
  
  return `${nf(minutes, 2)}:${nf(seconds, 2)}.${nf(milliseconds, 3)}`;
}

function handleStartStop() {
  let currentTime = millis();
  if (currentTime - lastButtonPress < DEBOUNCE_TIME) return;
  lastButtonPress = currentTime;

  if (!isRunning) {
    // Start the stopwatch
    startTime = millis();
    isRunning = true;
  } else {
    // Stop the stopwatch
    lastTime = elapsedTime;
    isRunning = false;
  }
}

function handleReset() {
  let currentTime = millis();
  if (currentTime - lastButtonPress < DEBOUNCE_TIME) return;
  lastButtonPress = currentTime;

  // Reset the stopwatch
  isRunning = false;
  startTime = 0;
  elapsedTime = 0;
  lastTime = 0;
}