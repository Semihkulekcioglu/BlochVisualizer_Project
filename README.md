# Bloch Visualizer

A compact, single-qubit Bloch sphere visualizer for education and rapid prototyping. Apply elementary gates (`H, X, Y, Z, S, T`) and rotation gates with angles (`RX, RY, RZ`), visualize the final state, or plot the full trajectory across a gate sequence. Optionally export step-by-step images for reports or teaching material.

## Features
- Visualize a single-qubit state as a vector on the Bloch sphere
- Gate sequences with per-gate angles, e.g. `--sequence "H,RY:1.5708,RZ:0.5,X"`
- Trajectory plotting across all intermediate states (`--trajectory`)
- Export each step to images (`--save-steps <dir>`)
- Save final visualization to an image file (`--save <file>`) or display interactively

## Requirements
- Python 3.9+
- Packages: listed in `requirements.txt`

## Installation
```bash
# From repository root
cd BlochVisualizer
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Quick Start
- Single gate, save to file:
```bash
python bloch_visualizer.py --gate H --save demo.png
```
- Gate sequence, show final state only:
```bash
python bloch_visualizer.py --sequence "H,RY:1.5708,RZ:0.5,X" --save final.png
```
- Trajectory over all intermediate states and save steps:
```bash
python bloch_visualizer.py --sequence "H,RY:1.5708,RZ:0.5,X" --trajectory --save-steps steps
```
- Interactive window (no file saved):
```bash
python bloch_visualizer.py --gate H
```

## CLI Reference
```text
optional arguments:
  --gate {H,X,Y,Z,S,T,RX,RY,RZ}
        Single-qubit gate to apply (use with --angle for RX/RY/RZ).
  --angle FLOAT
        Angle in radians for rotation gates RX/RY/RZ.
  --sequence STRING
        Comma-separated gates; angles with colon, e.g. "H,RY:1.57,RZ:0.5".
  --trajectory
        Plot all intermediate states as a trajectory on the same sphere.
  --save FILE
        Save the (single) visualization to FILE instead of showing a window.
  --save-steps DIR
        Save each intermediate step as PNG in DIR (created if missing).
```

## Output
<img width="640" height="640" alt="Ekran Görüntüsü (753)" src="https://github.com/user-attachments/assets/2e41d2f5-4124-4c89-a252-2b7c3a63f57f" />

## Notes
- Scope: single-qubit states; measurement, noise, and multi-qubit are out of scope.
- Compatibility: uses matplotlib-based plotting to work across Qiskit versions.

## License
MIT License — see `LICENSE`.
