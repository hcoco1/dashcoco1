import pandas as pd
import numpy as np
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
"""

# Create the initial DataFrame with the provided data
data = [
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "K", 8, 15, 7, 14, 10, 11, 19, 5, 9, 2, 18, 14, 6, 8, 13, 10, 12, 11, 4, 17, 9, 20, 18, 12, 15, 3, 7],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "1st", 10, 12, 8, 16, 11, 13, 17, 4, 8, 1, 20, 15, 7, 9, 12, 11, 13, 10, 5, 18, 8, 19, 17, 11, 14, 2, 6],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "2nd", 9, 14, 6, 15, 12, 10, 18, 7, 6, 3, 19, 17, 8, 10, 13, 9, 11, 12, 6, 16, 9, 18, 15, 13, 11, 4, 5],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "3rd", 11, 13, 9, 17, 10, 14, 16, 5, 7, 2, 18, 16, 9, 8, 12, 10, 14, 11, 7, 15, 10, 19, 14, 12, 13, 3, 8],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "4th", 12, 10, 8, 18, 13, 11, 19, 6, 10, 4, 17, 15, 7, 9, 11, 13, 12, 10, 6, 16, 11, 20, 16, 14, 15, 5, 4],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "5th", 8, 15, 7, 14, 10, 11, 19, 5, 9, 2, 18, 14, 6, 8, 13, 10, 12, 11, 4, 17, 9, 20, 18, 12, 15, 3, 7],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "6th", 11, 20, 16, 9, 7, 19, 8, 12, 18, 13, 6, 3, 17, 15, 14, 5, 10, 2, 4, 19, 17, 20, 18, 12, 15, 3, 7],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "7th", 12, 8, 11, 17, 5, 6, 19, 10, 9, 15, 20, 14, 13, 7, 8, 6, 2, 18, 12, 10, 7, 16, 5, 14, 3, 12, 5],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "8th", 14, 17, 10, 19, 8, 9, 16, 11, 14, 18, 7, 6, 12, 13, 15, 20, 3, 9, 11, 10, 13, 7, 16, 8, 4, 5, 19],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "9th", 9, 12, 6, 8, 14, 7, 16, 19, 11, 5, 13, 18, 20, 3, 9, 12, 11, 8, 15, 10, 14, 2, 4, 7, 10, 16, 15],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "10th", 10, 13, 15, 8, 12, 14, 16, 7, 10, 5, 9, 14, 17, 6, 11, 13, 9, 18, 15, 12, 6, 10, 14, 13, 8, 17, 9],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "11th", 11, 14, 16, 9, 13, 15, 17, 8, 11, 6, 10, 15, 18, 7, 12, 14, 10, 19, 16, 13, 7, 11, 15, 14, 9, 18, 10],
    ["John Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/john_doe.jpg?raw=true", "12th", 15, 19, 12, 18, 16, 14, 20, 9, 13, 6, 17, 16, 11, 10, 18, 14, 13, 15, 8, 17, 10, 20, 19, 13, 15, 7, 12],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "K", 13, 6, 18, 12, 15, 10, 9, 7, 14, 19, 11, 16, 5, 8, 20, 18, 12, 15, 10, 13, 3, 2, 6, 11, 17, 9, 14],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "1st", 12, 15, 17, 10, 14, 16, 18, 9, 12, 7, 11, 16, 19, 8, 13, 15, 11, 20, 17, 14, 8, 12, 16, 15, 10, 19, 11],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "2nd", 11, 14, 16, 9, 13, 15, 17, 8, 11, 6, 10, 15, 18, 7, 12, 14, 10, 19, 16, 13, 7, 11, 15, 14, 9, 18, 10],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "3rd", 10, 13, 15, 8, 12, 14, 16, 7, 10, 5, 9, 14, 17, 6, 11, 13, 9, 18, 15, 12, 6, 10, 14, 13, 8, 17, 9],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "4th", 9, 12, 6, 8, 14, 7, 16, 19, 11, 5, 13, 18, 20, 3, 9, 12, 11, 8, 15, 10, 14, 2, 4, 7, 10, 16, 15],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "5th", 13, 6, 18, 12, 15, 10, 9, 7, 14, 19, 11, 16, 5, 8, 20, 18, 12, 15, 10, 13, 3, 2, 6, 11, 17, 9, 14],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "6th", 14, 17, 10, 19, 8, 9, 16, 11, 14, 18, 7, 6, 12, 13, 15, 20, 3, 9, 11, 10, 13, 7, 16, 8, 4, 5, 19],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "7th", 9, 12, 6, 8, 14, 7, 16, 19, 11, 5, 13, 18, 20, 3, 9, 12, 11, 8, 15, 10, 14, 2, 4, 7, 10, 16, 15],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "8th", 10, 13, 15, 8, 12, 14, 16, 7, 10, 5, 9, 14, 17, 6, 11, 13, 9, 18, 15, 12, 6, 10, 14, 13, 8, 17, 9],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "9th", 11, 14, 16, 9, 13, 15, 17, 8, 11, 6, 10, 15, 18, 7, 12, 14, 10, 19, 16, 13, 7, 11, 15, 14, 9, 18, 10],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "10th", 12, 15, 17, 10, 14, 16, 18, 9, 12, 7, 11, 16, 19, 8, 13, 15, 11, 20, 17, 14, 8, 12, 16, 15, 10, 19, 11],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "11th", 13, 6, 18, 12, 15, 10, 9, 7, 14, 19, 11, 16, 5, 8, 20, 18, 12, 15, 10, 13, 3, 2, 6, 11, 17, 9, 14],
    ["Jane Doe", "https://github.com/hcoco1/dashcoco1/blob/main/data/jane_doe.jpg?raw=true", "12th", 14, 17, 10, 19, 8, 9, 16, 11, 14, 18, 7, 6, 12, 13, 15, 20, 3, 9, 11, 10, 13, 7, 16, 8, 4, 5, 19]
]


# Create DataFrame from data
columns = ["Name", "Image URL", "Year", "Matematicas Exam 1", "Matematicas Exam 2", "Matematicas Exam 3",
           "Literatura Exam 1", "Literatura Exam 2", "Literatura Exam 3", "English Exam 1", "English Exam 2", "English Exam 3",
           "Deporte Exam 1", "Deporte Exam 2", "Deporte Exam 3", "Geography Exam 1", "Geography Exam 2", "Geography Exam 3",
           "Art Exam 1", "Art Exam 2", "Art Exam 3", "Biologia Exam 1", "Biologia Exam 2", "Biologia Exam 3",
           "Orientacion Exam 1", "Orientacion Exam 2", "Orientacion Exam 3", "Participacion Exam 1", "Participacion Exam 2", "Participacion Exam 3"]

 df = pd.DataFrame(data, columns=columns) """
 
df = pd.read_csv('https://raw.githubusercontent.com/hcoco1/dashcoco1/main/data/grades_over_time%20.csv')
""" df = pd.read_csv('grades_over_time.csv')  """

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set the secret key for session management
server.secret_key = secret_key

# Set up basic authentication
auth = dash_auth.BasicAuth(app, {auth_username: auth_password})

# Specify custom favicon and custom title
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>My Dashboard</title>
        <link rel="icon" href="/assets/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# List of all possible years/grades
all_years = ["K", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"]

# Function to fill missing years with placeholder data
def fill_missing_years(df, all_years):
    students = df["Name"].unique()
    placeholder_data = []
    for student in students:
        student_data = df[df["Name"] == student]
        existing_years = student_data["Year"].tolist()
        for year in all_years:
            if year not in existing_years:
                placeholder_data.append([student, student_data["Image URL"].iloc[0], year] + [np.nan]*27)
    placeholder_df = pd.DataFrame(placeholder_data, columns=df.columns)
    return pd.concat([df, placeholder_df], ignore_index=True).sort_values(by=["Name", "Year"])

# Fill missing years
df = fill_missing_years(df, all_years)

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
