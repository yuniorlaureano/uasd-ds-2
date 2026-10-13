from pathlib import Path
import os

class Data:

    def get_data_folder(self):
        current_file_path = Path(__file__)
        project_directory_path = current_file_path.resolve().parent.parent.parent
        data_directory_path = os.path.join(
            project_directory_path,
            "data"
        )
        return data_directory_path

    def get_file_path(self, file_path):
        data_folder = self.get_data_folder()
        path = Path(
            os.path.join(data_folder),
            file_path
        )
        return str(path)

    def tab_separatd_file_to_csv(self, file_to_convert_path, new_file_path, separator="|"):
        data_folder = self.get_data_folder()
        file_to_convert_absolute_path = Path(
            os.path.join(data_folder),
            file_to_convert_path
        )

        new_file_absolute_path = Path(
            os.path.join(data_folder),
            new_file_path
        )

        with open(file_to_convert_absolute_path, 'r') as source_file:
            with open(new_file_absolute_path, 'w') as destination_file:
                destination_file.write(f'text{separator}label\n')
                while True:
                    line = source_file.readline().split('\t')
                    if line is None or len(line) != 2:
                        break

                    destination_file.write(f'{line[0].strip()}{separator}{line[1].strip()}\n')
