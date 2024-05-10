## Ising Model Simulation Flask App

This Flask app simulates the behavior of the Ising model over an external magnetic field of an uploaded image. The Ising model is a mathematical model used to describe the behavior of magnetic materials, particularly how their magnetic spins interact with each other and with an external magnetic field.

### How it works:

1. **Upload Image:**
   - Users can upload an image (in .png format) to the app.
   - The uploaded image is converted into a binary representation, where pixels above a certain threshold are considered as spin up and pixels below the threshold are considered as spin down.

2. **Simulation Parameters:**
   - Users can set various simulation parameters:
     - **Temperature:** Higher temperatures introduce more randomness to the system.
     - **Number of Steps:** The number of steps in the simulation.
     - **Downsample Factor:** Determines the level of downsampling applied to the image.
     - **Initial Spin Probability:** Probability of a pixel being initially spin up.
     - **External Field Weight:** Dictates how much force the external magnetic field exerts on the system.

3. **Start Simulation:**
   - After setting the parameters and uploading an image, users can start the simulation.
   - The app runs the Ising model simulation and generates an animated GIF that visualizes the evolution of the spin configuration over time.

4. **Simulation Visualization:**
   - The animated GIF is displayed to the user, showing the changing spin configuration over the course of the simulation.

### Files and Folders:
- `app.py`: Contains the Flask application code.
- `static/`: Folder for storing static files such as images and stylesheets.
- `templates/`: Folder for storing HTML templates.
- `uploads/`: Folder for temporarily storing uploaded images.
- `requirements.txt`: Contains a list of required Python packages for running the app.
- `.gitignore`: Specifies files and folders to be ignored by Git.

### Usage Instructions:

1. **Clone the Repository:**
  
   
2. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask App:**
   ```bash
   python flask_app.py
   ```

4. **Open the Local Server:**
   - Once the app is running, open a web browser and go to `http://127.0.0.1:5000` or `http://localhost:5000`.
   - Follow the instructions on the web page to upload an image and start the simulation.

### Example Uploaded Image and Resulting GIF:

- Uploaded Image: ![Van Gogh PNG](uploads/van_gogh.png)

- Resulting GIF: ![Van Gogh Animation](static/vg_animation.gif)

### Authors:
- Dylan Esguerra
