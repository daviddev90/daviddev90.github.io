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
3. My DB's schema name is **dict**, and table name is **words**, and it has these columns,
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
```

Write the above commands in your project root directory.
Below is the explanation of each step.

1. Create a 'server(or another preferred name)' folder inside your root folder.
2. Change the directory to the 'server' folder.
3. Initialize the npm project (They will ask you some questions, you can just push Enter button to skip through.)
4. Install packages. (with npm, yarn, or any preferred method)

### Create files

I create an index.js file in the **server** directory.
And I create a **db** folder and make four files.

I also create a **src** folder and another **config.js** file.
Which includes cors config.

![image-20230809032621880](/images/typora/image-20230809032621880.png)

## Codes

### db > config.js

```javascript
const mysql = require("mysql");

const db = mysql.createConnection({
  host: "127.0.0.1",
  user: "root", // if you didn't change, it must be 'root'
  password: "YOUR-PASSWORD",
  database: "dict", // YOUR-SCHEMA-NAME
});

module.exports = db;
```

### insert, delete, select common part

This is the common parts.

```javascript
const express = require("express");
const router = express.Router();

module.exports = (db) => {
  router.get("/", (req, res) => { 
    //router.post for insert, delete
    
    const query = "SQL QUERY SENTENCE";

    db.query(query, (err, results) => {
      if (err) {
        console.log(err);
        res.status(500).send({ message: "An error occurred" });
      } else {
        res.status(200).send(results);
      }
    });
  });

  return router;
};

```

### Individuals insert, delete, and select codes

#### insert.js

```javascript
const express = require("express");
const router = express.Router();

module.exports = (db) => {
  router.post("/", (req, res) => {
    const word = req.body;
    const query = "INSERT INTO words (f, w) VALUES (?, ?)";

    // word.f is number, but it will parsed safely into VALUES (?, ?)
    db.query(query, [word.f, word.w], (err, results) => { 
      if (err) {
        console.log(err);
        res.status(500).send({ message: "An error occurred" });
      } else {
        res.status(200).send(results);
      }
    });
  });

  return router;
};
```

#### select.js

```javascript
const express = require("express");
const router = express.Router();

module.exports = (db) => {
  router.get("/", (req, res) => {
    const query = "SELECT * FROM words";

    db.query(query, (err, results) => {
      if (err) {
        console.log(err);
        res.status(500).send({ message: "An error occurred" });
      } else {
        res.status(200).send(results);
      }
    });
  });

  return router;
};

```

#### delete.js

```javascript
const express = require("express");
const router = express.Router();

module.exports = (db) => {
  router.post("/", (req, res) => {
    const removingIds = req.body.removingIds;

    if (!Array.isArray(removingIds) || removingIds.length === 0) {
      return res.status(400).send({ message: "No IDs provided" });
    }
		
    // this time, to show another way to generate query, I just used join method and parsed directly into the query.
    const query = `DELETE FROM words WHERE id IN (${removingIds.join(",")})`;

    db.query(query, (err, result) => {
      if (err) {
        console.log(err);
        res.status(500).send({ message: "An error occurred" });
      } else {
        // If delete success, I will send changed words.
        // This is not a cost-efficient way to give feedback users.
        // But I just want to show how it works.
        const selectQuery = "SELECT * FROM words";
        db.query(selectQuery, (selectErr, selectResults) => {
          if (selectErr) {
            console.log(selectErr);
            res
              .status(500)
              .send({ message: "An error occurred fetching words" });
          } else {
            res.send(selectResults); // Send all words as the response
          }
        });
      }
    });
  });

  return router;
};

```

### src > config.js

```javascript
const cors = require("cors");

const corsConfig = cors({
  origin: "*",
  credentials: true, // Access-Control-Allow-Credentials
  optionsSuccessStatus: 200,
});

module.exports = {
  corsConfig,
};
```

### Index.js

```javascript
const express = require("express");
const app = express();
const { corsConfig } = require("./src/config");
const port = 4000;
const db = require("./db/config");

const selectRoute = require("./db/select");
const insertRoute = require("./db/insert");
const deleteRoute = require("./db/delete");

app.use(corsConfig);
app.use(express.json());
db.connect();

app.get("/", (req, res) => {
  res.send("Hello World!");
});
app.use("/insert", insertRoute(db));
app.use("/get", selectRoute(db));
app.use("/delete", deleteRoute(db));

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

```

### Client Side Code

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

## Some more Security Considerations for Real-World Applications

### 1. Prevent SQL injection.

In the **insert.js** code above, I used prepared statements like this:

```javascript
const word = req.body;
const query = "INSERT INTO words (f, w) VALUES (?, ?)";

// word.f is number, but it will parsed safely into VALUES (?, ?)
db.query(query, [word.f, word.w], (err, results) => { 
```

In the **delete.js** code, I directly put user inputs into queries.

```javascript
const removingIds = req.body.removingIds;
const query = `DELETE FROM words WHERE id IN (${removingIds.join(",")})`;
```

Directly putting user inputs into queries is DANGEROUS.
I strongly recommend you always use prepared statements.

Of course, this is just an essential first step to prevent SQL injection.

### 2. CORS Policy

```javascript
const cors = require("cors");

const corsConfig = cors({
  origin: "*",
...
```

In the above code, a wildcard (*) origin is allowed. 
In production, you should restrict this to specific trusted domains to prevent unauthorized domains from making requests to your server, 

```javascript
const whitelist = ['http://example1.com', 'http://example2.com'];

const corsConfig = cors({
  origin: function (origin, callback) {
    if (whitelist.indexOf(origin) !== -1 || !origin) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  }
})
```

CORS is a client-side security measure, and malicious users can still directly make requests to your server outside of a browser environment.

And ChatGPT told me more solutions like these:

### 3. Authentication

You can use JWT or some other authentication method

### 4. Rate-Limiting

This is a simple solution. But this can slow down or block brute-force attacks.

### 5. Use Secure Headers

Secure your application by setting appropriate HTTP headers like `X-Content-Type-Options`, `X-Frame-Options`, and `X-XSS-Protection`.

## Conclusion?

Well, I always don't know how to end the posts.

If you have any questions, feel free to ask.

So. Bye:)