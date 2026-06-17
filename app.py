import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="AI Diet Recommendation System")

# BMI Calculation
def calculate_bmi(weight, height):
    h = height / 100
    return round(weight / (h * h), 2)

# BMI Category
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Diet Recommendation
def get_diet(food_pref, goal):
    diets = {
        "Vegetarian": {
            "Weight Loss": {
                "Breakfast": "Oats, Fruits",
                "Lunch": "Brown Rice, Vegetables",
                "Dinner": "Soup, Salad"
            },
            "Weight Gain": {
                "Breakfast": "Milk, Banana",
                "Lunch": "Rice, Paneer",
                "Dinner": "Chapati, Dal"
            },
            "Maintenance": {
                "Breakfast": "Idli, Sambar",
                "Lunch": "Rice, Vegetables",
                "Dinner": "Chapati, Dal"
            }
        },
        "Non Vegetarian": {
            "Weight Loss": {
                "Breakfast": "Boiled Eggs",
                "Lunch": "Chicken Salad",
                "Dinner": "Grilled Fish"
            },
            "Weight Gain": {
                "Breakfast": "Egg Omelette",
                "Lunch": "Chicken Rice",
                "Dinner": "Fish Curry"
            },
            "Maintenance": {
                "Breakfast": "Eggs, Toast",
                "Lunch": "Chicken Curry",
                "Dinner": "Fish Curry"
            }
        }
    }
    return diets[food_pref][goal]

# PDF Generator
def create_pdf(name, bmi, category, meals):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("AI Diet Recommendation Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Name: {name}", styles["Normal"]),
        Paragraph(f"BMI: {bmi}", styles["Normal"]),
        Paragraph(f"Category: {category}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph("Recommended Diet Plan", styles["Heading2"])
    ]

    for meal, item in meals.items():
        content.append(Paragraph(f"<b>{meal}</b>: {item}", styles["Normal"]))

    doc.build(content)
    buffer.seek(0)
    return buffer

# Streamlit UI
st.title("🥗 AI Diet Recommendation System")

name = st.text_input("Enter Your Name")
age = st.number_input("Age", min_value=1, max_value=100, value=20)
height = st.number_input("Height (cm)", min_value=50, max_value=250, value=160)
weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=60.0)

food_pref = st.selectbox(
    "Food Preference",
    ["Vegetarian", "Non Vegetarian"]
)

goal = st.selectbox(
    "Fitness Goal",
    ["Weight Loss", "Weight Gain", "Maintenance"]
)

if st.button("Generate Diet Plan"):

    bmi = calculate_bmi(weight, height)
    category = bmi_category(bmi)
    meals = get_diet(food_pref, goal)

    st.success("Diet Plan Generated Successfully!")

    st.subheader("BMI Result")
    st.write("BMI:", bmi)
    st.write("Category:", category)

    st.subheader("Recommended Meals")
    for meal, item in meals.items():
        st.write(f"**{meal}:** {item}")

    pdf = create_pdf(name, bmi, category, meals)

    st.download_button(
        label="Download PDF Report",
        data=pdf,
        file_name="Diet_Report.pdf",
        mime="application/pdf"
    )