import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

# Load the dataset
df = pd.read_csv("Students_Grading_Dataset_Biased.csv")

# Aggregate attendance by department
attendance_by_dept = df.groupby("Department")["Attendance (%)"].mean().reset_index()

# Gender counts
gender_counts = df["Gender"].value_counts()

# Define Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Student Performance Dashboard"),
    dcc.Graph(
        id="attendance-graph",
        figure=px.bar(attendance_by_dept, x="Department", y="Attendance (%)", title="Average Attendance by Department")
    ),
    dcc.Graph(
        id="gender-pie-chart",
        figure=px.pie(names=gender_counts.index, values=gender_counts.values, title="Gender Distribution")
    )
])

if __name__ == "__main__":
    app.run(debug=True)