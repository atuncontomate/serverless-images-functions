const mysql = require('mysql2/promise');

const hostName = process.env.HOST_NAME || 'hostName';
const userName = process.env.USER_NAME || 'userName';
const password = process.env.PASSWORD || 'password';

async function connect(){
    const connection = await mysql.createConnection({
        host: hostName,
        user: userName,
        password: password,
        database: 'imagefunctions'
    });
    console.log("Connected to MySQL");
    return connection;
}

async function findById(id) {
    const conn = await connect();

    const [rows] = await conn.execute(
        'SELECT * FROM imagefunctions.tasks WHERE id = ?',
        [id]
    );

    await conn.close();
    console.log("Connection closed");

    return await rows[0];
}

async function save(filepath) {
    const conn = await connect();
    const now = new Date();
    const [{ insertId }] = await conn.execute(
        'INSERT INTO imagefunctions.tasks (filepath, status, createdDate, lastModifiedDate) VALUES (?, ?, ?, ?)', [filepath, 'PENDING', now, now]
    );
    await conn.close();

    return await insertId;
}

exports.findById = findById;
exports.save = save;
