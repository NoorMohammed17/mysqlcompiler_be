from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import sqlparse  # Add this at the top

app = Flask(__name__)
CORS(app)

# Update with your actual DB credentials
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Noor@123", # here change with your password
    "database": "testdb" # here change with your database name
}

@app.route('/execute', methods=['POST'])
def execute_query():
    data = request.get_json()
    full_query = data.get("query", "")

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # queries = [q.strip() for q in full_query.split(";") if q.strip()]
        queries = [str(stmt).strip() for stmt in sqlparse.parse(full_query) if str(stmt).strip()]

        final_result = None
        for query in queries:
            cursor.execute(query)

            # Capture the last SELECT query result to return
            if query.lower().startswith("select"):
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                final_result = {
                    "success": True,
                    "columns": columns,
                    "data": rows
                }
            else:
                connection.commit()
                final_result = {
                    "success": True,
                    "message": f"Query executed: {query}"
                }

        return jsonify(final_result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
