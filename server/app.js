const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');

const axios = require('axios');

const app = express();
const port = 31000;
const url_cve='http://localhost:5000/api/'

var lettre='H'

app.use(express.static(__dirname + '/public'));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'public'));
app.use(bodyParser.json());


app.get('/', (req, res) => {
  res.render('index');
});


// filtre

app.post('/cat', async (req, res) => {
  console.log("c'est moi")
  const { category } = req.body;
  lettre = category;
  
  try {
      const filteredData = await processFilters(category); 
      res.json(filteredData); 
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

              resolve(Array.from(cpeSet)); // Résoudre la promesse avec les données filtrées
          })
          .catch(error => {
              console.error('Erreur lors de la requête :', error);
              reject(error); // Rejeter la promesse en cas d'erreur
          });
  });
}
app.post('/filters',async (req, res) => {
  
  const selectedFilters = req.body.filters;
  console.log(selectedFilters)
  try{
  cve = await findcve(selectedFilters)

  res.json(cve)
} catch (error) {
  console.error('Erreur lors du traitement des filtres :', error);
  res.status(500).send('Erreur lors du traitement des filtres.');
}

});

function findcve(filters) {
  return new Promise((resolve, reject) => {
    var cve = new Set();
    axios.get(url_cve + lettre)
      .then(response => {
        const responseData = response.data;
        responseData.forEach(cveData => {
          cveData = JSON.stringify(cveData);
          filters.forEach(filtre => {
            if (cveData.includes(filtre)) {
              lst = cveData.split('\\');
              const id = lst[3].split('"')[1];
              const brand = filtre;
              const published = lst[11].split('"')[1].split("T")[0];
              const lastModified = lst[15].split('"')[1].split("T")[0];
              lst = lst.slice(22);
              const desc = lst[lst.indexOf('"en') + 4].split('"')[1];
              const cvss = lst[lst.indexOf('"baseScore') + 1].split(':')[1].split(",")[0].split("}")[0];
              const svr = lst[lst.indexOf('"baseSeverity') + 2].split('"')[1];
              const unite = [id,brand, published, lastModified, desc, cvss, svr];
              cve.add(unite);
            }
          });
        });
        console.log(cve)
        resolve(Array.from(cve)); // Résoudre la promesse avec les données CVE filtrées

      })
      .catch(error => {
        console.error('Erreur lors de la requête :', error);
        reject(error); // Rejeter la promesse en cas d'erreur
      });
  });
}


// Démarrage du serveur
app.listen(port, () => {
  console.log(`Le serveur est lancé sur http://localhost:${port}`);
});
