import pandas as pd
import matplotlib.pyplot as plt

# List of file paths
file_paths = [
    "qwe/USE1-April24.xlsx",
    "qwe/USE3-April22-Mar23.xlsx",
    "qwe/USE4-April21-Mar22.xlsx",
    "qwe/USE5-April20-Mar21.xlsx",
    "qwe/USE6-April19-Mar20.xlsx",
    "qwe/USE7-April18-Mar19.xlsx",
    "qwe/USE8-April17-Mar18.xlsx"
]

# Categories for the number of people involved
people_categories = ['1 person', '2-5 people', '6-10 people', 'more than 10 people']


# Function to process each file and generate plots
def process_file(file_path):
    # Load the UoFPO sheet
    use_of_force_details = pd.read_excel(file_path, sheet_name='UoFPO')

    # Map NoOfPeople to the correct categories
    use_of_force_details['People_Category'] = pd.Categorical(use_of_force_details['NoOfPeople'],
                                                             categories=people_categories, ordered=True)

    # Summarize the data
    people_involved_summary = use_of_force_details.groupby(['People_Category']).size()

    # Calculate the proportions
    total_cases = people_involved_summary.sum()
    proportions = people_involved_summary / total_cases

    # Plotting the bar chart
    plt.figure(figsize=(10, 6))
    proportions.plot(kind='bar')
    plt.title(f'Proportion of People Involved in Use of Force Cases\n{file_path.split("/")[-1].replace(".xlsx", "")}')
    plt.xlabel('Number of People Involved')
    plt.ylabel('Proportion of Cases')
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save the plot as an image file
    output_image_path = f"{file_path.split('/')[-1].replace('.xlsx', '')}_proportions.png"
    plt.savefig(output_image_path)
    plt.show()


# Process each file
for file_path in file_paths:
    process_file(file_path)
