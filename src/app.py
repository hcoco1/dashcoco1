# The following environment is selected: ~/dash-google/.venv/bin/python
import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

df = pd.read_csv('https://raw.githubusercontent.com/hcoco1/Dashboard-Plothy-Dash/main/hcoco1/src/data/grades_over_time.csv')


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server 


# Ensure grades are numeric
for col in df.columns[3:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Calculate final grades by averaging sublevels
subjects = ['Math', 'Science', 'English', 'History', 'Geography', 'Art']
for subject in subjects:
    df[f'{subject}'] = df[[f'{subject} Exam 1', f'{subject} Exam 2', f'{subject} Exam 3']].mean(axis=1)

# Calculate the final grade average across all subjects
df['Grade Average'] = df[[f'{subject}' for subject in subjects]].mean(axis=1)

# Prepare the summary table with only final grades
summary_df = df[['Name', 'Image URL', 'Year'] + [f'{subject}' for subject in subjects] + ['Grade Average']]



# Layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("High School Students' Grades Dashboard"), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='student-dropdown',
            options=[{'label': name, 'value': name} for name in df['Name'].unique()],
            value=df['Name'].unique()[0],
            clearable=False,
        ), width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Img(id='student-image', style={'width': '100px', 'height': '100px', 'display': 'block', 'margin': 'auto'}),
                        html.H4(id='average-grade', className="card-title", style={'textAlign': 'center'})
                    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
                ])
            ], style={'width': '100px', 'height': '120px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
        ], width=2, style={'marginLeft': 'auto'})  # Ensures the card is pushed to the right
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in df['Year'].unique()],
            value=df['Year'].unique()[0],
            clearable=False,
        ), width=4, className='mb-4')
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='subject-performance-chart'), width=12),
        #dbc.Col(dcc.Graph(id='exam-scores-pie-chart'), width=6)
    ], className='mb-4'),
    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id='summary-table',
            columns=[
                {"name": "Student Name", "id": "Name"},
                {"name": "Year", "id": "Year"},
                {"name": "Math", "id": "Math"},
                {"name": "Science", "id": "Science"},
                {"name": "English", "id": "English"},
                {"name": "History", "id": "History"},
                {"name": "Geography", "id": "Geography"},
                {"name": "Art", "id": "Art"},
                {"name": "Grade Average", "id": "Grade Average"},
            ],
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        ), width=12, className='mb-4')
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='subject-dropdown',
            options=[{'label': subject, 'value': subject} for subject in subjects],
            value=subjects[0],
            clearable=False,
        ), width=4, className='mb-4')
    ]),
    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id='exam-table',
            columns=[
                {"name": "Student Name", "id": "Name"},
                {"name": "Year", "id": "Year"},
                {"name": "Exam 1", "id": "Exam 1"},
                {"name": "Exam 2", "id": "Exam 2"},
                {"name": "Exam 3", "id": "Exam 3"},
            ],
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        ), width=12, className='mb-4')
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='performance-over-time'), width=12)
    ]),
], fluid=True,
   style={"max-width": "1000px"})

# Callback to update the summary table
@app.callback(
    Output('summary-table', 'data'),
    [Input('student-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_summary_table(selected_student, selected_year):
    filtered_summary_df = summary_df[(summary_df['Name'] == selected_student) & (summary_df['Year'] == selected_year)]
    return filtered_summary_df.to_dict('records')

# Callback to update the average grade card and student image
@app.callback(
    [Output('average-grade', 'children'),
     Output('student-image', 'src')],
    [Input('student-dropdown', 'value')]
)
def update_average_grade_and_image(selected_student):
    student_df = summary_df[summary_df['Name'] == selected_student]
    average_grade = student_df['Grade Average'].mean()
    image_url = student_df['Image URL'].values[0]  # Get the image URL for the student
    return f"{average_grade:.2f}", image_url

# Callback to update the exam table
@app.callback(
    Output('exam-table', 'data'),
    [Input('student-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('subject-dropdown', 'value')]
)
def update_exam_table(selected_student, selected_year, selected_subject):
    filtered_df = df[(df['Name'] == selected_student) & (df['Year'] == selected_year)]
    exam_df = filtered_df[['Name', 'Year', f'{selected_subject} Exam 1', f'{selected_subject} Exam 2', f'{selected_subject} Exam 3']]
    exam_df = exam_df.rename(columns={
        f'{selected_subject} Exam 1': 'Exam 1',
        f'{selected_subject} Exam 2': 'Exam 2',
        f'{selected_subject} Exam 3': 'Exam 3'
    })
    return exam_df.to_dict('records')

# Callback to update the performance over time line chart
@app.callback(
    Output('performance-over-time', 'figure'),
    [Input('student-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('subject-dropdown', 'value')]
)
def update_performance_chart(selected_student, selected_year, selected_subject):
    filtered_df = df[(df['Name'] == selected_student) & (df['Year'] == selected_year)]
    exam_grades = filtered_df[[f'{selected_subject} Exam 1', f'{selected_subject} Exam 2', f'{selected_subject} Exam 3']].values.flatten()
    exams = ['Exam 1', 'Exam 2', 'Exam 3']
    chart_data = pd.DataFrame({
        'Exam': exams,
        'Grade': exam_grades
    })
    fig = px.line(chart_data, x='Exam', y='Grade', title=f'Performance Over Exams for {selected_student} in {selected_subject} ({selected_year})',
                  markers=True)
    fig.update_layout(xaxis_title='Exam', yaxis_title='Grade')
    return fig

# Callback to update the subject performance bar chart
@app.callback(
    Output('subject-performance-chart', 'figure'),
    [Input('student-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_subject_performance_chart(selected_student, selected_year):
    filtered_df = summary_df[(summary_df['Name'] == selected_student) & (summary_df['Year'] == selected_year)]
    chart_data = filtered_df.melt(id_vars=['Name', 'Year'], value_vars=[f'{subject}' for subject in subjects], var_name='Subject', value_name='Grade')
    chart_data['Subject'] = chart_data['Subject'].str.replace(' ', '')
    fig = px.bar(chart_data, x='Subject', y='Grade', title=f'Subject-wise Performance for {selected_student} in {selected_year}', color='Subject')
    fig.update_layout(xaxis_title='Subject', yaxis_title='Grade')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



