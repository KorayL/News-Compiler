// Create a clickable title to reload the articles
const title = document.getElementById("title");
title.addEventListener("click", () => {
   window.open("reload", "_self")
})
title.style.cursor = "grab";
