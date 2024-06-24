const { createPool } = require('mysql');

const pool = createPool({
    host:"localhost",
    user:"rdmp_dev",
    password:"rdmp_dev_pwd",
    database:"rdmp_dev_db",
    connectionLimit:10
})

pool.query(`select * from roadmap`, (err, result, fields) => {
    if (err) {
        return console.log(err);
    }
    return console.log(result);
})