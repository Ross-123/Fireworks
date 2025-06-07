# Fireworks
Interactive fireworks simulation built with Pygame

This project is an interactive fireworks simulation built with Pygame. The animation features colorful fireworks that launch from the bottom of the screen, ascend with realistic motion, explode into particle systems, and gradually fade out. The simulation includes sound effects for both the launch whistle and explosion sounds.

Key Features
Realistic Firework Physics:
  Vertical launch trajectory with gravity effects
  Randomized explosion patterns
  Particle fading and decay
  Gravity-influenced particle movement
  Dynamic Visual Effects:
  Random color generation for each firework
  Particle transparency effects (alpha blending)
  Smooth particle dispersion in circular patterns
  Size variation in explosion particles

Sound Integration:

  Whistle sound during firework ascent
  Explosion sound effect on detonation
  Background sound looping capability
  Graceful sound resource management
  Autonomous Simulation:
  Random firework generation (1/20 chance per frame)
  Automatic cleanup of expired particles
  Continuous animation cycle at 60 FPS
  Self-contained runtime environment

Technical Implementation
  Object-oriented design with Firework and Particle classes
  Memory-efficient sound handling using io.BytesIO
  Graceful degradation for missing sound files
  Physics-based particle movement (velocity + gravity)
  Alpha-blended rendering for smooth particle fading
