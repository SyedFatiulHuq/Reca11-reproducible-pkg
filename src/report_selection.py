import os
import random
import copy

from issue_similarity import extract_max_match


SIMILARITY_THRESHOLD = .50
SIMILARITY_THRESHOLD2 = .80


def get_random_report_index(reports):
    return random.choice(list(reports.keys()))


def find_report_index_with_max_issues(reports):
    max_issues = -1
    reports_with_max_issues = []
    for key, report in reports.items():
        issue_count = len(report)
        if issue_count > max_issues:
            max_issues = issue_count
            reports_with_max_issues = [key]
        elif issue_count == max_issues:
            reports_with_max_issues.append(key)

    # Check if a file was found with issues
    if not reports_with_max_issues:
        return get_random_report_index(reports)

    # Return a random file from the files with the maximum number of issues
    return random.choice(reports_with_max_issues)


def find_report_index_with_min_issues(reports):
    min_issues = 10000
    reports_with_min_issues = []
    for key, report in reports.items():
        issue_count = len(report)
        if issue_count < min_issues:
            min_issues = issue_count
            reports_with_min_issues = [key]
        elif issue_count == min_issues:
            reports_with_min_issues.append(key)

    # Check if a file was found with issues
    if not reports_with_min_issues:
        return get_random_report_index(reports)

    # Return a random file from the files with the maximum number of issues
    return random.choice(reports_with_min_issues)


def extract_matching_issue(compared_issue, original_issues):
    text_to_compare = extract_text(compared_issue)

    for original_issue in original_issues:
        original_text = extract_text(original_issue)
        if text_to_compare == original_text:
            return original_issue


def remove_duplicates(issues):
    i = 0
    while i < len(issues):
        issue = issues[i]
        # print(issue['issue_title'])
        comparing_issues = issues[i + 1:]
        # print_titles(comparing_issues)
        if len(comparing_issues) == 0:
            break

        base_text = extract_text(issue)
        texts_to_compare = [extract_text(comparing_issue) for comparing_issue in comparing_issues]
        max_score, similarity_scores = extract_max_match(base_text, texts_to_compare)

        if max_score >= SIMILARITY_THRESHOLD2:
            max_score_index = similarity_scores.index(max_score)
            matching_issue = extract_matching_issue(comparing_issues[max_score_index], issues)
            # print(f"{issue['issue_title']} <{max_score}> {matching_issue['issue_title']}")
            issues.remove(matching_issue)
        i += 1


def extract_text(issue):
    return f"Title: {issue.issue_title}\nDescription: {issue.issue_description}"


def compare_new_issues_to_existing(all_issues, new_issues):
    for existing_issue in all_issues:
        base_text = extract_text(existing_issue)
        texts_to_compare = [extract_text(issue) for issue in new_issues]
        max_score, similarity_scores = extract_max_match(base_text, texts_to_compare)

        if max_score >= SIMILARITY_THRESHOLD:
            max_score_index = similarity_scores.index(max_score)
            matching_issue = new_issues[max_score_index]
            new_issues.remove(matching_issue)

        if len(new_issues) == 0:
            break

    for remaining_issue in new_issues:
        all_issues.append(remaining_issue)


def find_all_unique_issues(reports, report_max):
    all_issues = reports.pop(report_max)

    remove_duplicates(all_issues)

    for new_issues in reports.values():
        # remove_duplicates(file, new_issues)
        compare_new_issues_to_existing(all_issues, new_issues)

    remove_duplicates(all_issues)
    return all_issues


def create_new_report(issues, filename, project, session):
    dest_filepath = "../outputs/" + project + "/" + session

    if not os.path.exists(dest_filepath):
        os.makedirs(dest_filepath)

    with open(os.path.join(dest_filepath, filename), 'w') as file:
        for issue in issues:
            file.write(f"issue_title: {str(issue.issue_title)}\n")
            file.write(f"description: {str(issue.issue_description)}\n")
            file.write(f"timestamps: {str(issue.timestamps)}\n")

            file.write("\n")


def select_and_print_report(reports, session, project):

    report_random = get_random_report_index(reports)
    report_max = find_report_index_with_max_issues(reports)
    report_min = find_report_index_with_min_issues(reports)

    issues_all = find_all_unique_issues(copy.deepcopy(reports), report_max)

    create_new_report(reports[report_random], f"{session}-random.txt", project, session)
    create_new_report(reports[report_max], f"{session}-max.txt", project, session)
    create_new_report(reports[report_min], f"{session}-min.txt", project, session)
    create_new_report(issues_all, f"{session}-all.txt", project, session)
