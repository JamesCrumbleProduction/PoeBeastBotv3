import os

from dataclasses import dataclass

from .structure import RawTemplate


ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


@dataclass
class Paths:

    @dataclass
    class BeastsBotTemplates:

        __beasts_bot_templates = os.path.join(
            ROOT_PATH, 'beasts_bot'
        )
        buttons = os.path.join(__beasts_bot_templates, 'buttons')
        maps = os.path.join(__beasts_bot_templates, 'maps')
        nametags = os.path.join(__beasts_bot_templates, 'nametags')
        next_layout_nametags = os.path.join(
            __beasts_bot_templates,
            'nametags', 'next_layout_nametags'
        )
        other = os.path.join(__beasts_bot_templates, 'other')
        scarabs = os.path.join(__beasts_bot_templates, 'scarabs')

    @dataclass
    class UnpackingActionTemplates:
        __unpacking_action_templates = os.path.join(
            ROOT_PATH, 'unpacking_action'
        )
        beasts = os.path.join(__unpacking_action_templates, 'beasts')
        icons = os.path.join(__unpacking_action_templates, 'icons')
        labels = os.path.join(__unpacking_action_templates, 'labels')
        other = __unpacking_action_templates


@dataclass
class RawTemplates:

    @dataclass
    class BeastsBotRawTemplates:
        buttons = (
            RawTemplate(
                label=str(*buttons.split('.')[:-1]),
                path=os.path.join(Paths.BeastsBotTemplates.buttons, buttons)
            )
            for buttons in os.listdir(Paths.BeastsBotTemplates.buttons)
            if os.path.isfile(os.path.join(Paths.BeastsBotTemplates.buttons, buttons))
        )
        maps = (
            RawTemplate(
                label=str(*maps.split('.')[:-1]),
                path=os.path.join(Paths.BeastsBotTemplates.maps, maps)
            )
            for maps in os.listdir(Paths.BeastsBotTemplates.maps)
            if os.path.isfile(os.path.join(Paths.BeastsBotTemplates.maps, maps))
        )
        nametags = (
            RawTemplate(
                label=str(*nametags.split('.')[:-1]),
                path=os.path.join(Paths.BeastsBotTemplates.nametags, nametags)
            )
            for nametags in os.listdir(
                Paths.BeastsBotTemplates.nametags
            )
            if os.path.isfile(
                os.path.join(
                    Paths.BeastsBotTemplates.nametags,
                    nametags
                )
            )
        )
        next_layout_nametags = (
            RawTemplate(
                label=str(*next_layout_nametags.split('.')[:-1]),
                path=os.path.join(
                    Paths.BeastsBotTemplates.next_layout_nametags,
                    next_layout_nametags
                )
            )
            for next_layout_nametags in os.listdir(
                Paths.BeastsBotTemplates.next_layout_nametags
            )
            if os.path.isfile(
                os.path.join(
                    Paths.BeastsBotTemplates.next_layout_nametags,
                    next_layout_nametags
                )
            )
        )
        other = (
            RawTemplate(
                label=str(*other.split('.')[:-1]),
                path=os.path.join(Paths.BeastsBotTemplates.other, other)
            )
            for other in os.listdir(Paths.BeastsBotTemplates.other)
            if os.path.isfile(os.path.join(Paths.BeastsBotTemplates.other, other))
        )
        scarabs = (
            RawTemplate(
                label=str(*scarabs.split('.')[:-1]),
                path=os.path.join(Paths.BeastsBotTemplates.scarabs, scarabs)
            )
            for scarabs in os.listdir(Paths.BeastsBotTemplates.scarabs)
            if os.path.isfile(os.path.join(Paths.BeastsBotTemplates.scarabs, scarabs))
        )

    @dataclass
    class UnpackingActionRawTemplates:
        beasts = (
            RawTemplate(
                label=str(*beasts.split('.')[:-1]),
                path=os.path.join(
                    Paths.UnpackingActionTemplates.beasts, beasts
                )
            )
            for beasts in os.listdir(Paths.UnpackingActionTemplates.beasts)
            if os.path.isfile(
                os.path.join(
                    Paths.UnpackingActionTemplates.beasts,
                    beasts
                )
            )
        )
        icons = (
            RawTemplate(
                label=str(*icons.split('.')[:-1]),
                path=os.path.join(Paths.UnpackingActionTemplates.icons, icons)
            )
            for icons in os.listdir(Paths.UnpackingActionTemplates.icons)
            if os.path.isfile(
                os.path.join(
                    Paths.UnpackingActionTemplates.icons, icons
                )
            )
        )
        labels = (
            RawTemplate(
                label=str(*labels.split('.')[:-1]),
                path=os.path.join(
                    Paths.UnpackingActionTemplates.labels, labels)
            )
            for labels in os.listdir(Paths.UnpackingActionTemplates.labels)
            if os.path.isfile(
                os.path.join(
                    Paths.UnpackingActionTemplates.labels, labels
                )
            )
        )
        other = (
            RawTemplate(
                label=str(*other.split('.')[:-1]),
                path=os.path.join(Paths.UnpackingActionTemplates.other, other)
            )
            for other in os.listdir(Paths.UnpackingActionTemplates.other)
            if os.path.isfile(
                os.path.join(
                    Paths.UnpackingActionTemplates.other, other
                )
            )
        )

    def __str__(self) -> str:
        return '\n'.join(
            element
            for element in (
                '\n- - - - - - - UnpackingActionRawTemplates - - - - - - -\n',
                '\n'.join(
                    str(i)
                    for i in self.UnpackingActionRawTemplates.beasts
                ),
                '\n'.join(
                    str(i) for i in self.UnpackingActionRawTemplates.icons
                ),
                '\n'.join(
                    str(i) for i in self.UnpackingActionRawTemplates.labels
                ),
                '\n'.join(
                    str(i) for i in self.UnpackingActionRawTemplates.other
                ),
                '\n- - - - - - - BeastsBotRawTemplates - - - - - - -\n',
                '\n'.join(
                    str(i) for i in self.BeastsBotRawTemplates.buttons
                ),
                '\n'.join(
                    str(i) for i in self.BeastsBotRawTemplates.maps
                ),
                '\n'.join(
                    str(i) for i in self.BeastsBotRawTemplates.nametags
                ),
                '\n'.join(
                    str(i) for i in self.BeastsBotRawTemplates.next_layout_nametags
                ),
                '\n'.join(
                    str(i) for i in self.BeastsBotRawTemplates.other
                ),
                '\n'.join(
                    str(i) for i in self.BeastsBotRawTemplates.scarabs
                ),
            )
        )
