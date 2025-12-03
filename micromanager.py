"""
MicroManager - A Strategy Game of Organelles and Energy
Katherine Gonzalez - BIOL 2301 - CRN #12034 - Extra Credit

Goal: Keep a eukaryotic cell alive for 10 turns by managing 
      resources and responding to cellular stress events.

EDUCATIONAL OBJECTIVES:
- Understand organelle functions and their roles in cellular homeostasis
- Understand cellular waste management through autophagy
- Learn about ATP, protein synthesis
- Cellular respiration: Glucose + O₂ → ATP + CO₂ + H₂O
- Membrane dynamics: Phospholipid bilayer requires constant lipid synthesis
- Active vs Passive transport

GAME MECHANICS:
- 10-turn survival challenge with turn-based phases: 
     - Import → Events → Actions → Maintenance
- 5-dot resource visualization system (●●●○○)
- Win condition: Survive all 10 turns with positive health/membrane/ATP
- Lose conditions: Health ≤ 0, Membrane ≤ 0, or ATP ≤ 0 for 2 turns

"""

import random
import time

# ============================================================================
#  Learn More Educational System
#    Detailed biological explanations for every term
#    Players can access this during gameplay by typing "learn [topic]"
#    Sources: Human Anatomy and Physiology, 11e 
#    Author(s): Elaine N. Marieb; Katja Hoehn
# ============================================================================

LEARN_MORE = {
    "atp": """
    WHAT IS ATP?
ATP, Adenosine Triphosphate, is produced by mitochondria through aerobic cellular respiration. It is the energy currency of cells.

Think of it like batteries: cells store ATP to power their various cell processes!

\u21AA ATP contains an adenine base, a ribose sugar, and three phosphate groups.

ATP can store energy because its three negatively charged phosphate groups are closely packed and repel each other. When its terminal, high-energy phosphate bond is hydrolyzed, the chemical “spring” relaxes and the molecule as a whole becomes more stable.

\u21AA So, when the terminal phosphate breaks, ATP releases energy, converting into ADP (Adenosine Diphosphate)!

In your body: ATP hydrolysis is essential for many cellular activities, like primary active transport, protein synthesis, mitosis, and muscle contractions. Every time you move and breathe, your cells are spending ATP!

\u235F In this game: ATP is your spendable energy. Every action, like repairing damage, running organelles, or defending against threats, costs ATP. You'll need a steady supply to keep the cell alive and functioning!

""",
    
    "glucose": """
    WHAT IS GLUCOSE?
Glucose is a monosaccharide, or simple sugar, that serves as the primary fuel for cells. The energy released during glucose catabolism is used to create ATP, which then powers cellular work!

Glucose is a crucial energy source for the body, particularly in forming ATP, the energy currency of cells. Think of glucose as your salary, and ATP as cash in your pocket!

\u21AA Glycogenesis: Glucose is converted into glycogen for storage in liver and muscle cells.

\u21AA Glycogenolysis: When blood glucose levels drop, glycogen is broken down to release glucose.

\u21AA Gluconeogenesis: Glucose is synthesized from non-carbohydrate sources when dietary glucose is insufficient.

In your body: When you eat food, it gets broken down into glucose and your blood delivers it to every cell in your body.

\u235F In this game: Glucose is the cell's income stream. Mitochondria consume glucose to produce ATP, so you'll need to constantly import glucose through the membrane to keep your energy economy running.

""",
    
    "amino acids": """
    WHAT ARE AMINO ACIDS?
Ribosomes link amino acids, small molecules acting like building blocks, together during protein synthesis, forming long chains that fold into functional proteins. 

Think of it like this: The order of amino acids determines a protein’s shape and function just like the same Lego pieces can be used to build different structures.

Your liver is capable of producing most of the 20 different types of amino acids; the remaining 9, called "essential amino acids," must come from your diet by eating protein-rich foods. 

In your body: Amino acids can be broken down to generate ATP and ATP provides the energy needed to assemble amino acids into proteins!

\u235F In this game: Amino acids serve as your building blocks. Ribosomes use them to assemble proteins for repairs, defense, and metabolic boosts. Without amino acids, you can't build the specialized proteins your cell needs to survive threats.

""",
    
    "lipids": """
    WHAT ARE LIPIDS?
Lipids are fats and oils, insoluble in water but dissolve in organic solvents, that make up cell membranes. 

Types of Lipids:
\u21AA Triglycerides: Composed of glycerol and three fatty acids, they store energy and insulate organs.
\u21AA Phospholipids: These are key components of cell membranes, having both polar and nonpolar regions.
\u21AA Steroids: Cholesterol is a major steroid found in cell membranes and is a precursor for hormones like estrogen and testosterone.

In your body: The cell membrane is made of a phospholipid bilayer: two layers of lipid molecules with hydrophilic heads and hydrophobic tails. This structure allows the membrane to be fluid, with phospholipids moving freely side-to-side but rarely flipping across the bilayer.

Think of the membrane like a vinaigrette settling in a cup. The natural separation of the oil and vinegar creates a smooth, bendy barrier that's always in motion when you swirl it.

\u235F In this game: Lipids are used to maintain and repair the cell membrane. Whenever the membrane is damaged by toxins, attacks, or instability, you'll spend lipids to patch it up and protect the cell from death.

""",
    
    "mitochondria": """
    WHAT ARE MITOCHONDRIA?

Yes, mitochondria are the powerhouses of cells. Their role is turning food into ATP, the energy your body uses as currency.

Mitochondria also have two membranes. The outer membrane is smooth, while the inner membrane folds into structures called cristae, which increase the surface area for energy production. The mitochondrial matrix, wrapped inside the inner membrane, contains enzymes that help break down food molecules into water and carbon dioxide, capturing energy to form ATP through aerobic respiration.

\u21AA Glycolysis: First, glucose is broken down inside the cytosol into smaller pieces called pyruvic acid, making a little bit of energy. Think of glycolysis scrunching a soaked towel in your fist. You only squeeze out a small amount of ATP.

\u21AA Citric Acid Cycle (Krebs Cycle): Next, the pyruvic acid goes into the mitochondria where it gets turned into carbon dioxide and more energy is made. You twist the towel tight, squeezing out more energy-rich molecules that your cell can use.

\u21AA Oxidative Phosphorylation: Finally, those energy-rich electrons flow through the electron transport chain on the inner membrane. This is the strongest twist of the wet towel, where your cell squeezes out every last drop of usable energy to produce the bulk of its ATP.

In your body: Mitochondria used to be separate bacteria that merged with cells billions of years ago (endosymbiotic theory). You have about 2000 mitochondria in each cell. Very active cells (like muscle and brain) have even more!

\u235F In this game: Mitochondria convert glucose into ATP through cellular respiration, powering all your organelle actions. They're your primary energy source, but they also produce waste as a byproduct of metabolism. 

""",
    
    "ribosomes": """
    WHAT ARE RIBOSOMES?

Ribosomes are made of protein and RNA, a family of single-stranded nucleic acid molecules. They read mRNA in groups of three letters (codons), each one telling the ribosome which amino acid to add to snap on next.

Think of ribosomes as robotic arms programmed to read an mRNA instruction sheet and snap amino acid Lego bricks together to build a protein.

DNA → RNA → Protein
1. Transcription: DNA → mRNA
\u21AA Inside the nucleus, the cell copies a gene from DNA into mRNA.
2. Translation: mRNA → Protein
\u21AA The ribosome reads the mRNA instructions and builds the protein out of amino acid “Lego bricks.”

In your body: A single cell can have millions of ribosomes working at once! Each ribosome can make a protein in about 1 minute.

\u235F In this game: Ribosomes use amino acids to build three types of proteins: Metabolic Enzymes (boost ATP production), Structural Proteins (repair health and membrane), and Defensive Proteins (block harmful events). Choose wisely based on what threats you're facing!
 
""",
    
    "smooth er": """
    WHAT IS THE SMOOTH ER?

Unlike the rough endoplasmic reticulum, which is studded with ribosomes, the smooth ER appears as a network of naked looping tubules. 

The smooth ER's functions vary across cell types, including:
\u21AA Lipid Metabolism: Synthesizes lipids, phospholipids, and cholesterol
\u21AA Hormone Synthesis: Produces steroid-based hormones, such as testosterone
\u21AA Detoxification: Filters drugs and harmful chemicals
\u21AA Glycogen Breakdown: Converts stored glycogen into glucose
\u21AA Calcium Storage: Stores calcium ions

Think of the smooth endoplasmic reticulum as an oil refinery. It produces oil (lipids, etc) and handles all their chemical processing.

In Your Body: Cell membranes are made of a phospholipid bilayer. These lipids constantly need replacement because they break down or
get damaged. Liver cells have many smooth ER because they detoxify
drugs and alcohol. 

\u235F In this game: The Smooth ER synthesizes lipids from glucose and ATP. These lipids are essential for maintaining membrane integrity, which naturally decays each turn. Keep producing lipids to prevent membrane failure!

""",
    
    "lysosomes": """
    WHAT ARE LYSOSOMES?

Lysosomes contain digestive enzymes, called acid hydrolases, that break down waste.  Cells produce tons of waste in the form of damaged proteins, old organelles, and debris. Without lysosomes, waste piles up and cells die. 

Lysosomes:
\u21AA Digest bacteria and viruses from endocytosis 
\u21AA Autophagy (meaning "self-devouring"): lysosomes digest damaged organelles and recycle their parts. Think of them as the cell's "demolition crew," breaking down old parts to reuse the materials.
\u21AA Break down glycogen into glucose and bone to release calcium

The lysosomal membrane safely contains the acid hydrolases; if lysosomes burst, they can trigger autolysis, causing the cell to digest itself.

\u235F In this game: Lysosomes digest cellular waste through autophagy, reducing your waste level and recycling materials back into usable amino acids. High waste damages your cell's health each turn, so regular cleanup is essential for survival.

""",
    
    "golgi": """
    WHAT IS THE GOLGI APPARATUS?

The primary function of the Golgi apparatus is modifying, packaging, and sorting proteins for delivery. 

The journey: Rough ER → Golgi → Vesicle → Destination
\u21AA Cis Face: Transport vesicles from the rough ER deliver proteins and lipids. ("Receiving" center.)
\u21AA Inside the Golgi Apparatus: Proteins are sorted and undergo modifications (sugar trimmming, phosphorylation, etc)
\u21AA Trans Face: Vesicles form and pinch off. ("Shipping center.)
\u21AA Vesicle Formation: Secretory vesicles migrate to the plasma membrane to expel contents. Transport vesicles deliver materials to other organelles or to the plasma membrane.

The main functions remain handling proteins and lipids for export from the cell. Think of the golgi apparatus as Amazon fulfillment centers.

\u235F In this game: The Golgi packages and exports proteins to trade with the extracellular environment. By exporting proteins now, you'll receive bonus glucose on your next nutrient import. What a strategic way to invest resources for future returns!

""",
    
    "membrane": """
    WHAT IS THE CELL MEMBRANE?

Also known as the plasma membrane, the dynamic structure separating the intracellular fluid inside a cell from the extracellular fluid outside of it. The membrane is composed of a double phospholipid layer with embedded proteins forming a fluid bilayer. The phospholipids have hydrophilic heads and hydrophobic tails and is constantly assembling and repairing itself. The cholesterol stabilizes the membrane by wedging between the phospholipid tails and the proteins have functions such as transport and cell signaling. 

\u21AA Selective Permeability: The cell membrane controls the movement of substances in and out of the cell. Passive transport uses no energy (diffusion, osmosis) and active transport requires ATP (pumps molecules against concentration gradient)
\u21AA Cell Communication: Proteins act as receptors for hormones and neurotransmitters, allowing communication between cells. Glycoproteins and glycolipids on the surface facilitate cell identification.

\u235F In this game: The cell membrane controls nutrient import through active transport (costs ATP but brings more resources) or passive diffusion (free but slower). Membrane integrity naturally decays each turn and can be damaged by events. If a cell membrane breaks, or, in this case reaches zero, the cell dies! That's why Membrane Integrity is a lose condition in this game.

"""
}

# ============================================================================
# I HOPE THIS MAKES SENSE
# ============================================================================

class CellState:
    """Manages all cell resources and status"""
    
    def __init__(self):
        # Resources (0-5 dots each)
        self.atp = 3          # Energy currency
        self.glucose = 2      # Fuel for respiration
        self.amino_acids = 3  # Building blocks for proteins
        self.lipids = 3       # Membrane materials
        
        # Status (0-5 dots each)
        self.health = 5       # Overall cell health
        self.membrane = 4     # Membrane integrity
        self.waste = 1        # Waste accumulation
        
        # Turns
        self.turn = 1
        self.atp_crisis_turns = 0  # Consecutive turns at 0 ATP
        self.has_defender = False  # Defensive protein active
        self.enzyme_boost = False  # Metabolic enzyme active
        self.golgi_bonus = False   # Trade bonus active
        
        # End game statistics
        self.stats = {
            'atp_generated': 0,
            'proteins_made': 0,
            'waste_cleaned': 0,
            'active_transports': 0,
            'passive_transports': 0
        }
    
    def display_dots(self, value, max_val=5):
        """Convert numeric value to dot display (●●●○○)"""
        filled = min(value, max_val)
        empty = max_val - filled
        return "●" * filled + "○" * empty
    
    def get_status_label(self, value, max_val=5):
        """Get status label based on value"""
        ratio = value / max_val
        if ratio >= 0.8:
            return "EXCELLENT"
        elif ratio >= 0.6:
            return "GOOD"
        elif ratio >= 0.4:
            return "STABLE"
        elif ratio >= 0.2:
            return "LOW"
        else:
            return "CRITICAL"
    
    def display_status(self):
        """Display current cell status"""
        print("\n" + "="*60)
        print(f"{'TURN ' + str(self.turn) + '/10':^60}")
        print("="*60)
        print("\nRESOURCES:")
        print(f"  ATP (Energy):           {self.display_dots(self.atp)}  {self.get_status_label(self.atp)}")
        print(f"  GLUCOSE (Fuel):         {self.display_dots(self.glucose)}  {self.get_status_label(self.glucose)}")
        print(f"  AMINO ACIDS (Building): {self.display_dots(self.amino_acids)}  {self.get_status_label(self.amino_acids)}")
        print(f"  LIPIDS (Membranes):     {self.display_dots(self.lipids)}  {self.get_status_label(self.lipids)}")
        print("\nCELL STATUS:")
        print(f"  CELL HEALTH:            {self.display_dots(self.health)}  {self.get_status_label(self.health)}")
        print(f"  MEMBRANE INTEGRITY:     {self.display_dots(self.membrane)}  {self.get_status_label(self.membrane)}")
        # Waste display (more waste is bad)
        print("\n")
        waste_status = "CLEAN" if self.waste <= 1 else "MODERATE" if self.waste <= 3 else "HIGH"
        print(f"  WASTE LEVEL: {self.display_dots(self.waste)} {waste_status}")
        
        # Active effects
        if self.has_defender:
            print("\n  ACTIVE: Defensive Proteins (next event blocked!)")
        if self.enzyme_boost:
            print("  ACTIVE: Metabolic Enzymes (+1 ATP bonus this turn!)")
        if self.golgi_bonus:
            print("  ACTIVE: Golgi Trade Bonus (+1 Glucose next import!)")
        
        print()
    
    def check_lose_conditions(self):
        """Check if player has lost the game"""
        # Health ≤ 0: Cell has suffered necrosis
        if self.health <= 0:
            return True, "Cell health reached 0! The cell has died. "
        # Membrane ≤ 0: Cell death due to membrane rupture
        if self.membrane <= 0:
            return True, "Membrane integrity reached 0! The cell has burst. "
        # Energy crisis 
        if self.atp <= 0:
            self.atp_crisis_turns += 1
            if self.atp_crisis_turns >= 2:
                return True, "ATP depleted for 2 consecutive turns! Energy crisis. "
        else:
            self.atp_crisis_turns = 0
        
        return False, ""
    
    def check_win_condition(self):
        """Check if player has won"""
        return self.turn > 10

# ============================================================================
# EVENTS SYSTEM
# ============================================================================

def get_event_for_turn(turn):
    """
    Get appropriate event(s) based on turn number

    DIFFICULTY SCALING:
    Turns 1-3: Tutorial
    - Gentle events, single stressors
    - Goal: Teach mechanics without overwhelming
    - Events are recoverable with basic actions
    
    Turns 4-7: Challenge
    - Moderate stressors, 1-2 events
    - Goal: Force resource prioritization
    - Players must make trade-offs (energy vs repair vs defense)
    
    Turns 8-10: Survival
    - Severe compound problems, always 2 events
    - Goal: Test mastery of all systems
    - Mimics how real cells face multiple simultaneous stresses
    """
    
    # Turns 1-3: Gentle introduction
    if turn <= 3:
        events = [
            (" Everything's Normal!", "No threats detected. Practice your strategy!", None),
            (" Nutrient Windfall!", "Extra nutrients float by from the environment!", 
             lambda cell: setattr(cell, 'golgi_bonus', True)),
            (" Minor Membrane Wear", "Small wear on the phospholipid bilayer.", 
             lambda cell: setattr(cell, 'membrane', max(0, cell.membrane - 1))),
            (" Metabolic Waste Buildup", "Normal cellular processes produce waste.", 
             lambda cell: setattr(cell, 'waste', min(5, cell.waste + 1))),
        ]
        return [random.choice(events)]
    
    # Turns 4-7: Increased challenge
    elif turn <= 7:
        events = [
            (" Toxic Exposure!", "Environmental toxins damage the cell!",
             lambda cell: (setattr(cell, 'health', max(0, cell.health - 1)),
                          setattr(cell, 'waste', min(5, cell.waste + 2)))),
            (" Glucose Scarcity!", "Nutrient availability drops in environment!",
             lambda cell: print("  Next import will yield less glucose!")),
            (" Oxidative Stress!", "Reactive oxygen species (ROS) damage structures!",
             lambda cell: (setattr(cell, 'health', max(0, cell.health - 1)),
                          setattr(cell, 'membrane', max(0, cell.membrane - 1)))),
            (" Pathogen Detected!", "Harmful microorganism nearby!",
             lambda cell: None),  # Handled separately for defender check
            (" Membrane Breach!", "Phospholipid damage detected!",
             lambda cell: setattr(cell, 'membrane', max(0, cell.membrane - 2))),
        ]
        
        # 50% chance of 2 events
        if random.random() < 0.5:
            return random.sample(events, 2)
        return [random.choice(events)]
    
        # Turns 8-10: Survival mode
    else:
        # ONE severe event from survival pool
        severe_events = [
            (" SEVERE STARVATION!", "Critical nutrient shortage in environment!",
             lambda cell: print(" Next 2 imports will be severely reduced!")),
            (" TOXIC OVERLOAD!", "Multiple toxins attacking the cell!",
             lambda cell: (setattr(cell, 'health', max(0, cell.health - 2)),
                          setattr(cell, 'membrane', max(0, cell.membrane - 1)),
                          setattr(cell, 'waste', min(5, cell.waste + 3)))),
            (" VIRAL ATTACK!", "Virus attempting to hijack cellular machinery!",
             lambda cell: None),  # Handled separately for defender check
            (" METABOLIC CRISIS!", "ATP production severely disrupted!",
             lambda cell: print(" Mitochondria efficiency reduced next use!")),
            (" WASTE OVERLOAD!", "Cellular waste reaching critical levels!",
             lambda cell: setattr(cell, 'waste', min(5, cell.waste + 3))),
        ]
        
        # ONE event from ANY difficulty tier (gentle, moderate, or severe)
        all_events = [
            # Gentle events (from turns 1-3)
            (" Everything's Normal!", "No threats detected. Practice your strategy!", None),
            (" Nutrient Windfall!", "Extra nutrients float by from the environment!", 
             lambda cell: setattr(cell, 'golgi_bonus', True)),
            (" Minor Membrane Wear", "Small wear on the phospholipid bilayer.", 
             lambda cell: setattr(cell, 'membrane', max(0, cell.membrane - 1))),
            (" Metabolic Waste Buildup", "Normal cellular processes produce waste.", 
             lambda cell: setattr(cell, 'waste', min(5, cell.waste + 1))),
            
            # Moderate events (from turns 4-7)
            (" Toxic Exposure!", "Environmental toxins damage the cell!",
             lambda cell: (setattr(cell, 'health', max(0, cell.health - 1)),
                          setattr(cell, 'waste', min(5, cell.waste + 2)))),
            (" Glucose Scarcity!", "Nutrient availability drops in environment!",
             lambda cell: print(" Next import will yield less glucose!")),
            (" Oxidative Stress!", "Reactive oxygen species (ROS) damage structures!",
             lambda cell: (setattr(cell, 'health', max(0, cell.health - 1)),
                          setattr(cell, 'membrane', max(0, cell.membrane - 1)))),
            (" Pathogen Detected!", "Harmful microorganism nearby!",
             lambda cell: None),  # Handled separately for defender check
            (" Membrane Breach!", "Phospholipid damage detected!",
             lambda cell: setattr(cell, 'membrane', max(0, cell.membrane - 2))),
        ] + severe_events  # Add severe events to the pool
        
        # Pick 1 severe event + 1 random event from any tier
        severe_event = random.choice(severe_events)
        random_event = random.choice(all_events)
        
        # Return both events
        return [severe_event, random_event]

# ============================================================================
# ORGANELLE ACTIONS
# ============================================================================

def action_mitochondria(cell):
    """Mitochondria: Cellular Respiration"""
    print("\n  MITOCHONDRIA - Cellular Respiration")
    print("Uses: 1 Glucose → Produces: 2 ATP")
    print("Converts glucose into usable energy through cellular respiration.")
    
    if cell.glucose < 1:
        print("  Not enough glucose!")
        return False
    
    cell.glucose -= 1
    atp_gain = 2
    
    # Enzyme boost effect
    if cell.enzyme_boost:
        atp_gain += 1
        print("  Metabolic enzyme boost active! +1 extra ATP")
        cell.enzyme_boost = False
    
    cell.atp = min(5, cell.atp + atp_gain)
    cell.waste = min(5, cell.waste + 1)  # Respiration produces some waste
    cell.stats['atp_generated'] += atp_gain
    
    print(f"✓ Generated {atp_gain} ATP! (Waste +1)")
    return True

def action_ribosomes(cell):
    """Ribosomes: Protein Synthesis"""
    print("\n  RIBOSOMES - Protein Synthesis")
    print("Uses: 1 Amino Acid + 1 ATP")
    print("\nChoose protein type:")
    print("1. Metabolic Enzymes - Boost next ATP production (+1 ATP)")
    print("2. Structural Proteins - Repair damage (+1 Health OR Membrane)")
    print("3. Defensive Proteins - Block next harmful event")
    
    if cell.amino_acids < 1 or cell.atp < 1:
        print("  Not enough resources! Need 1 Amino Acid + 1 ATP")
        return False
    
    choice = input("Choose (1/2/3): ").strip()
    
    if choice == '1':
        cell.enzyme_boost = True
        print("✓ Synthesized Metabolic Enzymes! Next mitochondria action gets +1 ATP")
    elif choice == '2':
        repair_choice = input("Repair Health or Membrane? (h/m): ").strip().lower()
        if repair_choice == 'h':
            cell.health = min(5, cell.health + 1)
            print("✓ Synthesized Structural Proteins! Health +1")
        else:
            cell.membrane = min(5, cell.membrane + 1)
            print("✓ Synthesized Structural Proteins! Membrane +1")
    elif choice == '3':
        cell.has_defender = True
        print("✓ Synthesized Defensive Proteins! Next event will be blocked")
    else:
        print("Invalid choice!")
        return False
    
    cell.amino_acids -= 1
    cell.atp -= 1
    cell.stats['proteins_made'] += 1
    return True

def action_smooth_er(cell):
    """Smooth ER: Lipid Synthesis"""
    print("\n  SMOOTH ER - Lipid Synthesis")
    print("Uses: 1 Glucose + 1 ATP → Produces: 2 Lipids")
    print("Manufactures phospholipids for cell membrane maintenance.")
    
    if cell.glucose < 1 or cell.atp < 1:
        print("  Not enough resources! Need 1 Glucose + 1 ATP")
        return False
    
    cell.glucose -= 1
    cell.atp -= 1
    cell.lipids = min(5, cell.lipids + 2)
    
    print("✓ Synthesized 2 Lipids!")
    return True

def action_lysosomes(cell):
    """Lysosomes: Waste Digestion & Recycling"""
    print("\n  LYSOSOMES - Waste Digestion & Autophagy")
    print("Uses: 1 ATP → Removes: 2 Waste, Produces: 1 Amino Acid")
    print("Breaks down cellular waste and recycles components!")
    
    if cell.atp < 1:
        print("  Not enough ATP!")
        return False
    
    if cell.waste == 0:
        print("  No waste to clean!")
        return False
    
    cell.atp -= 1
    cell.waste = max(0, cell.waste - 2)
    cell.amino_acids = min(5, cell.amino_acids + 1)
    cell.stats['waste_cleaned'] += 2
    
    print("✓ Digested waste and recycled 1 Amino Acid!")
    return True

def action_golgi(cell):
    """Golgi: Package & Export"""
    print("\n  GOLGI APPARATUS - Package & Export Proteins")
    print("Uses: 1 Amino Acid + 1 ATP")
    print("Export proteins for trade: Next import gets +1 Glucose bonus!")
    
    if cell.amino_acids < 1 or cell.atp < 1:
        print("  Not enough resources! Need 1 Amino Acid + 1 ATP")
        return False
    
    cell.amino_acids -= 1
    cell.atp -= 1
    cell.golgi_bonus = True
    
    print("✓ Packaged proteins for export! Next import gets bonus glucose")
    return True

def action_membrane_repair(cell):
    """Membrane: Direct Lipid Repair"""
    print("\n  MEMBRANE REPAIR - Phospholipid Replacement")
    print("Uses: 2 Lipids → Restores: 1 Membrane Integrity")
    print("Directly repair the phospholipid bilayer.")
    
    if cell.lipids < 2:
        print("  Not enough lipids! Need 2 Lipids")
        return False
    
    cell.lipids -= 2
    cell.membrane = min(5, cell.membrane + 1)
    
    print("✓ Repaired membrane structure!")
    return True

# ============================================================================
# GAME PHASES
# ============================================================================

def import_phase(cell):
    """Phase 1: Import nutrients from environment"""
    print("\n" + "="*60)
    print("PHASE 1: NUTRIENT IMPORT")
    print("="*60)
    print("\nThe cell membrane controls what enters the cell.")
    print("Choose your transport method:\n")
    print("A.   ACTIVE TRANSPORT - Costs 1 ATP")
    print("   Uses ATP-powered pumps to import: 2 Glucose + 1 Amino Acid")
    print("   (Pumps molecules AGAINST concentration gradient)\n")
    print("B.   PASSIVE DIFFUSION - FREE")
    print("   Molecules naturally flow in: 1 Glucose + 1 Amino Acid")
    print("   (Slower, but no energy cost)\n")
    
    while True:
        choice = input("Choose (A/B): ").strip().upper()
        
        if choice == 'A':
            if cell.atp < 1:
                print("  Not enough ATP for active transport!")
                print("Falling back to passive diffusion...\n")
                choice = 'B'
            else:
                cell.atp -= 1
                glucose_gain = 2
                aa_gain = 1
                cell.stats['active_transports'] += 1
                print("\n✓ Active transport engaged!")
                break
        
        if choice == 'B':
            glucose_gain = 1
            aa_gain = 1
            cell.stats['passive_transports'] += 1
            print("\n✓ Passive diffusion occurring...")
            break
        
        print("Invalid choice! Please enter A or B")
    
    # Apply Golgi bonus if active
    if cell.golgi_bonus:
        glucose_gain += 1
        print("  Golgi trade bonus applied! +1 extra Glucose")
        cell.golgi_bonus = False
    
    cell.glucose = min(5, cell.glucose + glucose_gain)
    cell.amino_acids = min(5, cell.amino_acids + aa_gain)
    
    print(f"Imported: {glucose_gain} Glucose, {aa_gain} Amino Acids")
    input("\nPress ENTER to continue...")

def event_phase(cell):
    """Phase 2: Random stress events"""
    print("\n" + "="*60)
    print("PHASE 2: CELLULAR EVENTS")
    print("="*60)
    
    events = get_event_for_turn(cell.turn)
    
    for event_name, event_desc, event_effect in events:
        print(f"\n  EVENT: {event_name}")
        print(f"   {event_desc}")
        
        # Special handling for pathogen events (check defender)
        if "Pathogen" in event_name or "Viral" in event_name:
            if cell.has_defender:
                print("     Defensive Proteins activated! Attack blocked!")
                cell.has_defender = False
            else:
                damage = 2 if "VIRAL" in event_name else 1
                cell.health = max(0, cell.health - damage)
                print(f"     No defensive proteins! Health -{damage}")
        elif event_effect:
            event_effect(cell)

        #Helpful Hints
        if "Toxic" in event_name or "Oxidative" in event_name:
            print("\n      How to respond:")
            print("      • Use RIBOSOMES → Structural Proteins to repair health")
            print("      • Use LYSOSOMES to clean up the extra waste")
        
        elif "Membrane" in event_name:
            print("\n      How to respond:")
            print("      • Use SMOOTH ER to make lipids")
            print("      • Use MEMBRANE REPAIR to restore integrity")
        
        elif "Scarcity" in event_name or "Starvation" in event_name:
            print("\n      How to respond:")
            print("      • Use GOLGI now for bonus glucose next turn")
            print("      • Use LYSOSOMES to recycle amino acids")
            print("      • Conserve ATP - use Passive Diffusion next import")
        
        elif "Waste" in event_name:
            print("\n      How to respond:")
            print("      • Use LYSOSOMES immediately!")
            print("      • High waste damages health each turn")
    
    input("\nPress ENTER to continue...")

def action_phase(cell):
    """Phase 3: Player chooses organelle actions"""
    print("\n" + "="*60)
    print("PHASE 3: ORGANELLE ACTIONS")
    print("="*60)
    print("\nYou can use 3 ORGANELLES this turn.")
    print("\nChoose wisely to keep your cell alive!\n")

    #Turn Order
    print("  WHAT HAPPENS EACH TURN:")
    print("  ✓ Import nutrients (Phase 1)")
    print("  ✓ Events occur (Phase 2)")
    print("  → Choose 3 organelle actions (Phase 3) ← YOU ARE HERE")
    print("  → Automatic maintenance:")
    print("      • Membrane -1 (natural decay)")
    print("      • ATP -1 (basic functions)")
    if cell.waste >= 3:
        print(f"      • Waste damaging health (currently -{2 if cell.waste >= 4 else 1})")
    print()

    actions_remaining = 3

    def show_compact_status():
        """Display compact resource bar at top of menu"""
        print("CELL STATUS")
        print(f" ATP:       {cell.display_dots(cell.atp)}")
        print(f" Glucose:   {cell.display_dots(cell.glucose)}")
        print(f" Amino:     {cell.display_dots(cell.amino_acids)}")
        print(f" Lipids:    {cell.display_dots(cell.lipids)}")
        print(f" Health:    {cell.display_dots(cell.health)}")
        print(f" Membrane:  {cell.display_dots(cell.membrane)}")

        # Show waste warning if high
        waste_display = f"Waste: {cell.display_dots(cell.waste)}"
        if cell.waste >= 3:
            waste_display += " (HIGH!)"
        print(f" {waste_display:<55}\n")

    def show_warnings_and_tips():
        """Display contextual warnings based on current cell state"""
        warnings = []
        tips = []
        
        # Check for critical conditions
        if cell.atp <= 1:
            warnings.append("ATP is CRITICAL! Generate energy NOW or enter crisis mode")
        elif cell.atp <= 2:
            warnings.append("ATP is LOW! Consider using Mitochondria")
        
        if cell.waste >= 4:
            warnings.append("Waste is VERY HIGH! Damaging health each turn (-2)")
        elif cell.waste >= 3:
            warnings.append("Waste is HIGH (≥3)! Currently damaging health (-1/turn)")
        
        if cell.membrane <= 1:
            warnings.append("Membrane CRITICAL! Cell will burst at 0!")
        
        elif cell.membrane <= 2:
            warnings.append("Membrane is LOW! Consider making lipids or repairing")
        
        if cell.health <= 2:
            warnings.append("Health is LOW! Make Structural Proteins to recover")
        
        # Strategic tips
        if cell.has_defender:
            tips.append("You have Defensive Protein active - next event blocked!")
        
        if cell.enzyme_boost:
            tips.append("Metabolic enzyme ready - next Mitochondria gives +1 ATP bonus!")
        
        if cell.golgi_bonus:
            tips.append("Golgi bonus active - next import gives +1 Glucose!")
        
        if cell.glucose >= 4 and cell.atp >= 3:
            tips.append("Good resource levels! You're in a strong position")
        
        # Display warnings
        if warnings:
            print("\n   CRITICAL WARNINGS:")
            for warning in warnings:
                print(f"  • {warning}")
        
        # Display tips
        if tips:
            print("\n  STRATEGIC INFO:")
            for tip in tips:
                print(f"  • {tip}")
        
        print()  # Blank line for spacing

    def show_action_result(before_atp, before_glucose, before_aa, before_lipids, before_waste):
        """Show before/after comparison after an action"""
        print("\n" + "-"*60)
        print("RESULT:")
        
        # Show resources that changed only
        changes = []
        if cell.atp != before_atp:
            changes.append(f"  ATP: {cell.display_dots(before_atp)} → {cell.display_dots(cell.atp)}")
        if cell.glucose != before_glucose:
            changes.append(f"  Glucose: {cell.display_dots(before_glucose)} → {cell.display_dots(cell.glucose)}")
        if cell.amino_acids != before_aa:
            changes.append(f"  Amino Acids: {cell.display_dots(before_aa)} → {cell.display_dots(cell.amino_acids)}")
        if cell.lipids != before_lipids:
            changes.append(f"  Lipids: {cell.display_dots(before_lipids)} → {cell.display_dots(cell.lipids)}")
        if cell.waste != before_waste:
            changes.append(f"  Waste: {cell.display_dots(before_waste)} → {cell.display_dots(cell.waste)}")
        
        for change in changes:
            print(f"  {change}")
        
        print("-"*60)

    while actions_remaining > 0:
        print(f"\n--- Actions Remaining: {actions_remaining} ---")
        #Show status and warnings before each choice
        show_compact_status()
        show_warnings_and_tips()
        print("\nAvailable Organelles:")

        #1. Mitochondria
        print("\n1. MITOCHONDRIA")
        print("   Generate energy for other actions")
        print(f"   → Uses: 1 Glucose ({cell.display_dots(1, 1)}) | Produces: 2 ATP ({cell.display_dots(2, 2)})")
        print("     Good choice when: You're low on ATP")

        #2. Ribosomes
        print("\n2. RIBOSOMES")
        print("   Build specialized proteins for different jobs")
        print(f"   → Uses: 1 Amino Acid ({cell.display_dots(1, 1)}) + 1 ATP ({cell.display_dots(1, 1)})")
        print("     Good choice when: Cell needs defense, repair, or enzyme boost")

        #3. Smooth ER
        print("\n3. SMOOTH ER")
        print("   Make membrane materials to prevent rupture")
        print(f"   → Uses: 1 Glucose ({cell.display_dots(1, 1)}) + 1 ATP ({cell.display_dots(1, 1)}) | Produces: 2 Lipids ({cell.display_dots(2, 2)})")
        print("     Good choice when: Membrane integrity is dropping")

        #4. Lysosomes
        print("\n4. LYSOSOMES")
        print("   Earn materials in return for cleaning up waste")
        print(f"   → Uses: 1 ATP ({cell.display_dots(1, 1)}) | Removes: 2 Waste | Produces: 1 Amino Acid ({cell.display_dots(1, 1)})")
        print("     Good choice when: Waste is ≥ 3 (it damages health!)")

        #5. Golgi
        print("\n5. GOLGI APPARATUS")
        print("   Export proteins to get bonus glucose later")
        print(f"   → Uses: 1 Amino Acid ({cell.display_dots(1, 1)}) + 1 ATP ({cell.display_dots(1, 1)}) | Next import: +1 Glucose")
        print("     Good choice when: Planning ahead, glucose running low")
        
        # 6. Membrane Repair
        print("\n6. MEMBRANE REPAIR")
        print("   Direct repair of cell wall")
        print(f"   → Uses: 2 Lipids ({cell.display_dots(2, 2)}) | Restores: 1 Membrane ({cell.display_dots(1, 1)})")
        print("     Good choice when: Membrane is CRITICAL")
        
        print("\n7.   SKIP remaining actions")

        
        choice = input("\nChoose organelle (1-7): ").strip().lower()
        
        if choice == 'status':
            cell.display_status()
            continue
        
        if choice.startswith('learn'):
            topic = choice.replace('learn', '').strip()
            if topic in LEARN_MORE:
                print(LEARN_MORE[topic])
            else:
                print("Topic not found. Try: atp, glucose, amino acids, lipids,")
                print("mitochondria, ribosomes, smooth er, lysosomes, golgi, membrane")
            input("\nPress ENTER to continue...")
            continue
        
        #Snapshot before each action
        before_atp = cell.atp
        before_glucose = cell.glucose
        before_aa = cell.amino_acids
        before_lipids = cell.lipids
        before_waste = cell.waste

        success = False
        if choice == '1':
            success = action_mitochondria(cell)
        elif choice == '2':
            success = action_ribosomes(cell)
        elif choice == '3':
            success = action_smooth_er(cell)
        elif choice == '4':
            success = action_lysosomes(cell)
        elif choice == '5':
            success = action_golgi(cell)
        elif choice == '6':
            success = action_membrane_repair(cell)
        elif choice == '7':
            print("Skipping remaining actions...")
            break
        else:
            print("Invalid choice!")
            continue
        
        if success:
            show_action_result(before_atp, before_glucose, before_aa, before_lipids, before_waste)
            actions_remaining -= 1
            input("\nPress ENTER to continue...")

def maintenance_phase(cell):
    """Phase 4: Automatic maintenance and consequences"""
    print("\n" + "="*60)
    print("PHASE 4: CELLULAR MAINTENANCE")
    print("="*60)
    
    changes = []
    
    # Membrane naturally decays (lipid turnover)
    cell.membrane = max(0, cell.membrane - 1)
    changes.append("  Membrane naturally decayed (-1) - lipid turnover")
    
    # Base ATP upkeep
    cell.atp = max(0, cell.atp - 1)
    changes.append("  Basic cellular functions consumed ATP (-1)")
    
    # Waste damage to health
    if cell.waste >= 4:
        cell.health = max(0, cell.health - 2)
        changes.append("  HIGH waste levels damaged cell health (-2)!")
    elif cell.waste >= 3:
        cell.health = max(0, cell.health - 1)
        changes.append("  Waste accumulation damaged health (-1)")
    
    print("\nAutomatic processes:")
    for change in changes:
        print(f"  • {change}")
    
    input("\nPress ENTER to see results...")

def end_game_summary(cell, won):
    """Display educational summary"""
    print("\n" + "="*60)
    if won:
        print("  CONGRATULATIONS! YOUR CELL SURVIVED!  ")
    else:
        print("  GAME OVER  ")
    print("="*60)
    
    print("\n🎓 CELL BIOLOGY CONCEPTS YOU APPLIED:\n")
    
    print("  CELLULAR RESPIRATION")
    print(f"   You used mitochondria to generate {cell.stats['atp_generated']} total ATP")
    print("   Real equation: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + 30 ATP\n")
    
    print("  PROTEIN SYNTHESIS")
    print(f"   You synthesized {cell.stats['proteins_made']} proteins at ribosomes")
    print("   Process: DNA → mRNA → Protein\n")
    
    print("  AUTOPHAGY & CELLULAR RECYCLING")
    print(f"   Lysosomes recycled {cell.stats['waste_cleaned']} units of waste")
    print("   This won the 2016 Nobel Prize in Medicine!\n")
    
    print("  ACTIVE vs PASSIVE TRANSPORT")
    print(f"   Active transport: {cell.stats['active_transports']} times (costs ATP)")
    print(f"   Passive diffusion: {cell.stats['passive_transports']} times (free)\n")
    
    print("  HOMEOSTASIS")
    print("   You balanced energy, waste, repairs, and defense")
    print("   Real cells do this every second!\n")
    
    print("="*60)
    print(f"Turns Survived: {cell.turn - 1}/10")
    print("="*60)

# ============================================================================
# MAIN GAME LOOP
# ============================================================================

"""
    GAME FLOW:
    1. Intro/tutorial message
    2. Loop through turns 1-10:
       a. Display status       (show current resources/health)
       b. Phase 1: Import      (player chooses transport method)
       c. Phase 2: Events      (random stress applied)
       d. Phase 3: Actions     (player uses 3 organelles)
       e. Phase 4: Maintenance (automatic costs applied)
       f. Check win/lose conditions
    3. End-game summary        (educational recap)
    
    Scaffold:
    - Turn 1: Extra tutorial hints
    - Turn 2: Hint about membrane decay
    - Turn 3: Hint about waste management
    - Turns 4+: Player is on their own (test understanding)
    """

def main():
    """Main game loop"""
    print("="*60)
    print("  WELCOME TO MICROMANAGER!  ")
    print("="*60)
    print("\nYou are the manager of a eukaryotic cell!")
    print("Your mission: Keep the cell alive for 10 turns.\n")
    print("You'll manage resources, respond to stress events,")
    print("and use organelles to maintain cellular homeostasis.\n")
    print("Type 'learn [topic]' anytime to learn more about cell biology!")
    print("Type 'status' during actions to check your resources.\n")
    
    input("Press ENTER to start your cellular adventure...")
    
    # Initialize game
    cell = CellState()
    
    # Tutorial message for turn 1
    if cell.turn == 1:
        print("\n" + "="*60)
        print("  TUTORIAL - TURN 1")
        print("="*60)
        print("\nFirst, you'll import nutrients from the environment.")
        print("Try ACTIVE TRANSPORT to get more resources (costs ATP).")
        print("Then use organelles to generate energy and build proteins!")
        input("\nPress ENTER to begin...")
    
    # Main game loop
    while True:
        # Display current status
        cell.display_status()
        
        # Check win condition
        if cell.check_win_condition():
            end_game_summary(cell, won=True)
            break
        
        # Tutorial hints
        if cell.turn == 2:
            print("  TIP: Notice your Membrane went down? That's natural!")
            print("   Use Smooth ER to make lipids, then repair the membrane.\n")
        elif cell.turn == 3:
            print("  TIP: Waste is building up from metabolism.")
            print("   Use Lysosomes to clean it and recycle amino acids!\n")
        
        # Phase 1: Import nutrients
        import_phase(cell)
        
        # Phase 2: Events
        event_phase(cell)
        
        # Check lose condition after events
        lost, reason = cell.check_lose_conditions()
        if lost:
            print("\n" + "="*60)
            print(f"  {reason}")
            print("="*60)
            end_game_summary(cell, won=False)
            break
        
        # Phase 3: Player actions
        action_phase(cell)
        
        # Phase 4: Maintenance
        maintenance_phase(cell)
        
        # Check lose condition after maintenance
        lost, reason = cell.check_lose_conditions()
        if lost:
            print("\n" + "="*60)
            print(f"  {reason}")
            print("="*60)
            end_game_summary(cell, won=False)
            break
        
        # Advance to next turn
        cell.turn += 1
    
    # End game
    print("\n  Thank you for playing MicroManager!  ")
    print("\nYour cells are doing this RIGHT NOW in your body!")
    print("Every second, billions of cells work together to keep you alive.\n")
    
    # Offer to play again
    again = input("Play again? (y/n): ").strip().lower()
    if again == 'y':
        main()
    else:
        print("\n  Keep learning about the amazing world of cells!  ")

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    main()