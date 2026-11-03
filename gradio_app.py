import gradio as gr
import pandas as pd

def analyze_business(file):
    if file is None:
        return "Please upload a CSV file.", None

    try:
        df = pd.read_csv(file)

        required_columns = ["Product", "Category", "Sales", "Expenses"]

        if not all(column in df.columns for column in required_columns):
            return (
                "CSV must contain Product, Category, Sales and Expenses columns.",
                None
            )

        df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
        df["Expenses"] = pd.to_numeric(df["Expenses"], errors="coerce")
        df = df.dropna(subset=["Sales", "Expenses"])

        if df.empty:
            return "No valid business records found.", None

        df["Profit"] = df["Sales"] - df["Expenses"]

        df["Profit_Margin"] = (
            df["Profit"] / df["Sales"].replace(0, pd.NA)
        ) * 100

        total_sales = df["Sales"].sum()
        total_expenses = df["Expenses"].sum()
        total_profit = df["Profit"].sum()

        overall_margin = (
            total_profit / total_sales * 100
            if total_sales != 0 else 0
        )

        best_product = df.loc[df["Profit"].idxmax()]

        summary = f"""
## DataMind AI Business Report

**Total Sales:** ₹{total_sales:,.2f}

**Total Expenses:** ₹{total_expenses:,.2f}

**Total Profit:** ₹{total_profit:,.2f}

**Overall Profit Margin:** {overall_margin:.2f}%

**Best Performing Product:** {best_product['Product']}

**Product Profit:** ₹{best_product['Profit']:,.2f}
"""

        return summary, df

    except Exception as error:
        return f"Analysis Error: {error}", None


with gr.Blocks(title="DataMind AI") as demo:

    gr.Markdown("# DataMind AI")
    gr.Markdown("AI-Powered Business Sales Analysis System")

    file_input = gr.File(
        label="Upload Business CSV",
        file_types=[".csv"],
        type="filepath"
    )

    analyze_button = gr.Button("Analyze Business Data")

    report_output = gr.Markdown(label="Business Report")

    table_output = gr.Dataframe(
        label="Detailed Business Analysis",
        interactive=False
    )

    analyze_button.click(
        fn=analyze_business,
        inputs=file_input,
        outputs=[report_output, table_output]
    )

if __name__ == "__main__":
    import os
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )


