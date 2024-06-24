const express = require('express');
const cors = require('cors');
const api = require('./routes/api')

const app = express();
app.use(cors());
app.use(express.json());
app.use('/', api);

const PORT = process.env.port || 5000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
})
