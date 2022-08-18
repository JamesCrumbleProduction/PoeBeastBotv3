import os
import re
import tempfile

from dataclasses import dataclass, replace

ROOT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..',
)

LOCAL_FOLDER_PATH: str = os.path.join(
    os.path.dirname(os.path.abspath(__file__))
)

REPLACEMENT: dict[re.Pattern, str] = {
    re.compile('icon\.addFile\((.+)\)'): f'r"{os.path.join(LOCAL_FOLDER_PATH, "Bestiary_Brimmed_Hat_inventory_icon.webp")}", QSize(), QIcon.Normal, QIcon.Off'
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


DESIGN_UI_FILE = QtDesignFiles(
    raw_path=find_file('ui'),
    compiled_path=find_file(full_name='design.py')
).validate('design.ui')
RESOURCE_QRC_FILE = QtDesignFiles(
    raw_path=find_file('qrc'),
    compiled_path=find_file(full_name='resources_rc.py')
).validate('resources_rc.py')


# DESIGN_UI_COMPILE_COMMAND: str = (
#     f'pyside6-uic {DESIGN_UI_FILE.compiled_file_path_raw()} > '
#     f'{DESIGN_UI_FILE.compile_file_path_compiled()}'
# )
# RESOURCES_QRC_COMPILE_COMMAND: str = (
#     f'pyside6-rcc {RESOURCE_QRC_FILE.compiled_file_path_raw()} > '
#     f'{RESOURCE_QRC_FILE.compile_file_path_compiled()}'
# )

temp_file = tempfile.NamedTemporaryFile()
temp_file.close()

DESIGN_UI_COMPILE_COMMAND: str = (
    f'pyside6-uic {DESIGN_UI_FILE.compiled_file_path_raw()} > {temp_file.name}'
)
os.system(DESIGN_UI_COMPILE_COMMAND)
DESIGN_UI_COMPILE_DATA_STREAM: str = open(temp_file.name, 'r').read()


output: str = ''
slices_data = sorted(
    {
        replace_value: pattern.search(DESIGN_UI_COMPILE_DATA_STREAM).span(1)
        for pattern, replace_value in REPLACEMENT.items()
    }.items(),
    key=lambda v: v[1]
)

last_lower: int = 0

for replace_value, slice_ in slices_data:
    # print(replace_value, slice_)
    output += DESIGN_UI_COMPILE_DATA_STREAM[last_lower:slice_[0]]
    output += replace_value

    # TODO slice_[1] and len(replace_value) isn't correct cos of replace_value can be longer or shorter by span value
    last_lower += len(replace_value)  # <-

if last_lower != len(DESIGN_UI_COMPILE_DATA_STREAM):
    output += DESIGN_UI_COMPILE_DATA_STREAM[last_lower:]


print(output)

# for pattern, replace_value in REPLACEMENT.items():
#     DESIGN_UI_COMPILE_DATA_STREAM[
#         slice(
#             *pattern.search(DESIGN_UI_COMPILE_DATA_STREAM).span(1)
#         )
#     ] = replace_value
# print(DESIGN_UI_COMPILE_DATA_STREAM)
# print(
#     DESIGN_UI_COMPILE_DATA_STREAM[
#         slice(*re.search(
#             'icon\.addFile\((.+)\)',
#         ).span(1))
#     ]
# )
# print(COMPILED_DESIGN_UI)

# print('DESIGN_UI_COMPILE_COMMAND is start to executing...')
# os.system(DESIGN_UI_COMPILE_COMMAND)
# print('DESIGN_UI_COMPILE_COMMAND is done and successfully compiled')

# print('RESOURCES_QRC_COMPILE_COMMAND is start to executing...')
# os.system(RESOURCES_QRC_COMPILE_COMMAND)
# print('RESOURCES_QRC_COMPILE_COMMAND is done and successfully compiled')
