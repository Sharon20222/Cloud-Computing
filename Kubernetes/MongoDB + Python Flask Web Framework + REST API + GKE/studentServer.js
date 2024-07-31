var http = require('http');
var url = require('url');
var mongodb = require('mongodb');
const {
    MONGO_URL,
    MONGO_DATABASE
} = process.env;

// Expect the request to contain a query string with a key 'student_id' and a student ID as the value. For example: /api/score?student_id=1111
// The JSON response should contain only 'student_id', 'student_name' and 'student_score' properties. For example:
// {
//     "student_id": 1111,
//     "student_name": "Bruce Lee",
//     "student_score": 84
// }

var MongoClient = mongodb.MongoClient;
var uri = `mongodb://${MONGO_URL}/${MONGO_DATABASE}`;

// Connect to the db
console.log(`Connecting to MongoDB at ${uri}`);

var server = http.createServer(function (req, res) {
    // req.url = /api/score?student_id=11111
    var parsedUrl = url.parse(req.url, true);
    var student_id = parseInt(parsedUrl.query.student_id);

    // Match req.url with the string /api/score
    if (/^\/api\/score/.test(req.url) && !isNaN(student_id)) {
        MongoClient.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true }, function(err, client) {
            if (err) {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end("Database connection error\n");
                return;
            }
            var db = client.db(MONGO_DATABASE);
            db.collection("students").findOne({ "student_id": student_id }, (err, student) => {
                if (err) {
                    res.writeHead(500, { 'Content-Type': 'text/plain' });
                    res.end("Database query error\n");
                    return;
                }
                if (student) {
                    var response = {
                        student_id: student.student_id,
                        student_name: student.student_name,
                        student_score: student.student_score
                    };
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify(response) + '\n');
                } else {
                    res.writeHead(404, { 'Content-Type': 'text/plain' });
                    res.end("Student Not Found\n");
                }
                client.close();
            });
        });
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end("Wrong url or invalid student_id, please try again\n");
    }
});

server.listen(8080, () => {
    console.log('Server is listening on port 8080');
});
