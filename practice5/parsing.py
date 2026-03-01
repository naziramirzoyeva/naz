import re
import json


f = open("raw.txt", "r", encoding="utf-8")
text = f.read()
f.close()


lines = text.splitlines()

products = []
prices = []
total_amount = None
date_time = None
payment_method = None

current_product = None

for line in lines:
    line = line.strip()

    # 1 Product name
    if re.match(r"\d+\.", line):
        
        curr_prod = re.sub(r"\d+\.\s*", "", line)

    # 2 Price 
    elif re.match(r"\d+,\d{2}\Z", line):
        price = float(line.replace(",", "."))
        prices.append(price)

        # Attach price to the last found product
        if current_product:
            products.append({
                "name": current_product,
                "price": price
            })
            current_product = None

    # 3. Total amount 
    elif re.search(r"ИТОГО", line):
        total = re.findall(r"\d+,\d{2}", line)
        if total:
            total_amount = float(total[0].replace(",", "."))

    # 4. Date and time 
    elif re.search(r"Время", line):
        date_time = line

    # 5. Payment method 
    elif re.search(r"Банковская карта", line):
        payment_method = "Bank Card"


result = {
    "products": products,
    "all_prices": prices,
    "total_amount": total_amount,
    "date_time": date_time,
    "payment_method": payment_method
}

# Print JSON result
print(json.dumps(result, indent=4, ensure_ascii=False))