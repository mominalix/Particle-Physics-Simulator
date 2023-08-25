# Particle Physics Simulation with Gravitational Effects

This repository contains a simple particle physics simulation that demonstrates the behavior of particles with gravitational effects. The simulation is implemented using Pygame for visualization and PyOpenGL for rendering.

## Prerequisites

- Python 3.x
- Pygame (install using `pip install pygame`)
- PyOpenGL (install using `pip install PyOpenGL`)

## How to Run

1. Clone the repository to your local machine using Git or download the ZIP file.

2. Open a terminal or command prompt and navigate to the repository's directory.

3. Run the simulation script using the one of the following commands:

    ```
    python random_particle_simulation_2d.py
    python random_particle_simulation_3d.py
    ```

4. The simulation window will open, and you'll see particles moving and interacting with gravitational effects.

5. To exit the simulation, simply close the window.

## Functionality

The simulation showcases the following functionalities:

- Particles: A number of particles are generated randomly on the screen, each with a random weight, initial position, and velocity.

- Gravitational Effects: Particles experience a simplified form of gravitational interaction. As particles cross each other, their velocities and directions are affected by the gravitational pull based on their weights.

- Bouncing off Borders: The particles bounce off the borders of the simulation window, creating a bouncing effect when they reach the edges.


