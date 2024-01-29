const express = require('express');
const path = require('path');

const app = express();
const port = 31000;
app.use(express.static(__dirname + '/public'));
// Configuration du moteur de modèle EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'public'));

// Route pour la page d'accueil
app.get('/', (req, res) => {
  res.render('index');
});

// Démarrage du serveur
app.listen(port, () => {
  console.log(`Le serveur est lancé sur http://localhost:${port}`);
});
