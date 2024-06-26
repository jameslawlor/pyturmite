import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation
from functools import partial
import numpy as np


class Plotter:
    def __init__(self, mode, animation_interval, save_animation, frame_skip):
        self.turmite = None
        self.mode = mode
        self.animation_interval = animation_interval
        self.save_animation = save_animation
        self.frame_skip = frame_skip
        self.plot = self.get_plotting_function()

    def get_plotting_function(self):
        if self.mode == "static":
            return self.static_plot
        elif self.mode == "animate":
            return self.animate
        else:
            raise KeyError("Plotting mode not supported!")

    def static_plot(
        self,
        turmite,
        n_steps,
        plot_history=False,
    ):
        for _ in range(n_steps):
            turmite.update()

        data = np.array(turmite.grid)
        data[turmite.x][turmite.y] = turmite.n_colours + 1
        plt.figure()
        plt.imshow(
            data,
            interpolation="none",
            vmin=0,
            vmax=turmite.n_colours + 1,
            cmap=turmite.cmap,
        )
        plt.show()

        if plot_history:
            colour_history = turmite.colour_history
            step_list = range(1, len(colour_history))
            cumulative_average_of_colours_visited = [
                np.mean(colour_history[:_]) for _ in step_list
            ]
            plt.plot(step_list, cumulative_average_of_colours_visited)
            plt.xscale("log")
            plt.ylabel("Cumulative average of visited square colour")
            plt.xlabel("Number of steps")
            plt.show()

    def animate(self, turmite, n_steps):
        fig = plt.figure()

        im = plt.imshow(
            turmite.grid,
            interpolation="none",
            vmin=0,
            vmax=turmite.n_colours + 1,
            cmap=turmite.cmap,
        )
        ax = plt.gca()
        frame_num = ax.text(
            0.99,
            0.01,
            "",
            fontsize=5,
            horizontalalignment="right",
            verticalalignment="bottom",
            transform=ax.transAxes,
        )
        frame_num.set_bbox(
            dict(facecolor="white", alpha=0.3, edgecolor="black", lw=0.1)
        )
        plt.axis("off")

        def update(
            step,
            turmite,
        ):
            for _ in range(self.frame_skip):
                turmite.update()
            data = np.array(turmite.grid)
            data[turmite.x][turmite.y] = turmite.n_colours + 1
            im.set_data(data)
            frame_num.set_text(f"Step: {step*self.frame_skip:,}")
            return [im, frame_num]

        anim = FuncAnimation(  # noqa: F841
            fig,
            partial(
                update,
                turmite=turmite,
            ),
            frames=n_steps,
            interval=self.animation_interval,
            blit=True,
            repeat=False,
        )

        if self.save_animation:
            anim.save(
                "example.mp4",
                writer="ffmpeg",
                fps=120,
                progress_callback=lambda i, n: print(f"Saving frame {i}/{n}"),
            )

        plt.show()
