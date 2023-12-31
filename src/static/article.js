// Get json from browser storage
const article = JSON.parse(sessionStorage.getItem("article"));

// Extract needed data:
/** Url of article from which information was pulled from. */
const url = article["url"];
/** Title of the article. */
const title = article["title"];
/** URL of image to display. */
const image_url = article["image_url"];
/** Body with \n\n used to separate paragraphs. */
const body = article["body"];
/** *Seconds* since epoch (UNIX/POSIX time). */
const epoch = article["epoch"];
/** News website article is from. */
const source = article["source"];

// Setting up title
const title_element = document.getElementById("title");
title_element.textContent = title;
title_element.style.cursor = "grab";
title_element.addEventListener("click", function() {window.open(url)});

// Preparing image caption:

// Get all date information
let date_string = " ";
if (epoch !== null) {
    const date = new Date(epoch*1000); // Convert UNIX time to milliseconds to create Date
    const year = date.getFullYear();
    let month = date.getMonth();
    const day = date.getDate();
    let weekday = date.getDay();
    let hour = date.getHours();
    let minute = date.getMinutes();

    // Convert appropriately
    month = numToMonth(month);
    weekday = numToWeekday(weekday);
    minute = numToMinute(minute);
    const meridiem = getMeridiem(hour);
    hour = militaryTo12(hour);

    // Put everything together
    date_string = `${hour}:${minute} ${meridiem} ${weekday} ${month} ${day}, ${year}`;
}

// Set image caption
document.getElementById("meta").textContent = source + " | " + date_string;

// Setting up image
const image_tag = document.getElementById("image");
if (image_url != null) {  // If article has an image
    image_tag.src = image_url;
    image_tag.alt = "Image for article";
} else {  // If not image for the article
    image_tag.remove();
}

// Modified to break body into paragraphs
let string = body;
// Holds the substring to be placed in a paragraph
let substring;
// Stores the index of the end of a substring.
let n;

// Loop through body, cut up string, and place it in paragraph tags
do {
    n = string.search("\n\n");
    substring =string.slice(0, n);
    string = string.slice(n+2);

    const para = document.createElement("p");
    const text_node = document.createTextNode(substring);
    para.appendChild(text_node);
    document.getElementById("content").appendChild(para);
} while (n !== -1);

/**
 * Converts a number 0-11 to the full string name of a month.
 * @param num {int} Number representing a month.
 * @returns {String} Full name of month between January and December
 */
function numToMonth(num) {
    const months = ["January", "February", "March", "April", "May", "June", "July",
                            "August", "September", "October", "November", "December"];

    return months[num];
}

/**
 * Converts a number 0-6 to the full string name of a weekday. 0->Sunday and 6->Saturday.
 * @param num {int} Number representing a weekday.
 * @returns {string} Full name of weekday.
 */
function numToWeekday(num) {
    const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                           "Saturday"]

    return weekdays[num]
}

/**
 * Adds a 0 in from of a number if the number is single digit. This method is to be used when
 * converting a raw number into a string suitable for displaying time.
 * @param num {int} Number to convert
 * @returns {string} Original number as a number in a string with 2 digits.
 */
function numToMinute(num) {
    if (num < 10) {
        return `0${num}`;
    }

    return `${num}`;
}

/**
 * Converts the hours in 24-hour time to the hours in 12-hour time.
 * @param hr {int} 0-23 in 24-hour time
 * @return {int} 1-12 in 12-hour time
 */
function militaryTo12 (hr) {
    hr %= 12;
    return hr === 0 ? 12 : hr
}

/**
 * Gets the meridiem AM or PM from the hours of 24-hour time.
 * @param hr {int} The hour section of 24-hour time
 * @returns {string} AM or PM
 */
function getMeridiem(hr) {
    return Math.floor(hr / 12) < 1 ? "AM" : "PM"
}
