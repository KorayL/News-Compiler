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

    // Create new tile
    let div = document.createElement("div");
    div.id = article;
    div.classList.add("article");

    // Add article tile
    let title_tag = document.createElement("h2");
    title_tag.append(document.createTextNode(title));
    div.append(title_tag)

    // Add image
    let image_tag = document.createElement("img");
    image_tag.src = image_url;
    image_tag.alt = title;
    div.append(image_tag)

    // Add source
    let source_tag = document.createElement("p");
    source_tag.append(document.createTextNode(source));
    div.append(source_tag);

    // Append to document
    document.getElementsByClassName("articles")[0].appendChild(div);
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