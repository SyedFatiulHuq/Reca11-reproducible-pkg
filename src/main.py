import math
import os

import context_reader
import executor
import transcript_processor as tp
import utility as util
import report_selection


PROJECTS = ['money manager', 'goose sighting']
RUN_NUM = 5  # the number of runs per transcript
CAPTION_NUM = 100  # the number of captions per chunk


def get_chunk_size(transcript_segments, max_caption_number):
    total_captions = len(transcript_segments)
    chunk_num = math.ceil(total_captions / max_caption_number)
    last_len = total_captions % max_caption_number

    final_len = max_caption_number
    if chunk_num > 1 and last_len < max_caption_number / 3:
        padding = math.ceil(last_len / (chunk_num - 1))
        final_len += padding

    return final_len


def get_caption_chunks(transcript_segments, max_caption_number):
    chunks = []
    chunk = ""
    iterate = 0
    ideal_caption_number = get_chunk_size(transcript_segments, max_caption_number)
    for segment in transcript_segments:
        chunk += f"\n{str(segment)}\n"
        iterate += 1

        if iterate > ideal_caption_number:
            chunks.append(chunk)
            chunk = f"\n{str(segment)}\n"
            iterate = 0
    if len(chunk) > 0:
        chunks.append(chunk)

    return chunks


def remove_last_blank_line(s):
    lines = s.split('\n')

    # Check if the last line is blank and remove it if so
    if lines and lines[-1].strip() == '':
        lines.pop()

    return '\n'.join(lines)


def run_reca11():
    for project in PROJECTS:
        run_on_project(project)


def run_on_project(project):
    directory = os.path.join('../artifacts/transcripts', project)

    for file in sorted(os.listdir(directory)):
        filepath = os.path.join(directory, file)
        session = file.replace('.vtt', '')

        # for each session in each project, we analyze the transcript and create chunks of the transcript in SpeachSegment objects
        transcript_segments = tp.extract_segments_from_transcript(filepath)
        caption_chunks = get_caption_chunks(transcript_segments, CAPTION_NUM)

        print(f"{project} > {file}")

        reports = {}

        # now we feed the llm these chunks 'RUN_NUM' number of times
        for i in range(RUN_NUM):

            # we extract all the relevant contextual information to add to the prompt
            context_string = context_reader.get_all_context_string(project, file)
            print(context_string)

            total_tokens = 0
            current_report = []

            # we iterate through all the chunks, run the llm with the prompt, where prompt = chunk + contextual info
            for iteration, chunk in enumerate(caption_chunks):
                token_count, result = executor.run_model(chunk, context_string)

                # results from individual chunks are collected into one collection
                current_report.extend(result.issues)
                total_tokens += token_count

            # print(current_report)
            reports[i] = current_report

        # from the multiple runs, we conduct report selection and generate the final report
        report_selection.select_and_print_report(reports, session, project)

        # break  # this break enables only one session per project to be analyzed


if __name__ == '__main__':
    run_reca11()
