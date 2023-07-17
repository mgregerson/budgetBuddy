(function () {
  document
    .querySelector("#categoryInput")
    .addEventListener("keydown", function (e) {
      if (e.keyCode != 13) {
        return;
      }

      e.preventDefault();

      let categoryName = this.value;
      this.value = "";
      addNewCategory(categoryName);
      updateCategoriesString();
    });

  function addNewCategory(name) {
    document.querySelector("#categoriesContainer").insertAdjacentHTML(
      "beforeend",
      `<li class="category">
        <span class="name">${name}</span>
        <span onClick="removeCategory(this)" class="btnRemove bold">X</span>
      </li>`
    );
  }
})();

function fetchCategoryArray() {
  let categories = [];

  document.querySelectorAll(".category").forEach(function (e) {
    let name = e.querySelector(".name").innerHTML;
    if (name == "") return;
    categories.push(name);
  });

  return categories;
}

function updateCategoriesString() {
  categories = fetchCategoryArray();
  document.querySelector(`input[name="categoriesString"]`).value =
    categories.join(",");
  categories.join;
}

function removeCategory(e) {
  e.parentElement.remove();
  updateCategoriesString();
}
