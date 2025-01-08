import pandas as pd
import os


input_folder = "C:\SPTV21\HRFinder\parcing to db\json"
output_file = "combined.json"


dataframes = []


for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(input_folder, filename)
        try:

            df = pd.read_json(file_path)
            dataframes.append(df)
        except ValueError as e:
            print(f"Ошибка чтения {file_path}: {e}")


combined_df = pd.concat(dataframes, ignore_index=True)


combined_df.to_json(output_file, orient="records", indent=4, force_ascii=False)

print(f"Все данные объединены и сохранены в {output_file}")
