import pyopencl as cl
import numpy as np
import config

class OpenCLSimulation:
    def __init__(self, particles, physics_engine):
        self.particles = particles
        self.physics_engine = physics_engine

        # Create an OpenCL context and command queue
        platform = cl.get_platforms()[0]  # Use the first OpenCL platform
        device = platform.get_devices()[0]  # Use the first device on the platform
        self.ctx = cl.Context([device])
        self.queue = cl.CommandQueue(self.ctx)

        # Load and compile the OpenCL program (You should have a .cl file with your kernel)
        with open('particle_simulation_kernel.cl', 'r') as kernel_file:
            kernel_source = kernel_file.read()
        self.program = cl.Program(self.ctx, kernel_source).build()

        # Create OpenCL buffers for particle data
        self.particles_buffer = cl.Buffer(self.ctx, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR,
                                          hostbuf=np.array(particles, dtype=np.float32))

    def simulate(self):
        time_step = config.simulation_parameters['time_step']
        simulation_duration = config.simulation_parameters['simulation_duration']

        num_steps = int(simulation_duration / time_step)
        for step in range(num_steps):
            self.program.simulate_particles(self.queue, (len(self.particles),), None,
                                            self.particles_buffer, np.float32(time_step))
            
            cl.enqueue_copy(self.queue, self.particles, self.particles_buffer).wait()

            for particle in self.particles:
                self.physics_engine.apply_physics(particle)
