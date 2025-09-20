import argparse
import imageio
import numpy as np
from vispy import scene
from vispy.visuals.transforms import MatrixTransform
from vispy.app import run, Timer
from vispy.scene import visuals

output_filename = 'renders/rotating_fish_mesh.gif'
n_steps = 18
step_angle = 10.0
axis = [0.0, 1.0, 0.0]

parser = argparse.ArgumentParser(description="Display or export a rotating fish mesh.")
parser.add_argument('--export', action='store_true', help='Export rendering as GIF')
args = parser.parse_args()

canvas = scene.SceneCanvas(keys='interactive', bgcolor='white', size=(600, 600), show=True)
view = canvas.central_widget.add_view()
view.camera = scene.cameras.TurntableCamera(fov=45, center=(0,0,0))
view.camera.elevation = 90
view.camera.azimuth = -45
view.camera.distance = 3.5

# body
phi, theta = np.mgrid[0:np.pi:20j, 0:2*np.pi:20j]
x = 1.0 * np.sin(phi) * np.cos(theta)
y = 0.3 * np.sin(phi) * np.sin(theta)
z = 0.2 * np.cos(phi)
vertices_body = np.stack([x, y, z], axis=-1).reshape(-1, 3)

faces_body = []
rows, cols = phi.shape
for i in range(rows-1):
    for j in range(cols-1):
        a = i*cols + j
        b = a + cols
        faces_body.append([a, b, a+1])
        faces_body.append([b, b+1, a+1])
faces_body = np.array(faces_body, dtype=np.uint32)

# tail
base = np.array([[-1.0, 0, 0],
                 [-1.3, -0.3, 0],
                 [-1.3,  0.3, 0]], dtype=np.float32)
z_offset = 0.075
vertices_tail = np.vstack([base - [0,0,z_offset/2], base + [0,0,z_offset/2]])
faces_tail = np.array([
    [0,1,2], [3,5,4],           # front/back
    [0,1,4], [1,4,3],           # bottom side
    [1,2,5], [1,5,4],           # right side
    [2,0,3], [2,3,5],           # top side
], dtype=np.uint32) + vertices_body.shape[0]

vertices = np.vstack([vertices_body, vertices_tail])
faces = np.vstack([faces_body, faces_tail])

colors_body = np.tile(np.array([1.0,0.2,0.2,1.0], dtype=np.float32), (vertices_body.shape[0],1))
colors_tail = np.tile(np.array([0.8,0.2,0.2,1.0], dtype=np.float32), (vertices_tail.shape[0],1))
vertex_colors = np.vstack([colors_body, colors_tail])

fish = visuals.Mesh(vertices=vertices, faces=faces, vertex_colors=vertex_colors, shading='smooth', parent=view.scene)
fish.transform = MatrixTransform()

if args.export:
    import os
    os.makedirs('renders', exist_ok=True)
    writer = imageio.get_writer(output_filename, mode='I', loop=0)
    for i in range(n_steps * 2):
        if i >= n_steps:
            angle = step_angle * (i - n_steps + 1)
        else:
            angle = -step_angle * (n_steps - i)
        fish.transform.reset()
        fish.transform.rotate(angle, axis)
        canvas.context.clear(color=True, depth=True)
        im = canvas.render(alpha=True)
        writer.append_data(im)
    writer.close()
    print(f"Rendering saved to {output_filename}")
else:
    angle = [0.0]
    def update(event):
        angle[0] += 2.0
        fish.transform.reset()
        fish.transform.rotate(angle[0], axis)
        canvas.update()
    timer = Timer(interval=0.016, connect=update, start=True)
    run()
