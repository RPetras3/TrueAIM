import numpy as np
from scipy.integrate import solve_ivp

def ballistic_ode(t, state, bc, rho_factor=1.0, g=32.174):
    """
    state = [x, vx, vy]
    Returns derivatives: [dx/dt, dvx/dt, dvy/dt]
    """
    x, vx, vy = state
    v = np.sqrt(vx**2 + vy**2)
    if v < 1:  # avoid division by zero
        return [vx, 0, -g]
    
    # Drag acceleration magnitude (simplified standard form)
    drag = (v * rho_factor) / bc
    
    ax = -drag * (vx / v)
    ay = -g - drag * (vy / v)
    
    return [vx, ax, ay]

def find_drop_at_range(v0, theta0, bc, target_range=1500,  # 500 yards = 1500 ft
                       rho_factor=1.0, g=32.174, t_max=3.0):
    """
    v0: muzzle velocity (ft/s)
    theta0: launch angle in radians (will be small)
    bc: ballistic coefficient
    target_range: distance in feet
    """
    def event_reach_range(t, state, *args):
        return state[0] - target_range  # stop when x reaches target
    event_reach_range.terminal = True
    event_reach_range.direction = 1
    
    state0 = [0.0, v0 * np.cos(theta0), v0 * np.sin(theta0)]
    
    sol = solve_ivp(ballistic_ode, [0, t_max], state0,
                    args=(bc, rho_factor, g),
                    method='RK45', rtol=1e-8, atol=1e-8,
                    events=event_reach_range, dense_output=True)
    
    if sol.success and len(sol.t_events[0]) > 0:
        # Get state at exact target range
        t_target = sol.t_events[0][0]
        state_target = sol.sol(t_target)
        y_drop = state_target[2]   # this is raw y (vertical position)
        return y_drop, t_target, state_target[1]  # return drop, time, vx
    else:
        return None, None, None
    
if __name__ == "__main__":
    v0 = 2650          # fps (.308 example)
    bc = 0.45          # G1 BC
    theta0 = np.radians(0.15)   # small angle, we assume 0 for sake of simplicity
    drop_feet, tof, vx = find_drop_at_range(v0, theta0, bc, target_range=1500)
    print(f"Drop at 500 yd: {drop_feet*12:.1f} inches")