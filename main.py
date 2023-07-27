import pandas as pd
import streamlit as st

d = pd.read_excel('Transcript.xlsx')

df = pd.DataFrame(d)

st.set_page_config(layout='wide')


def get_year_students(year):
    result_df = df[df['Register Number'].astype(str).str.endswith(str(year))]
    return result_df


def sort_majors(dataframe):
    grouped_data = {}
    for major, group in dataframe.groupby('Program'):
        grouped_data[major] = group.reset_index(drop=True)
    return grouped_data


def read_text_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def create_new_dataframe(courses, dataframe):
    # Extract the unique names from the 'Names' column in the given DataFrame
    names = dataframe['Student Name'].unique()

    # Extract the unique values from the second column of the CSV file (Credits)
    columns = read_text_file(courses)

    # Create a new DataFrame with zeros
    new_dataframe = pd.DataFrame(0, index=names, columns=columns)

    new_dataframe = new_dataframe.rename_axis('Student Name', axis=1)

    return new_dataframe


def update_grades(initial_df, new_grades_df):
    # Function to map grades to PASS, SEMI, or FAIL
    def map_grade(grade):
        if grade in ['A+', 'A', 'B+', 'B', 'C+', 'C', 'P']:
            return '🟩'
        elif grade in ['D+', 'D']:
            return '🟨'
        else:
            return '🟥'

    # Iterate through the new grades DataFrame and update the initial DataFrame
    for index, row in new_grades_df.iterrows():
        student_name = row['Student Name']
        course_name = row['Course Name']
        grade = row['Grade']

        mapped_grade = map_grade(grade)
        initial_df.loc[student_name, course_name] = mapped_grade

    return initial_df


# Example usage:
# Assuming initial_df is your initial DataFrame and new_grades_df is the new DataFrame with grades
# updated_df = update_grades(initial_df, new_grades_df)


data = get_year_students(2024)

st.write(data)

majors_data = sort_majors(data)

with st.expander('BA'):
    ba_data = majors_data['B.Sc - Business Administration']
    st.write(ba_data)

    new_ba_table = create_new_dataframe('ba.txt', ba_data)
    # st.write(new_ba_table)

    updated_ba = update_grades(new_ba_table, ba_data)
    st.write(updated_ba)

with st.expander('CS'):
    cs_data = majors_data['B.Sc - Computer Science']
    st.write(cs_data)

    new_cs_table = create_new_dataframe('cs.txt', cs_data)
    # st.write(new_cs_table)

    updated_cs = update_grades(new_cs_table, cs_data)
    st.write(updated_cs)

with st.expander('MIS'):
    st.write(majors_data['B.Sc - Management Information Systems'])