import sqlite3

class Database:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)

    def list_test_cases(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM tcm_testcase')
        return cursor.fetchall()
    
    def delete_test_case(self, test_name: str):
        cursor = self.connection.cursor()
        cursor.execute(f'DELETE FROM tcm_testcase WHERE name ="{test_name}"')
        self.connection.commit()

    def close(self):
        self.connection.close()

