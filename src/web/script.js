var isHistoryDisplayed = false;


function RequestImage() {
    var textInput = document.getElementById("textInput").value;
    const varInput = document.getElementById("varInput").value;
    
    // Create a new XMLHttpRequest object
    var xhr = new XMLHttpRequest();
  
    // Set up a POST request
    xhr.open("POST", "http://localhost:8000/process-text", true);
    xhr.setRequestHeader("Content-Type", "application/json");
  
    // Define the callback function when the request is complete
    xhr.onload = function() {
      if (xhr.status === 200) {
        console.log("Text sent successfully!");

        // Show images
        var images = JSON.parse(xhr.responseText);
        displayImages(images, "result");
      } else {
        console.log("Error sending text. Status code: " + xhr.status);
      }
    };
  
    // Create a JSON object with the user input
    var data = JSON.stringify({ text: textInput , variations:varInput});
  
    // Send the request
    xhr.send(data);
  }

  function RequestHistory() {
    if (isHistoryDisplayed) {
      // Ocultar el contenedor de historial
      var historyDiv = document.getElementById("historyDiv");
      historyDiv.style.display = "none";
      historyDiv.innerHTML = "";
      isHistoryDisplayed = false;
    } else {
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "http://localhost:8000/access-history", true);
      xhr.setRequestHeader("Content-Type", "application/json");
  
      xhr.onload = function() {
        if (xhr.status === 200) {
          console.log("Request to access history sent successfully!");
  
          // Show images
          var images = JSON.parse(xhr.responseText);
          displayImagesAndClearContainer(images, "historyDiv", true);
  
          // Mostrar el contenedor de historial
          var historyDiv = document.getElementById("historyDiv");
          historyDiv.style.display = "block";
  
          // Actualizar el estado de la variable isHistoryDisplayed
          isHistoryDisplayed = true;
        } else {
          console.log("Error accessing history. Status code: " + xhr.status);
        }
      };
  
      xhr.send();
    }
  }

function displayImages(images, containerId) {
    var container = document.getElementById(containerId);
    container.innerHTML = "";
  
    images.forEach(function(imageUrl) {
      var img = document.createElement("img");
      img.src = imageUrl;
      container.appendChild(img);
    });
  }

function displayImagesAndClearContainer(images, containerId, clearContainer) {
    var container = document.getElementById(containerId);
    if (clearContainer) {
          container.innerHTML = "";
        }
      
    images.forEach(function(imageUrl) {
        var img = document.createElement("img");
          img.src = imageUrl;
          container.appendChild(img);

        // Agregar el nombre de la imagen
        var imageName = imageUrl.substring(imageUrl.lastIndexOf('/') + 1);

        // Recortar el nombre a 17 caracteres desde la derecha hacia la izquierda
        if (imageName.length > 17) {
          imageName = imageName.slice(0, -17);
        }

        var nameElement = document.createElement("p");
        nameElement.textContent = imageName;
        container.appendChild(nameElement);
        });
      
    if (clearContainer && images.length === 0) {
          container.style.display = "none";
        } else {
          container.style.display = "block";
    }
}

function uploadImage() {
  var fileInput = document.getElementById('fileInput');
  const varfileInput = document.getElementById("varfileInput").value;

  var file = fileInput.files[0];

  var reader = new FileReader();
  reader.onload = function(event) {
    var imageData = event.target.result;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:8000/upload-image", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Crear un objeto JSON con el archivo de imagen en formato base64
    // var data = JSON.stringify({ image: imageData, fileType: file.type });
    var data = JSON.stringify({ image: imageData, fileType: file.type, fileName: file.name, number: varfileInput});

    xhr.onload = function() {
      if (xhr.status === 200) {
        console.log("Image uploaded successfully!");

        // Show images
        var images = JSON.parse(xhr.responseText);
        displayImages(images, "newresult");
      
      } else {
        console.log("Error uploading image. Status code: " + xhr.status);
      }
    };

    xhr.send(data);
  };

  reader.readAsDataURL(file);
}




function fetchCategories() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "http://localhost:8000/categories", true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        var categories = JSON.parse(xhr.responseText);
        updateCategorySelect(categories);
      } else {
        console.log("Error fetching categories. Status code: " + xhr.status);
      }
    };
    xhr.send();
}
  
function updateCategorySelect(categories) {
    var categorySelect = document.getElementById('categorySelect');
    categorySelect.innerHTML = '<option value="" selected disabled>Select a category</option>';
  
    for (var i = 0; i < categories.length; i++) {
      var option = document.createElement('option');
      option.value = categories[i];
      option.textContent = categories[i];
      categorySelect.appendChild(option);
    }
}

function subscribeCategory() {
    var categorySelect = document.getElementById('categorySelect');
    var selectedCategory = categorySelect.value;
  
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:8000/subscribe", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function() {
      if (xhr.status === 200) {
        console.log("Subscribed to category:", selectedCategory);

      // Show images
      var images = JSON.parse(xhr.responseText);
      displayImages(images, "showCategory");

      } else {
        console.log("Error subscribing to category. Status code: " + xhr.status);
      }
    };
    xhr.send(JSON.stringify({ category: selectedCategory }));
  } 
  
fetchCategories();
  