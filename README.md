# **8 Ball Pool**

## **Description**

This project is a 2D rendition of the popular cue sport, **8-ball pool**. The game incorporates sprite animations to give the illusion of 3D ball movement, along with realistic physics based on shot power, point of impact, and collisions with other balls and walls.

The game is a **two-player competitive game** where each player aims to pocket all their designated balls and then legally pocket the 8 ball to win.

### **Features**

- **Physics-based gameplay:** Realistic ball movement and collisions.
- **Customizable settings:**
  - Adjust sound volume.
  - Toggle **cueball travel path** and **collision path** visualization.
  - Enable/disable a **debug mode**.
- **Debug Mode:**
  - Pause and step through game states.
  - Visualize collision shapes.
  - Quickly set up specific scenarios for testing.

---

## **Gamemodes**

- **Eight-Ball Pool:** Standard rules for two-player gameplay.
- **Practice Mode:** Hone your skills with these adjustable options:
  - Adjustable shot power.
  - Select different rack sizes.
  - Move balls freely to test scenarios.

---

## **How to Play**

1. **Run the program:**
   Execute the game using `main.py`.
2. **External Files Required:**
   Download additional resources from ...
3. **Install Required Library:**

   ```bash
   pip install numpy
   ```
### **Shortcut Commands**

- **Escape:** Access pause menu.
- **Debug Mode (toggle in settings):**
  - `P`: Pause the game.
  - `O`: Show collision shapes.
  - `L`: Set up a small ball scenario to test endgame conditions.
  - `Enter`: Step through the game manually.

---

## **Sprites**

- [Sprite Sheet 1](https://www.spriters-resource.com/nes/breaktime/sheet/207842/)
- [Sprite Sheet 2](https://www.spriters-resource.com/nes/breaktime/sheet/64047/)

## **Font**

- [Edit Undo Font](https://www.1001fonts.com/edit-undo-font.html)

## **Music and Sound Effects**

- [8-Bit Music Anthology - NES Edition](https://bbunker.itch.io/8-bit-music-anthology-nes-edition)
- [8-Bit SFX and Music Pack](https://hunteraudio.itch.io/8bit-sfx-and-music-pack)

---

## **Resources Used**

- **Physics**:
  - [Elastic Collision](https://en.wikipedia.org/wiki/Elastic_collision)
- **Geometry**:
  - [Line-Line Intersection](https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection)
  - [Circle-Line Collision Detection](https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm)
  - [Circle-Inside-Circle Collision](https://gamedev.stackexchange.com/questions/29650/circle-inside-circle-collision)
- **Linear Algebra**:
  - [Rotation Matrix](https://en.wikipedia.org/wiki/Rotation_matrix)
  - [Perpendicular Vector](https://mathworld.wolfram.com/PerpendicularVector.html)
- **Tutorials and Guides**:
  - [Physics of Pool Balls](https://www.youtube.com/watch?v=dJNFPv9Mj-Y)

---
