import pandas as pd
from dash import Dash, Input, Output, dash_table, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_auth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the secret key and auth credentials from environment variables
secret_key = os.getenv('SECRET_KEY')
auth_username = os.getenv('AUTH_USERNAME')
auth_password = os.getenv('AUTH_PASSWORD')

# Ensure the secret key is loaded correctly
if not secret_key:
    raise ValueError("No SECRET_KEY set for Flask application. Did you follow the instructions to set up the .env file?")

# Ensure auth credentials are loaded correctly
if not auth_username or not auth_password:
    raise ValueError("Authentication credentials are not set properly in the .env file.")

# Load the new dataset
df = pd.read_csv('grades_over_time (1).csv')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set the secret key for session management
server.secret_key = secret_key

# Set up basic authentication
auth = dash_auth.BasicAuth(app, {auth_username: auth_password})

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

# Translation dictionary
translations = {
    'en': {
        'student': "Student",
        'grade': "Grade",
        'subject': "Subject",
        'exam1': "Exam 1",
        'exam2': "Exam 2",
        'exam3': "Exam 3",
        'average_grade': "Average",
        'title': "Track Your Kid's Academic Progress",
        'download_app': "Download the app now!",
        'student_selection': "Student",
        'grade_selection': "Grade",
        'performance_overview': "Performance Overview",
        'detailed_exam_performance': "Detailed Exam Performance",
        'performance_over_time': "Performance Over Time",
        'subject_performance_comparison': "Subject Performance Comparison",
        'how_it_works': "How It Works",
        'data_handling': "Data Handling",
        'authentication': "Authentication",
        'dynamic_content': "Dynamic Content",
        'interactive_charts': "Interactive Charts",
        'conclusion': "Conclusion",
        'of': "of",
        'in': "in",
        'grades': {
            'K': "Kindergarten",
            '1st': "1st",
            '2nd': "2nd",
            '3rd': "3rd",
            '4th': "4th",
            '5th': "5th",
            '6th': "6th",
            '7th': "7th",
            '8th': "8th",
            '9th': "9th",
            '10th': "10th",
            '11th': "11th",
            '12th': "12th"
        }
    },
    'es': {
        'student': "Estudiante",
        'grade': "Grado",
        'subject': "Materia",
        'exam1': "Lapso 1",
        'exam2': "Lapso 2",
        'exam3': "Lapso 3",
        'average_grade': "Promedio",
        'title': "Seguimiento del Progreso Académico de su Hijo",
        'download_app': "¡Descargue la aplicación ahora!",
        'student_selection': "Estudiante",
        'grade_selection': "Grado",
        'performance_overview': "Resumen de Desempeño",
        'detailed_exam_performance': "Desempeño Detallado en Exámenes",
        'performance_over_time': "Desempeño a lo Largo del Tiempo",
        'subject_performance_comparison': "Comparación de Desempeño por Materia",
        'how_it_works': "Cómo Funciona",
        'data_handling': "Manejo de Datos",
        'authentication': "Autenticación",
        'dynamic_content': "Contenido Dinámico",
        'interactive_charts': "Gráficos Interactivos",
        'conclusion': "Conclusión",
        'of': "de",
        'in': "en",
        'grades': {
            'K': "Kinder",
            '1st': "1ro",
            '2nd': "2do",
            '3rd': "3ro",
            '4th': "4to",
            '5th': "5to",
            '6th': "6to",
            '7th': "7mo",
            '8th': "8vo",
            '9th': "9no",
            '10th': "10mo",
            '11th': "11vo",
            '12th': "12vo"
        }
    }
}

def get_columns(language):
    translation = translations[language]
    columns = [
        {"name": translation['student'], "id": "Name"},
        {"name": translation['grade'], "id": "Year"},
        {"name": "Matemáticas" if language == 'es' else "Mathematics", "id": "Matematicas"},
        {"name": "Literatura" if language == 'es' else "Literature", "id": "Literatura"},
        {"name": "Inglés" if language == 'es' else "English", "id": "English"},
        {"name": "Deporte" if language == 'es' else "Sport", "id": "Deporte"},
        {"name": "Geografía" if language == 'es' else "Geography", "id": "Geography"},
        {"name": "Arte" if language == 'es' else "Art", "id": "Art"},
        {"name": "Biología" if language == 'es' else "Biology", "id": "Biologia"},
        {"name": "Orientación" if language == 'es' else "Guidance", "id": "Orientacion"},
        {"name": "Participación" if language == 'es' else "Participation", "id": "Participacion"},
        {"name": translation['average_grade'], "id": "Grade Average"},
    ]
    return columns

def get_exam_columns(language, subject):
    translation = translations[language]
    columns = [
        {"name": translation['student'], "id": "Name"},
        {"name": translation['grade'], "id": "Year"},
        {"name": translation['exam1'], "id": f"{subject} Exam 1"},
        {"name": translation['exam2'], "id": f"{subject} Exam 2"},
        {"name": translation['exam3'], "id": f"{subject} Exam 3"},
    ]
    return columns

# Initialize the Dash app layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id='language-dropdown',
                            options=[
                                {'label': 'English', 'value': 'en'},
                                {'label': 'Español', 'value': 'es'}
                            ],
                            value='en',
                            clearable=False,
                            style={"width": "200px"}
                        ),
                    ],
                    width=2,
                    className="mt-4"
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5(id='student-label'),
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
                        html.H5(id='grade-label'),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[
                                {"label": translations['en']['grades'][year], "value": year}
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
                                                "AlignItems": "center",
                                            },
                                        )
                                    ]
                                )
                            ],
                            style={
                                "width": "200px",
                                "height": "200px",
                                "display": "flex",
                                "AlignItems": "center",
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
                        columns=get_columns('en'),  # Initialize with default language
                        data=summary_df.to_dict('records'),  # Ensure initial data is provided
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
                        html.H5(id='subject-label'),
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
                        columns=get_exam_columns('en', subjects[0]),  # Initialize with default language and first subject
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

# Callback to update year dropdown based on the selected language
@app.callback(
    Output("year-dropdown", "options"),
    [Input("language-dropdown", "value")]
)
def update_year_dropdown(language):
    translation = translations[language]['grades']
    options = [{'label': translation[year], 'value': year} for year in translation.keys()]
    return options

# Callback to update labels and average grade card
@app.callback(
    [Output('student-label', 'children'),
     Output('grade-label', 'children'),
     Output('subject-label', 'children'),
     Output('summary-table', 'columns'),
     Output('average-grade', 'children'),
     Output('student-image', 'src')],
    [Input('language-dropdown', 'value'),
     Input('student-dropdown', 'value')]
)
def update_labels_and_card(language, selected_student):
    translation = translations[language]
    columns = get_columns(language)  # Dynamically get columns based on language
    
    student_df = summary_df[summary_df["Name"] == selected_student]
    average_grade = student_df["Grade Average"].mean().round(0)
    image_url = student_df["Image URL"].values[0]

    return (translation['student_selection'],
            translation['grade_selection'],
            translation['subject'],
            columns,
            f"{translation['average_grade']}: {int(average_grade)}",
            image_url)

@app.callback(
    Output("summary-table", "data"),
    [Input("student-dropdown", 'value'), Input("year-dropdown", 'value'), Input("language-dropdown", 'value')]
)
def update_summary_table(selected_student, selected_year, language):
    filtered_summary_df = summary_df[
        (summary_df["Name"] == selected_student) & (summary_df["Year"] == selected_year)
    ].copy()
    
    # Translate the selected year
    translation = translations[language]
    translated_year = translation['grades'][selected_year]
    
    # Replace the original year with the translated year in the filtered DataFrame
    filtered_summary_df["Year"] = translated_year
    
    return filtered_summary_df.to_dict("records")

# Callback to update the exam table
@app.callback(
    [Output("exam-table", "columns"),
     Output("exam-table", "data")],
    [Input("language-dropdown", "value"),
     Input("student-dropdown", "value"),
     Input("year-dropdown", "value"),
     Input("subject-dropdown", "value")]
)
def update_exam_table(language, selected_student, selected_year, selected_subject):
    columns = get_exam_columns(language, selected_subject)  # Dynamically get columns based on language and subject
    
    filtered_df = df[(df["Name"] == selected_student) & (df["Year"] == selected_year)]
    
    # Translate the selected year
    translation = translations[language]
    translated_year = translation['grades'][selected_year]
    
    # Replace the original year with the translated year in the filtered DataFrame
    exam_df = filtered_df.copy()
    exam_df["Year"] = translated_year
    
    return columns, exam_df.to_dict("records")

# Callback to update the performance over time line chart
@app.callback(
    Output("performance-over-time", "figure"),
    [
        Input("student-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("subject-dropdown", "value"),
        Input('language-dropdown', 'value')
    ],
)
def update_performance_chart(selected_student, selected_year, selected_subject, language):
    filtered_df = df[(df["Name"] == selected_student) & (df["Year"] == selected_year)]
    exam_grades = filtered_df[
        [
            f"{selected_subject} Exam 1",
            f"{selected_subject} Exam 2",
            f"{selected_subject} Exam 3",
        ]
    ].values.flatten()
    translation = translations[language]
    exams = [translation['exam1'], translation['exam2'], translation['exam3']]
    chart_data = pd.DataFrame({"Lapso": exams, "Nota": exam_grades})
    
    # Translate the selected year
    translated_year = translation['grades'][selected_year]
    
    fig = px.line(
        chart_data,
        x="Lapso",
        y="Nota",
        title=f"{translations[language]['performance_over_time']} {translations[language]['of']} {selected_student} {translations[language]['in']} {selected_subject} ({translated_year})",
        markers=True,
        line_shape='spline',  # Smooth the lines
    )
    
    return fig

# Callback to update the subject performance bar chart
@app.callback(
    Output("subject-performance-chart", "figure"),
    [Input("student-dropdown", "value"), Input("year-dropdown", "value"), Input('language-dropdown', 'value')],
)
def update_subject_performance_chart(selected_student, selected_year, language):
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
    translation = translations[language]

    # Translate the selected year
    translated_year = translation['grades'][selected_year]

    fig = px.bar(
        chart_data,
        x="Subject",
        y="Grade",
        title=f"{translation['subject_performance_comparison']} {translation['of']} {selected_student} {translation['in']} {translated_year} {translation['grade']}",
        color="Subject",
    )
    
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
