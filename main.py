import streamlit as st
import pandas as pd
import joblib
randomforest_model = joblib.load("random_forest_regressor_model.joblib") # model
training_columns = joblib.load("training_columns.pkl") # for X-train contain all content which we use for train
# Page configuration
st.set_page_config(
    page_title="Superstore Dashboard",
    layout="wide"
)

# Dashboard title
st.title("📊 Superstore Profit Prediction Dashboard")

# Load dataset
df = pd.read_csv("Superstore_DIRTY_practice (1).csv")

# Basic information
st.subheader("Dataset Information")

col1, col2 = st.columns(2)

with col1:
        st.metric("Rows", df.shape[0])

with col2:
        st.metric("Columns", df.shape[1])

# recreate region
import numpy as np

df["Region"] = np.select(
        [
            df["Region_East"] == 1,
            df["Region_South"] == 1,
            df["Region_West"] == 1
        ],
        [
        "East",
        "South",
        "West"
        ],
        default="Central"
    )

    

# create category
import numpy as np
df["Category"]=np.select(
        [
            df['Category_Office Supplies']==1,
            df['Category_Technology']==1
        ],
        [
           "Office Supplies",
            "Technology"
        ],
        default="Furniture"
    )
    
# create sub category
import numpy as np
df["Sub-Category"]=np.select(
        [
            df['Sub-Category_Appliances']==1,
            df['Sub-Category_Art']==1,
            df['Sub-Category_Binders']==1,
            df['Sub-Category_Bookcases']==1,
            df['Sub-Category_Chairs']==1,
            df['Sub-Category_Envelopes']==1,
            df['Sub-Category_Fasteners']==1,
            df['Sub-Category_Furnishings']==1,
            df['Sub-Category_Labels']==1,
            df['Sub-Category_Machines']==1,
            df['Sub-Category_Paper']==1,
            df['Sub-Category_Phones']==1,
            df['Sub-Category_Storage']==1,
            df['Sub-Category_Supplies']==1,
            df['Sub-Category_Tables']==1
        ],
        [
            "Appliances" ,
            "Art",
            "Binders",
            "Bookcases",
            "Chairs",
            "Envelopes",
            "Fasteners",
            "Furnishings",
            "Labels",
            "Machines",
            "Paper",
            "Phones",
            "Storage",
            "Supplies",
            "Tables"
        ],
        default="Accessories"
    )


# year
df["Year"] = df["Order Year"]

# create copy for filtering
filtered_df = df.copy() # use to make dashboard dynamic
# navigation
from streamlit_option_menu import option_menu

with st.sidebar:
        selected = option_menu(
            menu_title="📂 Navigation",
                options=[
                "Overview",
                "Sales Analysis",
                "Profit Analysis",
                "Loss Analysis",
                "Discount Analysis",
                "ML Prediction"
            ],
            icons=[
             "house",
            "bar-chart",
            "graph-up",
            "exclamation-triangle",
            "percent",
            "robot"
        ],
        default_index=0,
    )
        # sidebar
st.sidebar.header("🔎 Filters")
# sidebar
# create region sidebar
region = st.sidebar.selectbox( # st-streamlit library , sidebar create sidebar widget,select box create drop down menu
        "Select Region", #label
        ["All"] + sorted(df["Region"].unique()) # add ALL in starting and sorted region
    )

if region != "All": # if user choose ALL then it become false 
#if it choose other like east then Region==east then it gave data only of east 
        filtered_df = filtered_df[filtered_df["Region"] == region]

# create category sidebar
category=st.sidebar.selectbox(
        "Select Categpry",
        ["All"] + sorted(df["Category"].unique())
    )
if category!="All":
        filtered_df=filtered_df[filtered_df["Category"]==category]

# create sub_category sidebar
sub_category=st.sidebar.selectbox(
        "Select Sub-Categpry",
        ["All"] + sorted(df["Sub-Category"].unique())
    )
if sub_category!="All":
        filtered_df=filtered_df[filtered_df["Sub-Category"]==sub_category]

# create year sidebar
year = st.sidebar.selectbox(
        "Select Year",
        ["All"] + sorted(df["Order Year"].unique())
    )
   

    

if year != "All":
    filtered_df = filtered_df[filtered_df["Order Year"] == year]

st.sidebar.markdown("---")
st.sidebar.markdown("### 👩‍💻 Developed by")
st.sidebar.markdown("**Sidakpreet Kaur**")
    # .........overview.........
if selected == "Overview":
    st.subheader("🔍 Current View Filters")

    
    st.markdown(f"""
    - 📅 **Year:** **{year}**
    - 🌍 **Region:** **{region}**
    - 📦 **Category:** **{category}**
    - 🔹 **Sub-Category:** **{sub_category}**
    """)

#KPI
    st.subheader("📈 Key Performance Indicators")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")

    with col2:
        st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")

    with col3:
        st.metric("Total Orders", len(filtered_df))

    with col4:
        st.metric("Average Discount", f"{filtered_df['Discount'].mean()*100:.1f}%")

    with col5:
        st.metric("Average Shipping Days",f"{filtered_df['Shipping_Days'].mean():.2f}Days")
    with col6:
        st.metric(
        "Profit Margin",
        f"{(filtered_df['Profit'].sum() / filtered_df['Sales'].sum()) * 100:.2f}%"
        )
# preview filtered data
    title = "📋 Preview Data"

    if year != "All":
        title += f" | Year: {year}"

    if region != "All":
        title += f" | Region: {region}"

    if category != "All":
        title += f" | Category: {category}"

    with st.expander(title, expanded=False):
        st.dataframe(filtered_df.head(10))
    #........... sales analysis..........
elif selected == "Sales Analysis":
# make chart
    st.title("📊 Superstore Sales Dashboard")
    st.subheader("📦 Sales by Category")
    import plotly.express as px # use to make interactive graph
# like Bar chart , Pie chart , Line chart , Scatter plot.

    sales_by_category = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar( # create bar chart
        sales_by_category,
        x="Category",
        y="Sales",
        title="Sales by Category",
        color="Category"
    )

    st.plotly_chart(fig, use_container_width=True) # display chart
    #  monthly sale trend
    st.subheader("📅 Monthly Sales Trend")
    import calendar
    monthly_sales = (
        filtered_df.groupby("Order Month")["Sales"]
        .sum()
        .reset_index()
    )
# Convert month numbers to month names
    monthly_sales["Month"] = monthly_sales["Order Month"].apply(lambda x: calendar.month_abbr[x])

    import plotly.express as px

    fig = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        title="Monthly Sales Trend",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Sales"
    )

    st.plotly_chart(fig, use_container_width=True)
    #............ profit analysis........
elif selected == "Profit Analysis":

# profit by category
    st.subheader("📈 Profit Analysis by Category")
    import plotly.express as px
    category_profit=(
        filtered_df.groupby("Category")["Profit"].sum().reset_index()
    )
    fig=px.bar(
        category_profit,
        x="Category",
        y="Profit",
        title="Profit by Category",
        color="Category"
    )
    st.plotly_chart(fig,use_container_width=True)

# profit distribution by region
    st.subheader("💰 Profit Distribution by Region")
    import plotly.express as px

    region_profit = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_profit,
        names="Region",
        values="Profit",
        hole=0.35,                 # Makes it a donut chart
        title="Profit by Region"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
    )

    fig.update_layout(
        legend_title="Region",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
# #  monthly sale trend
#     st.subheader("📅 Monthly Sales Trend")
#     import calendar
#     monthly_sales = (
#         filtered_df.groupby("Order Month")["Sales"]
#         .sum()
#         .reset_index()
#     )
# # Convert month numbers to month names
#     monthly_sales["Month"] = monthly_sales["Order Month"].apply(lambda x: calendar.month_abbr[x])

#     import plotly.express as px

#     fig = px.line(
#         monthly_sales,
#         x="Month",
#         y="Sales",
#         title="Monthly Sales Trend",
#         markers=True
#     )

#     fig.update_layout(
#         xaxis_title="Month",
#         yaxis_title="Total Sales"
#     )

#     st.plotly_chart(fig, use_container_width=True)

# profit distribution
    st.subheader("📈 Profit Distribution")

    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(8,5))

    sns.histplot(filtered_df["Profit"], kde=True, ax=ax)

    ax.set_title("Distribution of Profit")
    ax.set_xlabel("Profit")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)
# ..........loss analysis..........
elif selected == "Loss Analysis":
# profit vs loss
    st.subheader("📊 Order Profit Status")

    import plotly.express as px

    summary = filtered_df.copy()

    summary["Status"] = summary["Profit"].apply(
        lambda x: "Profit" if x > 0 else ("Loss" if x < 0 else "Break-even")
    )

    status_count = (
        summary["Status"]
        .value_counts()
        .reset_index()
    )

    status_count.columns = ["Status", "Orders"]

    fig = px.pie(
        status_count,
        values="Orders",
        names="Status",
        title="Profit vs Loss Orders"
    )

    st.plotly_chart(fig, use_container_width=True)
# calculate loss order
    import pandas as pd
    st.subheader("📉Distribution of Loss Orders Across Profit Ranges")
# Only loss orders
    loss_df = filtered_df[filtered_df["Profit"] < 0].copy()

# Define ranges
    bins = [-float("inf"), -100, -50, -10, 0]
    labels = ["<-100", "-100 to -50", "-50 to -10", "-10 to 0"]

    loss_df["Loss Range"] = pd.cut(
        loss_df["Profit"],
        bins=bins,
        labels=labels
    )

# Count orders in each range
    loss_summary = (
        loss_df["Loss Range"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    loss_summary.columns = ["Loss Range", "Orders"]

    st.dataframe(loss_summary)
    import plotly.express as px

    fig = px.bar(
        loss_summary,
        x="Loss Range",
        y="Orders",
        color="Orders",
        title="Loss Orders by Profit Range"
    )

    st.plotly_chart(fig, use_container_width=True)

# loss order by category
    st.subheader("📊 Loss Orders by Category")
    loss_df = filtered_df[filtered_df["Profit"] < 0]

    loss_category = (
        loss_df.groupby("Category")
        .size()
        .reset_index(name="Loss Orders")
    )
    import plotly.express as px

    fig = px.bar(
        loss_category,
        x="Category",
        y="Loss Orders",
        color="Loss Orders",
        title="Loss Orders by Category",
        text="Loss Orders"
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)
# loss order by subcategory
    st.subheader("📊 Loss Orders by Sub-Category")
    loss_df=filtered_df[filtered_df["Profit"] < 0]
    loss_subcategory=(
        loss_df.groupby("Sub-Category")
        .size()
        .reset_index(name="Loss Orders")
    )
    import plotly.express as px
    fig=px.bar(
        loss_subcategory,
        x="Sub-Category",
        y="Loss Orders",
        color="Loss Orders",
        text="Loss Orders"
    )
    st.plotly_chart(fig, use_container_width=True)
# which state has more loss
    st.subheader("📉 Loss Amount by State")

    loss_df = filtered_df[filtered_df["Profit"] < 0]

    loss_state = (
        loss_df.groupby("State")["Profit"]
        .sum()
        .reset_index()
    )

# Convert negative values to positive for visualization
    loss_state["Loss Amount"] = loss_state["Profit"].abs()

    import plotly.express as px

    fig = px.bar(
        loss_state.sort_values("Loss Amount", ascending=False),
        x="State",
        y="Loss Amount",
        color="Loss Amount",
        
        title="Loss Amount by State"
    )

    st.plotly_chart(fig, use_container_width=True)

    
# Discount analysis
elif selected == "Discount Analysis":
    st.subheader("💸 Average Profit by Discount")

    discount_profit = (
        filtered_df.groupby("Discount")["Profit"]
        .mean()
        .reset_index()
    )

    st.dataframe(discount_profit)
    import plotly.express as px

    fig = px.line(
        discount_profit,
        x="Discount",
        y="Profit",
        markers=True,
        title="Average Profit by Discount"
    )

    fig.update_layout(
        xaxis_title="Discount",
        yaxis_title="Average Profit"
    )

    st.plotly_chart(fig, use_container_width=True)
      # Discount vs Profit

    # Average Discount

    # Profit by Discount Range

elif selected == "ML Prediction":
    st.subheader("🤖 ML Prediction")
    st.write("Enter the order details below to predict the expected profit.")
    

    # make function



    def predict_profit(
        sales,
        quantity,
        discount,
        postal_code,
        order_date,
        ship_date,
        segment,
        category,
        sub_category,
        ship_mode,
        region
    ):
        
# -----------------------------
# Create new order
# -----------------------------
        new_order = pd.DataFrame({
            "Order Date": [order_date],
            "Ship Date": [ship_date],
            "Postal Code": [postal_code],
            "Sales": [sales],
            "Quantity": [quantity],
            "Discount": [discount],
            "Segment": [segment],
            "Category": [category],
            "Sub-Category": [sub_category],
            "Ship Mode": [ship_mode],
            "Region": [region]
        })

# -----------------------------
# Feature Engineering
# -----------------------------
        new_order["Order Date"] = pd.to_datetime(new_order["Order Date"])
        new_order["Ship Date"] = pd.to_datetime(new_order["Ship Date"])

        new_order["Order Year"] = new_order["Order Date"].dt.year
        new_order["Order Month"] = new_order["Order Date"].dt.month
        new_order["Order Day"] = new_order["Order Date"].dt.day

        new_order["Shipping_Days"] = (
            new_order["Ship Date"] - new_order["Order Date"]
        ).dt.days

        new_order["Sales_Per_Item"] = (
            new_order["Sales"] / new_order["Quantity"]
        )

        new_order["Discount_Amount"] = (
            new_order["Sales"] * new_order["Discount"]
        )

        new_order["Order Weekday"] = (
            new_order["Order Date"].dt.day_name()
        )

# -----------------------------
# One Hot Encoding
# -----------------------------
        new_order = pd.get_dummies(
            new_order,
            columns=[
            "Segment",
            "Category",
            "Sub-Category",
            "Ship Mode",
            "Region",
            "Order Weekday"
        ],
        drop_first=True
        )

# -----------------------------
# Remove unused columns
# -----------------------------
        new_order = new_order.drop(
            columns=["Order Date", "Ship Date"],
            errors="ignore"
        )

# -----------------------------
# Match training columns
# -----------------------------
        new_order = new_order.reindex(
            columns=training_columns, # conatain X-train which we use in colab to train model now we replacwe with training_columns
            fill_value=0
        )

# -----------------------------
# Predict
# -----------------------------
        prediction = randomforest_model.predict(new_order)[0]

# print("Predicted Profit:", prediction)
        st.success(f"Predicted Profit: ${prediction:.2f}")

        if prediction > 0:
    # print("Expected Result: Profit ✅")
            st.success("✅ Expected Result: Profit")
        elif prediction < 0:
    # print("Expected Result: Loss ❌")
            st.error("❌ Expected Result: Loss")
        else:
    # print("Expected Result: Break Even")
            st.info("⚖️ Expected Result: Break Even")

        return prediction
    sales = st.number_input(
        "Sales ($)",
        min_value=0.0,
        value=500.0
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=5
    )

    discount = st.number_input(
        "Discount",
        min_value=0.0,
        max_value=0.8,
        value=0.2
    )

    postal_code = st.number_input(
        "Postal Code",
        value=141401
    )


    order_date = st.date_input(
        "Order Date"
    )

    ship_date = st.date_input(
        "Ship Date"
    )


    segment = st.selectbox(
        "Segment",
        ["Consumer", "Corporate", "Home Office"]
    )

    category = st.selectbox(
        "Category",
        ["Furniture", "Office Supplies", "Technology"]
    )


    sub_category = st.selectbox(
        "Sub-Category",
        [
            "Chairs",
            "Tables",
            "Phones",
            "Storage",
            "Binders",
            "Paper"
        ]
    )


    ship_mode = st.selectbox(
        "Ship Mode",
        [
            "Standard Class",
            "Second Class",
            "First Class",
            "Same Day"
        ]
    )


    region = st.selectbox(
        "Region",
        [
            "Central",
            "East",
            "South",
            "West"
        ]
    )


    if st.button("Predict Profit"):

        predict_profit(
            sales,
            quantity,
            discount,
            postal_code,
            order_date,
            ship_date,
            segment,
            category,
            sub_category,
            ship_mode,
            region
        )
