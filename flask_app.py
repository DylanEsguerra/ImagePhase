import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.signal import convolve2d
import matplotlib.animation as animation
import matplotlib
import secrets
matplotlib.use('agg')

app = Flask(__name__)


secret_key = secrets.token_hex(16)

app.secret_key = secret_key

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'png'}

# Define the path to the uploads and static directories
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# Class for Ising Model Simulation
class IsingSimulation:
    def __init__(self, temperature, spin_config, magnetic_field=None):
        self.size = spin_config.shape
        self.temperature = temperature
        self.spin_config = spin_config
        self.kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        self.magnetic_field = magnetic_field
        self.spins_over_time = []

    def calculate_energy(self, spin_config):
        energy = -np.sum(np.multiply(convolve2d(spin_config, self.kernel, mode='same', boundary='wrap'),spin_config)) / 2
        if self.magnetic_field is not None:
            energy += -np.sum(np.multiply(self.magnetic_field, spin_config))
        return energy

    def metropolis_step(self):
        i, j = np.random.randint(0, self.size[0]), np.random.randint(0, self.size[1])
        spin = self.spin_config[i, j]
        old_energy = self.calculate_energy(self.spin_config)
        self.spin_config[i, j] *= -1
        new_energy = self.calculate_energy(self.spin_config)
        dE = new_energy - old_energy
        if dE > 0 and np.random.rand() >= np.exp(-dE / self.temperature):
            self.spin_config[i, j] *= -1

    def simulate(self, steps):
        for _ in range(steps):
            self.metropolis_step()
            average_spin = np.mean(self.spin_config)
            self.spins_over_time.append(np.copy(self.spin_config))

# Function to update the plot for animation
def update_plot(frame, ax, sim):
    ax.cla()
    ax.imshow(sim.spins_over_time[frame], cmap='gray')
    ax.set_title(f'Step {frame}')
    ax.axis('off')

# Function to convert image to binary
def image_to_binary(image_path, pixel_threshold, downsample_factor):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    binary_array = (img_array > pixel_threshold).astype(int)
    binary_array = np.where(binary_array == 0, -1, 1)
    return binary_array[::downsample_factor, ::downsample_factor]

# Function to run the simulation
def run_simulation(image_array, temperature, num_steps, downsample_factor, initial_spin_prob, external_field_weight,pixel_threshold):
    binary_pixels = image_to_binary(image_array, pixel_threshold, downsample_factor)

    initial_state = np.random.random(binary_pixels.shape)
    lattice = np.where(initial_state >= initial_spin_prob, 1, -1)
    sim = IsingSimulation(temperature, spin_config=lattice, magnetic_field=external_field_weight * binary_pixels)
    sim.simulate(steps=num_steps)

    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(left=0.15, bottom=0.25)
    anim = animation.FuncAnimation(fig, update_plot, frames=np.arange(0, len(sim.spins_over_time), 150), fargs=(ax, sim), interval=0.001)

    animation_path = os.path.join(app.config['STATIC_FOLDER'], "simulation_animation.gif")
    anim.save(animation_path, writer='pillow')
    return animation_path

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], "uploaded_image.png")
            file.save(file_path)
            temperature = float(request.form.get('temperature', 0.5))
            num_steps = int(request.form.get('num_steps', 20000))
            downsample_factor = int(request.form.get('downsample_factor', 8))
            initial_spin_prob = float(request.form.get('initial_spin_prob', 0.5))
            external_field_weight = float(request.form.get('external_field_weight', 5))
            pixel_threshold = float(request.form.get('pixel_threshold', 125))
            return redirect(url_for('display_simulation', temperature=temperature, num_steps=num_steps,
                                    downsample_factor=downsample_factor, initial_spin_prob=initial_spin_prob,
                                    external_field_weight=external_field_weight,pixel_threshold=pixel_threshold))
        else:
            flash('Invalid file type. Please upload an image file with .png extension.')
            return redirect(request.url)
    return render_template('index.html')

# Route for displaying the simulation
@app.route('/simulation', methods=['GET', 'POST'])
def display_simulation():
    if request.method == 'POST':
        print("Form Data (POST):", request.form)
    elif request.method == 'GET':
        print("Form Data (GET):", request.args)

    temperature = float(request.args.get('temperature', 0.5))
    num_steps = int(request.args.get('num_steps', 20000))
    downsample_factor = int(request.args.get('downsample_factor', 8))
    initial_spin_prob = float(request.args.get('initial_spin_prob', 0.5))
    external_field_weight = float(request.args.get('external_field_weight', 5))
    pixel_threshold = float(request.args.get('pixel_threshold', 125))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], "uploaded_image.png")

    if not os.path.exists(file_path):
        flash('Uploaded file not found.')
        return redirect(url_for('index'))

    try:
        animation = run_simulation(file_path, temperature, num_steps, downsample_factor, initial_spin_prob, external_field_weight, pixel_threshold)
        return send_file(animation, mimetype='image/gif')
    except Exception as e:
        flash(f'Error in simulation: {str(e)}')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
