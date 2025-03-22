import streamlit as st
import random

# Initialize session state
if 'snake' not in st.session_state:
    st.session_state.snake = [(5, 5), (5, 6), (5, 7)]  # Initial snake positions
if 'direction' not in st.session_state:
    st.session_state.direction = "RIGHT"
if 'food' not in st.session_state:
    st.session_state.food = (random.randint(0, 9), random.randint(0, 9))
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# Constants
GRID_SIZE = 10

def move_snake():
    """Move the snake based on the current direction."""
    head = st.session_state.snake[0]
    if st.session_state.direction == "UP":
        new_head = (head[0] - 1, head[1])
    elif st.session_state.direction == "DOWN":
        new_head = (head[0] + 1, head[1])
    elif st.session_state.direction == "LEFT":
        new_head = (head[0], head[1] - 1)
    elif st.session_state.direction == "RIGHT":
        new_head = (head[0], head[1] + 1)

    # Check for wall collision (wrap around)
    new_head = (new_head[0] % GRID_SIZE, new_head[1] % GRID_SIZE)

    # Check for self-collision
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        return

    # Add new head to the snake
    st.session_state.snake.insert(0, new_head)

    # Check if snake eats food
    if new_head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    else:
        st.session_state.snake.pop()  # Remove tail if no food is eaten

def draw_grid():
    """Draw the game grid with the snake and food."""
    grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for segment in st.session_state.snake:
        grid[segment[0]][segment[1]] = "🐍"
    grid[st.session_state.food[0]][st.session_state.food[1]] = "🍎"
    st.table(grid)

def reset_game():
    """Reset the game state."""
    st.session_state.snake = [(5, 5), (5, 6), (5, 7)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    st.session_state.score = 0
    st.session_state.game_over = False

# Game UI
st.title("Snake Game in Streamlit 🎮")

if st.session_state.game_over:
    st.error("Game Over! You collided with yourself.")
    if st.button("Restart Game"):
        reset_game()

if not st.session_state.game_over:
    # Display score
    st.write(f"Score: {st.session_state.score}")

    # Draw the game grid
    draw_grid()

    # Movement buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⬆️ Up"):
            st.session_state.direction = "UP"
    with col2:
        if st.button("⬇️ Down"):
            st.session_state.direction = "DOWN"
    with col3:
        if st.button("⬅️ Left"):
            st.session_state.direction = "LEFT"
    with col4:
        if st.button("➡️ Right"):
            st.session_state.direction = "RIGHT"

    # Move the snake after button press
    move_snake()