# src/knowledge_graph/query.py
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class PanditGraphQuery:
    def __init__(self):
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "pandit_secret_password")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_comprehensive_rules(self, chart_data, house_structure):
        """
        Retrieves rules for:
        1. Planet in House
        2. Lord of House X in House Y (The Backbone of BPHS)
        3. Conjunctions (Two planets in same house)
        """
        all_rules = []
        
        # We need a quick lookup for "Who is the Lord of House X?"
        # house_structure = {'House 1': {'Ruler': 'Mars'}, ...}
        house_lord_map = {int(k.split()[1]): v['Ruler'] for k, v in house_structure.items()}

        with self.driver.session() as session:
            # 1. ITERATE PLANETS (Standard Placement)
            for p_name, p_data in chart_data.items():
                if p_name == "Ascendant": continue
                
                h_num = p_data.get("house_number")
                if not h_num: continue

                # A. Direct Placement Rules (e.g., Sun in 10th)
                result = session.run("""
                    MATCH (p:Planet {name: $planet})<-[:MENTIONS_PLANET]-(r:Rule)-[:APPLIES_TO_HOUSE]->(h:House {number: $house})
                    RETURN r.text as text, r.condition as condition, r.type as type
                """, planet=p_name, house=h_num)
                
                for record in result:
                    all_rules.append({
                        "focus": p_name,
                        "type": "Placement",
                        "rule": record["text"],
                        "raw_cond": record["condition"]
                    })

            # 2. ITERATE HOUSES (Lordship Rules)
            # Logic: If Mars is Lord of 1st, and Mars is in 10th -> Fetch "Lord of 1st in 10th"
            for h_num in range(1, 13):
                lord_name = house_lord_map.get(h_num) # e.g., "Mars"
                if not lord_name or lord_name not in chart_data: continue
                
                lord_pos_house = chart_data[lord_name]["house_number"]
                
                # Fetch Logic: Rule must mention "Lord" and "House X" and apply to "House Y"
                # This is complex in strict Cypher without specific "Lord" nodes.
                # APPROXIMATION: We use Semantic Search for this specific pattern to find nodes.
                
                query_text = f"Lord of {h_num} in {lord_pos_house} House"
                vector_results = self.semantic_search(query_text, top_k=1)
                
                for res in vector_results:
                    if res['score'] > 0.82: # High confidence threshold
                        all_rules.append({
                            "focus": f"Lord of {h_num} ({lord_name})",
                            "type": "Lordship",
                            "rule": res['rule_text'],
                            "match_score": res['score']
                        })

        return all_rules

    def semantic_search(self, user_question, top_k=3):
        # Local import to avoid overhead if not used
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        question_vector = model.encode(user_question).tolist()

        query = """
        CALL db.index.vector.queryNodes('rule_embeddings', $k, $vec)
        YIELD node, score
        RETURN node.text as rule_text, node.source as source, score
        """
        with self.driver.session() as session:
            result = session.run(query, k=top_k, vec=question_vector)
            return [record.data() for record in result]