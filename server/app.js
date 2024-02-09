const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const port = 31000;
app.use(express.static(__dirname + '/public'));
// Configuration du moteur de modèle EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'public'));
app.use(bodyParser.json());

// Route pour la page d'accueil
app.get('/', (req, res) => {
  res.render('index');
});


// filtre
// Route pour le filtrage
app.post('/filters', (req, res) => {

  const { category, filters } = req.body;

  // Traiter les filtres en fonction de la catégorie (à implémenter )
  const filteredData = processFilters(category, filters);

  // Renvoyer les filtres traités au format JSON
  res.json(filteredData);
});

function processFilters(category, filters) {
  console.log("liste ok")
  // Implémentez votre logique de traitement des filtres ici
  const filteredResults=['filtre 1', 'filtre 2']
  return filteredResults;
}


// Démarrage du serveur
app.listen(port, () => {
  console.log(`Le serveur est lancé sur http://localhost:${port}`);
});
