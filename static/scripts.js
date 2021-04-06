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
    document.body.append(bundleDiv)

    rowDiv = document.createElement("div");
    rowDiv.className = "row";
    bundleDiv.append(rowDiv)

    colDiv = document.createElement("div");
    rowDiv.className = "col left";
    rowDiv.innerHTML = bundle.sent_1_left;
    rowDiv.append(colDiv)

    colDiv = document.createElement("div");
    rowDiv.className = "col-1 gap";
    rowDiv.innerHTML = bundle.sent_1_gap;
    rowDiv.append(colDiv)

    colDiv = document.createElement("div");
    rowDiv.className = "col right";
    rowDiv.innerHTML = bundle.sent_1_right;
    rowDiv.append(colDiv)

    // document.append(bundleDiv)
    // bundleDiv.append(rowDiv)
    // rowDiv.append(leftColDiv)
    // rowDiv.append(midColDiv)
    // rowDiv.append(rightColDiv)

    

    // sent1Left = document.getElementById("sent_1_left")
    // sent1Left.innerHTML = bundle.sent_1_left
    // sent1Gap = document.getElementById("sent_1_gap")
    // sent1Gap.innerHTML = bundle.sent_1_gap
    // sent1Right = document.getElementById("sent_1_right")
    // sent1Right.innerHTML = bundle.sent_1_right

    // sent2Left = document.getElementById("sent_2_left")
    // sent2Left.innerHTML = bundle.sent_2_left
    // sent2Gap = document.getElementById("sent_2_gap")
    // sent2Gap.innerHTML = bundle.sent_2_gap
    // sent2Right = document.getElementById("sent_2_right")
    // sent2Right.innerHTML = bundle.sent_2_right

    // sent3Left = document.getElementById("sent_3_left")
    // sent3Left.innerHTML = bundle.sent_3_left
    // sent3Gap = document.getElementById("sent_3_gap")
    // sent3Gap.innerHTML = bundle.sent_3_gap
    // sent3Right = document.getElementById("sent_3_right")
    // sent3Right.innerHTML = bundle.sent_3_right

    // sent4Left = document.getElementById("sent_4_left")
    // sent4Left.innerHTML = bundle.sent_4_left
    // sent4Gap = document.getElementById("sent_4_gap")
    // sent4Gap.innerHTML = bundle.sent_4_gap
    // sent4Right = document.getElementById("sent_4_right")
    // sent4Right.innerHTML = bundle.sent_4_right
}

function sleep(ms) {
    // From https://stackoverflow.com/a/39914235
    return new Promise(resolve => setTimeout(resolve, ms));
}