from ai_integration import extract_scenario
from config import backend_choices
from particle import Particle
from physics import PhysicsEngine
from simulation.simulation_cuda import CudaSimulation
from simulation.simulation_opencl import OpenCLSimulation
from simulation.simulation_cpu import CPUSimulation
from visualization import Visualization
from logging.logging import ParticleLogger

def main():
    # Get scenario from user input
    prompt = input("Enter the scenario: ")
    parsed_scenario = extract_scenario(prompt)

    # Initialize particles, physics engine, and chosen backend
    particles = [Particle(**particle_data) for particle_data in parsed_scenario['particles']]
    physics_engine = PhysicsEngine()
    backend_choice = input("Choose backend (CUDA/OpenCL/CPU): ")

    if backend_choice not in backend_choices:
        print("Invalid backend choice")
        return

    if backend_choice == 'CUDA':
        simulation = CudaSimulation(particles, physics_engine)
    elif backend_choice == 'OpenCL':
        simulation = OpenCLSimulation(particles, physics_engine)
    else:
        simulation = CPUSimulation(particles, physics_engine)

    # Run simulation and visualization
    simulation.simulate()
    visualization = Visualization()
    for particle in particles:
        visualization.draw_particle_trace(particle)

    # Log particle paths
    logger = ParticleLogger("particle_paths.log")
    for particle in particles:
        logger.log_particle_path(particle)

if __name__ == "__main__":
    main()
