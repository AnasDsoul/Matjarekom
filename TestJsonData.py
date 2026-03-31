import pandas as pd
import json
import openpyxl

# Charger le JSON
with open(r"D:\Formation\PY\test json file and GRAPHQLSOPIFY\MatjarekomTest.json", "r", encoding="utf-8") as F:
    file = json.load(F)

Data = file["data"]
allProduct = []
for Dat in Data:
    all_data = Dat["values"]["deliveries"]
    for l in all_data:
        row = {"city":l["city"],"subject":l["subject"],"returnStatus":l["returnStatus"],
        "createdOn": l["createdOn"],
        "id": l["id"],
        "amount": l["amount"],
        "address": l["address"],"deliveryStatusType": l["deliveryStatusType"],"phone": l["phone"],
        "recipient": l["recipient"],"deliveryStatus": l["deliveryStatus"],"status":l["status"]}
        allProduct.append(row)

df = pd.DataFrame(allProduct)

df.to_excel(
    r"C:\Users\Anas\Desktop\PythonDataAnalyst\Matjarekom.xlsx",
    index=False,
    engine="openpyxl"
)

print("Done — fichier généré.")
