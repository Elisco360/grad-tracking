import pandas as pd
import streamlit as st

t1 = st.file_uploader('Upload Year 1 file', type='xlsx', accept_multiple_files=True)

data_list = []
try:
    # st.write(t1)
    for i in t1:
        data_list.append(pd.read_excel(i))
except:
    pass

def get_year_students(dataframe, year):
    result_df = dataframe[dataframe['Register Number'].astype(str).str.endswith(str(year))]
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


try:
    year_list = []
    for i in data_list:
        year_list.append(get_year_students(i,2024))

    majors_list = []
    for j in year_list:
        majors_list.append(sort_majors(j))

    with st.expander('BA'):
        y1 = majors_list[0]
        ba_data = y1['B.Sc - Business Administration']

        new_ba_table = create_new_dataframe('ba.txt', ba_data)

        for x in majors_list:
            temp = x['B.Sc - Business Administration']
            ba_df = update_grades(new_ba_table, temp)
            new_ba_table = ba_df

        st.write(new_ba_table)
    
    with st.expander('CS'):
        y2 = majors_list[1]
        cs_data = y1['B.Sc - Computer Science']

        new_cs_table = create_new_dataframe('cs.txt', cs_data)

        for x in majors_list:
            temp = x['B.Sc - Computer Science']
            cs_df = update_grades(new_cs_table, temp)
            new_cs_table = cs_df

        st.write(new_cs_table)

except:
    st.warning('Upload all required documents')