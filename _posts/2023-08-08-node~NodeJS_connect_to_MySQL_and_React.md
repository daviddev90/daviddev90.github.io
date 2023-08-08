---
layout: single
title: "[node]NodeJS connect to MySQL and React"
categories: web
tag: [react, web]
toc: true
author_profile: false
typora-root-url: ../
sidebar:
  nav: "counts"
---

<nav class="cods"><h2>node posts</h2><ol><li><p>NodeJS connect to MySQL and React (current)</p></li></ol></nav>


## Before Start

1. I assume you already installed MySQL and NodeJS.

2. I wrote 'React' in the post title, but it works the same in other javascript environments.
   Because I don't use any 'React' only library.
3. My table name is **words**, and it has these columns,
   - id (INT, auto increasing key)
   - f (INT, frequency)
   - w (VARCHAR, word)

## Setup Node Express Environment.

### Make server directory and init npm

```bash
mkdir server
cd server
npm init
npm i express mysql cors
touch index.js
touch insert.js
touch db.js
```

Write the above commands in your project root directory.
Below is the explanation of each step.

1. Create a 'server(or another preferred name)' folder inside your root folder.
2. change the directory to the 'server' folder.
3. initialize npm project (They will ask you some questions, you can just push Enter button to skip through.)
4. install packages. (with npm, yarn, or any preferred method)
5. make **index.js**(or another preferred name) file in current(server) directory.
   (This command works only on Mac. On Window, you can just make an index.js file.)
6. And also, make an **insert.js** file and a **db.js** file. I recommend you make a sub-directory and put it there, but I'm making it in the same directory for now.

## Server side code

### Index.js

```javascript
const express = require("express");
const app = express();
const db = require("./db");
const corsConfig = require("./cors-config");
const insertRoute = require("./insert");
const cors = require("cors");
const port = 4000;

app.use(
  cors({
    origin: "*",
    credentials: true, // Access-Control-Allow-Credentials
    optionsSuccessStatus: 200,
  })
);

app.use(express.json());

db.connect();

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.use('/insert', insertRoute(db));

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```



### db.js

```javascript
const mysql = require("mysql");

const connection = mysql.createConnection({
  host: "127.0.0.1",
  user: "root",
  password: "qwer132",
  database: "dict",
});

module.exports.connect = () => {
  connection.connect((err) => {
    if (err) {
      throw err;
    }
    console.log("Connected to database");
  });
  return connection;
};
```

### insert.js

```javascript
const express = require("express");
const router = express.Router();

module.exports = (db) => {
  router.post("/", (req, res) => {
    const word = req.body;
    const query = 'INSERT INTO words (f, w) VALUES (?, ?)';
    connection.query(query, [word.f, word.w], (err, result) => {
      if (err) {
        res.status(500).send(err);
      } else {
        res.status(200).send('Word added successfully!');
      }
    });
  });
  return router;
}
```

## Client Side Code

```javascript
const url = "http://localhost:4000/insert";
const res = await fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    f: word.f,
    w: word.w,
  }),
})
// do someting with res message
```