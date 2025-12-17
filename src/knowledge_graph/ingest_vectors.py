import json
import os
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Load Model Globally
print("🧠 Loading Embedding Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "pandit_secret_password")

def ingest_with_vectors(json_file_path):
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    if not os.path.exists(json_file_path):
        print(f"❌ File not found: {json_file_path}")
        return

    with open(json_file_path, 'r', encoding='utf-8') as f:
        rules = json.load(f)
        
    print(f"🧠 Generating Vectors for {len(rules)} Yogas...")
    
    # 1. Create Vector Index
    with driver.session() as session:
        session.run("""
            CREATE VECTOR INDEX rule_embeddings IF NOT EXISTS
            FOR (r:Rule)
            ON (r.embedding)
            OPTIONS {indexConfig: {
                `vector.dimensions`: 384,
                `vector.similarity_function`: 'cosine'
            }}
        """)

    # 2. Ingest Rules
    with driver.session() as session:
        for rule in rules:
            # Handle new Schema
            main_cond = rule.get("main_condition", "")
            mod_cond = rule.get("modifying_condition", "")
            result = rule.get("result", "")
            
            # Embed the full context
            text_to_embed = f"Yoga: {main_cond}. Modification: {mod_cond}. Result: {result}"
            vector = model.encode(text_to_embed).tolist()
            
            # Merge Node
            session.run("""
                MERGE (r:Rule {id: $id})
                SET r.text = $result, 
                    r.main_condition = $main_cond,
                    r.modifying_condition = $mod_cond,
                    r.source = $source,
                    r.embedding = $vector,
                    r.type = 'yoga'
            """, id=rule["id"], result=result, 
                 main_cond=main_cond, mod_cond=mod_cond, 
                 source=rule.get("source", "Unknown"), vector=vector)
            
            # Link Planets
            for entity in rule.get("entities", []):
                # Simple normalization
                valid_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
                for vp in valid_planets:
                    if vp in entity:
                        session.run("""
                            MATCH (r:Rule {id: $id})
                            MATCH (p:Planet {name: $p_name})
                            MERGE (r)-[:MENTIONS_PLANET]->(p)
                        """, id=rule["id"], p_name=vp)

            # Link House (Regex for "10th House", "House 10", etc.)
            import re
            house_match = re.search(r'(\d+)(st|nd|rd|th)?\s+House', main_cond, re.IGNORECASE)
            if house_match:
                h_num = int(house_match.group(1))
                session.run("""
                    MATCH (r:Rule {id: $id})
                    MATCH (h:House {number: $h_num})
                    MERGE (r)-[:APPLIES_TO_HOUSE]->(h)
                """, id=rule["id"], h_num=h_num)

    print("✅ Ingestion Complete.")
    driver.close()

if __name__ == "__main__":
    ingest_with_vectors("./data/processed_graph/extracted_rules.json")