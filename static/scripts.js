let targetWord = "care";
let tries = 0;
let successes = 0;
let currentLevel = "C1";

// The input field calls this function on any input
function updateTopGaps() {
    guess = document.getElementById("guess").value.toLowerCase().trim();
    changeTopBundleGapText(guess);
}

// Check input if user presses enter
document.addEventListener("keydown", async function(event) {
    if (event.key == "Enter") {
        evaluate();
    }
});

async function getNewBundle() {
    let url = "/bundle?level=" + currentLevel;
    let response = await fetch(url, {method: "GET"})
    // Check for promise and http errors
    .catch(err => alert("Error b/c of promise rejection: ".concat(err)));

    if (response.ok) {
        // Parses json into js object
        bundle = await response.json();
    }
    else {
        alert("HTTP-Error: " + response.status);
    }

    // Expected JSON structure example:
    // bundle.target = "care"
    // bundle.sent_1_left = "I don't"
    // bundle.sent_1_right = "!"
    // And so on for all 4 sentences

    targetWord = bundle.target;

    bundleDiv = document.createElement("div");
    bundleDiv.className = "bundle";
    bundlesDiv = document.getElementsByClassName("bundles")[0];
    bundlesDiv.prepend(bundleDiv);

    // Prepare columns, remove target word
    let cols = Object.values(bundle).slice(1);

    for (let i = 0; i < 4; i++) {
        // Iterate through 0-1, 2-3, 4-5, 6-7
        startIndex = 2 * i
        colsForOneRow = [cols[startIndex], cols[startIndex + 1]]
        rowDiv = makeRow(colsForOneRow)
        bundleDiv.append(rowDiv)
    }
}

function evaluate() {
    // Evaluate input and update class

    // From the element, get text, lowercase it, remove whitespace
    guess = document.getElementById("guess").value.toLowerCase().trim();
    currentBundle = getTopMostBundle();

    if (guess === targetWord) {
        alert("Wow you're fucking amazing");
        currentBundle.classList.add("correct")
        successes++;
    } else {
        alert("Wow you're fucking dumb");
        currentBundle.classList.add("incorrect");
    }

    tries++;
    if (tries === 10) {
        // TODO
        alert("You've done 10 exercises and got " + successes + " right");
        tries = 0;
    }

    // Put user input into gaps
    gaps = currentBundle.getElementsByClassName("gap")
    for (let gap of gaps) {
        gap.innerHTML = guess
    }

    getNewBundle();
}

function changeTopBundleGapText(str) {
    // Changes the text of all gaps in the topmost bundle to str
    // Select topmost bundle with getTopMostBundle()
    topBundle = getTopMostBundle();
    gaps = topBundle.getElementsByClassName("gap")
    for (let gap of gaps) {
        gap.innerHTML = " " + str + " ";
    }
}

function getTopMostBundle() {
    let bundles = document.getElementsByClassName('bundle');
    let topMostBundle = bundles[0];
    return topMostBundle;
}

function makeRow(cols) {
    // Take contents of the 3 parts of a row (array) and spit out row element
    rowDiv = document.createElement("div");
    rowDiv.className = "row";

    // Make col elements with correct classnames and append to row
    for (let i = 0; i < 3; i++) {
        colDiv = document.createElement("div");
        switch (i) {
            case 0:
                colDiv.className = "col left";
                colDiv.innerHTML = cols[0];
                break;
            case 1:
                colDiv.className = "col-1 gap";
                colDiv.innerHTML = "";
                break;
            case 2:
                colDiv.className = "col right";
                colDiv.innerHTML = cols[1];
                break;
        }
        rowDiv.append(colDiv);
    }

    return rowDiv;
}

function sleep(ms) {
    // From https://stackoverflow.com/a/39914235
    return new Promise(resolve => setTimeout(resolve, ms));
}