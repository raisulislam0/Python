#define CROW_MAIN
#include <crow.h>
#include <sqlite3.h>
#include <iostream>

sqlite3* db;

/**
 * @page API Documentation
 * ## API documentation
 * Visit [API Documentation](http://localhost:8080/docs) for detailed API documentation.
 */

/**
 * @cond
 */
void initDatabase() {
    char* errMsg;
    const char* sql = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT);";
    if (sqlite3_exec(db, sql, 0, 0, &errMsg) != SQLITE_OK) {
        std::cerr << "Error creating table: " << errMsg << std::endl;
        sqlite3_free(errMsg);
    }
}

int main() {
    crow::SimpleApp app;
    if (sqlite3_open("users.db", &db)) {
        std::cerr << "Error opening database" << std::endl;
        return 1;
    }
    initDatabase();

    /**
     * @brief Add a new user.
     *
     * @param req The request object containing the user data in JSON format.
     * @return A response indicating the result of the operation.
     *
     * @Request:
     * {
     *     "name": "John Doe",
     *     "email": "john.doe@example.com"
     * }
     *
     * @Response:
     * HTTP 201 Created
     * "User added"
     */
    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::Post)([](const crow::request& req) {
        auto json = crow::json::load(req.body);
        if (!json || !json["name"].s() || !json["email"].s())
            return crow::response(400, "Invalid request");

        std::string sql = "INSERT INTO users (name, email) VALUES ('" + json["name"].s() + "', '" + json["email"].s() + "');";
        char* errMsg;
        if (sqlite3_exec(db, sql.c_str(), 0, 0, &errMsg) != SQLITE_OK) {
            sqlite3_free(errMsg);
            return crow::response(500, "Error inserting user");
        }
        return crow::response(201, "User added");
    });

    /**
     * @brief Retrieve all users.
     *
     * @return A response containing a JSON array of users.
     *
     * @Response:
     * [
     *     {
     *         "id": 1,
     *         "name": "John Doe",
     *         "email": "john.doe@example.com"
     *     },
     *     {
     *         "id": 2,
     *         "name": "Jane Smith",
     *         "email": "jane.smith@example.com"
     *     },
     *     {
     *          "id": 3,
     *         "name": "Alice Brown",
     *          "email": "alice@gmail.com"
     * }
     * ]
     */
    CROW_ROUTE(app, "/users").methods(crow::HTTPMethod::Get)([]() {
        crow::json::wvalue result;
        sqlite3_stmt* stmt;
        std::string sql = "SELECT * FROM users;";

        if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr) != SQLITE_OK)
            return crow::response(500, "Error retrieving users");

        int i = 0;
        while (sqlite3_step(stmt) == SQLITE_ROW) {
            result[i]["id"] = sqlite3_column_int(stmt, 0);
            result[i]["name"] = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            result[i]["email"] = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
            i++;
        }
        sqlite3_finalize(stmt);
        return crow::response(result);
    });

    /**
     * @brief Update an existing user.
     *
     * @param id The ID of the user to update.
     * @param req The request object containing the updated user data in JSON format.
     * @return A response indicating the result of the operation.
     *
     * @Request:
     * {
     *     "name": "John Doe",
     *     "email": "john.newemail@example.com"
     * }
     *
     * @Response:
     * HTTP 200 OK
     * "User updated"
     */
    CROW_ROUTE(app, "/users/<int>").methods(crow::HTTPMethod::Put)([](int id, const crow::request& req) {
        auto json = crow::json::load(req.body);
        if (!json || !json["name"].s() || !json["email"].s())
            return crow::response(400, "Invalid request");

        std::string sql = "UPDATE users SET name = '" + json["name"].s() + "', email = '" + json["email"].s() + "' WHERE id = " + std::to_string(id) + ";";
        char* errMsg;
        if (sqlite3_exec(db, sql.c_str(), 0, 0, &errMsg) != SQLITE_OK) {
            sqlite3_free(errMsg);
            return crow::response(500, "Error updating user");
        }
        return crow::response(200, "User updated");
    });

    /**
     * @brief Delete a user.
     *
     * @param id The ID of the user to delete.
     * @return A response indicating the result of the operation.
     *
     * @Response:
     * HTTP 200 OK
     * "User deleted"
     */
    CROW_ROUTE(app, "/users/<int>").methods(crow::HTTPMethod::Delete)([](int id) {
        std::string sql = "DELETE FROM users WHERE id = " + std::to_string(id) + ";";
        char* errMsg;
        if (sqlite3_exec(db, sql.c_str(), 0, 0, &errMsg) != SQLITE_OK) {
            sqlite3_free(errMsg);
            return crow::response(500, "Error deleting user");
        }
        return crow::response(200, "User deleted");
    });

    app.port(8080).multithreaded().run();
    sqlite3_close(db);
    return 0;
}
/**
 * @endcond
 */