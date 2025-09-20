import argparse
import imageio
import numpy as np
from vispy import scene
from vispy.visuals.transforms import MatrixTransform
from vispy.app import run, Timer
from vispy.scene import visuals

output_filename = 'renders/rotating_cube_mesh.gif'
n_steps = 18
step_angle = 10.0
axis = [0.25, 0.5, 1.0]

parser = argparse.ArgumentParser(description="Display or export a rotating cube mesh.")
parser.add_argument('--export', action='store_true', help='Export rendering as GIF')
args = parser.parse_args()

canvas = scene.SceneCanvas(keys='interactive', bgcolor='white', size=(600, 600), show=True)
view = canvas.central_widget.add_view()
view.camera = 'arcball'

vertices = np.array([
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1],
], dtype=np.float32)

faces = np.array([
    [0,1,2], [0,2,3],  # back
    [4,5,6], [4,6,7],  # front
    [0,1,5], [0,5,4],  # bottom
    [2,3,7], [2,7,6],  # top
    [1,2,6], [1,6,5],  # right
    [0,3,7], [0,7,4],  # left
], dtype=np.uint32)

vertex_colors = np.array([
    [1.0,0.2,0.2,1.0], 
    [1.0,0.2,0.2,1.0], 
    [0.8,0.2,0.2,1.0],  
    [0.8,0.2,0.2,1.0], 
    [1.0,0.2,0.2,1.0], 
    [1.0,0.2,0.2,1.0], 
    [0.2,0.2,0.2,1.0],
    [0.2,0.2,0.2,1.0], 
], dtype=np.float32)

cube = visuals.Mesh(vertices=vertices, faces=faces, vertex_colors=vertex_colors,
                    shading='smooth', parent=view.scene)
cube.transform = MatrixTransform()

if args.export:
    writer = imageio.get_writer(output_filename, mode='I', loop=0)
    for i in range(n_steps * 2):
        if i >= n_steps:
            angle = step_angle * (i - n_steps + 1)
        else:
            angle = -step_angle * (n_steps - i)
        cube.transform.reset()
        cube.transform.rotate(angle, axis)
        canvas.context.clear(color=True, depth=True)
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
