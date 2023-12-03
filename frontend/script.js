const data = await fetch("../data/articles.json")
                   .then((response) => {return response.json()});

for (const article of Object.keys(data)) {
    // Get data
    let title = data[article]["title"];
    let image_url = data[article]["image_url"];
    let source = data[article]["source"];

    let div = document.createElement("div");
    div.id = article;
    div.classList.add("article");

    let title_tag = document.createElement("h2");
    title_tag.append(document.createTextNode(title));
    div.append(title_tag)

    let image_tag = document.createElement("img");
    image_tag.src = image_url;
    image_tag.alt = title;
    div.append(image_tag)

    let source_tag = document.createElement("p");
    source_tag.append(document.createTextNode(source));
    div.append(source_tag);

    document.getElementsByClassName("articles")[0].appendChild(div);
}
