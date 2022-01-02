from textual.widgets import Footer as _Footer
from rich.text import Text


class Footer(_Footer):

    def make_key_text(self) -> Text:
        """ Create text containing all the keys """

        text = Text(
            style="white",
            no_wrap=True,
            overflow="ellipsis",
            justify="left",
            end="",
        )

        for binding in self.app.bindings.shown_keys:
            key_text = Text.assemble(
                f" ({Text(binding.description, style='white on cyan')}) ",
                meta={
                    "@click": f"app.press('{binding.key}')", "key": binding.key
                },
            )
            text.append_text(key_text)

        return text
