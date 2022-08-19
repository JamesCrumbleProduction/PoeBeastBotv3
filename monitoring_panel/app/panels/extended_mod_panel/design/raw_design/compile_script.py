import os
import re
import tempfile

from typing import Callable
from dataclasses import dataclass

ROOT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..',
)

DESIGN_REPLACEMENTS: dict[Callable[[str], tuple[int, int]], str] = {
    # should fix window icon problem with path
    lambda string: (0, 0): 'import os\n',
    lambda string: re.search('icon\.addFile\((.+)\)', string).span(1): (
        'f"{os.path.join(os.path.dirname(os.path.abspath(__file__)), \'..\', \'raw_design\', \'Bestiary_Brimmed_Hat_inventory_icon.webp\')}", QSize(), QIcon.Normal, QIcon.Off'
    ),

    # fixing import problems after recompiling
    lambda string: re.search('import resources_rc', string).span(): '',
}


@dataclass
class FileData:

    path_to_file: str
    filename: str
    extension: str


@dataclass
class QtDesignFiles:

    raw_path: FileData | None
    compiled_path: FileData

    def compiled_file_path_raw(self) -> str:
        return os.path.join(
            self.raw_path.path_to_file, f'{self.raw_path.filename}.{self.raw_path.extension}'
        )

    def compile_file_path_compiled(self, compiled_file_folder: str = 'compiled_design') -> str:
        if self.compiled_path is None:
            return os.path.join(
                self.raw_path.path_to_file, *[
                    '..',
                    compiled_file_folder,
                    f'{self.raw_path.filename}.py'
                ]
            )

        return os.path.join(
            self.compiled_path.path_to_file, *[
                '..',
                compiled_file_folder,
                f'{self.compiled_path.filename}.{self.compiled_path.extension}'
            ]
        )

    def validate(self, file: str) -> 'QtDesignFiles':
        if self.raw_path is None:
            raise NotImplementedError(
                f'Cannot compile "{file}" file couse doesn\'t exists'
            )
        return self


def find_file(extension: str = None, full_name: str = None) -> FileData:

    if extension is None and full_name is None:
        raise NotImplementedError(
            'extension and full_name arguments can\'t contains None at the same time'
        )

    for content in os.walk(ROOT_PATH):
        dir_path, _directories_, files = content

        for file in files:
            filename = ''.join(file.split('.')[:-1])
            file_extension = file.split('.')[-1]

            if full_name is not None:
                if file == full_name:
                    return FileData(
                        path_to_file=dir_path,
                        filename=filename,
                        extension=file_extension
                    )

            if file_extension == extension:
                return FileData(
                    path_to_file=dir_path,
                    filename=filename,
                    extension=file_extension
                )


def parse_data_stream(
    data_stream: str,
    replacements: dict[Callable[[str], tuple[int, int]], str] = None
) -> str:
    if replacements is None:
        return data_stream

    output: str = ''

    slices_data = sorted(
        {
            replace_value: parse_func(data_stream)
            for parse_func, replace_value in replacements.items()
        }.items(),
        key=lambda v: v[1][0]
    )

    last_lower: int = 0

    for replace_value, slice_ in slices_data:
        output += data_stream[last_lower:slice_[0]]
        output += replace_value
        last_lower = slice_[1]

    if last_lower != len(data_stream):
        output += data_stream[last_lower:]

    return output


def generate_raw_data_stream(command_prefix: str, file_path: str) -> str:

    temp_file = tempfile.NamedTemporaryFile()
    temp_file.close()

    shell_command: str = f'{command_prefix} {file_path} > {temp_file.name}'
    print(f'EXECUTING "{shell_command}" COMMAND')
    if os.system(shell_command) != 0:
        raise ValueError('Execution command return wrong complited value')
    return open(temp_file.name, 'r').read()


DESIGN_UI_FILE = QtDesignFiles(
    raw_path=find_file('ui'),
    compiled_path=find_file(full_name='design.py')
).validate('design.ui')
RESOURCE_QRC_FILE = QtDesignFiles(
    raw_path=find_file('qrc'),
    compiled_path=find_file(full_name='resources_rc.py')
).validate('resources_rc.py')


DESIGN_UI_PARSED_COMPILED_DATA: str = parse_data_stream(
    generate_raw_data_stream(
        'pyside6-uic', DESIGN_UI_FILE.compiled_file_path_raw()
    ), DESIGN_REPLACEMENTS
)
RESOURCES_QRC_PARSED_COMPILED_DATA: str = parse_data_stream(
    generate_raw_data_stream(
        'pyside6-rcc', RESOURCE_QRC_FILE.compiled_file_path_raw()
    )
)

with open(DESIGN_UI_FILE.compile_file_path_compiled(), 'w') as design_ui_file:
    design_ui_file.write(DESIGN_UI_PARSED_COMPILED_DATA)


with open(RESOURCE_QRC_FILE.compile_file_path_compiled(), 'w') as resource_qrc_file:
    resource_qrc_file.write(RESOURCES_QRC_PARSED_COMPILED_DATA)
