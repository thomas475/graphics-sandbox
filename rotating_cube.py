import argparse
import imageio
from vispy import scene
from vispy.visuals.transforms import MatrixTransform
from vispy.app import run, Timer
import numpy as np

output_filename = 'renders/rotating_cube.gif'
n_steps = 18
step_angle = 10.0
axis = [0.25, 0.5, 1.0]

parser = argparse.ArgumentParser(description="Display or export a rotating cube.")
parser.add_argument('--export', action='store_true', help='Export rendering as GIF')
args = parser.parse_args()

canvas = scene.SceneCanvas(keys='interactive', bgcolor='white', size=(600, 600), show=True)
view = canvas.central_widget.add_view()
view.camera = 'arcball'

cube = scene.visuals.Box(
    width=2, height=2, depth=2,
    face_colors=np.array([
        [1.0, 0.0, 0.0, 1.0], [1.0, 0.0, 0.0, 1.0],  # front
        [1.0, 0.0, 0.0, 1.0], [1.0, 0.0, 0.0, 1.0],  # back
        [0.8, 0.0, 0.0, 1.0], [0.8, 0.0, 0.0, 1.0],  # left
        [0.8, 0.0, 0.0, 1.0], [0.8, 0.0, 0.0, 1.0],  # right
        [0.6, 0.0, 0.0, 1.0], [0.6, 0.0, 0.0, 1.0],  # top
        [0.6, 0.0, 0.0, 1.0], [0.6, 0.0, 0.0, 1.0],  # bottom
    ]),
    edge_color='black',
    parent=view.scene
)
cube.transform = MatrixTransform()

if args.export:
    writer = imageio.get_writer(output_filename, loop=0)
    for i in range(n_steps * 2):
        if i >= n_steps:
            angle = step_angle * (i - n_steps + 1)
        else:
            angle = -step_angle * (n_steps - i)
        cube.transform.reset()
        cube.transform.rotate(angle, axis)
        im = canvas.render(alpha=True)
        writer.append_data(im)
    writer.close()
    print(f"Rendering saved to {output_filename}")
else:
    angle = [0.0]
    def update(event):
        angle[0] += 2.0
        cube.transform.reset()
        cube.transform.rotate(angle[0], axis)
        canvas.update()
    timer = Timer(interval=0.016, connect=update, start=True)
    run()
