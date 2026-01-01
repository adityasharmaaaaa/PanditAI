import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "pandit_secret_password")


def create_schema():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    print("🔌 Connecting to Neo4j...")

    queries = [
        # 1. Unique Constraints (Speed up lookups and prevent duplicates)
        "CREATE CONSTRAINT planet_name IF NOT EXISTS FOR (p:Planet) REQUIRE p.name IS UNIQUE",
        "CREATE CONSTRAINT sign_id IF NOT EXISTS FOR (s:Sign) REQUIRE s.id IS UNIQUE",
        "CREATE CONSTRAINT house_num IF NOT EXISTS FOR (h:House) REQUIRE h.number IS UNIQUE",
        # 2. Index for Rules (To search rules by keywords later)
        "CREATE INDEX rule_text IF NOT EXISTS FOR (r:Rule) ON (r.text)",
        # 3. Pre-seed the 12 Zodiac Signs
        """
        UNWIND range(0, 11) as i
        MERGE (s:Sign {id: i})
        ON CREATE SET s.name = 
            CASE i 
                WHEN 0 THEN 'Aries' WHEN 1 THEN 'Taurus' WHEN 2 THEN 'Gemini'
                WHEN 3 THEN 'Cancer' WHEN 4 THEN 'Leo' WHEN 5 THEN 'Virgo'
                WHEN 6 THEN 'Libra' WHEN 7 THEN 'Scorpio' WHEN 8 THEN 'Sagittarius'
                WHEN 9 THEN 'Capricorn' WHEN 10 THEN 'Aquarius' WHEN 11 THEN 'Pisces'
            END
        """,
        # 4. Pre-seed the 9 Planets (Grahas)
        """
        UNWIND ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'] as p_name
        MERGE (p:Planet {name: p_name})
        """,
        # 5. Pre-seed the 12 Houses (Bhavas)
        """
        UNWIND range(1, 12) as i
        MERGE (h:House {number: i})
        """,
    ]

    try:
        with driver.session() as session:
            for q in queries:
                session.run(q)
        print("  Graph Schema & Static Nodes initialized successfully.")
    except Exception as e:
        print(f"  Error initializing graph: {e}")
        print("Tip: Is your Docker container running? (docker-compose up -d)")
    finally:
        driver.close()


if __name__ == "__main__":
    create_schema()
