from ..raw_templates import RawTemplates
from ..template_compiler import TemplateCompiler, CompiledTemplates


class ExtraContentCompiledTemplates:

    _instance: 'ExtraContentCompiledTemplates' = None

    def __new__(cls: type['ExtraContentCompiledTemplates'], *args, **kwargs) -> 'ExtraContentCompiledTemplates':
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):

        self._portal_action_templates = CompiledTemplates(TemplateCompiler(
            RawTemplates.ExtraContentRawTemplates.portal_action_templates
        ).compile_templates())

    @property
    def portal_action_templates(self) -> CompiledTemplates:
        return self._portal_action_templates


EXTRA_CONTENT_COMPILED_TEMPLATES = ExtraContentCompiledTemplates()
