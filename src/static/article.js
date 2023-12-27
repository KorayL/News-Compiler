// Get json from browser storage
const article = JSON.parse(sessionStorage.getItem("article"));

// Extra needed data
const url = article["url"];
const title = article["title"];
const image_url = article["image_url"];
const body = article["body"];
const date = article["date"];
const source = article["source"];

// Setting up title
const title_element = document.getElementById("title");
title_element.textContent = title;
title_element.style.cursor = "grab";
title_element.addEventListener("click", function() {window.open(url)});

// Setting up caption of image
console.log(date)
const date_string = date !== null ? " | " + date : " "
document.getElementById("meta").textContent = source + date_string

// Setting up image
const image_tag = document.getElementById("image");
if (image_url != null) {  // If article has an image
    image_tag.src = image_url
    image_tag.alt = "Image for article";
} else {  // If not image for the article
    image_tag.remove()
}

// Modified to break body into paragraphs
console.log(body)
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

