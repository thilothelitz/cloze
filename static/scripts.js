let targetWord = "care";
let tries = 0;
let triesUntilChange = 3;
let successes = 0;
let currentLevel = "A2";

window.onload = getNewBundle()

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
        currentBundle.classList.add("correct")
        successes++;
    } else {
        currentBundle.classList.add("incorrect");
    }

    tries++;
    if (tries === triesUntilChange) {
        alert("You've done " + triesUntilChange + " exercises and got " + successes + " right!");
        if (successes / triesUntilChange > 0.6) {
            alert("Level up 😎");
            changeLevel(increase=true);
        } else {
            alert("Level down 😤");
            changeLevel(increase=false);
        }
        tries = 0;
        successes = 0;
    }

    // Put user input into gaps
    gaps = currentBundle.getElementsByClassName("gap")
    for (let gap of gaps) {
        gap.innerHTML = cleaned(targetWord)
    }

    getNewBundle();
    document.getElementById("guess").value = ""
}

function changeTopBundleGapText(str) {
    // Changes the text of all gaps in the topmost bundle to str
    // Select topmost bundle with getTopMostBundle()
    topBundle = getTopMostBundle();
    gaps = topBundle.getElementsByClassName("gap")
    for (let gap of gaps) {
        gap.innerHTML = " " + cleaned(str) + " ";
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
                colDiv.className = "col left d-flex align-items-center justify-content-end text-wrap";
                colDiv.innerHTML = cols[0];
                break;
            case 1:
                colDiv.className = "col-1 gap border-bottom d-flex align-items-center justify-content-center text-wrap";
                colDiv.innerHTML = "";
                break;
            case 2:
                colDiv.className = "col right d-flex align-items-center justify-content-start text-wrap";
                colDiv.innerHTML = cols[1];
                break;
        }
        rowDiv.append(colDiv);
    }

    return rowDiv;
}

function changeLevel(increase) {
    if (increase) {
        switch (currentLevel) {
            case "A1":
                currentLevel = "A2";
                break;
            case "A2":
                currentLevel = "B1";
                break;
            case "B1":
                currentLevel = "B2";
                break;
            case "B2":
                currentLevel = "C1";
                break;
            case "C1":
                break;
        }
    } else {
        switch (currentLevel) {
            case "A1":
                break;
            case "A2":
                currentLevel = "A1";
                break;
            case "B1":
                currentLevel = "A2";
                break;
            case "B2":
                currentLevel = "B1";
                break;
            case "C1":
                currentLevel = "B2";
                break;
        }
    }    
}

function cleaned(str) {
    if (str.length > 10) {
        str = str.slice(0, 8) + "..."
    }
    return str
}

function sleep(ms) {
    // From https://stackoverflow.com/a/39914235
    return new Promise(resolve => setTimeout(resolve, ms));
}