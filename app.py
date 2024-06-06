import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to generate the DataFrame
def generate_student_data(num_rows):
    np.random.seed(42)
    marks = np.random.normal(loc=10, scale=2, size=(num_rows, 6))
    marks = np.clip(marks, 0, 20)
    marks = np.round(marks, 2)
    df = pd.DataFrame(marks, columns=['mathematics', 'physics', 'english', 'arabic', 'computer science', 'algebra'])
    names = [''.join(np.random.choice(list('abcdefghijklmnopqrstuvwxyz'), size=6)) for _ in range(num_rows)]
    surnames = [''.join(np.random.choice(list('abcdefghijklmnopqrstuvwxyz'), size=8)) for _ in range(num_rows)]
    gender = np.random.choice(['male', 'female'], size=num_rows)
    def determine_orientation(row):
        if row['mathematics'] > row[['physics', 'english', 'arabic', 'computer science']].max() and row['algebra'] > row[['physics', 'english', 'arabic', 'computer science']].max():
            return 'mathematics'
        elif row['computer science'] > row[['physics', 'english', 'arabic', 'mathematics']].max() and row['algebra'] > row[['physics', 'english', 'arabic', 'mathematics']].max():
            return 'computer science'
        elif row[['arabic', 'english']].mean() > row[['physics', 'mathematics', 'computer science', 'algebra']].mean():
            return 'languages'
        else:
            return 'physics'
    df['orientation'] = df.apply(determine_orientation, axis=1)
    df['name'] = names
    df['surname'] = surnames
    df['gender'] = gender
    df = df[['name', 'surname', 'gender', 'mathematics', 'physics', 'english', 'arabic', 'computer science', 'algebra', 'orientation']]
    return df

# Function to estimate the number of departments needed
def estimate_departments(proportions, total_departments):
    return (proportions * total_departments).round().astype(int)

# Streamlit app
st.title("Student Orientation Analysis and Department Needs Estimation")

# Number of students input
num_students = st.sidebar.number_input("Number of Students", min_value=1, max_value=100000, value=10000)

# Generate student data
student_data = generate_student_data(num_students)

st.subheader("Student Data Sample")
st.write(student_data.head())

# Calculate the proportion of each orientation
orientation_counts = student_data['orientation'].value_counts()
total_students = len(student_data)
orientation_proportions = orientation_counts / total_students

st.subheader("Proportion of Students in Each Orientation")
st.write(orientation_proportions)

# Plot pie chart of orientation distribution
fig1, ax1 = plt.subplots()
ax1.pie(orientation_proportions, labels=orientation_proportions.index, autopct='%1.1f%%', startangle=140)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)

st.write("""
### Explanation:
The pie chart above shows the distribution of student orientations. This helps in understanding the proportion of students excelling in different fields.
""")

# Estimate the number of departments needed
total_departments = st.sidebar.number_input("Total Number of Departments", min_value=1, value=10)
department_estimates = estimate_departments(orientation_proportions, total_departments)

st.subheader("Estimated Number of Departments Needed for Each Orientation")
st.write(department_estimates)

# Plot bar chart of department estimates
fig2, ax2 = plt.subplots()
department_estimates.plot(kind='bar', ax=ax2, color=['blue', 'green', 'red', 'purple'])
ax2.set_title('Estimated Number of Departments Needed by Orientation')
ax2.set_xlabel('Orientation')
ax2.set_ylabel('Number of Departments')
ax2.set_xticklabels(department_estimates.index, rotation=45)
st.pyplot(fig2)

st.write("""
### Explanation:
The bar chart above shows the estimated number of departments needed for each orientation. This is based on the proportion of students in each orientation category and the total number of departments specified.
""")

# Additional graphs: Distribution of marks for each subject
st.subheader("Distribution of Marks for Each Subject")
subjects = ['mathematics', 'physics', 'english', 'arabic', 'computer science', 'algebra']

fig3, axes = plt.subplots(2, 3, figsize=(18, 12))

for i, subject in enumerate(subjects):
    row, col = divmod(i, 3)
    axes[row, col].hist(student_data[subject], bins=20, edgecolor='black', alpha=0.7)
    axes[row, col].set_title(f'Distribution of Marks in {subject.capitalize()}')
    axes[row, col].set_xlabel('Marks')
    axes[row, col].set_ylabel('Number of Students')

plt.tight_layout()
st.pyplot(fig3)

st.write("""
### Explanation:
The histograms above show the distribution of marks for each subject. This helps in understanding the performance of students in different subjects and identifying areas where students excel or need improvement.
""")
