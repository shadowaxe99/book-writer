const express = require('express');
const { spawn } = require('child_process');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  const python = spawn('python', ['main.py']);
  python.stdout.on('data', (data) => {
    res.send(data.toString());
  });
});

app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});