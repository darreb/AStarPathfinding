from a_star_simulator import *

# === Main Function ====
pygame.init()                                                   # Initialize
screen = pygame.display.set_mode(SIZE)                          # Display screen
sim = Simulator(screen)                                         # Simulator

sim.run()
pygame.quit()
