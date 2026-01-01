import json
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "pandit_secret_password")


def ingest_rules(json_file_path):
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    with open(json_file_path, "r") as f:
        rules = json.load(f)

    print(f"🚀 Ingesting {len(rules)} Smart Rules into Neo4j...")

    with driver.session() as session:
        for rule in rules:
            # 1. Create the Abstract Rule Node
            # We add a 'prediction' property which is crucial for the UI
            session.run(
                """
                MERGE (r:Rule {id: $id})
                SET r.text = $prediction, 
                    r.condition = $condition,
                    r.source = $source,
                    r.type = $type
            """,
                id=rule["id"],
                prediction=rule["prediction"],
                condition=rule["condition"],
                source=rule["source"],
                type=rule["type"],
            )

            # 2. Dynamic Entity Linking
            # If the rule mentions "Sun", link it to the Sun node
            for entity in rule.get("entities", []):
                # Standardize entity name (Simple normalization)
                if "Sun" in entity:
                    e_name = "Sun"
                elif "Moon" in entity:
                    e_name = "Moon"
                elif "Jupiter" in entity:
                    e_name = "Jupiter"
                elif "Mars" in entity:
                    e_name = "Mars"
                elif "Saturn" in entity:
                    e_name = "Saturn"
                elif "Venus" in entity:
                    e_name = "Venus"
                elif "Mercury" in entity:
                    e_name = "Mercury"
                else:
                    e_name = None

                if e_name:
                    session.run(
                        """
                        MATCH (r:Rule {id: $id})
                        MATCH (p:Planet {name: $p_name})
                        MERGE (r)-[:MENTIONS_PLANET]->(p)
                    """,
                        id=rule["id"],
                        p_name=e_name,
                    )

            # 3. Handle House Numbers (if mentioned in condition)
            # Simple regex to find "10th House" or "10"
            import re

            house_match = re.search(
                r"(\d+)(st|nd|rd|th)?\s+House", rule["condition"], re.IGNORECASE
            )
            if house_match:
                h_num = int(house_match.group(1))
                session.run(
                    """
                    MATCH (r:Rule {id: $id})
                    MATCH (h:House {number: $h_num})
                    MERGE (r)-[:APPLIES_TO_HOUSE]->(h)
                """,
                    id=rule["id"],
                    h_num=h_num,
                )

    print("  Knowledge Graph Upgrade Complete.")
    driver.close()


if __name__ == "__main__":
    # Point to the NEW extracted file
    ingest_rules("./data/processed_graph/extracted_rules.json")
