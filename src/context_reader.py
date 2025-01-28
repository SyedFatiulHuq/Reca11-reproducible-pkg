import csv
import re

from docx import Document

project = ""
session = ""


def find_tech_params_from_file():
    file_path = "../artifacts/context-files/tech_params.csv"
    try:
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Session'] == session:
                    params = {k: row[k] for k in ['AT', 'AT type', 'Platform', 'Device']}
                    return params
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except KeyError:
        print("Required column not found in the CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None


def params_match(at_types, devices, params):
    current_device = params['Device'].lower()
    if '/' in params['Device']:
        current_device = params['Device'].lower().split('/')[1]

    if (params['AT type'].lower() in at_types) and (current_device in devices):
        # print(f"AT types: {at_types}, Devices: {devices} | params: {params}")
        return True
    else:
        return False


def extract_a_param(line):
    listed_values = line.split(': ')[1]
    return [s.strip().lower() for s in (listed_values.split(', '))]


def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        if para.style.name.startswith('Heading'):
            if para.text.lower().startswith('takeaway') or para.text.lower().startswith('best practice'):
                full_text.append(para.text)
        elif para.text != '':
            full_text.append(para.text.strip())
    return '\n'.join(full_text)


def extract_internal_guidelines():
    text = read_docx("../artifacts/context-files/internal_guidelines.docx")
    if text == "":
        return text
    preamble = "You can use the following internal guidelines to better understand relevant accessibility and usability practices.\n```\n"
    return f"{preamble} \n + {text}"


def extract_wcag_guidelines():
    return "WCAG 2.1 is an internationally sanctioned guideline for accessibility standards on web and mobile applications. " \
           "You can use these guidelines to understand accessibility and usability standards better. " \
           "You can find the guidelines here: https://www.w3.org/TR/WCAG21/ "


def find_task_desc_from_file():
    file_path = "../artifacts/context-files/tasks.csv"
    try:
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['project'] == project:
                    return row['task']
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except KeyError:
        print("Required column not found in the CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None


def extract_project_task():
    if project == "fable":
        return ""
    preamble = "To provide you with some context about the testing session, following is a description of the tasks the tester was asked to do:\n"

    return f"{preamble}{find_task_desc_from_file()}"


def extract_tech_params():
    tech_params = find_tech_params_from_file()
    print(tech_params)
    return f"For assistive technology, the tester used {tech_params['AT']}, a type of {tech_params['AT type']}.\n" \
           f"The tester conducted the session on a {tech_params['Platform']} {tech_params['Device']}."


context_extraction_func = {
    "Internal guidelines": extract_internal_guidelines,
    "WCAG": extract_wcag_guidelines,
    "Task description": extract_project_task,
    "Technical parameters": extract_tech_params,
}


def extract_context(context):
    if context in context_extraction_func:
        return context_extraction_func[context]()
    else:
        print("No such function for the given parameter")


def get_selected_contexts_string(selected_contexts):
    context_string = ""
    for key, value in selected_contexts.items():
        if value:
            context_string += str(extract_context(key))
            context_string += "\n\n"
    return context_string


def extract_all_contexts():
    return get_selected_contexts_string({
        "Task description": True,
        "Technical parameters": True,
        "WCAG": True,
        "Internal guidelines": True,
    })


def get_all_context_string(project1, session1):
    global project
    project = project1
    global session
    session = session1
    return str(extract_all_contexts())
