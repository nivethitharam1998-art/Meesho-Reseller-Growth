import csv

def evaluate_growth_alerts(orders_csv_path):
    category_month_gmv = {}
    
    with open(orders_csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['status'] == 'Delivered':
                month = row['month']
                cat = row['category']
                gmv = float(row['quantity']) * float(row['unit_price'])
                category_month_gmv.setdefault(month, {}).setdefault(cat, 0.0)
                category_month_gmv[month][cat] += gmv

    alerts = []
    # Compare May vs June
    for cat in category_month_gmv.get('May', {}):
        may_gmv = category_month_gmv['May'].get(cat, 0)
        june_gmv = category_month_gmv['June'].get(cat, 0)
        
        if may_gmv > 0:
            pct_change = ((june_gmv - may_gmv) / may_gmv) * 100
            if pct_change >= 20:
                alerts.append({"category": cat, "type": "HIGH_GROWTH", "change_pct": round(pct_change, 2)})
            elif pct_change <= -20:
                alerts.append({"category": cat, "type": "SIGNIFICANT_DROP", "change_pct": round(pct_change, 2)})

    return alerts

if __name__ == "__main__":
    alerts = evaluate_growth_alerts("../data/orders.csv")
    print("Triggered Rules Engine Alerts:", alerts)