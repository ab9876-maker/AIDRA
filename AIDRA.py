import tkinter as tk
from tkinter import ttk
import random
import heapq
import math

# ============================================================
# AIDRA — Adaptive Intelligent Disaster Response Agent
# Python Desktop Version using Tkinter
# ============================================================

COLS = 20
ROWS = 12
CELL = 40

HAZARD_CELLS = {
    (3,1),(4,1),(5,1),(3,2),(4,2),(5,2),(3,3),(4,3),
    (10,6),(11,6),(12,6),(11,7),(12,7),(13,7),(14,7),(11,8),(12,8)
}

BASE_BLOCKED = {
    (7,3),(8,3),(15,4),(16,4)
}

DIRS = [(1,0),(-1,0),(0,1),(0,-1)]


# ============================================================
# DATA MODELS
# ============================================================

class Victim:
    def __init__(self, vid, sev, x, y, priority):
        self.id = vid
        self.severity = sev
        self.x = x
        self.y = y
        self.priority = priority
        self.rescued = False
        self.assigned = None
        self.survival = 0
        self.rescue_time = None


class Ambulance:
    def __init__(self, aid):
        self.id = aid
        self.x = 0
        self.y = 6
        self.busy = False
        self.kits = 5
        self.trips = 0
        self.risk_cells = 0
        self.path = []
        self.path_index = 0
        self.target = None


# ============================================================
# MAIN APPLICATION
# ============================================================

class AIDRAApp:

    def __init__(self, root):
        self.root = root
        self.root.title('AIDRA — Python Edition')
        self.root.geometry('1400x820')
        self.root.configure(bg='#0b1020')

        self.running = False
        self.tick = 0
        self.dynamic_blocked = set()

        self.create_data()
        self.create_ui()
        self.draw_grid()
        self.update_panels()

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def create_data(self):
        self.victims = [
            Victim('V1', 'critical', 5, 2, 1),
            Victim('V2', 'critical', 12, 3, 2),
            Victim('V3', 'moderate', 8, 9, 3),
            Victim('V4', 'moderate', 16, 7, 4),
            Victim('V5', 'minor', 3, 10, 5),
        ]

        self.ambulances = {
            'AMB1': Ambulance('AMB1'),
            'AMB2': Ambulance('AMB2')
        }

    # ========================================================
    # UI
    # ========================================================

    def create_ui(self):

        # HEADER
        header = tk.Frame(self.root, bg='#101830', height=50)
        header.pack(fill='x')

        title = tk.Label(
            header,
            text='◆ AIDRA — Adaptive Intelligent Disaster Response Agent',
            fg='#33aaff',
            bg='#101830',
            font=('Consolas', 16, 'bold')
        )
        title.pack(side='left', padx=15, pady=10)

        self.status_label = tk.Label(
            header,
            text='SYSTEM READY',
            fg='#00ff88',
            bg='#101830',
            font=('Consolas', 11, 'bold')
        )
        self.status_label.pack(side='right', padx=20)

        # MAIN BODY
        body = tk.Frame(self.root, bg='#0b1020')
        body.pack(fill='both', expand=True)

        # LEFT SIDE
        left = tk.Frame(body, bg='#0b1020')
        left.pack(side='left', fill='both', expand=True)

        # CANVAS
        self.canvas = tk.Canvas(
            left,
            width=COLS*CELL,
            height=ROWS*CELL,
            bg='#081018',
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

        # METRICS
        metrics = tk.Frame(left, bg='#0b1020')
        metrics.pack(fill='x', padx=10)

        self.metric_saved = self.metric_box(metrics, 'VICTIMS SAVED')
        self.metric_saved.pack(side='left', padx=5)

        self.metric_routes = self.metric_box(metrics, 'ROUTES')
        self.metric_routes.pack(side='left', padx=5)

        self.metric_risk = self.metric_box(metrics, 'RISK CELLS')
        self.metric_risk.pack(side='left', padx=5)

        self.metric_tick = self.metric_box(metrics, 'SIMULATION TICK')
        self.metric_tick.pack(side='left', padx=5)

        # RIGHT PANEL
        right = tk.Frame(body, bg='#101830', width=360)
        right.pack(side='right', fill='y')
        right.pack_propagate(False)

        # VICTIMS PANEL
        victim_title = tk.Label(
            right,
            text='VICTIMS',
            bg='#101830',
            fg='#33aaff',
            font=('Consolas', 12, 'bold')
        )
        victim_title.pack(anchor='w', padx=10, pady=(10,0))

        self.victim_box = tk.Text(
            right,
            height=14,
            bg='#0b1020',
            fg='#dddddd',
            insertbackground='white',
            font=('Consolas', 10)
        )
        self.victim_box.pack(fill='x', padx=10, pady=5)

        # RESOURCES PANEL
        resource_title = tk.Label(
            right,
            text='RESOURCES',
            bg='#101830',
            fg='#33aaff',
            font=('Consolas', 12, 'bold')
        )
        resource_title.pack(anchor='w', padx=10, pady=(10,0))

        self.resource_box = tk.Text(
            right,
            height=10,
            bg='#0b1020',
            fg='#dddddd',
            font=('Consolas', 10)
        )
        self.resource_box.pack(fill='x', padx=10, pady=5)

        # LOGS PANEL
        log_title = tk.Label(
            right,
            text='DECISION LOG',
            bg='#101830',
            fg='#33aaff',
            font=('Consolas', 12, 'bold')
        )
        log_title.pack(anchor='w', padx=10, pady=(10,0))

        self.log_box = tk.Text(
            right,
            bg='#0b1020',
            fg='#00ff88',
            font=('Consolas', 9)
        )
        self.log_box.pack(fill='both', expand=True, padx=10, pady=5)

        # FOOTER BUTTONS
        footer = tk.Frame(self.root, bg='#101830', height=60)
        footer.pack(fill='x')

        tk.Button(
            footer,
            text='START SIMULATION',
            command=self.start_sim,
            bg='#0f3050',
            fg='white',
            font=('Consolas', 11, 'bold')
        ).pack(side='left', padx=10, pady=10)

        tk.Button(
            footer,
            text='ADD BLOCKAGE',
            command=self.add_blockage,
            bg='#502020',
            fg='white',
            font=('Consolas', 11, 'bold')
        ).pack(side='left', padx=10)

        tk.Button(
            footer,
            text='NEW VICTIM',
            command=self.new_victim,
            bg='#504010',
            fg='white',
            font=('Consolas', 11, 'bold')
        ).pack(side='left', padx=10)

        tk.Button(
            footer,
            text='REPLAN ROUTES',
            command=self.plan_routes,
            bg='#104020',
            fg='white',
            font=('Consolas', 11, 'bold')
        ).pack(side='left', padx=10)

    def metric_box(self, parent, label):
        frame = tk.Frame(parent, bg='#101830', width=150, height=70)
        frame.pack_propagate(False)

        value = tk.Label(
            frame,
            text='0',
            bg='#101830',
            fg='#33aaff',
            font=('Consolas', 20, 'bold')
        )
        value.pack()

        caption = tk.Label(
            frame,
            text=label,
            bg='#101830',
            fg='#999999',
            font=('Consolas', 9)
        )
        caption.pack()

        frame.value_label = value
        return frame

    # ========================================================
    # DRAWING
    # ========================================================

    def draw_grid(self):

        self.canvas.delete('all')

        for c in range(COLS):
            for r in range(ROWS):

                x1 = c * CELL
                y1 = r * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL

                fill = '#111820'

                if (c, r) in HAZARD_CELLS:
                    fill = '#401010'

                if (c, r) in BASE_BLOCKED:
                    fill = '#202020'

                if (c, r) in self.dynamic_blocked:
                    fill = '#aa2222'

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill,
                    outline='#203050'
                )

        # Base
        bx = 0 * CELL
        by = 6 * CELL

        self.canvas.create_rectangle(
            bx, by, bx+CELL, by+CELL,
            fill='#004400'
        )

        self.canvas.create_text(
            bx+20,
            by+20,
            text='B',
            fill='white',
            font=('Consolas', 14, 'bold')
        )

        # Medical Centers
        self.draw_medical_center(17,1,'MC1')
        self.draw_medical_center(18,10,'MC2')

        # Paths
        for amb in self.ambulances.values():
            if len(amb.path) > 1:
                self.draw_path(amb.path)

        # Victims
        for victim in self.victims:
            if not victim.rescued:
                self.draw_victim(victim)

        # Ambulances
        for amb in self.ambulances.values():
            self.draw_ambulance(amb)

    def draw_medical_center(self, x, y, name):

        px = x * CELL
        py = y * CELL

        self.canvas.create_rectangle(
            px, py,
            px+CELL, py+CELL,
            fill='#003355'
        )

        self.canvas.create_text(
            px+20,
            py+20,
            text='✚',
            fill='#33aaff',
            font=('Arial', 16, 'bold')
        )

    def draw_victim(self, victim):

        colors = {
            'critical': '#ff3333',
            'moderate': '#ffaa00',
            'minor': '#33ff33'
        }

        x = victim.x * CELL + 20
        y = victim.y * CELL + 20

        self.canvas.create_oval(
            x-12, y-12,
            x+12, y+12,
            fill=colors[victim.severity],
            outline='white'
        )

        self.canvas.create_text(
            x,
            y,
            text=victim.id[1:],
            fill='black',
            font=('Consolas', 10, 'bold')
        )

    def draw_ambulance(self, amb):

        x = amb.x * CELL + 20
        y = amb.y * CELL + 20

        color = '#ffaa00' if amb.busy else '#33aaff'

        self.canvas.create_rectangle(
            x-15, y-10,
            x+15, y+10,
            fill=color,
            outline='white'
        )

        self.canvas.create_text(
            x,
            y,
            text=amb.id[-1],
            fill='black',
            font=('Consolas', 10, 'bold')
        )

    def draw_path(self, path):

        for i in range(len(path)-1):
            x1 = path[i][0] * CELL + 20
            y1 = path[i][1] * CELL + 20
            x2 = path[i+1][0] * CELL + 20
            y2 = path[i+1][1] * CELL + 20

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill='#33aaff',
                width=3
            )

    # ========================================================
    # SEARCH ALGORITHMS
    # ========================================================

    def heuristic(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def is_blocked(self, x, y):
        return (x,y) in BASE_BLOCKED or (x,y) in self.dynamic_blocked

    def astar(self, start, goal, avoid_risk=True):

        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}

        while open_set:

            current = heapq.heappop(open_set)[1]

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for dx, dy in DIRS:

                nx = current[0] + dx
                ny = current[1] + dy

                if nx < 0 or ny < 0 or nx >= COLS or ny >= ROWS:
                    continue

                if self.is_blocked(nx, ny):
                    continue

                cost = 1

                if avoid_risk and (nx, ny) in HAZARD_CELLS:
                    cost = 6

                tentative = g_score[current] + cost

                if (nx, ny) not in g_score or tentative < g_score[(nx, ny)]:
                    came_from[(nx, ny)] = current
                    g_score[(nx, ny)] = tentative

                    f = tentative + self.heuristic((nx, ny), goal)
                    heapq.heappush(open_set, (f, (nx, ny)))

        return []

    def reconstruct_path(self, came_from, current):

        path = [current]

        while current in came_from:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path

    # ========================================================
    # PLANNING
    # ========================================================

    def plan_routes(self):

        pending = [v for v in self.victims if not v.rescued and v.assigned is None]

        if not pending:
            return

        severity_weight = {
            'critical': 3,
            'moderate': 2,
            'minor': 1
        }

        pending.sort(
            key=lambda v: severity_weight[v.severity],
            reverse=True
        )

        for amb in self.ambulances.values():

            if amb.busy:
                continue

            if not pending:
                break

            victim = pending.pop(0)

            path = self.astar(
                (amb.x, amb.y),
                (victim.x, victim.y),
                avoid_risk=True
            )

            if not path:
                continue

            victim.assigned = amb.id
            amb.target = victim
            amb.path = path
            amb.path_index = 0
            amb.busy = True

            if victim.severity == 'critical':
                victim.survival = 0.65
            elif victim.severity == 'moderate':
                victim.survival = 0.82
            else:
                victim.survival = 0.94

            self.log(
                f'{amb.id} assigned to {victim.id} '
                f'({victim.severity.upper()})'
            )

        self.draw_grid()
        self.update_panels()

    # ========================================================
    # SIMULATION LOOP
    # ========================================================

    def start_sim(self):

        if self.running:
            return

        self.running = True

        self.status_label.config(
            text='SIMULATION ACTIVE',
            fg='#ffaa00'
        )

        self.log('AIDRA system initialized')
        self.log('Running A* path planning')
        self.log('Running CSP resource allocation')
        self.log('Running ML triage analysis')

        self.plan_routes()
        self.step()

    def step(self):

        if not self.running:
            return

        self.tick += 1

        for amb in self.ambulances.values():

            if not amb.busy:
                continue

            if amb.path_index < len(amb.path)-1:

                amb.path_index += 1
                pos = amb.path[amb.path_index]

                amb.x = pos[0]
                amb.y = pos[1]

                if pos in HAZARD_CELLS:
                    amb.risk_cells += 1

            else:

                victim = amb.target

                if victim and not victim.rescued:
                    victim.rescued = True
                    victim.rescue_time = self.tick

                    amb.trips += 1
                    amb.kits -= 2

                    self.log(
                        f'{victim.id} rescued by {amb.id} '
                        f'| Survival {int(victim.survival*100)}%'
                    )

                amb.x = 0
                amb.y = 6
                amb.busy = False
                amb.path = []
                amb.path_index = 0
                amb.target = None

        if all(v.rescued for v in self.victims):
            self.running = False
            self.status_label.config(
                text='MISSION COMPLETE',
                fg='#00ff88'
            )
            self.log('All victims rescued — Mission complete')
        else:
            self.plan_routes()
            self.root.after(500, self.step)

        self.draw_grid()
        self.update_panels()

    # ========================================================
    # DYNAMIC EVENTS
    # ========================================================

    def add_blockage(self):

        options = [
            (5,3), (6,4), (9,5),
            (13,6), (14,5), (4,8)
        ]

        free = [p for p in options if p not in self.dynamic_blocked]

        if not free:
            return

        pos = random.choice(free)

        self.dynamic_blocked.add(pos)

        self.log(f'Aftershock blockage at {pos}')

        for amb in self.ambulances.values():

            if amb.target:
                new_path = self.astar(
                    (amb.x, amb.y),
                    (amb.target.x, amb.target.y)
                )

                if new_path:
                    amb.path = new_path
                    amb.path_index = 0
                    self.log(f'{amb.id} replanned route')

        self.draw_grid()

    def new_victim(self):

        vid = f'V{len(self.victims)+1}'

        severity = random.choice([
            'critical',
            'moderate',
            'minor'
        ])

        while True:

            x = random.randint(2, 17)
            y = random.randint(1, 10)

            if not self.is_blocked(x, y):
                break

        victim = Victim(
            vid,
            severity,
            x,
            y,
            len(self.victims)+1
        )

        self.victims.append(victim)

        self.log(
            f'New victim {vid} detected at ({x},{y}) '
            f'[{severity.upper()}]'
        )

        self.plan_routes()
        self.draw_grid()
        self.update_panels()

    # ========================================================
    # UTILITIES
    # ========================================================

    def update_panels(self):

        saved = len([v for v in self.victims if v.rescued])

        routes = sum(a.trips for a in self.ambulances.values())

        risk = sum(a.risk_cells for a in self.ambulances.values())

        self.metric_saved.value_label.config(text=str(saved))
        self.metric_routes.value_label.config(text=str(routes))
        self.metric_risk.value_label.config(text=str(risk))
        self.metric_tick.value_label.config(text=str(self.tick))

        self.victim_box.delete('1.0', tk.END)

        for v in self.victims:

            status = 'RESCUED' if v.rescued else v.severity.upper()

            line = (
                f'{v.id:<4} '
                f'{status:<10} '
                f'POS({v.x},{v.y}) '
                f'SURV:{int(v.survival*100)}%\n'
            )

            self.victim_box.insert(tk.END, line)

        self.resource_box.delete('1.0', tk.END)

        for amb in self.ambulances.values():

            state = 'ACTIVE' if amb.busy else 'IDLE'

            text = (
                f'{amb.id}\n'
                f'  STATUS : {state}\n'
                f'  KITS   : {amb.kits}\n'
                f'  TRIPS  : {amb.trips}\n'
                f'  RISK   : {amb.risk_cells}\n\n'
            )

            self.resource_box.insert(tk.END, text)

    def log(self, message):

        self.log_box.insert(
            '1.0',
            f'[T={self.tick}] {message}\n'
        )

    # ========================================================
    # ML PLACEHOLDER FUNCTIONS
    # ========================================================

    def knn_prediction(self, severity, distance):

        if severity == 'critical' and distance < 6:
            return 'HIGH'

        if severity == 'moderate':
            return 'MEDIUM'

        return 'LOW'

    def naive_bayes_prediction(self, severity, elapsed_time):

        if severity == 'critical' and elapsed_time > 5:
            return 'HIGH'

        return 'MEDIUM'

    # ========================================================
    # FUZZY LOGIC
    # ========================================================

    def fuzzy_block_probability(self, vibration, smoke):

        score = (vibration * 0.6) + (smoke * 0.4)

        return min(score / 10.0, 1.0)


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == '__main__':

    root = tk.Tk()

    app = AIDRAApp(root)

    root.mainloop()
