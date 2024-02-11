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
  fetch('/filters', {
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
  filterList.innerHTML = ''; // Effacer les éléments précédents
  
  Object.values(filteredData).forEach(filter => {
      addFilterElement(filter, filterList); // Passer filterList à la fonction addFilterElement
  });
  const panel= document.getElementById('filter-panel')
  panel.style.display = 'block';

}

// Fonction pour ajouter un élément de filtre
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

  li.appendChild(input); // Placer la case à cocher en premier
  li.appendChild(label); // Placer le texte de l'étiquette après la case à cocher

  filterList.appendChild(li);
}



//Recherche

// Sélection de la barre de recherche
const searchInput = document.getElementById('search-input');

// Sélection de la liste des filtres
const filterList = document.getElementById('filter-list');

// Écouter les changements dans la barre de recherche
searchInput.addEventListener('input', function() {
  const searchText = searchInput.value.toLowerCase(); // Convertir le texte en minuscules

  // Sélectionner tous les éléments de la liste des filtres
  const filters = filterList.getElementsByTagName('li');

  // Parcourir tous les filtres
  for (const filter of filters) {
    const filterName = filter.textContent.toLowerCase(); // Convertir le texte du filtre en minuscules
    
    // Vérifier si le filtre correspond au texte de recherche
    if (filterName.includes(searchText)) {
      filter.style.display = 'block'; // Afficher le filtre s'il correspond
    } else {
      filter.style.display = 'none'; // Masquer le filtre s'il ne correspond pas
    }
  }
});
