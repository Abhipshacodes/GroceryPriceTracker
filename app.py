import streamlit as st
import pandas as pd

# Mock price data (per unit)
grocery_prices = {
    'milk': {'BigBasket': 60, 'Blinkit': 58, 'Amazon': 62},
    'rice': {'BigBasket': 80, 'Blinkit': 85, 'Amazon': 78},
    'bread': {'BigBasket': 40, 'Blinkit': 42, 'Amazon': 39},
    'eggs': {'BigBasket': 60, 'Blinkit': 62, 'Amazon': 59},
    'atta': {'BigBasket': 280, 'Blinkit': 290, 'Amazon': 275}
}

st.title("🛒 Grocery Price Tracker & Cart Optimizer")
st.markdown("Compare grocery prices across platforms and find the cheapest cart!")

# Shopping list input
st.subheader("Enter the quantity for each item:")
shopping_list = {}
for item in grocery_prices:
    qty = st.number_input(f"{item.capitalize()} (units)", min_value=0, step=1)
    if qty > 0:
        shopping_list[item] = qty

# Find cheapest cart
def find_cheapest_cart(shopping_list, price_data):
    cart_total = {'BigBasket': 0, 'Blinkit': 0, 'Amazon': 0}
    item_sources = {}

    for item, qty in shopping_list.items():
        for platform in cart_total:
            cart_total[platform] += price_data[item][platform] * qty
        cheapest_platform = min(price_data[item], key=price_data[item].get)
        item_sources[item] = cheapest_platform

    overall_cheapest = min(cart_total, key=cart_total.get)
    return cart_total, item_sources, overall_cheapest

if st.button("Compare Prices"):
    if not shopping_list:
        st.warning("Please enter quantities!")
    else:
        cart_total, item_sources, best_platform = find_cheapest_cart(shopping_list, grocery_prices)

        st.subheader("🛍️ Cheapest Platform Per Item")
        for item, source in item_sources.items():
            st.write(f"- **{item.capitalize()}**: {source} at ₹{grocery_prices[item][source]}/unit")

        st.subheader("💰 Total Cart Cost Comparison")
        df = pd.DataFrame(cart_total.items(), columns=["Platform", "Total Cost"])
        st.bar_chart(df.set_index("Platform"))

        st.success(f"✅ Best platform overall: **{best_platform}** (₹{cart_total[best_platform]})")

