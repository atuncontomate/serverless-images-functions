const express = require ('express');

const server = express();
const tasksRouter = require('./routes/tasks');

let fs = require('fs');
let https = require('https');

server.use(express.json());
server.use('/tasks',tasksRouter);

https.createServer({
    key: fs.readFileSync('./certs/server.key', 'utf8'),
    cert: fs.readFileSync('./certs/server.cert', 'utf8')
}, server).listen(3443, () => {
    console.log("Https server started in port 3443");
});