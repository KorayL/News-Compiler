// Get data from json
const data = await fetch("../data/articles.json")
                   .then((response) => {return response.json()});

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
    template_image.src = image_url;
    template_image.alt = title;

    // Get and set source
    const template_src = template.getElementById("template_src");
    template_src.textContent = source;

    // Set up div wrapping article
    const template_container = template.firstElementChild;
    template_container.id = article;
    template_container.addEventListener("click", function() {openArticle(this.id)})

    // Add template to site
    const container = document.getElementsByClassName("articles")[0];
    container.appendChild(template);
}

/**
 * Checks whether any necessary article attributes are null.
 * @param Object article with attributes: source, category, title, image_url, and body.
 * @return false if any of the Object attributes are null, true if not.
 */
function checkArticle(Object) {
    // Boolean flag
    let valid = true;

    // Create an array of necessary attributes to check
    let attributes = ["source", "category", "image_url", "body"];

    // Check if necessary attributes are null.
    for (let attribute of attributes) {
        if (Object[attribute] == null) valid = false;
    }

    return valid;
}

/**
 * Stores the article object with the given id as object name in session storage and opens the
 * article site. Article site is to then pull the data from session storage and use to display
 * the article.
 * @param id ID belonging to the article clicked. Will also match name of article object from data.
 */
function openArticle(id) {
    // Get article object from data
    const article = data[id];

    // Store article object as string in browser
    sessionStorage.setItem("article", JSON.stringify(article));

    // Open article html doc in same tab
    window.open("article.html", "_self");
}
