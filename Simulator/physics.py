class PhysicsEngine:
    def __init__(self):
        self.gravity = 9.81  # m/s^2,  adjustable
        self.air_resistance_coefficient = 0.1  # Adjustable

    def apply_gravity(self, particle):
        particle.vy -= self.gravity  # Apply downward acceleration

    def apply_air_resistance(self, particle):
        # Calculate air resistance force
        air_resistance = -self.air_resistance_coefficient * particle.weight * particle.vy

        # Apply air resistance to the particle's velocity
        particle.vy += air_resistance

    def apply_physics(self, particle):
        # Apply different physics properties to the particle
        self.apply_gravity(particle)
        self.apply_air_resistance(particle)

        # You can add more physics properties here
