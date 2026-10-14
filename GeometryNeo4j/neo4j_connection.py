import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


class Neo4jConnection:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
        self.username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD","12345678")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")

        if not self.password:
            raise ValueError("Chưa cấu hình NEO4J_PASSWORD trong file .env")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def verify_connection(self):
        self.driver.verify_connectivity()

    def execute_query(self, query, parameters=None):
        with self.driver.session(database=self.database) as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def close(self):
        self.driver.close()
