"""Generate a recruiter-friendly Excel analytics workbook from the source CSV."""
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_mobile_money_transaction_dataset.csv"
OUTPUT_PATH = ROOT / "excel" / "Financial_Transaction_Fraud_Analytics.xlsx"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset missing: {DATA_PATH}. See data/README.md."
    )

df = pd.read_csv(DATA_PATH)
required = {"step", "transactionType", "amount", "isFraud"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

df["isFraud"] = pd.to_numeric(df["isFraud"], errors="coerce").fillna(0).astype(int)
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
transfers = df[df["transactionType"].eq("TRANSFER")].copy()

type_summary = (
    df.groupby("transactionType")
      .agg(Transactions=("isFraud", "size"),
           Fraud_Label_Count=("isFraud", "sum"),
           Average_Amount=("amount", "mean"),
           Median_Amount=("amount", "median"))
      .reset_index()
)
type_summary["Fraud_Label_Rate_%"] = (
    type_summary["Fraud_Label_Count"] / type_summary["Transactions"] * 100
)

step_summary = (
    transfers.groupby("step")
    .agg(Transactions=("isFraud", "size"), Fraud_Label_Count=("isFraud", "sum"))
    .reset_index()
)
step_summary["Fraud_Label_Rate_%"] = (
    step_summary["Fraud_Label_Count"] / step_summary["Transactions"] * 100
)

bins = [-float("inf"), 1000, 10000, 50000, 100000, float("inf")]
labels = ["< 1K", "1K–10K", "10K–50K", "50K–100K", "100K+"]
transfers["Amount_Band"] = pd.cut(transfers["amount"], bins=bins, labels=labels)
amount_summary = (
    transfers.groupby("Amount_Band", observed=False)
    .agg(Transactions=("isFraud", "size"),
         Fraud_Label_Count=("isFraud", "sum"),
         Average_Amount=("amount", "mean"))
    .reset_index()
)
amount_summary["Fraud_Label_Rate_%"] = (
    amount_summary["Fraud_Label_Count"] / amount_summary["Transactions"] * 100
)

wb = Workbook()
overview = wb.active
overview.title = "Executive Summary"
for ws in list(wb.worksheets):
    ws.sheet_view.showGridLines = False

navy = "17365D"
blue = "1F4E78"
light_blue = "D9EAF7"
pale = "F3F6FA"
white = "FFFFFF"
green = "E2F0D9"
thin_gray = Side(style="thin", color="D9E1F2")

def title(ws, text, subtitle=None):
    ws["A1"] = text
    ws["A1"].font = Font(name="Aptos Display", size=18, bold=True, color=white)
    ws["A1"].fill = PatternFill("solid", fgColor=navy)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=6)
    ws.row_dimensions[1].height = 32
    if subtitle:
        ws["A2"] = subtitle
        ws["A2"].font = Font(italic=True, color="666666")
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=6)

def write_df(ws, frame, start_row=4, start_col=1):
    for j, col in enumerate(frame.columns, start_col):
        cell = ws.cell(start_row, j, str(col).replace("_", " "))
        cell.font = Font(bold=True, color=white)
        cell.fill = PatternFill("solid", fgColor=blue)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    for i, row in enumerate(frame.itertuples(index=False, name=None), start_row + 1):
        for j, value in enumerate(row, start_col):
            if pd.isna(value):
                value = None
            elif hasattr(value, "item"):
                value = value.item()
            cell = ws.cell(i, j, value)
            cell.fill = PatternFill("solid", fgColor=white if i % 2 else pale)
            cell.border = Border(bottom=thin_gray)
            if isinstance(value, float):
                cell.number_format = "#,##0.00"
    ws.freeze_panes = f"A{start_row+1}"
    ws.auto_filter.ref = f"{get_column_letter(start_col)}{start_row}:{get_column_letter(start_col+len(frame.columns)-1)}{start_row+len(frame)}"
    for j, col in enumerate(frame.columns, start_col):
        values = [len(str(col))] + [len(str(v)) for v in frame[col].head(200) if pd.notna(v)]
        ws.column_dimensions[get_column_letter(j)].width = min(max(max(values) + 3, 14), 30)

title(overview, "FINANCIAL TRANSACTION FRAUD ANALYTICS",
      "Excel business analysis | Synthetic mobile-money dataset | Retrospective investigation")
total = int(len(df))
fraud = int(df["isFraud"].sum())
transfer_total = int(len(transfers))
transfer_fraud = int(transfers["isFraud"].sum())
kpis = [
    ("Total transactions", total),
    ("Fraud-labelled transactions", fraud),
    ("Overall label rate (%)", fraud / total * 100 if total else 0),
    ("Transfer transactions", transfer_total),
    ("Fraud-labelled transfers", transfer_fraud),
    ("Transfer label rate (%)", transfer_fraud / transfer_total * 100 if transfer_total else 0)
]
for idx, (label, value) in enumerate(kpis):
    r = 4 + (idx // 2) * 3
    c = 1 + (idx % 2) * 3
    overview.cell(r, c, label).font = Font(bold=True, color=blue)
    overview.cell(r+1, c, value).font = Font(size=16, bold=True, color=navy)
    overview.cell(r+1, c).fill = PatternFill("solid", fgColor=light_blue)
    overview.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c+1)
    overview.merge_cells(start_row=r+1, start_column=c, end_row=r+1, end_column=c+1)
    overview.cell(r+1, c).number_format = "#,##0.00" if "%" in label else "#,##0"

overview["A14"] = "Interpretation guardrails"
overview["A14"].font = Font(bold=True, color=white)
overview["A14"].fill = PatternFill("solid", fgColor=blue)
overview.merge_cells("A14:F14")
notes = [
    "All fraud rates are rates of dataset labels in a synthetic sample, not real-world fraud probabilities.",
    "All fraud-labelled rows in this supplied dataset are TRANSFER records; do not generalise this to other payment systems.",
    "Balance mismatch measures based on new balances are retrospective and may not be available at authorisation time.",
    "The existing classifier has weak test performance and is not suitable for operational decisions."
]
for r, note in enumerate(notes, 15):
    overview.cell(r, 1, "• " + note)
    overview.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    overview.cell(r, 1).alignment = Alignment(wrap_text=True)
    overview.row_dimensions[r].height = 30
overview.column_dimensions["A"].width = 25
overview.column_dimensions["B"].width = 20
overview.column_dimensions["C"].width = 18
overview.column_dimensions["D"].width = 20
overview.column_dimensions["E"].width = 18
overview.column_dimensions["F"].width = 18

ws = wb.create_sheet("Transaction Type")
title(ws, "TRANSACTION TYPE ANALYSIS", "Compare transaction volumes, label counts and average/median values.")
write_df(ws, type_summary, 4)
chart = BarChart()
chart.title = "Fraud-label rate by transaction type"
chart.y_axis.title = "Label rate (%)"
chart.x_axis.title = "Transaction type"
chart.add_data(Reference(ws, min_col=6, min_row=4, max_row=4+len(type_summary)), titles_from_data=True)
chart.set_categories(Reference(ws, min_col=1, min_row=5, max_row=4+len(type_summary)))
chart.height, chart.width = 8, 15
ws.add_chart(chart, "H4")

ws = wb.create_sheet("Step Trends")
title(ws, "TRANSFER LABEL TRENDS", "Fraud-label rates by simulation step; descriptive, not causal.")
write_df(ws, step_summary, 4)
chart = LineChart()
chart.title = "Fraud-label rate over simulation steps"
chart.y_axis.title = "Label rate (%)"
chart.x_axis.title = "Simulation step"
chart.add_data(Reference(ws, min_col=4, min_row=4, max_row=4+len(step_summary)), titles_from_data=True)
chart.set_categories(Reference(ws, min_col=1, min_row=5, max_row=4+len(step_summary)))
chart.height, chart.width = 9, 18
ws.add_chart(chart, "F4")

ws = wb.create_sheet("Amount Bands")
title(ws, "TRANSFER AMOUNT SEGMENTATION", "Amount bands and observed fraud-label rates.")
write_df(ws, amount_summary, 4)
ws.conditional_formatting.add(
    f"E5:E{4+len(amount_summary)}",
    ColorScaleRule(start_type="min", start_color="F8696B",
                   mid_type="percentile", mid_value=50, mid_color="FFEB84",
                   end_type="max", end_color="63BE7B")
)

ws = wb.create_sheet("Data Dictionary")
title(ws, "DATA DICTIONARY & DEFINITIONS", "Definitions used in this workbook.")
dictionary = pd.DataFrame([
    ["step", "Simulation time step in the synthetic dataset."],
    ["transactionType", "Transaction category supplied in the source data."],
    ["amount", "Transaction amount in dataset units."],
    ["initiator", "Sender/account identifier; use carefully and avoid exposing personal data."],
    ["recipient", "Recipient/account identifier; use carefully and avoid exposing personal data."],
    ["isFraud", "Synthetic dataset fraud label (1 = labelled fraud, 0 = not labelled fraud)."],
    ["Fraud-label rate", "Fraud-labelled rows divided by total rows in the selected group."],
    ["Amount band", "Transfer amount grouped into fixed descriptive ranges."]
], columns=["Field / metric", "Definition"])
write_df(ws, dictionary, 4)

for ws in wb.worksheets:
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_view.zoomScale = 90

wb.save(OUTPUT_PATH)
print(f"Workbook created: {OUTPUT_PATH}")
print("Sheets:", ", ".join(wb.sheetnames))
print("Rows analysed:", total)
