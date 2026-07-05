class FileReader:

    def read_job_description(self):

        with open("data/job_description.txt", "r", encoding="utf-8") as file:

            return file.read()