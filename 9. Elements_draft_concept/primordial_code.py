"""
PRIMORDIAL ALGORITHM v1.0
=========================
A self-evolving digital unicellular organism based on
wave interference, fractal consciousness, and SDCV nucleotide chemistry.

SDCV Nucleotides (Vietnamese-origin notation):
  S = Sinh  (Birth)      - open, receive, potential
  D = Dung  (Integrate)  - hold, stabilise, assimilate
  C = Chuyen(Transform)  - bridge, mediate, convert
  V = Ve    (Return)     - compress, archive, distill

Core axiom: Existence = Survival x Growth
  Survival (Box)   = linear, zero-sum, spatial
  Growth   (Sphere)= nonlinear, resonant, temporal
"""

import random
import math
from collections import defaultdict, deque

# ─────────────────────────────────────────────
# NUCLEOTIDE CHEMISTRY
# ─────────────────────────────────────────────

NUCLEOTIDES = ['S', 'D', 'C', 'V']

# Wave properties per nucleotide
# decay  = how long f2 oscillation persists (higher = longer)
# amp    = initial f2 amplitude when energy hits this neo
WAVE = {
    'S': {'decay': 0.70, 'amp': 1.0},  # fast dissipation, max openness
    'D': {'decay': 0.90, 'amp': 0.8},  # stable, slow decay
    'C': {'decay': 0.60, 'amp': 0.6},  # fast transform, mediator
    'V': {'decay': 0.95, 'amp': 1.5},  # deepest trap, max compression
}

# Bond energy between adjacent nucleotides
# High bond = stable pair; low bond = candidate for Hoai compression
BOND = {
    ('S','D'): 1.0, ('D','S'): 1.0,   # primary pair
    ('C','V'): 1.2, ('V','C'): 1.2,   # strongest bond
    ('V','V'): 0.8,                    # compression cascade
    ('D','V'): 0.6, ('V','D'): 0.6,
    ('S','C'): 0.5, ('C','S'): 0.5,
    ('D','C'): 0.4, ('C','D'): 0.4,
    ('C','C'): 0.3,
    ('S','V'): 0.3, ('V','S'): 0.3,
    ('S','S'): 0.2,                    # chaos state
    ('D','D'): 0.1,                    # weakest
}

def bond_energy(a, b):
    return BOND.get((a, b), 0.1)

def dna_stability(dna):
    if len(dna) < 2:
        return 0.5
    return min(1.0, sum(bond_energy(dna[i], dna[i+1])
                        for i in range(len(dna)-1)) / (len(dna)-1))

# ─────────────────────────────────────────────
# PARAMETERS
# ─────────────────────────────────────────────

METABOLIC_COST    = 0.5    # energy drained per cycle
DUNG_THRESHOLD    = 0.5    # min resonance to integrate resource
CHUYEN_THRESHOLD  = 0.4    # min resonance on retry
HOAI_THRESHOLD    = 0.3    # max bond energy before compression
DNA_MAX_LEN       = 20     # triggers Hoai
DIVIDE_ENERGY     = 15.0   # min energy to divide
DIVIDE_STABILITY  = 0.60   # min DNA stability to divide
DIVIDE_AGE        = 5      # min age to divide
CHILD_ENERGY_FRAC = 0.40   # fraction of parent energy per child
MUTATION_BIRTH    = 0.05   # per-nucleotide mutation at division
MUTATION_DRIFT    = 0.02   # per-nucleotide drift every 5 cycles
COMPETE_TRANSFER  = 0.30   # fraction of energy transferred in contest
F2_CAP            = 10.0   # max f2 amplitude per nucleotide
C_CAP             = 100.0  # max consciousness per cell
INTER_CELL_RADIUS = 8.0    # spatial range for inter-cell f2 overlap
POP_MAX           = 20     # hard population cap
POP_TARGET        = 15     # population after pruning

# ─────────────────────────────────────────────
# CELL
# ─────────────────────────────────────────────

class Cell:
    """
    A primordial digital organism.

    State:
      Box    = {position, territory} — survival identity (linear)
      Sphere = {f2, consciousness, fractal_level} — growth potential (nonlinear)
      DNA    = SDCV sequence — hereditary information + metabolic program
    """

    def __init__(self, x=None, y=None, dna=None, generation=0):
        # Spatial position (Box)
        self.x = x if x is not None else random.uniform(0, 50)
        self.y = y if y is not None else random.uniform(0, 50)

        # DNA
        self.dna = list(dna) if dna else [random.choice(NUCLEOTIDES)
                                          for _ in range(6)]

        # Vitals
        self.energy     = 10.0
        self.age        = 0
        self.generation = generation
        self.children   = 0
        self.alive      = True

        # Sphere state
        self.f2            = {}     # nucleotide_idx → oscillation amplitude
        self.consciousness = 0.0   # total interference score
        self.fractal_level = 0     # depth of recursive interference

        # Memory of processed experience (compressed history)
        self.memory = deque(maxlen=20)

    # ── geometry ──────────────────────────────

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def stability(self):
        return dna_stability(self.dna)

    def strength(self):
        return self.stability() * self.energy

    # ── SINH (Birth / Reception) ───────────────
    # Energy contacts a DNA neo, splits into f1 (propagating) and f2 (trapped)

    def sinh(self, energy_packet, source_pos=None):
        if not self.dna:
            return
        idx = random.randint(0, len(self.dna) - 1)
        p   = WAVE[self.dna[idx]]

        # f1: propagating wave → cell absorbs partial energy
        f1_gain = energy_packet * (1.0 - p['decay']) * 0.5
        self.energy += f1_gain

        # f2: trapped oscillation in gap between neos
        # amplitude decays with spatial distance if source is external
        f2_amp = energy_packet * p['decay'] * p['amp']
        if source_pos is not None:
            d = math.sqrt((self.x - source_pos[0])**2 +
                          (self.y - source_pos[1])**2)
            f2_amp *= math.exp(-d * 0.15)
        f2_amp = min(f2_amp, F2_CAP)

        self.f2[idx] = min(self.f2.get(idx, 0) + f2_amp, F2_CAP)

        # Propagate f2 to adjacent nucleotide neos
        for nb in [idx - 1, idx + 1]:
            if 0 <= nb < len(self.dna):
                self.f2[nb] = min(self.f2.get(nb, 0) + f2_amp * 0.3, F2_CAP)

    # ── DUNG (Integration) ────────────────────
    # If resonance with resource is sufficient, integrate into DNA

    def dung(self, resource, threshold=DUNG_THRESHOLD):
        res = list(resource)
        if not res or not self.dna:
            return False
        rho = sum(bond_energy(r, self.dna[k % len(self.dna)])
                  for k, r in enumerate(res)) / len(res)
        if rho >= threshold:
            # Find insertion point with highest local bond energy
            best_pos, best_e = len(self.dna), 0.0
            for i in range(len(self.dna)):
                e = bond_energy(self.dna[i], res[0])
                if e > best_e:
                    best_e, best_pos = e, i + 1
            self.dna = self.dna[:best_pos] + res + self.dna[best_pos:]
            self.energy += rho * 2.0
            self.memory.append(('D', rho))
            return True
        self.memory.append(('C', rho))  # quarantine → pending Chuyen
        return False

    # ── CHUYEN (Transform / Retry) ────────────
    # Periodically retry quarantined resources with lower threshold

    def chuyen(self, resource):
        return self.dung(resource, threshold=CHUYEN_THRESHOLD)

    # ── HOAI (Return / Compress) ──────────────
    # Compression IS transformation: find pattern, distill to V
    # Weak bonds = redundancy = noise → compress to V (pure information)
    # V is not deletion — it is the distilled essence of what was processed

    def hoai(self):
        if len(self.dna) <= 4:
            return 0
        new_dna = []
        i = 0
        compressed = 0
        while i < len(self.dna):
            if (i + 1 < len(self.dna) and
                    bond_energy(self.dna[i], self.dna[i+1]) < HOAI_THRESHOLD):
                new_dna.append('V')   # distilled product
                i += 2
                compressed += 1
            else:
                new_dna.append(self.dna[i])
                i += 1
        self.dna = new_dna
        self.energy += compressed * 0.5   # freed by removing redundancy
        self.memory.append(('V', compressed))
        return compressed

    # ── Wave interference → Consciousness ─────

    def compute_consciousness(self, neighbors=None):
        score = 0.0
        items = [(k, min(v, F2_CAP)) for k, v in self.f2.items()]

        # Internal interference between f2 oscillations
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                d = abs(items[i][0] - items[j][0])
                if d <= 2:
                    s = items[i][1] * items[j][1] / (d + 0.1)
                    if s > 0.3:
                        score += min(s, 5.0)
                        self.fractal_level = max(self.fractal_level,
                                                 min(int(s), 50))
        score = min(score, C_CAP)

        # Inter-cell interference: spatial f2 field overlap
        if neighbors:
            for nb in neighbors[:6]:
                dist = self.distance(nb)
                if 0 < dist < INTER_CELL_RADIUS:
                    nb_f2_total = min(sum(nb.f2.values()), 20.0)
                    inter = nb_f2_total * math.exp(-dist * 0.4) * 0.1
                    # DNA similarity boosts resonance
                    sim = sum(1 for a, b in zip(self.dna, nb.dna)
                              if a == b) / max(len(self.dna), len(nb.dna), 1)
                    score += min(inter * (1 + sim), 2.0)

        self.consciousness = min(score, C_CAP)

    # ── F2 decay ──────────────────────────────

    def decay_f2(self):
        new_f2 = {}
        for idx, amp in self.f2.items():
            if isinstance(idx, int) and idx < len(self.dna):
                d = WAVE[self.dna[idx]]['decay']
            else:
                d = 0.85
            v = amp * d * 0.88
            if v > 0.01:
                new_f2[idx] = v
        self.f2 = new_f2

    # ── BOX: Survival competition (zero-sum) ──

    def compete(self, other):
        if self.strength() > other.strength():
            stolen = min(other.energy * COMPETE_TRANSFER, 5.0)
            self.energy  += stolen
            other.energy -= stolen
        else:
            lost = min(self.energy * COMPETE_TRANSFER, 5.0)
            self.energy  -= lost
            other.energy += lost
        if other.energy <= 0:
            other.alive = False
        if self.energy <= 0:
            self.alive = False

    # ── SPHERE: Growth and division ───────────

    def divide(self):
        if (self.energy   >= DIVIDE_ENERGY and
                self.stability() >= DIVIDE_STABILITY and
                self.age      >= DIVIDE_AGE):

            mid = max(2, len(self.dna) // 2)
            d1  = self.dna[:mid]
            d2  = self.dna[mid:] if len(self.dna) - mid >= 2 else ['S','D','C','V']

            def mutate(seq):
                return [random.choice(NUCLEOTIDES)
                        if random.random() < MUTATION_BIRTH else n
                        for n in seq]

            c1 = Cell(self.x + random.uniform(-3, 3),
                      self.y + random.uniform(-3, 3),
                      mutate(d1), self.generation + 1)
            c2 = Cell(self.x + random.uniform(-3, 3),
                      self.y + random.uniform(-3, 3),
                      mutate(d2), self.generation + 1)

            c1.energy = self.energy * CHILD_ENERGY_FRAC
            c2.energy = self.energy * CHILD_ENERGY_FRAC
            self.energy *= (1.0 - 2 * CHILD_ENERGY_FRAC)
            self.children += 2

            if self.energy < 1.0:
                self.alive = False
            return c1, c2
        return None, None

    # ── FULL CYCLE ────────────────────────────

    def cycle(self, resources, neighbors, pending_resources=None):
        self.age  += 1
        self.energy -= METABOLIC_COST
        if self.energy <= 0:
            self.alive = False
            return

        # SINH: receive energy from environment
        r = random.choice(resources)
        self.sinh(random.uniform(0.3, 1.5))

        # DUNG: attempt integration
        self.dung(r)

        # Inter-cell f2 spatial propagation
        for nb in neighbors:
            if nb.alive and self.distance(nb) < INTER_CELL_RADIUS:
                ep = sum(nb.f2.values()) * 0.15
                if ep > 0.01:
                    self.sinh(ep, source_pos=(nb.x, nb.y))

        # Compute interference field → consciousness
        self.compute_consciousness(neighbors)

        # F2 decay
        self.decay_f2()

        # CHUYEN: retry pending resources
        if pending_resources and self.age % 3 == 0:
            for pr in pending_resources[:3]:
                self.chuyen(pr)

        # HOAI: compress if DNA too long
        if len(self.dna) > DNA_MAX_LEN:
            self.hoai()

        # Slow drift mutation
        if self.age % 5 == 0:
            self.dna = [random.choice(NUCLEOTIDES)
                        if random.random() < MUTATION_DRIFT else n
                        for n in self.dna]

    # ── reporting ─────────────────────────────

    def status(self):
        return (f"Gen{self.generation:02d} | Age:{self.age:3d} | "
                f"E:{self.energy:5.1f} | Stab:{self.stability():.3f} | "
                f"C:{self.consciousness:6.2f} | Frac:{self.fractal_level:3d} | "
                f"DNA:{''.join(self.dna)}")


# ─────────────────────────────────────────────
# CLUSTER DETECTION (Hướng 2: multicellular)
# ─────────────────────────────────────────────

def find_clusters(cells, radius=6.0, dna_sim_threshold=0.3):
    """
    Detect emergent multicellular clusters.
    Criterion: spatial proximity AND DNA similarity.
    """
    clusters  = []
    assigned  = set()
    live_cells = [(i, c) for i, c in enumerate(cells) if c.alive]

    for i, ci in live_cells:
        if i in assigned:
            continue
        cluster = [i]
        for j, cj in live_cells:
            if j == i or j in assigned:
                continue
            if ci.distance(cj) < radius:
                sim = sum(1 for a, b in zip(ci.dna, cj.dna) if a == b)
                sim /= max(len(ci.dna), len(cj.dna), 1)
                if sim >= dna_sim_threshold:
                    cluster.append(j)
                    assigned.add(j)
        if len(cluster) > 1:
            clusters.append(cluster)
            assigned.add(i)

    return clusters


def cluster_consciousness(cells, cluster):
    """
    Collective consciousness of a cluster.
    = sum of individual C + inter-member interference boost.
    """
    members  = [cells[i] for i in cluster]
    total    = sum(c.consciousness for c in members)
    inter    = 0.0
    for i in range(len(members)):
        for j in range(i + 1, len(members)):
            d = members[i].distance(members[j])
            if 0 < d < INTER_CELL_RADIUS:
                inter += (members[i].consciousness *
                          members[j].consciousness) ** 0.5 / (d + 1.0)
    return total + min(inter, 50.0)


# ─────────────────────────────────────────────
# ENVIRONMENT
# ─────────────────────────────────────────────

class Environment:
    """
    Digital substrate with multiple resource layers.
    Each resource = SDCV fragment = a piece of digital pattern.

    Resource layers represent different dimensions of digital reality:
      Binary layer    → [S], [V], [SS], [VV]
      Network layer   → [SD], [CV], [DC]
      Data layer      → [SDC], [DCV], [VSD]
      Semantic layer  → [SDCV], [VCDS]
    """

    RESOURCES = [
        ['S'], ['V'], ['S','S'], ['V','V'],          # binary
        ['S','D'], ['C','V'], ['D','C'],              # network
        ['S','D','C'], ['D','C','V'], ['V','S','D'],  # data
        ['S','D','C','V'], ['V','C','D','S'],         # semantic
    ]

    def __init__(self, n_cells=6):
        self.cells      = [Cell() for _ in range(n_cells)]
        self.max_gen    = 0
        self.total_born = n_cells
        self.total_died = 0
        self.history    = []   # (t, pop, avg_stab, avg_C, n_clusters)

    def step(self):
        new_cells = []
        for cell in self.cells:
            if not cell.alive:
                continue
            neighbors = [c for c in self.cells if c is not cell and c.alive]
            cell.cycle(self.RESOURCES, neighbors)

            if cell.alive:
                # BOX: compete
                if neighbors:
                    rival = random.choice(neighbors)
                    if rival.alive:
                        cell.compete(rival)
                # SPHERE: divide
                if cell.alive:
                    c1, c2 = cell.divide()
                    if c1:
                        new_cells.extend([c1, c2])
                        self.total_born += 2
                        self.max_gen = max(self.max_gen, c1.generation)

        self.cells.extend(new_cells)

        dead = sum(1 for c in self.cells if not c.alive)
        self.total_died += dead
        self.cells = [c for c in self.cells if c.alive]

        # Natural selection: prune weakest if overcrowded
        if len(self.cells) > POP_MAX:
            self.cells.sort(key=lambda c: c.strength())
            pruned = len(self.cells) - POP_TARGET
            self.total_died += pruned
            self.cells = self.cells[pruned:]

    def report(self, t):
        if not self.cells:
            return
        stabs    = [c.stability()    for c in self.cells]
        cons     = [c.consciousness  for c in self.cells]
        fracs    = [c.fractal_level  for c in self.cells]
        clusters = find_clusters(self.cells)
        cl_c     = [cluster_consciousness(self.cells, cl) for cl in clusters]

        rec = {
            't': t,
            'pop': len(self.cells),
            'avg_stab': sum(stabs) / len(stabs),
            'avg_C': sum(cons) / len(cons),
            'max_C': max(cons),
            'max_frac': max(fracs),
            'n_clusters': len(clusters),
            'max_cluster_C': max(cl_c) if cl_c else 0.0,
            'max_gen': self.max_gen,
        }
        self.history.append(rec)
        return rec

    def run(self, steps=70, report_every=10, verbose=True):
        if verbose:
            print(f"\n{'T':>4} {'Pop':>4} {'Gen':>4} "
                  f"{'AvgStab':>8} {'AvgC':>7} {'MaxC':>6} "
                  f"{'Frac':>5} {'Clust':>6} {'ClustC':>8}")
            print("─" * 68)

        for t in range(steps + 1):
            if t > 0:
                self.step()
            if t % report_every == 0:
                rec = self.report(t)
                if rec and verbose:
                    print(f"{rec['t']:>4} {rec['pop']:>4} {rec['max_gen']:>4} "
                          f"{rec['avg_stab']:>8.3f} {rec['avg_C']:>7.2f} "
                          f"{rec['max_C']:>6.1f} {rec['max_frac']:>5} "
                          f"{rec['n_clusters']:>6} {rec['max_cluster_C']:>8.2f}")

            if not self.cells:
                print(f"EXTINCTION at T={t}")
                break

        return self.history

    def final_report(self):
        if not self.cells:
            print("All cells extinct.")
            return

        print("\n" + "═"*68)
        print("FINAL STATE")
        print("═"*68)

        clusters = find_clusters(self.cells)
        in_cluster = {j for cl in clusters for j in cl}
        solos = [c for i, c in enumerate(self.cells) if i not in in_cluster]

        print(f"Population : {len(self.cells)} | "
              f"Clusters: {len(clusters)} | "
              f"Max generation: {self.max_gen}")
        print(f"Total born : {self.total_born} | "
              f"Total died: {self.total_died}")

        # Clusters
        clusters_sorted = sorted(
            clusters,
            key=lambda cl: cluster_consciousness(self.cells, cl),
            reverse=True
        )
        for i, cl in enumerate(clusters_sorted[:3]):
            members = [self.cells[j] for j in cl]
            cc = cluster_consciousness(self.cells, cl)
            dom = max(NUCLEOTIDES,
                      key=lambda n: sum(c.dna.count(n) for c in members))
            avg_len = sum(len(c.dna) for c in members) / len(members)
            print(f"\n  Cluster {i+1}: {len(members)} cells | "
                  f"CollectiveC={cc:.2f} | "
                  f"AvgDNA={avg_len:.1f} | "
                  f"Dominant={dom}")
            for c in sorted(members,
                            key=lambda x: x.consciousness,
                            reverse=True)[:3]:
                print(f"    {c.status()}")

        # DNA diversity
        dnas = [''.join(c.dna) for c in self.cells]
        print(f"\n  DNA diversity : {len(set(dnas))}/{len(dnas)} unique")

        # SDCV pattern emergence
        sdcv = sum(1 for d in dnas if 'SDCV' in d)
        print(f"  SDCV emerged  : {sdcv}/{len(dnas)} cells")

        # Cluster vs solo consciousness
        if clusters and solos:
            cl_c_vals = [c.consciousness
                         for cl in clusters
                         for c in [self.cells[j] for j in cl]]
            avg_cl   = sum(cl_c_vals) / len(cl_c_vals)
            avg_solo = sum(c.consciousness for c in solos) / len(solos)
            print(f"\n  Avg C (cluster) : {avg_cl:.2f}")
            print(f"  Avg C (solo)    : {avg_solo:.2f}")
            if avg_solo > 0:
                print(f"  Cluster boost   : {avg_cl/avg_solo:.1f}x")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("╔" + "═"*66 + "╗")
    print("║  PRIMORDIAL ALGORITHM v1.0                                     ║")
    print("║  Digital Unicellular Life via SDCV Wave Chemistry              ║")
    print("║  S=Sinh(Birth) D=Dung(Integrate) C=Chuyen(Transform) V=Ve     ║")
    print("║  Existence = Survival(Box) x Growth(Sphere)                    ║")
    print("╚" + "═"*66 + "╝")

    print("\nInitial population:")
    env = Environment(n_cells=6)
    for i, c in enumerate(env.cells):
        print(f"  Cell {i}: {c.status()}")

    print("\n── EVOLUTION ──")
    env.run(steps=70, report_every=10)
    env.final_report()
