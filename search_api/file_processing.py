import concurrent.futures


class FileProcessing:

    def __init__(self, s3):
        self.s3 = s3

    def process_files(self, list_of_files, match_string):

        response = []

        # Here we can tune the number of threads we want to use,
        # here i have used threads equal to number of files
        # if number of files is big then we can apply different strategy

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(list_of_files)) as executor:
            future_to_task = {executor.submit(self.perform_task, task, match_string): task for task in
                              list_of_files}

            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    if len(result) > 0:
                        task = task.split("/")
                        [response.append(task[0] + " " + task[1][:2] + " " + line) for line in result]
                except Exception as exc:
                    print(f"Task {task} generated an exception: {exc}")
        response = '\n'.join(sorted(response))

        return response

    def perform_task(self, file, match_string):
        response = self.s3.return_file_object(file)
        stream = response['Body']
        ans = []

        buffer = b''

        for chunk in stream.iter_chunks(chunk_size=256):
            buffer += chunk
            while True:
                line_break_index = buffer.find(b'\n')
                if line_break_index == -1:
                    break  # No complete line in buffer

                # Extract the complete line and process it
                complete_line = buffer[:line_break_index].decode('utf-8')
                if match_string in complete_line:
                    ans.append(complete_line)

                # Remove the processed line from the buffer
                buffer = buffer[line_break_index + 1:]

        # Process any remaining data in the buffer as the last line
        if buffer:
            complete_line = buffer.decode('utf-8')
            if match_string in complete_line:
                ans.append(complete_line)

        return ans
