from __future__ import annotations

from ..raw_templates import RawTemplates
from ..template_compiler import TemplateCompiler, CompiledTemplates


class BeastBotCompiledTemplates:

    _instance: BeastBotCompiledTemplates = None

    def __new__(cls: type[BeastBotCompiledTemplates], *args, **kwargs) -> BeastBotCompiledTemplates:
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self._buttons_templates = CompiledTemplates(TemplateCompiler(
            RawTemplates.BeastsBotRawTemplates.buttons
        ).compile_templates())
        self._maps_templates = CompiledTemplates(TemplateCompiler(
            RawTemplates.BeastsBotRawTemplates.maps
        ).compile_templates())
        self._nametags_templates = CompiledTemplates(TemplateCompiler(
            RawTemplates.BeastsBotRawTemplates.nametags
        ).compile_templates())
        self._next_layout_nametags_templates = CompiledTemplates(TemplateCompiler(
            RawTemplates.BeastsBotRawTemplates.next_layout_nametags
        ).compile_templates())
        self._other_templates = CompiledTemplates(TemplateCompiler(
            RawTemplates.BeastsBotRawTemplates.other
        ).compile_templates())

        self._scarabs_templates = CompiledTemplates(TemplateCompiler(
            RawTemplates.BeastsBotRawTemplates.scarabs
        ).compile_templates())

    @property
    def buttons_templates(self) -> CompiledTemplates:
        return self._buttons_templates

    @property
    def maps_templates(self) -> CompiledTemplates:
        return self._maps_templates

    @property
    def nametags_templates(self) -> CompiledTemplates:
        return self._nametags_templates

    @property
    def next_layout_nametags_templates(self) -> CompiledTemplates:
        return self._next_layout_nametags_templates

    @property
    def other_templates(self) -> CompiledTemplates:
        return self._other_templates

    @property
    def portals_templates(self) -> CompiledTemplates:
        return self._portals_templates

    @property
    def scarabs_templates(self) -> CompiledTemplates:
        return self._scarabs_templates


BEAST_BOT_COMPILED_TEMPLATES = BeastBotCompiledTemplates()
