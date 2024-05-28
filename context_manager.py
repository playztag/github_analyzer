class ContextManager:
    def __init__(self):
        self.global_context = {
            "summaries": {},
            "previous_prompts": [],
            "analyzed_files": [],
            "analyzed_directories": [],
            "file_contents": {}  # New dictionary to store file contents
        }

    def add_analyzed_directory(self, directory_path):
        self.global_context["analyzed_directories"].append(directory_path)

    def add_analyzed_file(self, file_path):
        self.global_context["analyzed_files"].append(file_path)

    def add_file_content(self, file_path, content):
        self.global_context["file_contents"][file_path] = content  # Store file content

    def add_summary(self, key, summary):
        self.global_context["summaries"][key] = summary

    def add_previous_prompt(self, prompt):
        self.global_context["previous_prompts"].append(prompt)

    def summarize_previous_interactions(self):
        summary = "Summary of previous interactions:\n"
        for item in self.global_context["summaries"].values():
            summary += f"{item}\n"
        return summary

    def get_context(self):
        return self.global_context

context_manager = ContextManager()
