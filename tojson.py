import pandas as pd
import json


df = pd.read_json("us.txt", lines=True)


df.to_json("us.json", orient="records", indent=4, force_ascii=False)

df = pd.read_json("india.txt", lines=True)


df.to_json("india.json", orient="records", indent=4, force_ascii=False)

df = pd.read_json("israel.txt", lines=True)


df.to_json("israel.json", orient="records", indent=4, force_ascii=False)

df = pd.read_json("japan.txt", lines=True)


df.to_json("japan.json", orient="records", indent=4, force_ascii=False)

df = pd.read_json("singapore.txt", lines=True)

df.to_json("singapore.json", orient="records", indent=4, force_ascii=False)