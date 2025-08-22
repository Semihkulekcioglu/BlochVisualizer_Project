import argparse
from typing import List, Optional, Sequence, Tuple

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt


SUPPORTED_GATES = {
	"H": "H",
	"X": "X",
	"Y": "Y",
	"Z": "Z",
	"S": "S",
	"T": "T",
	"RX": "RX",
	"RY": "RY",
	"RZ": "RZ",
}


def apply_gate(circuit: QuantumCircuit, gate: str, angle: Optional[float] = None) -> None:
	g = gate.upper()
	if g == "H":
		circuit.h(0)
	elif g == "X":
		circuit.x(0)
	elif g == "Y":
		circuit.y(0)
	elif g == "Z":
		circuit.z(0)
	elif g == "S":
		circuit.s(0)
	elif g == "T":
		circuit.t(0)
	elif g == "RX":
		if angle is None:
			raise ValueError("RX requires --angle")
		circuit.rx(angle, 0)
	elif g == "RY":
		if angle is None:
			raise ValueError("RY requires --angle")
		circuit.ry(angle, 0)
	elif g == "RZ":
		if angle is None:
			raise ValueError("RZ requires --angle")
		circuit.rz(angle, 0)
	else:
		raise ValueError(f"Unsupported gate: {gate}")


def statevector_to_bloch_vector(state: Statevector) -> List[float]:
	vec = np.asarray(state.data, dtype=np.complex128).flatten()
	if vec.shape[0] != 2:
		raise ValueError("Only single-qubit states are supported.")
	alpha = vec[0]
	beta = vec[1]
	x = 2.0 * np.real(np.conjugate(alpha) * beta)
	y = 2.0 * np.imag(np.conjugate(alpha) * beta)
	z = np.abs(alpha) ** 2 - np.abs(beta) ** 2
	return [float(x), float(y), float(z)]


def plot_bloch(state: Statevector, save_path: Optional[str] = None) -> None:
	bloch_vector = statevector_to_bloch_vector(state)
	ax = plot_bloch_vector(bloch_vector)
	fig = ax.get_figure()
	if save_path:
		fig.savefig(save_path, bbox_inches="tight", dpi=150)
		plt.close(fig)
	else:
		plt.show()


def plot_bloch_trajectory(states: Sequence[Statevector], save_path: Optional[str] = None) -> None:
	# Draw a base Bloch sphere, then overlay arrows for each state
	# Start sphere with initial |0> vector so axes are created
	base_ax = plot_bloch_vector([0.0, 0.0, 1.0])
	fig = base_ax.get_figure()

	# Overlay all state vectors
	for idx, st in enumerate(states):
		vx, vy, vz = statevector_to_bloch_vector(st)
		# Use varying colors for visibility
		color = "C0" if idx == 0 else f"C{(idx % 9) + 1}"
		base_ax.quiver(0, 0, 0, vx, vy, vz, length=1.0, normalize=False, color=color, linewidth=1.5)
		base_ax.scatter([vx], [vy], [vz], color=color, s=20)

	if save_path:
		fig.savefig(save_path, bbox_inches="tight", dpi=150)
		plt.close(fig)
	else:
		plt.show()


def parse_sequence(seq_text: str) -> List[Tuple[str, Optional[float]]]:
	# Example token forms: "H", "RX:1.5708", "rz:-0.5"
	if not seq_text:
		return []
	tokens = [t.strip() for t in seq_text.split(",") if t.strip()]
	result: List[Tuple[str, Optional[float]]] = []
	for token in tokens:
		if ":" in token:
			name, angle_text = token.split(":", 1)
			gate = name.strip().upper()
			try:
				angle = float(angle_text)
			except ValueError:
				raise ValueError(f"Invalid angle in token '{token}'")
			result.append((gate, angle))
		else:
			result.append((token.strip().upper(), None))
	return result


def build_circuit(gate: Optional[str], angle: Optional[float]) -> QuantumCircuit:
	qc = QuantumCircuit(1)
	if gate is not None:
		apply_gate(qc, gate, angle)
	return qc


def build_circuit_from_sequence(ops: Sequence[Tuple[str, Optional[float]]]) -> QuantumCircuit:
	qc = QuantumCircuit(1)
	for gate, angle in ops:
		apply_gate(qc, gate, angle)
	return qc


def states_after_each_step(ops: Sequence[Tuple[str, Optional[float]]]) -> List[Statevector]:
	# Includes initial |0> state as first element
	states: List[Statevector] = [Statevector.from_label("0")]
	qc = QuantumCircuit(1)
	for gate, angle in ops:
		apply_gate(qc, gate, angle)
		states.append(Statevector.from_instruction(qc))
	return states


def main() -> None:
	parser = argparse.ArgumentParser(description="Bloch sphere visualizer with step-by-step support")
	parser.add_argument("--gate", type=str, choices=sorted(SUPPORTED_GATES.keys()), default=None, help="Single-qubit gate to apply")
	parser.add_argument("--angle", type=float, default=None, help="Angle (radians) for rotation gates RX/RY/RZ")
	parser.add_argument("--sequence", type=str, default=None, help="Comma-separated gate list, e.g. 'H,RY:1.57,RZ:0.5,X'")
	parser.add_argument("--trajectory", action="store_true", help="Plot trajectory with all intermediate steps")
	parser.add_argument("--save", type=str, default=None, help="Save final plot to file instead of showing window")
	parser.add_argument("--save-steps", type=str, default=None, help="Directory path to save per-step plots")
	args = parser.parse_args()

	if args.sequence:
		ops = parse_sequence(args.sequence)
		# Validate angles for rotation gates
		for g, a in ops:
			if g in ("RX", "RY", "RZ") and a is None:
				raise ValueError(f"Gate {g} requires an angle in sequence, e.g. {g}:1.5708")

		if args.trajectory:
			states = states_after_each_step(ops)
			plot_bloch_trajectory(states, args.save)
		else:
			qc = build_circuit_from_sequence(ops)
			state = Statevector.from_instruction(qc)
			plot_bloch(state, args.save)

		# Optionally save each step as separate image
		if args.save_steps:
			states = states_after_each_step(ops)
			for idx, st in enumerate(states):
				# Step 0 is the initial |0> state
				path = f"{args.save_steps}\\step_{idx:02d}.png"
				plot_bloch(st, path)
	else:
		# Single-gate mode (or no gate -> initial state)
		qc = build_circuit(args.gate, args.angle)
		state = Statevector.from_instruction(qc)
		plot_bloch(state, args.save)


if __name__ == "__main__":
	main()


