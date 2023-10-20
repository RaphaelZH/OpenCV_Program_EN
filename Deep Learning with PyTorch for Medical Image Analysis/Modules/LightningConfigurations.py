from lightning.pytorch.callbacks import RichProgressBar
from lightning.pytorch.callbacks.progress.rich_progress import RichProgressBarTheme

from .CustomColors import *


def custom_progress_bar():
    colors = calm_color_generator(2)
    color_group_1 = gradient_dark_generator(colors[0], 3)
    color_group_1.append(colors[0])
    color_group_2 = gradient_dark_generator(colors[1], 3)
    color_group_2.append(colors[1])
    return RichProgressBar(
        theme=RichProgressBarTheme(
            description=color_group_1[3],
            progress_bar=color_group_1[1],
            progress_bar_finished=color_group_1[2],
            progress_bar_pulse=color_group_1[0],
            batch_progress=color_group_2[2],
            time=color_group_2[1],
            processing_speed=color_group_2[0],
            metrics=color_group_2[3],
            metrics_text_delimiter="\n",
            metrics_format="<7n",
        ),
        leave=True,
    )
