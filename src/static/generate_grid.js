/**
 * Distributes elements/templates/fragments within columns. Tiles will be distributed left to right,
 * then top to bottom. Vertical gaps between tiles will be filled to create a masonic layout.
 * @param {int} num_columns Number of columns to have on the page.
 * @param {array.<Node>} tiles Document fragments to be distributed among columns.
 * @returns {void}
 */
export function generate_grid(num_columns, tiles) {
    remove_columns();

    // Create and store columns from template
    for (let i = 0; i < num_columns; i++){
        const column = document.getElementById("template_column").content.cloneNode(true);

        // Add articles to column
        for (let j = i; j < tiles.length; j += num_columns) {
            const tile = tiles[j].cloneNode(true);
            column.getElementById("column").appendChild(tile);
        }
        // console.log("add")
        document.getElementsByClassName("articles")[0].appendChild(column);
    }
}

function remove_columns() {
    const columns= document.getElementsByClassName("column");

    while (columns.length > 0) {
        columns[0].remove();
    }
}