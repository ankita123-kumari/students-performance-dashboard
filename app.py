import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import dash.dependencies as dd

# Load dataset (Ensure your CSV file includes the given columns)
df = pd.read_csv("Students_Grading_Dataset_Biased.csv")

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Student Performance Dashboard", style={"textAlign": "center"}),

    # Summary Section
    html.Div([
        html.H3(f"Avg Attendance: {df['Attendance (%)'].mean():.2f}%"),
        html.H3(f"Avg Midterm Score: {df['Midterm_Score'].mean():.2f}"),
        html.H3(f"Avg Final Score: {df['Final_Score'].mean():.2f}"),
        html.H3(f"Avg Total Score: {df['Total_Score'].mean():.2f}"),
        html.H3(f"Avg Stress Level: {df['Stress_Level (1-10)'].mean():.2f}"),
        html.H3(f"Avg Sleep Hours: {df['Sleep_Hours_per_Night'].mean():.2f}")
    ], style={"display": "flex", "justify-content": "space-around"}),

    # Filters
    html.Div([
        html.Label("Select Department:"),
        dcc.Dropdown(id="department-filter", options=[{"label": d, "value": d} for d in df["Department"].unique()], value=df["Department"].unique()[0]),
        
        html.Label("Select Gender:"),
        dcc.Dropdown(id="gender-filter", options=[{"label": g, "value": g} for g in df["Gender"].unique()], value=df["Gender"].unique()[0]),
        
        html.Label("Select Study Hours per Week:"),
        dcc.Dropdown(id="study-hours-filter", options=[{"label": sh, "value": sh} for sh in df["Study_Hours_per_Week"].unique()], value=df["Study_Hours_per_Week"].unique()[0]),
        
        html.Label("Select Family Income Level:"),
        dcc.Dropdown(id="income-filter", options=[{"label": fi, "value": fi} for fi in df["Family_Income_Level"].unique()], value=df["Family_Income_Level"].unique()[0])
    ], style={"width": "60%", "margin": "auto"}),

    # Graphs
    dcc.Graph(id="attendance-chart"),
    dcc.Graph(id="gender-chart"),
    dcc.Graph(id="stress-sleep-chart"),
    dcc.Graph(id="total-score-chart"),
    dcc.Graph(id="internet-access-chart"),
])

# Callback for updating graphs based on filters
@app.callback(
    [dd.Output("attendance-chart", "figure"),
     dd.Output("gender-chart", "figure"),
     dd.Output("stress-sleep-chart", "figure"),
     dd.Output("total-score-chart", "figure"),
     dd.Output("internet-access-chart", "figure")],
    [dd.Input("department-filter", "value"),
     dd.Input("gender-filter", "value"),
     dd.Input("study-hours-filter", "value"),
     dd.Input("income-filter", "value")]
)
def update_graphs(selected_department, selected_gender, selected_study_hours, selected_income):
    filtered_df = df[(df["Department"] == selected_department) & 
                     (df["Gender"] == selected_gender) & 
                     (df["Study_Hours_per_Week"] == selected_study_hours) & 
                     (df["Family_Income_Level"] == selected_income)]

    # Attendance Bar Chart
    attendance_fig = px.bar(filtered_df, x="Department", y="Attendance (%)", title="Attendance by Department")

    # Gender Distribution Pie Chart
    gender_counts = filtered_df["Gender"].value_counts()
    gender_fig = px.pie(names=gender_counts.index, values=gender_counts.values, title="Gender Distribution")

    # Sleep vs. Stress Scatter Plot
    sleep_stress_fig = px.scatter(filtered_df, x="Sleep_Hours_per_Night", y="Stress_Level (1-10)", color="Gender", 
                                  title="Sleep vs. Stress Levels", size="Study_Hours_per_Week")

    # Total Score Bar Chart
    total_score_fig = px.bar(filtered_df, x="Department", y="Total_Score", title="Average Total Score by Department")

    # Internet Access Pie Chart
    internet_counts = filtered_df["Internet_Access_at_Home"].value_counts()
    internet_fig = px.pie(names=internet_counts.index, values=internet_counts.values, title="Internet Access Distribution")

    return attendance_fig, gender_fig, sleep_stress_fig, total_score_fig, internet_fig

if __name__ == "__main__":
   app.run(debug=True)