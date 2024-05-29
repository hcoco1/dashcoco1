import pandas as pd
from dash import Dash, Input, Output, dash_table, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_auth

# Load the new dataset
df = pd.read_csv('https://raw.githubusercontent.com/hcoco1/Dashboard-Plothy-Dash/main/hcoco1/src/data/grades_over_time.csv')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set the secret key for session management
server.secret_key = 'supersecretkey'  # Replace with a strong secret key

# Set up basic authentication
auth = dash_auth.BasicAuth(app, {'bugsbunny': 'topsecret'})

# Ensure grades are numeric
for col in df.columns[3:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Calculate final grades by averaging sublevels
subjects = ["Matematicas", "Literatura", "English", "Deporte", "Geography", "Art", "Biologia", "Orientacion", "Participacion"]
for subject in subjects:
    df[f"{subject}"] = df[
        [f"{subject} Exam 1", f"{subject} Exam 2", f"{subject} Exam 3"]
    ].mean(axis=1).round(0)

# Calculate the final grade average across all subjects
df["Grade Average"] = df[[f"{subject}" for subject in subjects]].mean(axis=1).round(0)

# Prepare the summary table with only final grades
summary_df = df[
    ["Name", "Image URL", "Year"]
    + [f"{subject}" for subject in subjects]
    + ["Grade Average"]
]

# Ensure all final grades have no more than two decimal places
summary_df = summary_df.round(0)

# Layout of the app
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Estudiante"),
                        dcc.Dropdown(
                            id="student-dropdown",
                            options=[
                                {"label": name, "value": name}
                                for name in df["Name"].unique()
                            ],
                            value=df["Name"].unique()[0],
                            clearable=False,
                            style={"width": "200px"}
                        ),
                    ],
                    width=2,
                    style={"margin-bottom": "10px", "margin-right":"10px"},
                    className="mt-4"
                ),
                dbc.Col(
                    [
                        html.H5("Grado"),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[
                                {"label": year, "value": year}
                                for year in df["Year"].unique()
                            ],
                            value=df["Year"].unique()[0],
                            clearable=False,
                            style={"width": "200px"}
                        ),
                    ],
                    width=2,
                    style={"margin-bottom": "10px", "margin-right":"10px"},
                    className="mt-4"
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.Img(
                                                    id="student-image",
                                                    style={
                                                        "width": "150px",
                                                        "height": "150px",
                                                        "display": "block",
                                                        "margin-top": "10px",
                                                    },
                                                    className="mt-4"
                                                ),
                                                html.H4(
                                                    id="average-grade",
                                                    className="card-title",
                                                    style={"textAlign": "center"},
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "flexDirection": "column",
                                                "alignItems": "center",
                                            },
                                        )
                                    ]
                                )
                            ],
                            style={
                                "width": "200px",
                                "height": "200px",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                            },
                        )
                    ],
                    width=2,
                    style={"marginLeft": "auto", "border": "none"},
                    className="mt-4"
                ),
            ],
            className="align-items-start",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dash_table.DataTable(
                        id="summary-table",
                        columns=[
                            {"name": "Nombre", "id": "Name"},
                            {"name": "Grado", "id": "Year"},
                            {"name": "Matematicas", "id": "Matematicas"},
                            {"name": "Literatura", "id": "Literatura"},
                            {"name": "English", "id": "English"},
                            {"name": "Deporte", "id": "Deporte"},
                            {"name": "Geografia", "id": "Geography"},
                            {"name": "Arte", "id": "Art"},
                            {"name": "Biologia", "id": "Biologia"},
                            {"name": "Orientacion", "id": "Orientacion"},
                            {"name": "Participacion", "id": "Participacion"},
                            {"name": "Final Grado", "id": "Grade Average"},
                        ],
                        style_table={"overflowX": "auto"},
                        style_header={
                            "backgroundColor": "rgb(230, 230, 230)",
                            "fontWeight": "bold",
                        },
                        style_cell={"textAlign": "center"},
                    ),
                    width=12,
                    className="mb-4 mt-4",
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="subject-performance-chart"), width=12),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Materia"),
                        dcc.Dropdown(
                            id="subject-dropdown",
                            options=[
                                {"label": subject, "value": subject} for subject in subjects
                            ],
                            value=subjects[0],
                            clearable=False,
                            style={"width": "200px"}
                        ),
                    ],
                    width=2,
                )
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dash_table.DataTable(
                        id="exam-table",
                        columns=[
                            {"name": "Nombre", "id": "Name"},
                            {"name": "Grado", "id": "Year"},
                            {"name": "Lapso 1", "id": "Exam 1"},
                            {"name": "Lapso 2", "id": "Exam 2"},
                            {"name": "Lapso 3", "id": "Exam 3"},
                        ],
                        style_table={"overflowX": "auto"},
                        style_header={
                            "backgroundColor": "rgb(230, 230, 230)",
                            "fontWeight": "bold",
                        },
                        style_cell={"textAlign": "center"},
                    ),
                    width=12,
                    className="mb-4",
                )
            ]
        ),
        dbc.Row([dbc.Col(dcc.Graph(id="performance-over-time"), width=12)]),
    ],
    fluid=True,
    style={"max-width": "1200px"},
)

# Callback to update the summary table
@app.callback(
    Output("summary-table", "data"),
    [Input("student-dropdown", "value"), Input("year-dropdown", "value")],
)
def update_summary_table(selected_student, selected_year):
    filtered_summary_df = summary_df[
        (summary_df["Name"] == selected_student) & (summary_df["Year"] == selected_year)
    ]
    return filtered_summary_df.to_dict("records")

# Callback to update the average grade card and student image
@app.callback(
    [Output("average-grade", "children"), Output("student-image", "src")],
    [Input("student-dropdown", "value")],
)
def update_average_grade_and_image(selected_student):
    student_df = summary_df[summary_df["Name"] == selected_student]
    average_grade = student_df["Grade Average"].mean().round(0)
    image_url = student_df["Image URL"].values[0]  # Get the image URL for the student
    return f" Promedio:{int(average_grade)}", image_url

# Callback to update the exam table
@app.callback(
    Output("exam-table", "data"),
    [
        Input("student-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("subject-dropdown", "value"),
    ],
)
def update_exam_table(selected_student, selected_year, selected_subject):
    filtered_df = df[(df["Name"] == selected_student) & (df["Year"] == selected_year)]
    exam_df = filtered_df[
        [
            "Name",
            "Year",
            f"{selected_subject} Exam 1",
            f"{selected_subject} Exam 2",
            f"{selected_subject} Exam 3",
        ]
    ]
    exam_df = exam_df.rename(
        columns={
            f"{selected_subject} Exam 1": "Exam 1",
            f"{selected_subject} Exam 2": "Exam 2",
            f"{selected_subject} Exam 3": "Exam 3",
        }
    )
    return exam_df.to_dict("records")

# Callback to update the performance over time line chart
@app.callback(
    Output("performance-over-time", "figure"),
    [
        Input("student-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("subject-dropdown", "value"),
    ],
)
def update_performance_chart(selected_student, selected_year, selected_subject):
    filtered_df = df[(df["Name"] == selected_student) & (df["Year"] == selected_year)]
    exam_grades = filtered_df[
        [
            f"{selected_subject} Exam 1",
            f"{selected_subject} Exam 2",
            f"{selected_subject} Exam 3",
        ]
    ].values.flatten()
    exams = ["Lapso 1", "Lapso 2", "Lapso 3"]
    chart_data = pd.DataFrame({"Lapso": exams, "Nota": exam_grades})
    fig = px.line(
        chart_data,
        x="Lapso",
        y="Nota",
        title=f"Notas por Lapso de {selected_student} en {selected_subject} ({selected_year})",
        markers=True,
        line_shape='spline',  # Smooth the lines
    )
    
    # Customize line color and style
    fig.update_traces(line=dict(color='black', width=4), marker=dict(symbol='x', size=10, color='red'))
    
    fig.add_shape(
        type="line",
        x0=0, x1=1, y0=10, y1=10,
        line=dict(color="Red", width=1, dash="dash"),
        xref="paper", yref="y"
    )
    
    fig.add_shape(
        type="line",
        x0=0, x1=1, y0=15, y1=15,
        line=dict(color="blue", width=1, dash="dash"),
        xref="paper", yref="y"
    )
        
    fig.add_shape(
        type="line",
        x0=0, x1=1, y0=18, y1=18,
        line=dict(color="green", width=1, dash="dash"),
        xref="paper", yref="y"
    )
    
    fig.update_layout(xaxis_title="Lapso", yaxis_title="Nota")
    
    return fig

# Callback to update the subject performance bar chart
@app.callback(
    Output("subject-performance-chart", "figure"),
    [Input("student-dropdown", "value"), Input("year-dropdown", "value")],
)
def update_subject_performance_chart(selected_student, selected_year):
    filtered_df = summary_df[
        (summary_df["Name"] == selected_student) & (summary_df["Year"] == selected_year)
    ]
    chart_data = filtered_df.melt(
        id_vars=["Name", "Year"],
        value_vars=[f"{subject}" for subject in subjects],
        var_name="Subject",
        value_name="Grade",
    )
    chart_data["Subject"] = chart_data["Subject"].str.replace(" ", "")
    fig = px.bar(
        chart_data,
        x="Subject",
        y="Grade",
        title=f"Calificaciones de {selected_student} en {selected_year}",
        color="Subject",
    )
    fig.update_layout(xaxis_title="Subject", yaxis_title="Grade")
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
