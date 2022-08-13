from ..raw_templates import RawTemplates
from ..template_compiler import TemplateCompiler, CompiledTemplates


class UnpackingActionCompiledTemplates:

    _instance: 'UnpackingActionCompiledTemplates' = None

    def __new__(cls: type['UnpackingActionCompiledTemplates'], *args, **kwargs) -> 'UnpackingActionCompiledTemplates':
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):

        self._beasts_templates = CompiledTemplates(TemplateCompiler(
            RawTemplates.UnpackingActionRawTemplates.beasts
        ).compile_templates())
        self._icons_templates = CompiledTemplates(TemplateCompiler(
            RawTemplates.UnpackingActionRawTemplates.icons
        ).compile_templates())
        self._labels_templates = CompiledTemplates(TemplateCompiler(
            RawTemplates.UnpackingActionRawTemplates.labels
        ).compile_templates())
        self._other_templates = CompiledTemplates(TemplateCompiler(
            RawTemplates.UnpackingActionRawTemplates.other
        ).compile_templates())

    @property
    def beasts_templates(self) -> CompiledTemplates:
        return self._beasts_templates

    @property
    def icons_templates(self) -> CompiledTemplates:
        return self._icons_templates

    @property
    def labels_templates(self) -> CompiledTemplates:
        return self._labels_templates

    @property
    def other_templates(self) -> CompiledTemplates:
        return self._other_templates


UNPACKING_ACTION_COMPILED_TEMPLATES = UnpackingActionCompiledTemplates()
