//gestion des filtres

function sendCategory(category) {
  
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

function processFiltersForDisplay(filteredData) {
  const brandsWithProducts = {}; // Objet pour stocker les marques et leurs produits

  filteredData.forEach(filter => {
    const [brand, product] = filter.split(':'); // Sépare la chaîne "marque:produit"

    if (!brandsWithProducts[brand]) {
      brandsWithProducts[brand] = []; // Initialise un nouveau tableau si la marque n'existe pas
    }
    brandsWithProducts[brand].push(product); // Ajoute le produit au tableau de la marque
  });

  return brandsWithProducts;
}

function generateFilterElements(filteredData) {
  const brandsWithProducts = processFiltersForDisplay(filteredData);
  const brandsList = document.getElementById('brands-list'); // Supposons que vous avez un <select id="brands-list"></select>
  brandsList.innerHTML = ''; // Efface les options précédentes

  Object.keys(brandsWithProducts).forEach(brand => {
    const option = document.createElement('option');
    option.value = brand;
    option.textContent = brand;
    brandsList.appendChild(option);
  });

  // Événement change sur la sélection de la marque pour charger les produits
  brandsList.addEventListener('change', function() {
    const selectedBrand = this.value;
    const productsList = document.getElementById('products-list'); // Supposons que vous avez un second <select id="products-list"></select>
    productsList.innerHTML = ''; // Efface les options précédentes

    brandsWithProducts[selectedBrand].forEach(product => {
      const option = document.createElement('option');
      option.value = product;
      option.textContent = product;
      productsList.appendChild(option);
    });
  });
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


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Recherche


const searchInput = document.getElementById('search-input');


const filterList = document.getElementById('filter-list');


searchInput.addEventListener('input', function() {
  const searchText = searchInput.value.toLowerCase(); 


  const filters = filterList.getElementsByTagName('li');


  for (const filter of filters) {
    const filterName = filter.textContent.toLowerCase(); 

    if (filterName.includes(searchText)) {
      filter.style.display = 'block'; 
    } else {
      filter.style.display = 'none'; 
    }
  }
});

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
async function sendFilters() {
  
  const selectedFilters = getSelectedFilters();
  
  await sendFiltersToServer(selectedFilters);
}


function getSelectedFilters() {
  console.log("getting filters");
  
  // Récupère la marque sélectionnée
  const selectedBrand = document.getElementById('brands-list').value;
  
  // Récupère le produit sélectionné
  const selectedProduct = document.getElementById('products-list').value;
  
  // Crée un filtre sous la forme "marque:produit" si les deux sont sélectionnés
  const selectedFilters = [];
  if (selectedBrand !== "Choisir une marque" && selectedProduct !== "Choisir un produit") {
    selectedFilters.push(`${selectedBrand}:${selectedProduct}`);
  }
  
  return selectedFilters;
}


function sendFiltersToServer(filters) {
  
  console.log("sending")
  
  fetch('/filters', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ filters: filters })
  })
  .then(response => {
    if (response.ok) {
      console.log('filters sent successfully.');
      const panel= document.getElementById('filter-panel')
      panel.style.display = 'none';
      
      response.json().then(data => {
        console.log(Object.values(data))

        generateArticles(data);
      });

  } else {
      console.error('Failed to send filters.');
  }
  })
  .catch(error => {
    console.error('Erreur lors de l\'envoi des filtres :', error);
  });
}

//article
function generateOneArticle(cveData) {
  console.log("generating article")
  const article = document.createElement('div');
  console.log(article)
  article.classList.add('article');

  const img = document.createElement('img');
  img.src = 'test.png';
  img.alt = "Image de l'article";
  article.appendChild(img);

  const articleDetails = document.createElement('div');
  articleDetails.classList.add('article-details');

  const title = document.createElement('h2');
  title.textContent = cveData[0]; 
  articleDetails.appendChild(title);

  const detailsList = document.createElement('ul');

 
  const details = ['Marque','Date de publication', 'Dernière modification', 'Description', 'CVSS', 'Sévérité de base'];
  for (let i = 0; i < details.length; i++) {
    const listItem = document.createElement('li');
    listItem.textContent = `${details[i]}: ${cveData[i+1]}`;
    detailsList.appendChild(listItem);
  }

  articleDetails.appendChild(detailsList);
  article.appendChild(articleDetails);

  return article;
}

function generateArticles(filteredData) {
  console.log(filteredData)
  const articlesContainer = document.querySelector('.articles');

  // Efface les articles précédents
  articlesContainer.innerHTML = '';
  const reversedData = Object.values(filteredData).reverse();
  // Boucle sur les données des CVE
  reversedData.forEach(cve => {
    
    const article = generateOneArticle(cve);
    articlesContainer.appendChild(article);
  });

  const art = document.getElementById('articles');
  art.style.display = 'block';
}
document.getElementById('filter-panel').classList.add('hidden');
