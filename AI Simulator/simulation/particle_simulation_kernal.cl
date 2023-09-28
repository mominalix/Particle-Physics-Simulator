// Define the data structure for a particle
typedef struct {
    float x, y, z;
    float vx, vy, vz;
    float weight;
} Particle;

// Kernel to simulate particle motion
__kernel void simulate_particles(__global Particle* particles, float time_step) {
    int particle_id = get_global_id(0);  // Get the particle index

    // Retrieve the particle's data
    Particle particle = particles[particle_id];

    // Applying physics calculations
    // Apply gravity (negative acceleration in y direction)
    particle.vy -= 9.81f * time_step;

    // Apply air resistance
    float air_resistance = -0.1f * particle.weight * particle.vy;
    particle.vy += air_resistance * time_step;

    // Update particle position based on velocity
    particle.x += particle.vx * time_step;
    particle.y += particle.vy * time_step;
    particle.z += particle.vz * time_step;

    // Store the updated particle data back to global memory
    particles[particle_id] = particle;
}
