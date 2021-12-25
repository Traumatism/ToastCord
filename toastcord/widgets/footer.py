from textual.widgets import Footer
from rich.text import Text


class Footer(Footer):

    def make_key_text(self) -> Text:
        """Create text containing all the keys."""
        text = Text(
            style="white on bright_black",
            no_wrap=True,
            overflow="ellipsis",
            justify="left",
            end="",
        )

        for binding in self.app.bindings.shown_keys:
            key_text = Text.assemble(
                f" {binding.description} ",
                meta={
                    "@click": f"app.press('{binding.key}')", "key": binding.key
                }
            )
            text.append_text(key_text)
        return text
