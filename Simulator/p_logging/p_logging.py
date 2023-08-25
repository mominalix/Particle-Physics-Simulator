class ParticleLogger:
    def __init__(self, log_file):
        self.log_file = log_file

    def log_particle_path(self, particle):
        with open(self.log_file, 'a') as f:
            f.write(f"Particle: ({particle.x}, {particle.y}, {particle.z})\n")

    # Implement other logging methods as needed
