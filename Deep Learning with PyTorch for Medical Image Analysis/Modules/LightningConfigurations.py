from lightning.pytorch.callbacks import RichProgressBar
from lightning.pytorch.callbacks.progress.rich_progress import RichProgressBarTheme

from .CustomColors import *


def custom_gradient_colors(colors, color_index):
    color_list = gradient_dark_generator(colors[color_index], 3)
    color_list.append(colors[color_index])
    color_list.remove(color_list[0])
    return color_list


def custom_progress_bar():
    colors = calm_color_generator(2)
    color_group_1 = custom_gradient_colors(colors, 0)
    color_group_2 = custom_gradient_colors(colors, 1)
    return RichProgressBar(
        theme=RichProgressBarTheme(
            description=color_group_1[2],
            progress_bar=color_group_1[0],
            progress_bar_finished=color_group_1[1],
            progress_bar_pulse=color_group_1[1],
            batch_progress=color_group_1[2],
            time=color_group_2[1],
            processing_speed=color_group_2[0],
            metrics=color_group_2[2],
            metrics_text_delimiter="\n",
            metrics_format="<7n",
        ),
        leave=False,
    )
