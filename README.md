# Space Shooter

A 2D space survival shooter made with Python and Pygame.

Meteor storms are destroying Earth. Help the last dinosaurs escape through space in their spaceship. Destroy meteors, collect resources, manage your fuel, and survive for as long as possible.

## Play Online

[Click here to play the game](https://yashnooo.github.io/space-shooter-game/)

Press **Space** if the game is waiting to start.

[Watch a video of the game](https://cdn.hackclub.com/01a0d448-31bb-78c4-bc49-3c9f1aa16097/Screencast%20From%202026-09-24%2022-06-32.mp4)

## Controls

| Key | Action |
|---|---|
| Arrow Keys | Move the spaceship |
| Space | Start the game and fire lasers |

## Features

- Spaceship movement in four directions
- Laser shooting with a cooldown
- Randomly falling and rotating meteors
- Explosion animations and sound effects
- Background music
- Three-heart health system
- Survival score counter
- Randomly falling coins with a coin counter
- Fuel system that continuously decreases
- Fuel pickups restore 25% fuel
- Shield power-up gives six seconds of protection
- Health power-up restores one heart when health is below three
- Game ends when health or fuel reaches zero

## Power-Ups and Collectibles

### Shield

A shield power-up appears every 10 seconds. Collecting it protects the spaceship from meteor damage for six seconds.

### Health

A health power-up appears every 20 seconds. It restores one heart when the player has fewer than three hearts.

### Fuel

Fuel continuously decreases during the game. Fuel pickups appear every 12 seconds and restore 25% fuel, up to a maximum of 100%.

### Coins

Coins continuously fall from random positions. Collect them to increase the coin counter.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/yashNooo/space-shooter-game.git
cd space-shooter-game
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Pygame-ce

```bash
pip install pygame-ce
```

### 4. Run the game

```bash
python3 main.py
```

## Technologies Used

- Python
- Pygame-ce
- Pygbag
- GitHub Pages

## Project Structure

```text
space-shooter-game/
├── galary/
│   ├── audio/
│   └── images/
├── build/
│   └── web/
├── docs/                 # Browser build used by GitHub Pages
├── main.py               # Local game
├── main-pygbag.py        # Browser-compatible game
└── README.md
```

## Author

Made by [Yash Jain](https://github.com/yashNooo)
