const mysql = require('mysql2')
const express = require('express')
const { promisify } = require('util');

const app = express()
app.use(express.json())

const con = mysql.createConnection({
    host: '172.16.16.105',
    port: '3306',
    user: 'prabPC',
    password: 'Synergy2023?',
    multipleStatements: true,
    database: 'TestDB'
});

// ,
//     database: 'TestDB'
const queryPromise = promisify(con.query).bind(con);

con.connect((err) => {
    if(err){
        console.log("Connection Error");
        console.log(err);
    }else{
        console.log("Connection to MySQL Database");
    }
});

app.listen(3000, () => {
    console.log('Node API app is running on port 3000')
})

app.get('/', (req, res) =>{
    res.send('Hello Node API')
})

app.get('/database-name', async (req, res) => {
  try {
      const databaseNames = await getDatabaseNames();
      res.send(databaseNames);

  } catch (err) {
      console.log('Error retrieving data:', err);
      res.status(500).send('Internal Server Error');
  }
});

app.get('/all-table', async (req, res) => {
    try {
        const tableNames = await getTableNames();
        res.send(tableNames);

    } catch (err) {
        console.log('Error retrieving data:', err);
        res.status(500).send('Internal Server Error');
    }
  });

app.get('/all-data', async (req, res) => {
    try {
        const tableNames = await getTableNames();
        const allData = {};

        for (const tableName of tableNames) {
            const data = await getAllDataFromTable(tableName);
            allData[tableName] = data;
        }

        res.send(allData);

    } catch (err) {
        console.log('Error retrieving data:', err);
        res.status(500).send('Internal Server Error');
    }
  });

  async function getTableNames() {
    const query = 'SHOW TABLES';
    try {
      const result = await queryPromise(query);
      console.log(result);
  
      if (Array.isArray(result)) {
        const tableNames = result.map(row => {
          const values = Object.values(row);
          return values.length > 0 ? values[0] : null;
        });
        console.log(tableNames);
        return tableNames.filter(tableName => tableName !== null);
      } else if (typeof result === 'object') {
        const tableNames = Object.values(result).filter(tableName => tableName !== null);
        console.log(tableNames);
        return tableNames;
      } else {
        console.error('Error retrieving table names:', result);
        throw new Error('Failed to retrieve table names');
      }
    } catch (err) {
      console.error('Error executing query:', err);
      throw err;
    }
  }
  
  async function getAllDataFromTable(tableName) {
    const query = `SELECT * FROM ${tableName}`;
    const rows = await queryPromise(query);
    return rows;
  }

  async function getDatabaseNames() {
    const query = 'SHOW DATABASES';
    try {
      const result = await queryPromise(query);
      console.log(result);
  
      if (Array.isArray(result)) {
        const databaseNames = result.map(row => {
          const values = Object.values(row);
          return values.length > 0 ? values[0] : null;
        });
        console.log(databaseNames);
        return databaseNames.filter(dbName => dbName !== null);
      } else if (typeof result === 'object') {
        const databaseNames = Object.values(result).filter(dbName => dbName !== null);
        console.log(databaseNames);
        return databaseNames;
      } else {
        console.error('Error retrieving database names:', result);
        throw new Error('Failed to retrieve database names');
      }
    } catch (err) {
      console.error('Error executing query:', err);
      throw err;
    }
  }