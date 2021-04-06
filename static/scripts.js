targetWord = "care";

// Does something everytime something is input into the guess field, typing
// or copy-pasting or text-to-speech input
//guess.oninput = isCorrectGuess();

async function isCorrectGuess() {
    if (guess.value.toLowerCase() === targetWord) {
        alert("Wow you're fucking amazing");
        sleep(1000)
        getNewBundle()
    }
}

async function getNewBundle() {
    let url = "/bundle";
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
    // bundle.sent_1_gap = "care"
    // bundle.sent_1_right = "!"
    // And so on for all 4 sentences

    targetWord = bundle.target;

    bundleDiv = document.createElement("div");
    bundleDiv.className = "bundle";
    bundlesDiv = document.getElementsByClassName("bundles")[0];
    bundlesDiv.append(bundleDiv);

    // Prepare columns, remove target word
    let cols = Object.values(bundle).slice(1);

    for (let i = 0; i < 4; i++) {
        // Iterate through 0-2, 3-5, 6-8, 9-11
        startIndex = 3 * i
        colsForOneRow = [cols[startIndex], cols[startIndex + 1], cols[startIndex + 2]]
        rowDiv = makeRow(colsForOneRow)
        bundleDiv.append(rowDiv)
    }
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
                break;
            case 1:
                colDiv.className = "col-1 gap";
                break;
            case 2:
                colDiv.className = "col right";
                break;
        }
        colDiv.innerHTML = cols[i];
        rowDiv.append(colDiv);
    }

    return rowDiv;
}

function sleep(ms) {
    // From https://stackoverflow.com/a/39914235
    return new Promise(resolve => setTimeout(resolve, ms));
}