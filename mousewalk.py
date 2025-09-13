import time, pyautogui, random
from pynput.mouse import Listener

MONITOR_WIDTH, MONITOR_HEIGHT, pyautogui.PAUSE = 1920, 1080, 0.01
base_step,stuck_count, max_stuck_count,last_positions = 3, 0, 5, []
max_step = 10
center_mouse = True
move_x = move_y = base_step

current_x, current_y = pyautogui.position()
current_monitor = (current_x // MONITOR_WIDTH, current_y // MONITOR_HEIGHT)
monitor_center_x = current_monitor[0] * MONITOR_WIDTH + MONITOR_WIDTH // 2
monitor_center_y = current_monitor[1] * MONITOR_HEIGHT + MONITOR_HEIGHT // 2
current_x, current_y = pyautogui.position()
    
pyautogui.moveTo(monitor_center_x, monitor_center_y)
x_prev, y_prev = monitor_center_x, monitor_center_y
going_exit = False
programmatic_movement = False 

def on_move(x, y):
    global going_exit, x_prev, y_prev, programmatic_movement
    if programmatic_movement:
        x_prev, y_prev = x, y
        return
    if abs(x_prev - x) != abs(y_prev - y):
        going_exit = True
        return False
    x_prev, y_prev = x, y

Listener(on_move=on_move).start()

while not going_exit:

    current_x, current_y = pyautogui.position()
    current_monitor_x = current_x // MONITOR_WIDTH
    current_monitor_y = current_y // MONITOR_HEIGHT

    if (current_monitor_x, current_monitor_y) != current_monitor:
        programmatic_movement = True
        pyautogui.moveTo(monitor_center_x, monitor_center_y)
        programmatic_movement = False
        continue
    
    last_positions.append((current_x, current_y))
    
    if len(last_positions) > 5:
        last_positions.pop(0)
    
    if len(set(last_positions)) <= 2:
        stuck_count += 1
    
    else:
        stuck_count = 0
    
    if stuck_count > max_stuck_count:
        move_x = random.choice([-base_step-2, base_step+2])
        move_y = random.choice([-base_step-2, base_step+2])
        stuck_count = 0
    
    next_x = current_x + move_x
    next_y = current_y + move_y
    
    monitor_left = current_monitor[0] * MONITOR_WIDTH
    monitor_right = monitor_left + MONITOR_WIDTH
    monitor_top = current_monitor[1] * MONITOR_HEIGHT
    monitor_bottom = monitor_top + MONITOR_HEIGHT
    
    if next_x >= monitor_right-1 or next_x <= monitor_left:
        move_x = -move_x
        next_x = current_x + move_x
    
    if next_y >= monitor_bottom-1 or next_y <= monitor_top:
        move_y = -move_y
        next_y = current_y + move_y

    move_x = max(-max_step, min(max_step, move_x))
    move_y = max(-max_step, min(max_step, move_y))
    programmatic_movement = True
    pyautogui.moveTo(next_x, next_y, duration=0.0001)
    programmatic_movement = False
    time.sleep(0.0001)