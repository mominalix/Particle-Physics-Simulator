import config
class CPUSimulation:
    def __init__(self, particles, physics_engine):
        self.particles = particles
        self.physics_engine = physics_engine

    def simulate(self):
        time_step = config.simulation_parameters['time_step']
        simulation_duration = config.simulation_parameters['simulation_duration']

        num_steps = int(simulation_duration / time_step)
        for step in range(num_steps):
            for particle in self.particles:
                self.physics_engine.apply_physics(particle)
                particle.x += particle.vx * time_step
                particle.y += particle.vy * time_step
                particle.z += particle.vz * time_step
