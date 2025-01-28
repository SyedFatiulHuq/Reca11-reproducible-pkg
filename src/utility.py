import os
from structure_classes import Report

OUTPUT_RQ2_FILEPATH = "model-outputs/"
TXT = "txt"


def report_to_string(report: Report) -> str:
    report_str_list = []
    for issue in report.issues:
        issue_str = f"Issue Title: {issue.issue_title}\n"
        issue_str += f"Description: {issue.issue_description}\n"
        issue_str += f"Timestamps: {', '.join(issue.timestamps)}\n"
        issue_str += f"WCAG Guideline: {issue.wcag}\n"
        # issue_str += f"Internal Reference: {issue.internal}\n"
        issue_str += "-" * 40 + "\n"  # Divider between issues
        report_str_list.append(issue_str)

    return "\n".join(report_str_list)


def save_model_output(filename, project, string_data):
    # Step 1: Determine the sub-folder name and the base name of the file
    base_name = os.path.splitext(filename)[0]
    sub_folder = os.path.join(OUTPUT_RQ2_FILEPATH, project, base_name)

    # Step 2: Create the sub-folder if it doesn't exist
    if not os.path.exists(sub_folder):
        os.makedirs(sub_folder)

    # Step 3: Find a new filename if the file already exists
    file_index = 1
    new_filename = f"{base_name}-{file_index}.{TXT}"
    while os.path.exists(os.path.join(sub_folder, new_filename)):
        file_index += 1
        new_filename = f"{base_name}-{file_index}.{TXT}"

    # Step 4: Write the string data to the new file
    with open(os.path.join(sub_folder, new_filename), 'w') as file:
        file.write(string_data)


if __name__ == '__main__':
    save_model_output("test", "fable", "test test\ntest2")