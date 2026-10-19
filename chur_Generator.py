import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

# ==============================
# SETTINGS
# ==============================
N = 10000
random.seed(42)
np.random.seed(42)

# ==============================
# HELPER FUNCTIONS
# ==============================
def gen_id(i):
    prefix = f"{i+1:04d}"
    suffix = ''.join(random.choices(string.ascii_uppercase, k=5))
    return f"{prefix}-{suffix}"

def random_dob():
    start = datetime(1975, 1, 1)
    end = datetime(2005, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

def random_sub_date(start_y=2019, end_y=2024):
    start = datetime(start_y, 1, 1)
    end = datetime(end_y, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

# ==============================
# NAME POOLS (expanded for uniqueness)
# ==============================
male_first = [
    "Aarav","Vivaan","Aditya","Vihaan","Arjun","Sai","Reyansh","Ayaan","Krishna","Ishaan",
    "Shaurya","Atharva","Advik","Kabir","Ritvik","Aryan","Darsh","Veer","Rohan","Kunal",
    "Harsh","Yash","Nikhil","Pranav","Siddharth","Abhishek","Rahul","Amit","Vikram","Suresh",
    "Ravi","Manoj","Sanjay","Deepak","Ankit","Vivek","Ajay","Rajesh","Nitin","Gaurav",
    "Karan","Varun","Sahil","Tushar","Anuj","Mohit","Pankaj","Rakesh","Sachin","Naveen",
    "Dev","Om","Parth","Rudra","Shivansh","Tejas","Utkarsh","Viraj","Yuvraj","Zayan",
    "Anirudh","Bhavesh","Chirag","Dhruv","Eshan","Farhan","Girish","Hemant","Ishan","Jatin"
]

female_first = [
    "Aadhya","Ananya","Aarohi","Diya","Pari","Myra","Sara","Anika","Aanya","Navya",
    "Kiara","Riya","Saanvi","Avni","Ira","Prisha","Anvi","Ishita","Priya","Neha",
    "Pooja","Kavita","Sunita","Anita","Geeta","Nisha","Swati","Preeti","Divya","Meena",
    "Kiran","Sneha","Shreya","Tanvi","Isha","Aditi","Kriti","Nidhi","Pallavi","Ritu",
    "Sonal","Megha","Jyoti","Anjali","Poonam","Komal","Bhavna","Rashmi","Trisha","Vanya",
    "Aisha","Bhavya","Charvi","Dhriti","Esha","Falguni","Garima","Hina","Inaya","Jhanvi"
]

last_names = [
    "Sharma","Verma","Patel","Singh","Kumar","Gupta","Joshi","Mehta","Shah","Reddy",
    "Nair","Iyer","Rao","Chopra","Malhotra","Kapoor","Agarwal","Jain","Bhat","Desai",
    "Kulkarni","Pillai","Menon","Banerjee","Mukherjee","Chatterjee","Das","Bose","Sen","Ghosh",
    "Thakur","Pandey","Mishra","Tiwari","Yadav","Chauhan","Rathore","Saxena","Bansal","Goel",
    "Khanna","Arora","Bedi","Sethi","Anand","Bhatt","Trivedi","Dwivedi","Pathak","Shukla"
]

states_india = [
    "Maharashtra","Karnataka","Delhi","Nagaland","Meghalaya","Rajasthan","Telangana",
    "Uttar Pradesh","Gujarat","West Bengal","Tamil Nadu","Kerala","Punjab","Haryana","Bihar",
    "Madhya Pradesh","Odisha","Assam","Jharkhand","Chhattisgarh"
]

interests_list = ["travel","movie","drama","job","sports","music","reading","cooking",None,None,None,None]
sub_types = ["Refferal","Paid","Organic"]
plan_types = ["Basic","Standard","Premium"]
contract_types = ["Annual","Monthly"]
cancel_reasons = [
    "Switched to competitor","Too expensive","Not enough content",
    "Poor streaming quality","Forgot to cancel trial","Service issues"
]
comments = [
    "service issue","demaned refund","intention to renew","received refund",
    "billing problem","app crash","slow loading",None,None
]

# ==============================
# 1. GENERATE db_customer
# ==============================
used_names = set()
customers = []

for i in range(N):
    cid = gen_id(i)
    
    # Clean unique name (no numbers)
    name = None
    for attempt in range(100):
        gender_choice = np.random.choice(["Male","Female","Men","Women"], p=[0.38,0.38,0.12,0.12])
        first = random.choice(male_first if gender_choice in ["Male","Men"] else female_first)
        last = random.choice(last_names)
        candidate = f"{first} {last}".lower()
        if candidate not in used_names:
            name = candidate
            used_names.add(name)
            break
    
    # Rare fallback (still clean)
    if name is None:
        middle = random.choice(string.ascii_lowercase)
        name = f"{first} {middle} {last}".lower()
        used_names.add(name)
    
    country = np.random.choice(["India","Nepal",None], p=[0.86,0.07,0.07])
    if country == "Nepal":
        state = "Kathmandu"
    elif country is None:
        state = random.choice(["Delhi","Kathmandu","Telangana","Maharashtra"])
    else:
        state = random.choice(states_india)
    
    customers.append({
        "customerid": cid,
        "name": name,
        "country": country,
        "state": state,
        "gender": gender_choice,
        "dob": random_dob(),
        "interests": random.choice(interests_list),
        "pincode": None
    })

df_customer = pd.DataFrame(customers)

# ==============================
# 2. GENERATE db_subscription
# ==============================
subs = []
for _, row in df_customer.iterrows():
    start = random_sub_date()
    renewal = start + timedelta(days=random.randint(365, 1460))
    plan = np.random.choice(plan_types, p=[0.28, 0.42, 0.30])
    is_churn = np.random.rand() < 0.28
    
    if is_churn:
        cancel = start + timedelta(days=random.randint(30, 850))
        if cancel > datetime(2025, 12, 31):
            cancel = datetime(2025, random.randint(1, 8), random.randint(1, 28))
        cancel_reason = random.choice(cancel_reasons)
        score = random.randint(70, 99)
    else:
        cancel = None
        cancel_reason = None
        score = random.randint(3, 65)
    
    if plan == "Basic":
        charges = round(random.uniform(6.99, 12.99), 2)
    elif plan == "Standard":
        charges = round(random.uniform(12.99, 19.99), 2)
    else:
        charges = round(random.uniform(19.99, 92.99), 2)
    
    subs.append({
        "customerid": row["customerid"],
        "subscription_start_date": start.strftime("%Y-%m-%d"),
        "subscription_type": random.choice(sub_types),
        "renewal_date": renewal.strftime("%Y-%m-%d"),
        "plan_type": plan,
        "contract_type": np.random.choice(contract_types, p=[0.55, 0.45]),
        "cancellation_date": cancel.strftime("%Y-%m-%d") if cancel else None,
        "cancellation_reason": cancel_reason,
        "monthly_charges": charges,
        "cltv": int(charges * random.randint(12, 110)),
        "churn_score": score
    })

df_sub = pd.DataFrame(subs)

# ==============================
# 3. GENERATE db_support
# ==============================
support = []
support_cids = random.sample(list(df_customer["customerid"]), k=int(N * 0.38))

for cid in support_cids:
    n_tick = np.random.choice([1, 2], p=[0.78, 0.22])
    for _ in range(n_tick):
        support.append({
            "customerid": cid,
            "complaint_date": random_sub_date(2023, 2025).strftime("%Y-%m-%d"),
            "escalations": np.random.choice(["Y", "N"], p=[0.35, 0.65]),
            "csat_score": random.randint(10, 95),
            "col_1": None,
            "comment": random.choice(comments)
        })

df_support = pd.DataFrame(support)

# ==============================
# SAVE TO EXCEL
# ==============================
output_file = "customer_churn_data_2500_clean.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df_customer.to_excel(writer, sheet_name="db_customer", index=False)
    df_sub.to_excel(writer, sheet_name="db_subscription", index=False)
    df_support.to_excel(writer, sheet_name="db_support", index=False)

print("✅ Dataset generated successfully!")
print(f"Customers      : {len(df_customer)}")
print(f"Subscriptions  : {len(df_sub)}")
print(f"Support records: {len(df_support)}")
print(f"Unique IDs     : {df_customer['customerid'].nunique()}")
print(f"Unique Names   : {df_customer['name'].nunique()}")
print(f"Names with numbers: {df_customer['name'].str.contains(r'\\d').sum()}")
print(f"File saved as  : {output_file}")