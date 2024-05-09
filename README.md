**Ising Model Simulation Flask App**

This Flask app simulates the behavior of the Ising model over an external magnetic field of an uploaded image. The Ising model is a mathematical model used to describe the behavior of magnetic materials, particularly how their magnetic spins interact with each other and with an external magnetic field.

**How it works:**

1. **Upload Image:**
   - Users can upload an image (in .png, .jpg, or .jpeg format) to the app.
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

**Files and Folders:**
- `app.py`: Contains the Flask application code.
- `static/`: Folder for storing static files such as images and stylesheets.
- `templates/`: Folder for storing HTML templates.
- `uploads/`: Folder for temporarily storing uploaded images.
- `requirements.txt`: Contains a list of required Python packages for running the app.
- `.gitignore`: Specifies files and folders to be ignored by Git.


**Authors:**
- Dylan Esguerra 
