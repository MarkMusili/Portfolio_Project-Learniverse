const express = require('express');
const mysql = require('mysql');
const cors = require('cors');

const port = process.env.port || 5000;

const app = express();
app.use(cors());

app.get('/', (_re, res) => {
    return res.json("From Backend Side")
})

app.listen(port, () => {
    console.log(`Listening from port ${port}`);
})
