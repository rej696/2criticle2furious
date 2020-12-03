function setUpCategorySelectionListeners() {
    var categoryCombo = document.getElementById('category');
    categoryCombo.addEventListener('change', function() {
        var selectedCategory = categoryCombo.value;
        showOrHideInputsForCategory(selectedCategory);
    });
}

function showOrHideInputsForCategory(category) {
    switch(category) {
        case 'movies':
            displayMovieInputs();
            break;
        case 'books':
            displayBookInputs();
            break;
    }
}

function displayMovieInputs() {
    document.getElementById('director').style.display = 'block';
    document.getElementById('author').style.display = 'none';
    document.getElementById('director_label').style.display = 'block';
    document.getElementById('author_label').style.display = 'none';
}

function displayBookInputs() {
    document.getElementById('director').style.display = 'none';
    document.getElementById('author').style.display = 'block';
    document.getElementById('director_label').style.display = 'none';
    document.getElementById('author_label').style.display = 'block';
}