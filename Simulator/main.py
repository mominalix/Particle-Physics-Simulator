from ai_integration import extract_scenario
from config import backend_choices
from particle import Particle
from physics import PhysicsEngine
from simulation.simulation_cuda import CudaSimulation
from simulation.simulation_opencl import OpenCLSimulation
from simulation.simulation_cpu import CPUSimulation
from visualization.Visualization import Visualization
from p_logging.p_logging import ParticleLogger
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox, QLineEdit

class ParticleSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Particle Simulator")
        self.setGeometry(100, 100, 600, 400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.scenario_label = QLabel("Enter the scenario:")
        layout.addWidget(self.scenario_label)

        self.scenario_input = QLineEdit()
        layout.addWidget(self.scenario_input)

        self.backend_label = QLabel("Choose backend:")
        layout.addWidget(self.backend_label)

        self.backend_combo = QComboBox()
        self.backend_combo.addItems(backend_choices)
        layout.addWidget(self.backend_combo)

        self.run_simulation_button = QPushButton("Run Simulation")
        self.run_simulation_button.clicked.connect(self.run_simulation)
        layout.addWidget(self.run_simulation_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def run_simulation(self):
        prompt = self.scenario_input.text()
        parsed_scenario = extract_scenario(prompt)

        particles = [Particle(**particle_data) for particle_data in parsed_scenario['particles']]
        physics_engine = PhysicsEngine()
        backend_choice = self.backend_combo.currentText()

        if backend_choice not in backend_choices:
            print("Invalid backend choice")
            return

        if backend_choice == 'CUDA':
            simulation = CudaSimulation(particles, physics_engine)
        elif backend_choice == 'OpenCL':
            simulation = OpenCLSimulation(particles, physics_engine)
        else:
            simulation = CPUSimulation(particles, physics_engine)

        simulation.simulate()
        visualization = Visualization()
        for particle in particles:
            visualization.draw_particle_trace(particle)

        logger = ParticleLogger("particle_paths.log")
        for particle in particles:
            logger.log_particle_path(particle)

def main():
    app = QApplication(sys.argv)
    window = ParticleSimulatorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
