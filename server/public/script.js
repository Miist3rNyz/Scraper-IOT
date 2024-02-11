function showPopup(title, author, date, desc) {
    var popup = document.getElementById('popup');
    var popupTitle = document.getElementById('popup-title');
    var popupAuthor = document.getElementById('popup-author');
    var popupDate = document.getElementById('popup-date');
    var popupDesc = document.getElementById('popup-desc')
    popupTitle.textContent = title;
    popupAuthor.textContent = 'Auteur: ' + author;
    popupDate.textContent = 'Date: ' + date;
    popupDesc.textContent='Description: ' + desc;
    
    popup.style.display = 'block';
  }

function hidePopup(){
    var popup = document.getElementById('popup');
    popup.style.display='none';
}

//gestion des filtres

function sendCategory(category) {
  console.log("appelé");
  
  // Envoyer la catégorie au serveur
  fetch('/cat', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ category })
  })
  .then(response => {
      if (response.ok) {
          console.log('Category sent successfully.');
          
          response.json().then(data => {
            generateFilterElements(data);
          });

      } else {
          console.error('Failed to send category.');
      }
  })

  .catch(error => {
      console.error('Error:', error);
  });
}


function generateFilterElements(filteredData) {

  const filterList = document.getElementById('filter-list');
  filterList.innerHTML = ''; //efface
  
  Object.values(filteredData).forEach(filter => {
      addFilterElement(filter, filterList); 
  });
  const panel= document.getElementById('filter-panel')
  panel.style.display = 'block';

}

// Fonction pour ajouter un élément de filtre

function addFilterElement(filterName, filterList) {
  const li = document.createElement('li');
  const label = document.createElement('label');
  const input = document.createElement('input');

  input.type = 'checkbox';
  input.id = filterName;
  input.name = 'filter';
  input.value = filterName;

  label.htmlFor = filterName;
  label.textContent = filterName;

  li.appendChild(input); 
  li.appendChild(label); 

  filterList.appendChild(li);
}



//Recherche


const searchInput = document.getElementById('search-input');


const filterList = document.getElementById('filter-list');


searchInput.addEventListener('input', function() {
  const searchText = searchInput.value.toLowerCase(); // Convertir le texte en minuscules


  const filters = filterList.getElementsByTagName('li');


  for (const filter of filters) {
    const filterName = filter.textContent.toLowerCase(); // Convertir le texte du filtre en minuscules

    if (filterName.includes(searchText)) {
      filter.style.display = 'block'; 
    } else {
      filter.style.display = 'none'; 
    }
  }
});

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function sendFilters() {
  
  const selectedFilters = getSelectedFilters();
  
  sendFiltersToServer(selectedFilters);
}


function getSelectedFilters() {
  const checkboxes = document.querySelectorAll('#filter-list input[type="checkbox"]');
  const selectedFilters = [];
  checkboxes.forEach(function(checkbox) {
    if (checkbox.checked) {
      selectedFilters.push(checkbox.value);
    }
  });
  return selectedFilters;
}


function sendFiltersToServer(filters) {
  
  fetch('/filters', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ filters: filters })
  })
  .then(response => {
    // Traitez la réponse du serveur si nécessaire
  })
  .catch(error => {
    console.error('Erreur lors de l\'envoi des filtres :', error);
  });
}