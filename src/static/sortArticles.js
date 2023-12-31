/**
 * Sorts the given articles by date via the epoch attribute. Newest articles will be first.
 * @param articles_obj {Object} Object containing articles to be sorted.
 * @returns {Object} Object containing sorted articles.
 */
export function sortArticles(articles_obj) {
    // Place all article objects into an array
    let article_arr = [];
    const keys = Object.keys(articles_obj)
    for (let i = 0; i < keys.length; i++) {
        const key = keys[i];  // Get key for current iteration
        let article = articles_obj[key];  // Get article for current iteration
        article["key"] = key;  // Add key to article object for use later
        article_arr.push(article);  // Append article to array of articles
    }

    quickSort(article_arr, 0, article_arr.length - 1);

    // Create new object with sorted array to return
    let sorted_articles_obj = {};
    for (let i = 0; i < article_arr.length; i++) {
        const article = article_arr[i];  // Get article from array
        const key = article.key;  // Get key from article object
        delete article["key"];  // Delete key from article object
        sorted_articles_obj[key] = article;  // Use key as key for article in sorted object
    }

    return sorted_articles_obj
}

/**
 * Recursive function that sorts a given array between the given low/high values.
 * @param array {array.<Object>} Array of article objects to sort.
 * @param low {int} Smallest index to begin sorting the array from.
 * @param high {int} Largest index to sort the array to.
 * @returns {void}
 */
function quickSort(array, low, high) {
    if (high - low > 1) {
        const pivot_loc = partition(array, low, high);

        quickSort(array, low, pivot_loc - 1);
        quickSort(array, pivot_loc + 1, high);
    }
}

/**
 * Chooses the first index of the array to be a pivot. Moves the pivot into its correct sorted
 * position in the array. Items on the left of the pivot may not be sorted but will be less that
 * than the pivot. Items to the right of the pivot may not be sorted but will be greater than
 * the pivot.
 * @param array {array.<Object>} Array of article objects to partition.
 * @param low {int} Smallest index to partition from.
 * @param high {int} Largest index to partition to.
 * @returns {int} The index of the pivot.
 */
function partition(array, low, high) {
    const pivot = array[low];  // Use first element as pivot
    let swapIndex = high;
    for (let i = low + 1; i <= swapIndex; i++) {
        if (array[i]["epoch"] <= pivot["epoch"]) {
            swap(array, i, swapIndex);
            i--; swapIndex--;
        }
    }

    swap(array, low, swapIndex);
    return swapIndex;
}

/**
 * Swaps two elements in a given array.
 * @param array {array} Array in which elements will be swapped.
 * @param i1 {int} Index of first element to be swapped.
 * @param i2 {int} Index of second element to be swapped.
 * @returns {void}
 */
function swap(array, i1, i2) {
    const temp = array[i1];
    array[i1] = array[i2];
    array[i2] = temp;
}