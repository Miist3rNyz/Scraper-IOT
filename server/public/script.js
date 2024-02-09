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

function showFilterPanel(category) {
  console.log("appelé");
  const filterPanel = document.querySelector('.filter-panel');
  filterPanel.style.display = 'block';

  // Récupérer les données du formulaire
  const filterForm = document.getElementById('filter-form');
  filterForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Empêche le comportement par défaut de soumission du formulaire
  
    const formData = new FormData(filterForm);
    const filters = Array.from(formData.getAll('filter'));
  
    // Envoyer la catégorie et les valeurs des cases cochées au serveur
    fetch('/filters', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ category, filters })
    })
    .then(response => {
      if (response.ok) {
        console.log('Filters sent successfully.');
        // Masquer le panneau de filtres après l'envoi
        filterForm.reset();
        document.querySelector('.filter-panel').style.display = 'none';
      } else {
        console.error('Failed to send filters.');
      }
    })
    .catch(error => console.error('Error:', error));
  });
}
