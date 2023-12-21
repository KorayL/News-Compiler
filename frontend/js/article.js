// Get json from browser storage
const article = JSON.parse(sessionStorage.getItem("article"));

// Extra needed data
const title = article["title"];
const image_url = article["image_url"];
const body = article["body"];
const date = article["date"] == null ? "" : article["date"];
const source = article["source"];

document.getElementById("title").textContent = title;
document.getElementById("meta").textContent = source + " | " + date;

const image_tag = document.getElementById("image");
image_tag.src = image_url
image_tag.alt = title;

// Modified to break body into paragraphs */
let string = body;
// Holds the substring to be placed in a paragraph
let substring;
// Stores the index of the end of a substring.
let n;

// Loop through body, cut up string, and place it in paragraph tags
do {
    n = string.search("\n\n");
    substring =string.slice(0, n)
    string = string.slice(n+2)

    const para = document.createElement("p");
    const text_node = document.createTextNode(substring);
    para.appendChild(text_node);
    document.getElementById("content").appendChild(para);
} while (n !== -1)

