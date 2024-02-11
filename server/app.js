const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');

const axios = require('axios');

const app = express();
const port = 31000;
const url_cve='http://localhost:5000/api/'

var lettre='H'

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
app.post('/filters', async (req, res) => {
  const { category } = req.body;
  
  try {
      const filteredData = await processFilters(category); // Attendre la fin du calcul de processFilters
      console.log("renvoyé");
      res.json(filteredData); // Renvoyer les données filtrées au client au format JSON
  } catch (error) {
      console.error('Erreur lors du traitement des filtres :', error);
      res.status(500).send('Erreur lors du traitement des filtres.');
  }
});

function processFilters(category) {
  return new Promise((resolve, reject) => {
      // Effectuer la requête pour obtenir les données CVE
      var cpeSet = new Set();
      console.log(category);
      axios.get(url_cve + category)
          .then(response => {
              const responseData = response.data;
              var cpeRegex = /cpe:[^"]+/g;
              responseData.forEach(element => {
                  str = JSON.stringify(element);
                  var cpeMatches = str.match(cpeRegex);
                  if (cpeMatches) {
                      cpeMatches.forEach(function (cpe) {
                          var cpeParts = cpe.split(':');
                          if (cpeParts.length >= 5) {
                              // Récupérer les parties 3 et 4 (indexés à partir de 0)
                              var extractedCPE = cpeParts[3] + ":" + cpeParts[4];
                              // Ajout du CPE à l'ensemble pour éliminer les duplicatas
                              if (!cpeSet.has(extractedCPE)) {
                                  cpeSet.add(extractedCPE);
                              }
                          }
                      });
                  }
              });
              console.log("Nombre d'éléments dans cpeSet :", cpeSet.size);
              resolve(Array.from(cpeSet)); // Résoudre la promesse avec les données filtrées
          })
          .catch(error => {
              console.error('Erreur lors de la requête :', error);
              reject(error); // Rejeter la promesse en cas d'erreur
          });
  });
}

// Route pour le filtrage
app.post('/filters', async (req, res) => {
  const { category } = req.body;

  try {
      const filteredData = await processFilters(category); // Attendre la fin du calcul de processFilters
      console.log("renvoyé");
      res.json(filteredData); // Renvoyer les données filtrées au client au format JSON
  } catch (error) {
      console.error('Erreur lors du traitement des filtres :', error);
      res.status(500).send('Erreur lors du traitement des filtres.');
  }
});

 



// Démarrage du serveur
app.listen(port, () => {
  console.log(`Le serveur est lancé sur http://localhost:${port}`);
});
