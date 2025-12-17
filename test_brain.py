from src.knowledge_graph.query import PanditGraphQuery

# Initialize
brain = PanditGraphQuery()

# Ask: What happens if the Sun is in the 10th House?
results = brain.get_rules_for_planet_in_house("Sun", 10)

print("🔍 Found Rules:")
for r in results:
    print(f"- {r['rule_text']} ({r['source']})")
    
brain.close()