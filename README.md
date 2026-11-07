# Gesture Media Control

Two historical webcam/desktop-input experiments. This is an early computer-vision
prototype archive, separate from the later HANDORA system.

## Experiments

- `motion_gestures.py`: background subtraction and contour-centre history.
  Sideways movement sends Ctrl+Left/Right; a steady position sends Space.
- `yolo_hand_control.py`: loads your local `best.pt` Ultralytics model and looks
  for a class containing `hand`, then sends a media shortcut.

Both scripts open the camera and generate real keyboard input. They run their
loops at module level; importing them is not a safe side-effect-free smoke test.
The YOLO weights are not included and must be trusted, compatible hand-detection
weights, not an arbitrary file renamed `best.pt`.

## Local experiment setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python motion_gestures.py
# Or, after supplying a trusted model: python yolo_hand_control.py
```

Use a desktop session with camera permissions and, where required, accessibility
permissions. Check the active application's shortcut behavior first. Press `q`
to quit; `r` resets the background in the motion experiment. Illumination,
background movement, camera placement and the active application affect results.

## Validation and privacy

The audit parsed the source but did not open a webcam, load an external model or
send keyboard commands. There is no automated functional suite or verified
cross-platform detection benchmark. Test manually with synthetic/local scenes
you are permitted to capture, and do not commit recordings, personal images or
model files whose distribution rights you do not hold.

## License

No license file is included; no new license grant is asserted. Author: [Muhammet Fatih Çetintaş](https://github.com/M-Fatih-C).
