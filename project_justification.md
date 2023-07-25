In The Shadows
By Rama Janco, Deven Ellis, Ryan Lewis, Jason Baron, and Carson Sobolewski

Below are the reasonings for why we believe our code deserves points for each category in the rubric.


# INTERFACE 

## Element Visibility

All the elements are clearly visible because we used high-contrast colors and large text so that all the intractable elements are visible. 
Additionally, all the tile designs for the game are designed to be easily distinguishable from each other so players cannot get any tiles confused with each other.
The items and instructions are displayed with enough spacing to be clear and easily read.

## Element Usability

All of the elements are usable because all the buttons that can be clicked light up when the mouse hovers over them, so the user knows which components are functional and which are not.
Additionally, the controls are displayed on the screen so the user knows how to interact with the game, and the items are displayed on the screen so the user knows what items they have available to them.

## Intuitiveness
We believe all the elements are intuitive because our game has no special controls that are unique to it, so the user can use the same controls they would use in any other game.
Additionally, the controls are all displayed on the screen which the option to use WASD or the arrow keys, which allows the user to use whatever they're most comfortable with.

## Consistency 
We believe all the elements are consistent because the same person designed every graphic, so the art style is consistent throughout the game.
Additionally, every text box uses the same font and color, giving the game a uniform and consistent feel.

## Status Visibility
We believe all the elements are visible because we implemented a HUD at the bottom of the screen when the player is in the game.
The HUD is designed to display everything the player needs to know while playing the game.


# NAVIGATION 

## Mechanics / API

We believe all the elements and mechanics are intuitive because we used the same controls as any other game
and explain how to use the objects in our game when the user picks them up.
Additionally, the controls are displayed on the screen so the user knows how to interact with the game
and the items are displayed on the screen so the user knows what items they have available.

## Tested / Not Buggy

We believe all the elements are thorough and not buggy tested because we have most,
if not, all the code that can cause a crash in the game is wrapped with a try-except clause to ensure a consistent experience for the user.
Additionally, we have tested the game multiple times in various unorthodox edge cases to ensure that the game is not buggy and that the user can play the game without any issues.

## Minimal Acclimation

The elements in our game require minimal acclimation because the controls for the game are what anybody would expect and are clearly defined in the instructions.
We use the arrow keys for people to assume to use but also allow for WASD input for people more accustomed to other PC games.
The game's mechanics do not require the most acclimation either because they are explained in simple terms, and the concept behind all of them is simple.

## Predictability

We believe the elements in our game are predictable because the guard paths and levels are all predefined so that the levels will react the same way every single play-through.
The user input can be changed to whatever the player wants, and the guards pathing and actions will remain the same for any repeated input.

## Discoverability

We believe the elements in our game are discoverable because the items are very easily accessible to the player, and the instructions on how to use them are shown to the player every time they pick one up.
Additionally, levels increase in difficulty and require different items and techniques to complete the level, so the player is forced to discover how to use the items to beat the level.


# USER PERCEPTION 

## Enjoyability
Our game is enjoyable because the soundtrack and gameplay are simple, and accomplishing the tasks in the game is satisfying because it takes effort to complete them.

## Minimal Frustration
Our game is minimally frustrating because the mechanics are all simple, and the game is not designed to be overly tricky and unfair.
It is more strategic than other games because the player has to think about what they are doing, but it is not designed to be frustrating.

## General Usability
We believe our game is generally usable because of the high-contrast UI. In addition to supporting multiple input modes, make this game accessible to a wide range of people.
Color blindness or other issues should not be an issue because the colors are easily distinguishable, and the audio cues are all supported with visual updates.


# RESPONSIVENESS 

## Action Indications / Non-Blocking

Our game has a clear indicator of the action going on in the game.
This is because of our HUD on the bottom of our screen. The left side of the HUD tells the player if they have any abilities or items ready to use.

## State Indications

Our game clearly indicates the state because the HUD at the bottom of the screen tells the player what state the game is in.
The right side of the HUD tells the player what the current object is and changes based on what step and level the character is on.

## Task Success

Our game makes it extremely clear when the player has won because it will stop and display a message saying, "You Win!"

## Task failure

Our game makes it extremely clear when the player has lost because it will stop and display a message saying, "Game Over."


# BUILD QUALITY 

## Robustness
Our game is robust because our code was written with error-checking and handling in mind.
Every time any coordinates are called, they are wrapped in a try/except clause to ensure there is no way an out-of-bounds error can crash the game.
Additionally, we leveraged predefined levels, which are designed to be impossible to break because they are surrounded by walls that cannot be passed.
This results in a game where any user input cannot result in a crash from the user's actions; there may be bugs from other functions that are out of the player's control.
The game was also tested on all three major operating systems (Windows, Mac, and Linux) to ensure it would run on any system.

## Consistency

Our game is consistent because we used a consistent naming scheme for all our variables and functions.
These rules were enforced by a GitHub task on push, so every coder had to conform to using the same scheme.

## Aesthetic Rigor
Our game is aesthetically rigorous because we developed every asset by hand without using any tools or libraries.
The animations are all done by hand, so this is an entirely student-designed game that took extreme effort.


# FEATURES 

## Front-End

The front end of our game is the user interface that the player interacts with. We have worked to ensure the user experience is as smooth as possible.
This includes using a persistent state to keep track of the user's progress, a HUD to display the user's current state, and a menu that is easy to follow and interact with.
The menu, player inventory, and player stats are all stored in a file saved to the user's computer, so their experience is consistent every time they play the game.

## Data Store

For each of our game features, such as item count, difficulty selection,
turns passed, torches extinguished, and level selection,
we stored these values as object variables to keep track of their values and continuously update the game state.
These connect to the front and back end through our persistent state.
For example, when picking up a smoke bomb or water flask,
it will immediately update the user inventory or the user HUD and the game's persistent state.
Our persistent state includes music selection, turns passed, current level,
items possessed, items used, difficulty selection, and torches extinguished.
We store these in a text file unique to every user that loads
and saves the user's progress at the start and end of the program,
respectively.
These are appropriately connected, as when items are interacted with, they are constantly updated in the back end.

## Back-End

The back end of our game is the code that runs the game and handles all the logic.
It takes the settings stored in the persistent state to display and set up the game for the user to play.
Once the user inputs a command, the back end handles the game's logic and updates the persistent state accordingly.