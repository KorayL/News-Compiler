import {sortArticles} from "./sortArticles.js";
import {generate_grid} from "./generate_grid.js";

// Get data from json
let data = await fetch("../static/articles.json")
                   .then((response) => {return response.json()});

data = sortArticles(data);
removeDuplicates(data);

/**
 * Array into which document fragments are placed to be later added to columns
 * @type {array.<Node>}
 */
let articles = [];

// Loop through the articles from json
for (const article of Object.keys(data)) {
    // If article has null fields skip it
    if (!checkArticle(data[article])) continue;

    // Get data
    const title = data[article]["title"];
    const image_url = data[article]["image_url"];
    const source = data[article]["source"];

    // Get template from html doc
    const template = document.getElementById("template_article").content.cloneNode(true);

    // Get and set title
    const template_title = template.getElementById("template_title");
    template_title.textContent = title;

    // Get and set image
    const template_image = template.getElementById("template_image");
    if (image_url != null) {  // If article has an image
        template_image.src = image_url;
        template_image.alt = "Image for article";
    } else {  // If not image for the article
        template_image.remove();
    }

    // Get and set source
    const template_src = template.getElementById("template_src");
    template_src.textContent = source;

    // Set up div wrapping article
    const template_container = template.firstElementChild;
    template_container.id = article;
    template_container.addEventListener("click", function() {openArticle(this.id)})
    template_container.style.cursor = "grab";

    // Add template to list of article templates
    articles.push(template);
}

let prev_num_cols = calcNumCols();

generate_grid(prev_num_cols, articles);
addEventListenersToArticles()

// Dynamically adjust number of columns
window.addEventListener("resize", () => {
    const new_num_cols = calcNumCols();

    if (new_num_cols !== prev_num_cols) {
        generate_grid(new_num_cols, articles);
        addEventListenersToArticles()
        prev_num_cols = new_num_cols;
    }
})

/**
 * The generate_grid() method remove all event listeners from articles due to the .cloneNode()
 * function. This method is intended to be used to fix that. It should be run after the
 * generate_grid() method.
 * @returns {void}
 */
function addEventListenersToArticles() {
    const articles = document.getElementsByClassName("article");

    for (let article of articles) {
        article.addEventListener("click", function() {openArticle(this.id)});
    }
}

/**
 * Calculates, based on the width of the window, the number of columns the website should use to
 * make masonry grid layout.
 * @returns {number} The number of columns to be used.
 */
function calcNumCols() {
    const width = window.innerWidth;

    if (width <= 600) {
        return 1;
    } else {
        return Math.floor(width / 300);
    }
}

/**
 * Checks whether any necessary article attributes are null.
 * @param object {Object} article with attributes: source, category, title, image_url, and body.
 * @returns {boolean} false if any of the Object attributes are null, true if not.
 */
function checkArticle(object) {
    // Boolean flag
    let valid = true;

    // Create an array of necessary attributes to check
    let attributes = ["source", "category", "body"];

    // Check if necessary attributes are null.
    for (let attribute of attributes) {
        if (object[attribute] == null) valid = false;
    }

    return valid;
}

/**
 * Stores the article object with the given id as object name in session storage and opens the
 * article site. Article site is to then pull the data from session storage and use to display
 * the article.
 * @param id {string} ID belonging to the article clicked. Will also match name of article
 * object from
 * data.
 * @returns {void}
 */
function openArticle(id) {
    // Get article object from data
    const article = data[id];

    // Store article object as string in browser
    sessionStorage.setItem("article", JSON.stringify(article));

    // Open article html doc in same tab
    window.open("article.html", "_self");
}

/**
 * Remove adjacent duplicate articles by date and name. Articles should be sorted by date before
 * being passed to this function.
 * @param articles {Object} Object containing all article objects.
 * @returns {void}
 */
function removeDuplicates(articles) {
    // Iterate through all articles starting at first and ending at second to last.
    for (let i = 0; i < Object.keys(articles).length - 1; i++) {
        // Get current and next articles
        const keys = Object.keys(articles);

        // Move forward and delete until a non-duplicate article is found
        for (let j = i + 1; isDuplicate(articles[keys[i]], articles[keys[j]]); j++)
            delete articles[keys[j]];
    }
}

/**
 * Checks if two articles are duplicates based on their date and title.
 * @param article1 {Object} First article object.
 * @param article2 {Object} Second article object.
 * @returns {boolean} True if articles are duplicates, false if not.
 */
function isDuplicate(article1, article2) {
    return article1["epoch"] === article2["epoch"] &&
           article1["title"] === article2["title"];
}
