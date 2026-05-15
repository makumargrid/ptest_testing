from flask import Flask, request

app = Flask(__name__)


@app.get("/users")
def users():
    user_id = request.args.get("id")
    query = "SELECT * FROM users WHERE id = " + user_id
    return {"query": query}
