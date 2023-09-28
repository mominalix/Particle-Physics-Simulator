# Particle Physics Simulation

This is a Python-based particle physics simulation program that allows you to create and simulate scenarios involving particles with various properties. You can choose from different simulation backends, such as CUDA, OpenCL, or CPU, and customize the scenarios using an AI-powered prompt.

## Table of Contents

- [Particle Physics Simulation](#particle-physics-simulation)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Functionality](#functionality)
  - [Contributing](#contributing)

## Prerequisites

Before you can run this program, you need to have the following dependencies installed on your system:

- Python 3.x
- PyQt5
- PyOpenCL (if using OpenCL backend)
- Pygame (for visualization)
- OpenAI Python library (for AI integration)

You also need to obtain an API key from OpenAI and save it in a file named `apikey.txt` located in the project folder.

## Installation

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/mominalix/Particle-Physics-Simulation.git
   ```

2. Install the required Python packages using pip:

   ```shell
   pip install PyQt5 PyOpenCL pygame openai
   ```

3. Save your OpenAI API key in a file named `apikey.txt` in the project folder.

## Usage

To run the simulation program, follow these steps:

1. Open a terminal and navigate to the project folder.

2. Run the main.py script:

   ```shell
   python main.py
   ```

3. The Particle Simulator application window will open. You can enter a scenario description in the input field and select the simulation backend (CUDA, OpenCL, or CPU).

4. Click the "Run Simulation" button to start the simulation.

5. The simulation results will be displayed in a 3D visualization window. The particle paths will be recorded in a log file named "particle_paths.log."

## Functionality

- **Scenario Input**: You can describe the scenario you want to simulate in plain text using the input prompt. The program uses OpenAI's API to generate the initial conditions for the simulation based on your description.

- **Backend Selection**: You can choose the simulation backend (CUDA, OpenCL, or CPU) to perform the calculations. Each backend uses different technologies for simulation.

- **Customizable Particles**: The scenarios are customizable, allowing you to define the number of particles, their positions, velocities, and weights. The program generates initial conditions based on your input.

- **Physics Properties**: The simulation includes physics properties like gravity and air resistance. You can customize these properties or turn them on/off.

- **Visualization**: The program provides a 3D visualization of the particle paths. You can see how particles move and interact in the simulated environment.

- **Logging**: Simulation data, including particle paths, is recorded in log files for further analysis.

## Contributing

Contributions to this project are welcome. You can contribute by reporting issues, suggesting improvements, or submitting pull requests. Please follow the project's coding standards and guidelines.
