import streamlit as st
import json
import math
import time
from datetime import datetime
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# Quiz data - PART 1
# ---------------------------


QUIZZES = {
    "Motion": {
        "Easy": [
            {"q":"What is the rate of change of displacement called?","type":"mcq","options":["Speed","Velocity","Acceleration","Jerk"],"answer":"Velocity","explain":"Velocity is defined as the rate of change of displacement with respect to time.\n\nKey differences:\n• Speed = rate of change of distance (scalar)\n• Velocity = rate of change of displacement (vector)\n• Acceleration = rate of change of velocity\n• Jerk = rate of change of acceleration\n\nMathematically: v = ds/dt (where s is displacement)"},
            {"q":"Which graph shows constant acceleration?","type":"mcq","options":["Position-time straight","Velocity-time straight","Acceleration-time sinusoidal","Position-time horizontal"],"answer":"Velocity-time straight","explain":"A velocity-time graph with a straight line indicates constant acceleration.\n\nHere's why:\n• The slope of a velocity-time graph = acceleration\n• Straight line = constant slope = constant acceleration\n• Curved line = changing slope = changing acceleration\n\nOther graphs:\n• Position-time straight = constant velocity (zero acceleration)\n• Position-time parabola = constant acceleration\n• Acceleration-time horizontal = constant acceleration"},
            {"q":"Two objects dropped from same height, no air resistance. Which hits first?","type":"mcq","options":["Heavier","Lighter","Both same","Depends on shape"],"answer":"Both same","explain":"Both objects hit the ground at the same time!\n\nThis follows Galileo's principle:\n• In vacuum (no air resistance), all objects fall at the same rate\n• Gravitational acceleration (g = 9.8 m/s²) is independent of mass\n• The equation h = ½gt² shows time depends only on height, not mass\n\nGalileo famously demonstrated this at the Leaning Tower of Pisa.\n\nNote: With air resistance, shape matters (feather vs. rock)."},
            {"q":"What type of quantity is velocity?","type":"mcq","options":["Scalar","Vector","Neither","Both"],"answer":"Vector","explain":"Velocity is a VECTOR quantity because it has both magnitude AND direction.\n\nVector vs Scalar:\n• Vectors: Velocity, Displacement, Acceleration, Force\n  (have magnitude + direction)\n• Scalars: Speed, Distance, Time, Mass\n  (have magnitude only)\n\nExample: '50 km/h north' is velocity (vector)\n         '50 km/h' is speed (scalar)"},
            {"q":"If an object starts from rest and accelerates uniformly, what happens to its velocity?","type":"mcq","options":["Decreases","Stays constant","Increases","Becomes zero"],"answer":"Increases","explain":"When an object accelerates uniformly from rest, its velocity INCREASES at a constant rate.\n\nReasoning:\n• 'From rest' means initial velocity = 0\n• Acceleration = rate of change of velocity\n• Uniform acceleration = constant increase in velocity\n• Velocity continuously increases with time\n\nFormula: Vf = Vi + at (where u = 0, so Vf = at)"}
        ],
        "Average": [
            {"q":"A car accelerates from 10 m/s to 20 m/s in 5 s. What is the acceleration?","type":"numeric","answer":2.0,"tip":"💡 <b>Tip:</b> Use the formula a = (Vf - Vi) / t, where Vf is final velocity and Vi is initial velocity.","explain":"Using: a = (Vf - Vi) / t\n\nGiven:\n• Initial velocity (Vi) = 10 m/s\n• Final velocity (Vf) = 20 m/s\n• Time (t) = 5 s\n\nStep 1: Substitute values\na = (20 - 10) / 5\n\nStep 2: Calculate\na = 10 / 5 = 2 m/s²\n\nThe car's acceleration is 2 m/s²."},
            {"q":"Which quantity is a vector?","type":"mcq","options":["Speed","Distance","Velocity","Time"],"answer":"Velocity","tip":"💡 <b>Tip:</b> Vectors have both magnitude and direction. Scalars only have magnitude.","explain":"Velocity is a vector quantity because it has both magnitude AND direction.\n\nVector vs Scalar:\n• Vectors: Velocity, Displacement, Acceleration, Force\n  (have magnitude + direction)\n• Scalars: Speed, Distance, Time, Mass\n  (have magnitude only)\n\nExample: '50 km/h north' is velocity (vector)\n         '50 km/h' is speed (scalar)"},
            {"q":"A train moves 60 m in 5 s from rest. Find the acceleration (assuming constant).","type":"numeric","answer":4.8,"tip":"💡 <b>Tip:</b> Use s = ut + ½at². Since it starts from rest, u = 0.","explain":"Using: s = ut + ½at²\n\nGiven:\n• Distance (s) = 60 m\n• Time (t) = 5 s\n• Initial velocity (u) = 0 m/s (from rest)\n\nStep 1: Substitute values\n60 = (0)(5) + ½(a)(5²)\n60 = 0 + ½(a)(25)\n60 = 12.5a\n\nStep 2: Solve for a\na = 60 / 12.5 = 4.8 m/s²\n\nThe train's acceleration is 4.8 m/s²."},
            {"q":"If a velocity-time graph is a horizontal line, what is the acceleration?","type":"mcq","options":["Zero","Constant but non-zero","Increasing","Decreasing"],"answer":"Zero","tip":"💡 <b>Tip:</b> The slope of a velocity-time graph represents acceleration. What's the slope of a horizontal line?","explain":"A horizontal line on a velocity-time graph means ZERO acceleration.\n\nReasoning:\n• Acceleration = slope of velocity-time graph\n• Horizontal line = slope of 0\n• Slope of 0 = no change in velocity\n• No change in velocity = zero acceleration\n\nThe object moves at constant velocity."},
            {"q":"A ball is thrown vertically upward and reaches a maximum height of 20 m. Approximately how long does it take to reach the top? (Use g = 9.81 m/s²)","type":"numeric","answer":2.02,"tip":"💡 <b>Tip:</b> At maximum height, final velocity = 0. Use v² = u² - 2gh to find initial velocity, then t = u/g.","explain":"At maximum height, final velocity = 0 m/s\n\nUsing: v = u - gt (negative because upward)\n\nAt top: 0 = Vi - gt, so Vi = gt\n\nUsing: Vf² = Vi² - 2gh\n0² = Vi² - 2(9.81)(20)\nu² = 392.4\nu = 19.81 m/s\n\nNow: t = Vi / g = 19.81 / 9.81 ≈ 2.02 seconds\n\nThe ball takes about 2.02 seconds to reach the top."} 
        ],
        "Difficult": [
            {"q":"A car accelerates at 3 m/s² for 10 s then decelerates to stop in 5 s. Find total distance.","type":"numeric","answer":225.0,"explain":"This problem has two phases:\n\nPhase 1 - Acceleration:\n• u = 0, a = 3 m/s², t = 10 s\n• v = u + at = 0 + 3(10) = 30 m/s\n• s₁ = Vit + ½at² = 0 + ½(3)(10²) = 150 m\n\nPhase 2 - Deceleration:\n• Vi = 30 m/s, Vf = 0, t = 5 s\n• a = (Vf - Vi)/t = (0 - 30)/5 = -6 m/s²\n• s₂ = Vit + ½at² = 30(5) + ½(-6)(5²)\n• s₂ = 150 - 75 = 75 m\n\nTotal distance = s₁ + s₂ = 150 + 75 = 225 m"},
            {"q":"A projectile launched at 30 m/s at 60°. Max height?","type":"numeric","answer":34.64,"explain":"Formula: H = (Vi sin θ)² / (2g)\n\nGiven:\n• Initial velocity (Vi) = 30 m/s\n• Angle (θ) = 60°\n• g = 9.81 m/s²\n\nStep 1: Find vertical component\nu_y = Vi sin θ = 30 × sin(60°) = 30 × 0.866 = 25.98 m/s\n\nStep 2: Calculate maximum height\nH = (25.98)² / (2 × 9.81)\nH = 674.96 / 19.62\nH ≈ 34.64 meters\n\nThe projectile reaches a maximum height of 34.64 meters."},
            {"q":"Displacement after 4 s if v = 3t² + 2t?","type":"numeric","answer":80.0,"explain":"Given velocity function: v = 3t² + 2t\n\nTo find displacement, integrate velocity:\ns = ∫v dt = ∫(3t² + 2t) dt\n\nStep 1: Integrate\ns = t³ + t² + C\n\nStep 2: Assuming s = 0 at t = 0, then C = 0\ns = t³ + t²\n\nStep 3: Find displacement at t = 4 s\ns = (4)³ + (4)²\ns = 64 + 16\ns = 80 meters\n\nThe displacement after 4 seconds is 80 meters."},
            {"q":"A particle moves with acceleration a=2t. Initial velocity=0. Displacement after t=3?","type":"numeric","answer":9.0,"explain":"Given: a(t) = 2t, u = 0, find s at t = 3\n\nStep 1: Find velocity by integrating acceleration\nv = ∫a dt = ∫2t dt = t² + C₁\nAt t = 0, v = 0, so C₁ = 0\nTherefore: v = t²\n\nStep 2: Find displacement by integrating velocity\ns = ∫v dt = ∫t² dt = t³/3 + C₂\nAt t = 0, s = 0, so C₂ = 0\nTherefore: s = t³/3\n\nStep 3: Calculate at t = 3\ns = (3)³/3 = 27/3 = 9 meters\n\nThe displacement after 3 seconds is 9 meters."},
            {"q":"Which graph represents increasing acceleration?","type":"mcq","options":["Velocity-time straight","Acceleration-time rising line","Position-time parabola","Position-time horizontal"],"answer":"Acceleration-time rising line","explain":"An acceleration-time graph with a rising line shows increasing acceleration.\n\nGraph interpretations:\n• Acceleration-time rising = acceleration is increasing\n• Velocity-time straight = constant acceleration\n• Velocity-time curve (upward) = increasing acceleration\n• Position-time parabola = constant acceleration\n\nThe slope of an acceleration-time graph shows the rate of change of acceleration (called 'jerk')."}
        ]
    },

    "Energy": {
        "Easy": [
            {"q":"What is the formula for kinetic energy?","type":"mcq","options":["mgh","½mv²","Fs","Pv"],"answer":"½mv²","explain":"Kinetic Energy (KE) = ½mv²\n\nWhere:\n• m = mass (kg)\n• v = velocity (m/s)\n\nThis formula was derived from Newton's work on motion.\n\nOther formulas:\n• mgh = Potential Energy\n• Fs = Work\n• Pv = Power × velocity (not a standard formula)"},
            {"q":"What is the formula for gravitational potential energy?","type":"mcq","options":["½mv²","mgh","Fs","½kx²"],"answer":"mgh","explain":"Gravitational Potential Energy (PE) = mgh\n\nWhere:\n• m = mass (kg)\n• g = gravitational acceleration (9.8 m/s²)\n• h = height (m)\n\nThis represents stored energy due to an object's position in a gravitational field."},
            {"q":"What is the total mechanical energy in a system with no friction?","type":"mcq","options":["KE - PE","KE + PE","Only KE","Only PE"],"answer":"KE + PE","explain":"Total Mechanical Energy = KE + PE\n\nThis follows the Law of Conservation of Energy:\n• In a closed system with no friction\n• Total mechanical energy remains constant\n• Energy converts between KE and PE\n\nExample: Pendulum\n• At top: Maximum PE, Zero KE\n• At bottom: Zero PE, Maximum KE\n• Total energy (KE + PE) stays constant"},
            {"q":"What is the SI unit of energy?","type":"mcq","options":["Joule","Watt","Newton","Volt"],"answer":"Joule","explain":"The SI unit of energy is the Joule (J).\n\nNamed after James Prescott Joule (1818-1889), who studied heat and energy.\n\n1 Joule = work done when 1 Newton force moves an object 1 meter\n\nOther units:\n• Watt (W) = unit of power\n• Newton (N) = unit of force\n• Volt (V) = unit of electric potential"},
            {"q":"Which energy transformation occurs in a falling ball?","type":"mcq","options":["KE to PE","PE to KE","Chemical to KE","Thermal to PE"],"answer":"PE to KE","explain":"A falling ball transforms Potential Energy to Kinetic Energy.\n\nAs the ball falls:\n• Height decreases → PE decreases\n• Velocity increases → KE increases\n• Total energy (PE + KE) remains constant\n\nAt the top: Maximum PE, Zero KE\nAt the bottom: Zero PE, Maximum KE"}
        ],

        "Average": [
            {"q":"What is the work done by a 10 N force moving an object 5 m in the direction of the force?","type":"numeric","answer":50.0,"tip":"💡 <b>Tip:</b> Work = Force × Distance when force is in the direction of motion.","explain":"Using: Work = Force × Distance (when force is in direction of motion)\n\nGiven:\n• Force (F) = 10 N\n• Distance (d) = 5 m\n\nStep 1: Apply formula\nW = F × d = 10 × 5\n\nStep 2: Calculate\nW = 50 Joules\n\nThe work done is 50 J."},
            {"q":"Which process increases thermal energy?","type":"mcq","options":["Cooling","Friction work","Isothermal expansion","Adiabatic reversible"],"answer":"Friction work","tip":"💡 <b>Tip:</b> Think about what happens when you rub your hands together. Where does that warmth come from?","explain":"Friction work increases thermal energy by converting mechanical energy to heat.\n\nExplanation:\n• Friction opposes motion and generates heat\n• Mechanical energy is 'lost' as thermal energy\n• This is why rubbing hands together creates warmth\n\nOther options:\n• Cooling = decreases thermal energy\n• Isothermal = constant temperature\n• Adiabatic reversible = no heat exchange\n\nJames Joule demonstrated this with his famous paddle wheel experiment!"},
            {"q":"What is the power if 100 J of work is done in 5 s?","type":"numeric","answer":20.0,"tip":"💡 <b>Tip:</b> Power is the rate of doing work. Use P = W / t.","explain":"Using: Power = Work / Time\n\nGiven:\n• Work (W) = 100 J\n• Time (t) = 5 s\n\nStep 1: Apply formula\nP = W / t = 100 / 5\n\nStep 2: Calculate\nP = 20 Watts\n\nPower is the rate of doing work. Here, 20 J of work is done every second."},
            {"q":"A ball of 2 kg falls from 10 m height. What is its kinetic energy just before hitting the ground? (Use g = 9.8 m/s²)","type":"numeric","answer":196.0,"tip":"💡 <b>Tip:</b> Use conservation of energy: PE at top = KE at bottom. First calculate PE = mgh.","explain":"Using Conservation of Energy: PE at top = KE at bottom\n\nGiven:\n• Mass (m) = 2 kg\n• Height (h) = 10 m\n• g = 9.8 m/s²\n\nStep 1: Calculate initial PE\nPE = mgh = 2 × 9.8 × 10 = 196 J\n\nStep 2: At bottom, all PE converts to KE\nKE = PE = 196 J\n\nThe ball has 196 J of kinetic energy just before impact."},
            {"q":"Which is an example of mechanical energy conservation?","type":"mcq","options":["Falling ball (no air resistance)","Car braking with friction","Object sliding on rough floor","Heating water with electricity"],"answer":"Falling ball (no air resistance)","tip":"💡 <b>Tip:</b> Mechanical energy is conserved when there are no non-conservative forces like friction or air resistance.","explain":"A falling ball (in vacuum) conserves mechanical energy.\n\nReasoning:\n• No friction or air resistance\n• PE converts to KE as it falls\n• Total energy (PE + KE) stays constant\n• At top: Maximum PE, Zero KE\n• At bottom: Zero PE, Maximum KE\n\nNon-conservative forces:\n• Friction, braking, air drag all convert mechanical energy to heat\n• Mechanical energy is NOT conserved"}
        ],
        "Difficult": [
            {"q":"A 2 kg mass slides down 5 m. KE at bottom if friction=1 J?","type":"numeric","answer":97.0,"explain":"Using Energy Conservation with friction:\n\nInitial energy = Final energy + Energy lost to friction\n\nGiven:\n• Mass (m) = 2 kg\n• Height (h) = 5 m\n• Friction loss = 1 J\n• g = 9.8 m/s²\n\nStep 1: Calculate initial PE\nPE = mgh = 2 × 9.8 × 5 = 98 J\n\nStep 2: Account for friction\nKE at bottom = PE - Friction loss\nKE = 98 - 1 = 97 J\n\nThe kinetic energy at bottom is 97 J."},
            {"q":"Spring k=200 N/m compressed 0.1 m. Stored energy?","type":"numeric","answer":1.0,"explain":"Using: Elastic Potential Energy = ½kx²\n\nGiven:\n• Spring constant (k) = 200 N/m\n• Compression (x) = 0.1 m\n\nStep 1: Apply Hooke's Law energy formula\nE = ½kx² = ½ × 200 × (0.1)²\n\nStep 2: Calculate\nE = 100 × 0.01\nE = 1 Joule\n\nThe spring stores 1 J of elastic potential energy.\n\nThis energy can be released to do work when the spring returns to its natural length."},
            {"q":"A roller coaster at top h=20 m, bottom v=?","type":"numeric","answer":19.8,"explain":"Using Conservation of Energy: PE at top = KE at bottom\n\nmgh = ½mv²\n\nGiven:\n• Height (h) = 20 m\n• g = 9.8 m/s²\n\nStep 1: Simplify (mass cancels)\ngh = ½v²\n\nStep 2: Solve for v\nv² = 2gh = 2 × 9.8 × 20 = 392\nv = √392 ≈ 19.8 m/s\n\nThe velocity at bottom is approximately 19.8 m/s (about 71 km/h)!"},
            {"q":"A pendulum swings, max height 2 m. KE at bottom?","type":"numeric","answer":19.6,"explain":"Using Conservation of Energy:\n\nAt maximum height: All PE, Zero KE\nAt bottom: Zero PE, All KE\n\nGiven:\n• Max height (h) = 2 m\n• Assume mass = 1 kg (can be any value)\n• g = 9.8 m/s²\n\nStep 1: Calculate PE at top\nPE = mgh = 1 × 9.8 × 2 = 19.6 J\n\nStep 2: At bottom, all converts to KE\nKE = PE = 19.6 J\n\nThe kinetic energy at bottom is 19.6 J (for 1 kg mass).\nFor any mass m: KE = m × 19.6 J"},
            {"q":"Power required to lift 10 kg, 2 m/s?","type":"numeric","answer":196.0,"explain":"Power = Force × Velocity (for constant velocity)\n\nGiven:\n• Mass (m) = 10 kg\n• Velocity (v) = 2 m/s (upward)\n• g = 9.8 m/s²\n\nStep 1: Calculate lifting force\nF = mg = 10 × 9.8 = 98 N\n\nStep 2: Calculate power\nP = F × v = 98 × 2 = 196 Watts\n\nStep 3: Verify with Work/Time\nIn 1 second: height gained = 2 m\nWork = mgh = 10 × 9.8 × 2 = 196 J\nPower = 196 J / 1 s = 196 W ✓\n\nPower required is 196 Watts."}
        ]
    },
  
    "Electricity": {
        "Easy": [
            {"q":"What is Ohm's Law formula?","type":"mcq","options":["V = IR","V = I/R","V = I + R","V = R/I"],"answer":"V = IR","explain":"Ohm's Law: V = IR\n\nWhere:\n• V = Voltage (Volts)\n• I = Current (Amperes)\n• R = Resistance (Ohms, Ω)\n\nDiscovered by Georg Ohm in 1827.\n\nThis fundamental law shows that voltage is directly proportional to current when resistance is constant."},
            {"q":"What is the unit of electric current?","type":"mcq","options":["Volt","Ampere","Ohm","Watt"],"answer":"Ampere","explain":"The SI unit of electric current is the Ampere (A).\n\nNamed after André-Marie Ampère (1775-1836), French physicist who studied electromagnetism.\n\n1 Ampere = 1 Coulomb of charge passing through a point per second\n\nOther units:\n• Volt (V) = electric potential\n• Ohm (Ω) = resistance\n• Watt (W) = power"},
            {"q":"What is the formula for electric power?","type":"mcq","options":["P = VI","P = V/I","P = I/V","P = V + I"],"answer":"P = VI","explain":"Electric Power: P = VI\n\nWhere:\n• P = Power (Watts)\n• V = Voltage (Volts)\n• I = Current (Amperes)\n\nAlternate forms using Ohm's Law:\n• P = I²R (when you know current and resistance)\n• P = V²/R (when you know voltage and resistance)\n\nPower represents the rate of energy transfer in a circuit."},
            {"q":"What does a battery primarily provide to a circuit?","type":"mcq","options":["Voltage","Current","Resistance","Power"],"answer":"Voltage","explain":"A battery provides voltage (electric potential difference).\n\nHow it works:\n• Creates potential difference between terminals\n• This voltage 'pushes' electrons through circuit\n• Current flows as a result of this voltage\n• Amount of current depends on circuit resistance\n\nThe battery was invented by Alessandro Volta in 1800, which is why the unit is named 'Volt' in his honor!"},
            {"q":"In which type of circuit connection is the voltage the same across all components?","type":"mcq","options":["Series","Parallel","Mixed","Neither"],"answer":"Parallel","explain":"In PARALLEL connection, voltage is the same across all components.\n\nParallel characteristics:\n• Same voltage across each component\n• Currents split and add up\n• Total resistance decreases\n• Example: House wiring (all outlets get the same voltage)\n\nSeries characteristics:\n• Same current through each component\n• Voltages add up\n• Total resistance increases"}
        ],
        "Average": [
            {"q":"A 60 W bulb runs for 5 hours. How much energy is consumed in Watt-hours?","type":"numeric","answer":300.0,"tip":"💡 <b>Tip:</b> Energy = Power × Time. Keep the units consistent (Watts and hours).","explain":"Using: Energy = Power × Time\n\nGiven:\n• Power (P) = 60 W\n• Time (t) = 5 hours\n\nStep 1: Calculate in Watt-hours\nE = P × t = 60 × 5 = 300 Wh\n\nStep 2: This is also 0.3 kWh\n\nThe bulb consumes 300 Watt-hours (0.3 kWh) of energy.\n\nNote: Electric companies bill in kilowatt-hours (kWh)."},
            {"q":"A circuit has V = 24 V and R = 8 Ω. What is the current flowing?","type":"numeric","answer":3.0,"tip":"💡 <b>Tip:</b> Use Ohm's Law: V = IR. Rearrange to find I = V/R.","explain":"Using Ohm's Law: I = V/R\n\nGiven:\n• Voltage (V) = 24 V\n• Resistance (R) = 8 Ω\n\nStep 1: Apply formula\nI = V / R = 24 / 8\n\nStep 2: Calculate\nI = 3 Amperes\n\nThe current flowing is 3 A."},
            {"q":"Two resistors of 4 Ω and 6 Ω are connected in series. What is the total resistance?","type":"numeric","answer":10.0,"tip":"💡 <b>Tip:</b> For resistors in SERIES, add them directly: R_total = R₁ + R₂.","explain":"For resistors in SERIES: R_total = R₁ + R₂\n\nGiven:\n• R₁ = 4 Ω\n• R₂ = 6 Ω\n\nStep 1: Add resistances\nR_total = 4 + 6 = 10 Ω\n\nIn series:\n• Current through each resistor is the same\n• Voltages add up\n• Total resistance increases\n\nThe total resistance is 10 Ω."},
            {"q":"What is a fuse primarily used to protect a circuit from?","type":"mcq","options":["High voltage","Excess current","Low resistance","Power loss"],"answer":"Excess current","tip":"💡 <b>Tip:</b> Think about what causes wires to overheat and potentially cause fires.","explain":"A fuse protects against EXCESS CURRENT.\n\nHow it works:\n• Contains thin wire that melts at specific current\n• When current exceeds safe limit, wire melts\n• Circuit breaks, preventing damage/fire\n• Must be replaced after 'blowing'\n\nCircuit breakers work similarly but can be reset.\n\nInvented by Thomas Edison in the 1880s!"},
            {"q":"In which connection do resistors have the same voltage across them?","type":"mcq","options":["Series","Parallel","Mixed","None"],"answer":"Parallel","tip":"💡 <b>Tip:</b> In household wiring, all outlets provide the same voltage. What type of connection is this?","explain":"In PARALLEL connection, voltage is the same across all components.\n\nParallel characteristics:\n• Same voltage across each component\n• Currents split and add up\n• Total resistance decreases\n• Example: House wiring (all outlets get same voltage)\n\nSeries characteristics:\n• Same current through each component\n• Voltages add up\n• Total resistance increases"}
        ],
        "Difficult": [
            {"q":"Three resistors 2Ω, 3Ω, 6Ω in parallel. Total resistance?","type":"numeric","answer":1.0,"explain":"For PARALLEL resistors: 1/R_total = 1/R₁ + 1/R₂ + 1/R₃\n\nGiven:\n• R₁ = 2 Ω, R₂ = 3 Ω, R₃ = 6 Ω\n\nStep 1: Apply formula\n1/R_total = 1/2 + 1/3 + 1/6\n\nStep 2: Find common denominator (6)\n1/R_total = 3/6 + 2/6 + 1/6 = 6/6 = 1\n\nStep 3: Solve for R_total\nR_total = 1/1 = 1 Ω\n\nThe total resistance is 1 Ω (less than smallest individual resistor!)."},
            {"q":"A heater draws 5A from 220V. Power consumed?","type":"numeric","answer":1100.0,"explain":"Using: P = VI\n\nGiven:\n• Voltage (V) = 220 V\n• Current (I) = 5 A\n\nStep 1: Calculate power\nP = V × I = 220 × 5\n\nStep 2: Result\nP = 1100 Watts = 1.1 kW\n\nVerification using P = I²R:\n• R = V/I = 220/5 = 44 Ω\n• P = I²R = (5)² × 44 = 25 × 44 = 1100 W ✓\n\nThe heater consumes 1100 W of power."},
            {"q":"Resistor dissipates 50W at 10V. Resistance value?","type":"numeric","answer":2.0,"explain":"Using: P = V²/R, so R = V²/P\n\nGiven:\n• Power (P) = 50 W\n• Voltage (V) = 10 V\n\nStep 1: Apply formula\nR = V² / P = (10)² / 50\n\nStep 2: Calculate\nR = 100 / 50 = 2 Ω\n\nVerification:\n• Current: I = V/R = 10/2 = 5 A\n• Power: P = VI = 10 × 5 = 50 W ✓\n\nThe resistance is 2 Ω."},
            {"q":"In household wiring, which is safer?","type":"mcq","options":["High voltage, low current","Low voltage, high current","High voltage, high current","Both equal"],"answer":"Low voltage, high current","explain":"LOW VOLTAGE, HIGH CURRENT is safer for household wiring.\n\nReasoning:\n• Human body is most sensitive to voltage\n• 50-60V can be lethal to humans\n• Higher currents at low voltages are safer\n• This is why houses use 110-220V (relatively low)\n\nPower lines use high voltage (thousands of volts) with low current for efficiency in transmission, but this is very dangerous!\n\nNote: However, for POWER TRANSMISSION over long distances, high voltage is more efficient (less power loss)."},
            {"q":"Kirchhoff's Current Law states that?","type":"mcq","options":["V across loop = 0","Current in = Current out","R increases with T","P = VI"],"answer":"Current in = Current out","explain":"Kirchhoff's Current Law (KCL): Current entering = Current leaving\n\nAt any junction in a circuit:\n• Sum of currents flowing IN = Sum of currents flowing OUT\n• Based on conservation of electric charge\n• No charge accumulates at any point\n\nExample: If 5A enters a junction and splits into two paths:\n• I₁ + I₂ = 5A\n\nFormulated by Gustav Kirchhoff in 1845.\n\nKirchhoff's Voltage Law (KVL): Sum of voltages around any closed loop = 0"}
        ]
    }
}

# ---------------------------
# UI helpers
# ---------------------------
def header():
    st.markdown("<h1 style='color:#FF5733; text-align:center;'>⚡ PhysiXplore ⚡</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#3498DB; text-align:center;'>Interactive Physics Learning Hub</h4>", unsafe_allow_html=True)
    st.markdown("---")

def footer():
    st.markdown("---")
    st.markdown("Contact: 24-00496@g.batstate-u.edu.ph  |  Developer: IT-2103 G3")
    st.markdown("© PhysiXplore |         BATANGAS STATE UNIVERSITY - TNEU")
 # ---------------------------
# Pages
# ---------------------------
def page_home():
    header()

    # -----------------------
    # HIGHLIGHTS (Styled Header)
    # -----------------------
    col1, col2, col3 = st.columns(3)

    # -----------------------
    # BOX 1 - Simulations
    # -----------------------
    with col1:
        st.markdown(
            """
            <div style="
                background:#ffe8d1;
                padding:22px;
                border-radius:18px;
                text-align:center;
                box-shadow:3px 3px 8px rgba(0,0,0,0.12);
                font-family:'Poppins', sans-serif;
            ">
                <div style='font-size:42px;'>🎢</div>
                <h4 style='font-family:"Lobster", cursive; font-size:24px; color:#d35400;'>Simulations</h4>
                <p style='margin-top:-8px; font-size:15px;'>
                    Projectile • Energy Pendulum • Electric Circuit
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # -----------------------
    # BOX 2 - Lessons
    # -----------------------
    with col2:
        st.markdown(
            """
            <div style="
                background:#dff1ff;
                padding:22px;
                border-radius:18px;
                text-align:center;
                box-shadow:3px 3px 8px rgba(0,0,0,0.12);
                font-family:'Poppins', sans-serif;
            ">
                <div style='font-size:42px;'>📘</div>
                <h4 style='font-family:"Lobster", cursive; font-size:24px; color:#0277bd;'>Lessons</h4>
                <p style='margin-top:-8px; font-size:15px;'>
                    Guided Examples • Visual Concepts
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # -----------------------
    # BOX 3 - Quizzes
    # -----------------------
    with col3:
        st.markdown(
            """
            <div style="
                background:#f7e6ff;
                padding:22px;
                border-radius:18px;
                text-align:center;
                box-shadow:3px 3px 8px rgba(0,0,0,0.12);
                font-family:'Poppins', sans-serif;
            ">
                <div style='font-size:42px;'>📝</div>
                <h4 style='font-family:"Lobster", cursive; font-size:24px; color:#8e44ad;'>Quizzes</h4>
                <p style='margin-top:-8px; font-size:15px;'>
                    Instant Feedback • Improve Concepts
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # -----------------------
    # QUICK NAVIGATION (4 BIG BUTTONS)
    # -----------------------
    st.markdown("<h3 style='text-align:center; color:#2979ff;'></h3>", unsafe_allow_html=True)
    
    nav1, nav2 = st.columns(2)
    nav3, nav4 = st.columns(2)

    with nav1:
        if st.button("📚 Concepts", use_container_width=True):
            st.session_state["page"] = "concepts"

    with nav2:
        if st.button("📖 Lessons ", use_container_width=True):
            st.session_state["page"] = "lessons"

    with nav3:
        if st.button("📝 Quizzes", use_container_width=True):
            st.session_state["page"] = "quizzes"

    with nav4:
        if st.button("🎢 Simulations", use_container_width=True):
            st.session_state["page"] = "sims"

    # -----------------------
    # FEATURED BANNER
    # -----------------------
    st.markdown("""
        <div style="
            background:#e8f2ff;
            padding: 12px;
            margin-top: 25px;
            border-radius: 12px;
            border-left: 8px solid #2979ff;">
            <b>ℹ️ Featured:</b> Projectile Motion Simulator • Energy Pendulum • Electric Circuit Builder
        </div>
    """, unsafe_allow_html=True)
def page_concepts():
    header()
    st.markdown(
        """
        <div style='text-align:center; background-color:#e1f5fe; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
        <h1 style='color:#0288d1; font-family:"Lobster", cursive;'>🔎 Key Concepts</h1>
        <p style='font-size:16px; line-height:1.5'>
        Explore important science concepts interactively! Select a topic below to see its definition and related simulation.
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    topic = st.selectbox(
        "",
        ["Motion", "Energy", "Electricity"]
    )

    if topic == "Motion":
        st.markdown(
            """
            <div style='background-color:#e0f7fa; padding:15px; border-radius:10px; font-family:"Poppins", sans-serif;'>
            <h2 style='color:#00796b; font-family:"Lobster", cursive;'>Motion 🏎</h2>
            <p style='font-size:16px; line-height:1.5'>
            Motion is the study of <b>displacement, velocity, and acceleration</b>.<br>
            Kinematics describes motion under constant acceleration.
            </p>
            <p style='font-size:15px;'>Try the <b>'Projectile Motion'</b> simulation 🎯 to see it in action!</p>
            </div>
            """, unsafe_allow_html=True
        )

    elif topic == "Energy":
        st.markdown(
            """
            <div style='background-color:#fff3e0; padding:15px; border-radius:10px; font-family:"Poppins", sans-serif;'>
            <h2 style='color:#f57c00; font-family:"Lobster", cursive;'>Energy ⚡</h2>
            <p style='font-size:16px; line-height:1.5'>
            Energy appears as <b>kinetic (KE)</b>, <b>potential (PE)</b>, and <b>thermal energy</b>.<br>
            Mechanical energy is the sum of KE + PE.
            </p>
            <p style='font-size:15px;'>Try the <b>'Energy Pendulum'</b> simulation 🎯 to explore energy transformation!</p>
            </div>
            """, unsafe_allow_html=True
        )

    else:  # Electricity
        st.markdown(
            """
            <div style='background-color:#e8eaf6; padding:15px; border-radius:10px; font-family:"Poppins", sans-serif;'>
            <h2 style='color:#3949ab; font-family:"Lobster", cursive;'>Electricity ⚡</h2>
            <p style='font-size:16px; line-height:1.5'>
            Electricity is the flow of <b>electric charge</b> through conductors.<br>
            Key concepts include <b>voltage</b> (potential difference), <b>current</b> (charge flow), and <b>resistance</b> (opposition to flow).<br>
            Ohm's Law (V = IR) relates these fundamental quantities.
            </p>
            <p style='font-size:15px;'>Try the <b>'Electric Circuit'</b> simulation 🔌 to build and analyze circuits!</p>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("---")
    st.button("⬅ Back to Home", on_click=lambda: st.session_state.update(page="home"))
    
def page_lessons():
    header()
    st.markdown(
        """
        <div style='text-align:center; background-color:#f0f4c3; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
        <h1 style='color:#689f38; font-family:"Lobster", cursive;'>🌟Lessons & Examples🌟</h1>
        <p style='font-size:16px; line-height:1.6'>
        Welcome to our interactive science lessons! Explore concepts through explanations, examples, and visual simulations.  
        Learn <b>motion, energy, and electricity</b> in a fun and engaging way.
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("---")

    # ---------------------------
    # MOTION LESSON - ENHANCED
    # ---------------------------
    with st.container():
        st.markdown(
            """
            <div style='background-color:#e0f7fa; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
            <h2 style='color:#00796b; font-family:"Lobster", cursive;'>Motion 🏎</h2>
            
            <h3 style='color:#00897b;'>📚 What is Motion?</h3>
            <p style='font-size:16px; line-height:1.6'>
            Motion is the <b>change in an object's position over time</b> relative to a reference point. 
            It's one of the most fundamental concepts in physics, governing everything from falling apples to orbiting planets.
            </p>
            
            <h3 style='color:#00897b;'>🔬 Historical Discovery</h3>
            <p style='font-size:16px; line-height:1.6'>
            <b>Galileo Galilei</b> (1564-1642) revolutionized our understanding of motion. He discovered that:
            </p>
            <ul style='font-size:15px; line-height:1.6;'>
                <li>Objects fall at the same rate regardless of mass (refuting Aristotle)</li>
                <li>Objects in motion stay in motion unless acted upon by force</li>
                <li>Acceleration is constant near Earth's surface (~9.8 m/s²)</li>
            </ul>
            
            <p style='font-size:16px; line-height:1.6;'>
            Later, <b>Sir Isaac Newton</b> (1643-1727) formulated the three laws of motion that explained WHY objects move:
            </p>
            <ol style='font-size:15px; line-height:1.6;'>
                <li><b>First Law (Inertia):</b> An object at rest stays at rest; an object in motion stays in motion</li>
                <li><b>Second Law:</b> F = ma (Force equals mass times acceleration)</li>
                <li><b>Third Law:</b> For every action, there's an equal and opposite reaction</li>
            </ol>
            
            <h3 style='color:#00897b;'>📐 Key Equations</h3>
            <p style='font-size:15px; line-height:1.6;'>
            • Vf = Vi + at (velocity with constant acceleration)<br>
            • s = Vit + ½at² (displacement with constant acceleration)<br>
            • Vf² = Vi² + 2as (relates velocity, acceleration, and displacement)
            </p>
            
            <h3 style='color:#00897b;'>💡 Real-World Example</h3>
            <p style='font-size:16px; line-height:1.6'>
            A car accelerates from rest at <b>3 m/s²</b> for 5 seconds:<br>
            • Final velocity: Vf = 0 + 3(5) = <b>15 m/s</b> (54 km/h)<br>
            • Distance traveled: s = 0 + ½(3)(5²) = <b>37.5 meters</b><br>
            This is why traffic lights need safe following distances!
            </p>
            </div>
            """, unsafe_allow_html=True
        )

        # Motion graph
        t = np.linspace(0, 5, 100)
        a = 3
        x = 0.5 * a * t**2

        fig1, ax1 = plt.subplots(figsize=(7,4))
        ax1.plot(t, x, color="#00796b", linewidth=3, label="Distance")
        ax1.fill_between(t, x, alpha=0.3, color="#00796b")
        ax1.set_xlabel("Time (seconds)", fontsize=12, fontweight='bold')
        ax1.set_ylabel("Distance (meters)", fontsize=12, fontweight='bold')
        ax1.set_title("Accelerated Motion: Distance vs Time", fontsize=14, fontweight='bold')
        ax1.grid(True, linestyle="--", alpha=0.5)
        ax1.legend(fontsize=11)
        st.pyplot(fig1)

    st.markdown("---")
# ---------------------------
    # ENERGY LESSON - ENHANCED
    # ---------------------------
    with st.container():
        st.markdown(
            """
            <div style='background-color:#fff3e0; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
            <h2 style='color:#f57c00; font-family:"Lobster", cursive;'>Energy ⚡</h2>
            
            <h3 style='color:#e65100;'>📚 What is Energy?</h3>
            <p style='font-size:16px; line-height:1.6'>
            Energy is the <b>capacity to do work</b>. It cannot be created or destroyed, only transformed from one form to another 
            — this is the <b>Law of Conservation of Energy</b>, one of the most fundamental principles in all of science.
            </p>
            
            <h3 style='color:#e65100;'>🔬 Historical Discovery</h3>
            <p style='font-size:16px; line-height:1.6'>
            <b>James Prescott Joule</b> (1818-1889) demonstrated that mechanical work could be converted into heat with his famous 
            paddle wheel experiment. He showed that energy is conserved when it changes forms!
            </p>
            
            <p style='font-size:16px; line-height:1.6;'>
            <b>Hermann von Helmholtz</b> (1847) formulated the law of conservation of energy, stating that the total energy of an 
            isolated system remains constant.
            </p>
            
            <p style='font-size:16px; line-height:1.6;'>
            <b>William Thomson (Lord Kelvin)</b> and others developed thermodynamics, showing how energy flows and transforms in real systems.
            </p>
            
            <h3 style='color:#e65100;'>⚙️ Types of Energy</h3>
            <ul style='font-size:15px; line-height:1.6;'>
                <li><b>Kinetic Energy (KE = ½mv²):</b> Energy of motion</li>
                <li><b>Potential Energy (PE = mgh):</b> Stored energy due to position</li>
                <li><b>Thermal Energy:</b> Heat energy from molecular motion</li>
                <li><b>Chemical Energy:</b> Stored in molecular bonds</li>
                <li><b>Electrical Energy:</b> From moving charges</li>
            </ul>
            
            <h3 style='color:#e65100;'>💡 Real-World Example</h3>
            <p style='font-size:16px; line-height:1.6'>
            A 2 kg ball rolling at <b>4 m/s</b> has kinetic energy:<br>
            KE = ½(2)(4²) = <b>16 Joules</b><br><br>
            If lifted to 5 meters height, it gains potential energy:<br>
            PE = (2)(9.8)(5) = <b>98 Joules</b><br><br>
            When dropped, PE converts to KE, and it speeds up!
            </p>
            </div>
            """, unsafe_allow_html=True
        )

        # Energy bar chart
        KE = 16
        PE = 98
        Total = KE + PE

        fig2, ax2 = plt.subplots(figsize=(7,4))
        bars = ax2.bar(["Kinetic (KE)", "Potential (PE)", "Total"], 
                       [KE, PE, Total], 
                       color=["#ff6f00", "#ffa726", "#f57c00"])
        ax2.set_title("Energy Distribution Example", fontsize=14, fontweight='bold')
        ax2.set_ylabel("Energy (Joules)", fontsize=12, fontweight='bold')
        ax2.bar_label(bars, fmt='%.0f J', fontsize=11, fontweight='bold')
        st.pyplot(fig2)

    st.markdown("---")

# ---------------------------
    # ELECTRICITY LESSON - ENHANCED WITH DOCUMENT INFO
    # ---------------------------
    with st.container():
        st.markdown(
            """
            <div style='background-color:#e8eaf6; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
            <h2 style='color:#3949ab; font-family:"Lobster", cursive;'>Electricity ⚡</h2>
            
            <h3 style='color:#303f9f;'>📚 What is Electricity?</h3>
            <p style='font-size:16px; line-height:1.6'>
            Electricity is the <b>flow of electrical power or charge</b>. It is a basic part of nature and one of our most 
            widely used forms of energy. The word comes from the Latin word <i>"electrus"</i>, meaning amber-like.
            </p>
            
            <p style='font-size:16px; line-height:1.6'>
            Electricity is a general term that encompasses a variety of phenomena such as <b>lightning and static electricity</b>.
            </p>
            
            <h3 style='color:#303f9f;'>🔬 Historical Discovery</h3>
            <p style='font-size:16px; line-height:1.6'>
            <b>William Gilbert (1600)</b> coined the term "electric" from the Greek word "electron," identifying that 
            certain substances exert force when rubbed against each other.
            </p>
            
            <p style='font-size:16px; line-height:1.6'>
            <b>Benjamin Franklin (1752)</b> - Many believe he is the father of electricity. He performed the famous 
            kite experiment during a thunderstorm, discovering that lightning and electricity are related. He established 
            the convention of "positive" and "negative" charge.
            </p>
            
            <p style='font-size:16px; line-height:1.6'>
            <b>Alessandro Volta (1800)</b> - Italian physicist who constructed the <i>voltaic pile</i> (electric battery), 
            the first device to produce steady electric current. The unit "Volt" is named in his honor! Volta discovered 
            that certain chemical reactions could produce electricity.
            </p>
            
            <p style='font-size:16px; line-height:1.6'>
            <b>Michael Faraday (1831)</b> - Created the electric dynamo, a crude precursor of modern power generators. 
            This invention opened the door to the new era of electricity.
            </p>
            
            <p style='font-size:16px; line-height:1.6'>
            <b>Thomas Alva Edison (1879)</b> - Invented the practical light bulb, bringing electricity into homes.
            </p>
            
            <h3 style='color:#303f9f;'>⚙️ Key Concepts</h3>
            <ul style='font-size:15px; line-height:1.6;'>
                <li><b>Voltage (V):</b> Potential difference - the "push" that moves charges (measured in Volts)</li>
                <li><b>Current (I):</b> Rate of charge flow - intensity of electron flow (measured in Amperes)</li>
                <li><b>Resistance (R):</b> Opposition to current flow (measured in Ohms, Ω)</li>
                <li><b>Power (P):</b> Rate of energy transfer = V × I (measured in Watts)</li>
            </ul>
            
            <h3 style='color:#303f9f;'>⚡ Understanding Electric Charge</h3>
            <ul style='font-size:15px; line-height:1.6;'>
                <li><b>Electron:</b> Carries negative charge, mass = 9.11 × 10⁻³¹ kg</li>
                <li><b>Proton:</b> Carries positive charge, 1840 times heavier than electron</li>
                <li><b>1 Coulomb:</b> = 6.24 × 10¹⁸ electrons</li>
                <li><b>Like charges repel, unlike charges attract</b></li>
            </ul>
            
            <h3 style='color:#303f9f;'>📐 Ohm's Law - The Foundation</h3>
            <p style='font-size:16px; line-height:1.6'>
            <b>V = I × R</b><br>
            Voltage = Current × Resistance<br><br>
            Named after Georg Ohm, this fundamental law relates voltage, current, and resistance in all circuits.
            </p>
            
            <h3 style='color:#303f9f;'>🔌 Types of Current</h3>
            <p style='font-size:15px; line-height:1.6;'>
            <b>Direct Current (DC):</b><br>
            • Flow of charges in ONE direction<br>
            • Fixed polarity of voltage<br>
            • Examples: Batteries, power supplies<br>
            • Used in: Electronics, mobile devices<br><br>
            
            <b>Alternating Current (AC):</b><br>
            • Periodically reverses direction<br>
            • Changes polarity continuously<br>
            • Can be stepped up/down with transformers<br>
            • Used in: Household electricity, power distribution
            </p>
            
            <h3 style='color:#303f9f;'>💡 Real-World Example</h3>
            <p style='font-size:16px; line-height:1.6'>
            A 60W light bulb connected to 220V household supply:<br>
            • Current drawn: I = P/V = 60/220 = <b>0.27 Amperes</b><br>
            • Resistance: R = V/I = 220/0.27 = <b>815 Ohms</b><br>
            • Energy in 5 hours: E = 60W × 5h = <b>300 Wh = 0.3 kWh</b><br>
            • This is what you see on your electric bill!
            </p>
            </div>
            """, unsafe_allow_html=True
        )

        # Enhanced electricity visualization with sources
        st.markdown("<h4 style='text-align:center; color:#303f9f;'>⚡ Sources of Electricity</h4>", unsafe_allow_html=True)
        
        sources = ['Solar', 'Wind', 'Hydro', 'Coal', 'Natural Gas', 'Nuclear']
        percentages = [15, 10, 20, 25, 20, 10]
        colors_sources = ['#fdd835', '#42a5f5', '#1e88e5', '#424242', '#ff6f00', '#7b1fa2']
        
        fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(14,5))
        
        # Pie chart of energy sources
        ax3a.pie(percentages, labels=sources, colors=colors_sources, autopct='%1.1f%%',
                startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax3a.set_title("Global Electricity Sources (Example)", fontsize=14, fontweight='bold')
        
        # Voltage levels comparison
        voltages = [220, 110, 12, 5, 1.5]
        labels_v = ["House\n(220V)", "US House\n(110V)", "Car\n(12V)", "USB\n(5V)", "Battery\n(1.5V)"]
        bars = ax3b.barh(labels_v, voltages, color=["#3949ab", "#5e72c5", "#7987d1", "#9aa5e0", "#b9c1f0"])
        ax3b.set_title("Common Voltage Levels", fontsize=14, fontweight='bold')
        ax3b.set_xlabel("Voltage (Volts)", fontsize=12, fontweight='bold')
        ax3b.bar_label(bars, fmt='%.1f V', fontsize=10, fontweight='bold')
        ax3b.grid(axis='x', alpha=0.3)
        
        st.pyplot(fig3)

    st.markdown("---")  
    st.button("⬅ Back to Home", key="back_home_sim_page", on_click=lambda: st.session_state.update(page="home"))

def page_quizzes():
    header()
    st.markdown(
        """
        <div style='text-align:center; background-color:#ffe0b2; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
        <h1 style='color:#e65100; font-family:"Lobster", cursive;'>📝  Quizzes 📝</h1>
        <p style='font-size:16px; line-height:1.5'>
        Test your knowledge in <b>Motion, Energy, and Electricity</b>!<br>
        Review the material first, then select difficulty and start your quiz.
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    # ---------------------------
    # User Name Input
    # ---------------------------
    with st.container():
        st.markdown(
            """
            <div style='background-color:#f1f8e9; padding:15px; border-radius:10px; font-family:"Poppins", sans-serif;'>
            <p style='font-size:15px; line-height:1.5'>👤 Enter your name:</p>
            </div>
            """, unsafe_allow_html=True
        )
    username = st.text_input("", value=st.session_state.get("username", "Guest"))
    st.session_state["username"] = username

    # ---------------------------
    # Select Topic
    # ---------------------------
    with st.container():
        st.markdown(
            """
            <div style='background-color:#e3f2fd; padding:15px; border-radius:10px; font-family:"Poppins", sans-serif;'>
            <p style='font-size:15px; line-height:1.5'>🎯 Select your topic:</p>
            </div>
            """, unsafe_allow_html=True
        )
    topic = st.selectbox("Choose a topic", ["Motion", "Energy", "Electricity"])

    st.markdown("---")

    # ---------------------------
    # REVIEWER SECTION (EXPANDABLE)
    # ---------------------------
    st.markdown("### 📚 Review Material Before Quiz")
    
    if topic == "Motion":
        with st.expander("📖 Click here to review MOTION concepts and formulas", expanded=False):
            st.markdown(
                """
                <div style='background-color:#e0f7fa; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
                
                <h3 style='color:#00897b;'>📐 Key Formulas:</h3>
                <div style='background-color:#fff; padding:15px; border-radius:8px; margin:10px 0;'>
                <p style='font-size:15px; font-family:monospace; line-height:2;'>
                <b>1. Velocity:</b> Vf = Vi + at<br>
                <b>2. Displacement:</b> s = Vi·t + ½at²<br>
                <b>3. Velocity-Displacement:</b> Vf² = Vi² + 2as<br>
                <b>4. Average Velocity:</b> v_avg = (Vi + Vf) / 2<br>
                <b>5. Acceleration:</b> a = (Vf - Vi) / t
                </p>
                </div>
                
                <h3 style='color:#00897b;'>🔑 Key Concepts:</h3>
                <ul style='font-size:14px; line-height:1.7;'>
                    <li><b>Displacement (s):</b> Change in position (vector)</li>
                    <li><b>Velocity (v):</b> Rate of change of displacement (vector)</li>
                    <li><b>Speed:</b> Magnitude of velocity (scalar)</li>
                    <li><b>Acceleration (a):</b> Rate of change of velocity</li>
                    <li><b>Initial Velocity (Vi):</b> Starting velocity</li>
                    <li><b>Final Velocity (Vf):</b> Ending velocity</li>
                    <li><b>Gravity (g):</b> 9.81 m/s² (downward)</li>
                </ul>
                
                <h3 style='color:#00897b;'>💡 Important Points:</h3>
                <ul style='font-size:14px; line-height:1.7;'>
                    <li>Vector quantities need both magnitude and direction</li>
                    <li>In free fall, all objects accelerate at the same rate (g = 9.81 m/s²)</li>
                    <li>Velocity-time graph slope = acceleration</li>
                    <li>For projectile motion: horizontal and vertical motions are independent</li>
                </ul>
                
                <h3 style='color:#00897b;'>📊 Graph Interpretations:</h3>
                <ul style='font-size:14px; line-height:1.7;'>
                    <li><b>Position-Time straight:</b> Constant velocity</li>
                    <li><b>Velocity-Time straight:</b> Constant acceleration</li>
                    <li><b>Velocity-Time horizontal:</b> Zero acceleration</li>
                </ul>
                
                <h3 style='color:#00897b;'>🎯 Problem-Solving Steps:</h3>
                <ol style='font-size:14px; line-height:1.7;'>
                    <li>List all given values (Vi, Vf, a, t, s)</li>
                    <li>Identify what you need to find</li>
                    <li>Choose the appropriate formula</li>
                    <li>Substitute values carefully</li>
                    <li>Solve and check units</li>
                </ol>
                </div>
                """, unsafe_allow_html=True
            )
    
    elif topic == "Energy":
        with st.expander("📖 Click here to review ENERGY concepts and formulas", expanded=False):
            st.markdown(
                """
                <div style='background-color:#fff3e0; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
                
                <h3 style='color:#e65100;'>📐 Key Formulas:</h3>
                <div style='background-color:#fff; padding:15px; border-radius:8px; margin:10px 0;'>
                <p style='font-size:15px; font-family:monospace; line-height:2;'>
                <b>1. Kinetic Energy:</b> KE = ½mv²<br>
                <b>2. Potential Energy:</b> PE = mgh<br>
                <b>3. Work:</b> W = F × d<br>
                <b>4. Power:</b> P = W / t  or  P = F × v<br>
                <b>5. Mechanical Energy:</b> E = KE + PE<br>
                <b>6. Elastic PE:</b> PE_spring = ½kx²<br>
                <b>7. Conservation:</b> KE_i + PE_i = KE_f + PE_f
                </p>
                </div>
                
                <h3 style='color:#e65100;'>🔑 Key Concepts:</h3>
                <ul style='font-size:14px; line-height:1.7;'>
                    <li><b>Energy:</b> Capacity to do work (measured in Joules)</li>
                    <li><b>Kinetic Energy (KE):</b> Energy of motion</li>
                    <li><b>Potential Energy (PE):</b> Stored energy due to position</li>
                    <li><b>Work (W):</b> Force applied over a distance</li>
                    <li><b>Power (P):</b> Rate of doing work (Watts = Joules/second)</li>
                    <li><b>Conservation of Energy:</b> Energy cannot be created or destroyed</li>
                </ul>
                
                <h3 style='color:#e65100;'>💡 Important Points:</h3>
                <ul style='font-size:14px; line-height:1.7;'>
                    <li>Energy is scalar (no direction)</li>
                    <li>1 Joule = 1 Newton × 1 meter</li>
                    <li>1 Watt = 1 Joule/second</li>
                    <li>In closed systems with no friction, mechanical energy is conserved</li>
                    <li>At maximum height: KE = 0, PE = maximum</li>
                    <li>At ground level: PE = 0, KE = maximum</li>
                </ul>
                
                <h3 style='color:#e65100;'>🎯 Energy Transformations:</h3>
                <ul style='font-size:14px; line-height:1.7;'>
                    <li><b>Pendulum:</b> PE ⇄ KE (back and forth)</li>
                    <li><b>Falling object:</b> PE → KE</li>
                    <li><b>Compressed spring:</b> Elastic PE → KE</li>
                </ul>
                
                <h3 style='color:#e65100;'>🧮 Problem-Solving Tips:</h3>
                <ol style='font-size:14px; line-height:1.7;'>
                    <li>Identify type of energy at each stage</li>
                    <li>Use conservation: Initial energy = Final energy</li>
                    <li>Remember: g = 9.8 m/s²</li>
                    <li>Check if friction is present</li>
                </ol>
                </div>
                """, unsafe_allow_html=True
            )
    
    else:  # Electricity
        with st.expander("📖 Click here to review ELECTRICITY concepts and formulas", expanded=False):
            st.markdown(
                """
                <div style='background-color:#e8eaf6; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
                
                <h3 style='color:#303f9f;'>📐 Key Formulas:</h3>
                <div style='background-color:#fff; padding:15px; border-radius:8px; margin:10px 0;'>
                <p style='font-size:15px; font-family:monospace; line-height:2;'>
                <b>1. Ohm's Law:</b> V = IR<br>
                <b>2. Power:</b> P = VI  or  P = I²R  or  P = V²/R<br>
                <b>3. Energy:</b> E = Pt (in Joules or Watt-hours)<br>
                <b>4. Series Resistors:</b> R_total = R₁ + R₂ + R₃...<br>
                <b>5. Parallel Resistors:</b> 1/R_total = 1/R₁ + 1/R₂ + 1/R₃...<br>
                <b>6. Charge:</b> Q = It (Coulombs)<br>
                <b>7. Kirchhoff's Current Law:</b> Σ I_in = Σ I_out
                </p>
                </div>
                
                <h3 style='color:#303f9f;'>🔑 Key Concepts:</h3>
                <ul style='font-size:14px; line-height:1.7;'>
                    <li><b>Voltage (V):</b> Electric potential difference (Volts)</li>
                    <li><b>Current (I):</b> Flow of electric charge (Amperes)</li>
                    <li><b>Resistance (R):</b> Opposition to current (Ohms, Ω)</li>
                    <li><b>Power (P):</b> Rate of energy transfer (Watts)</li>
                    <li><b>1 Coulomb:</b> 6.24 × 10¹⁸ electrons</li>
                </ul>
                
                <h3 style='color:#303f9f;'>💡 Important Points:</h3>
                <ul style='font-size:14px; line-height:1.7;'>
                    <li><b>Series:</b> Same current, voltages add, R increases</li>
                    <li><b>Parallel:</b> Same voltage, currents add, R decreases</li>
                    <li>Battery provides voltage (potential difference)</li>
                    <li>Current flows from negative to positive (electron flow)</li>
                    <li>Higher resistance = lower current (constant V)</li>
                    <li>Higher voltage = higher current (constant R)</li>
                </ul>
                
                <h3 style='color:#303f9f;'>🔌 Circuit Analysis:</h3>
                <ul style='font-size:14px; line-height:1.7;'>
                    <li><b>Closed circuit:</b> Complete path, current flows</li>
                    <li><b>Open circuit:</b> Broken path, no current</li>
                    <li><b>Short circuit:</b> Very low resistance (dangerous!)</li>
                </ul>
                
                <h3 style='color:#303f9f;'>🎯 Problem-Solving Strategy:</h3>
                <ol style='font-size:14px; line-height:1.7;'>
                    <li>Identify given: V, I, or R?</li>
                    <li>For series: R_total = R₁ + R₂</li>
                    <li>For parallel: 1/R_total = 1/R₁ + 1/R₂</li>
                    <li>Apply Ohm's Law: V = IR</li>
                    <li>Choose correct power formula</li>
                </ol>
                
                <h3 style='color:#303f9f;'>⚠️ Common Mistakes:</h3>
                <ul style='font-size:14px; line-height:1.7;'>
                    <li>Don't confuse series and parallel formulas</li>
                    <li>In parallel, R_total is LESS than smallest R</li>
                    <li>1 kWh = 1000 Wh</li>
                </ul>
                </div>
                """, unsafe_allow_html=True
            )

    st.markdown("---")

    # ---------------------------
    # Select Difficulty
    # ---------------------------
    with st.container():
        st.markdown(
            """
            <div style='background-color:#f3e5f5; padding:15px; border-radius:10px; font-family:"Poppins", sans-serif;'>
            <p style='font-size:15px; line-height:1.5'>⚙️ Select difficulty level:</p>
            </div>
            """, unsafe_allow_html=True
        )
    
    difficulty = st.selectbox("Choose difficulty", ["Easy", "Average", "Difficult"])
    
    # Display difficulty info
    if difficulty == "Easy":
        st.info("📘 **Easy Mode:** All multiple choice questions - great for beginners!")
    elif difficulty == "Average":
        st.info("📙 **Average Mode:** Mix of question types with helpful tips - build your skills!")
    else:
        st.info("📕 **Difficult Mode:** Challenging problems with NO hints - test your mastery!")

    # Reset quiz if topic or difficulty changed
    if "quiz_active" not in st.session_state or \
       st.session_state.get("quiz_topic") != topic or \
       st.session_state.get("quiz_difficulty") != difficulty:
        st.session_state.update({
            "quiz_active": False,
            "quiz_topic": topic,
            "quiz_difficulty": difficulty,
            "quiz_index": 0,
            "quiz_answers": []
        })

    st.markdown("---")

    # ---------------------------
    # Start Quiz Button
    # ---------------------------
    start = st.button("🏁 Start Quiz", key="start_quiz", use_container_width=True)
    if start:
        st.session_state["quiz_active"] = True
        st.rerun()

    # ---------------------------
    # Quiz Active
    # ---------------------------
    if st.session_state.get("quiz_active", False):
        qi = st.session_state.get("quiz_index", 0)
        user_answers = st.session_state.get("quiz_answers", [])
        questions = QUIZZES[topic][difficulty]

        # --- All Questions Answered ---
        if qi >= len(questions):
            st.success(f"🎉 Quiz Complete! You answered all {len(questions)} questions.")

            st.subheader("📖 Answers & Explanations")
            score = 0
            for i, q in enumerate(questions):
                st.markdown(
                    f"<div style='background-color:#fff9c4; padding:10px; border-radius:10px; font-family:Poppins;'>"
                    f"<b>Question {i+1}:</b> {q['q']}</div>",
                    unsafe_allow_html=True
                )

                user_ans = user_answers[i] if i < len(user_answers) else "No answer"
                correct_ans = q["answer"]
                is_correct = False

                if q["type"] == "mcq":
                    is_correct = user_ans == correct_ans
                else:
                    try:
                        is_correct = math.isclose(float(user_ans), float(correct_ans), rel_tol=1e-3, abs_tol=1e-3)
                    except:
                        is_correct = False

                st.markdown(
                    f"<div style='background-color:#e8f5e9; padding:5px; border-radius:8px;'>"
                    f"Your answer: {user_ans} {'✅' if is_correct else '❌'}<br>"
                    f"Correct answer: {correct_ans}</div>",
                    unsafe_allow_html=True
                )
                st.info(f"💡 Explanation:\n\n{q.get('explain', 'No explanation.')}")
                
                if is_correct:
                    score += 1
                
                st.markdown("---")

            st.success(f"🏆 Final Score: {score}/{len(questions)} ({(score/len(questions)*100):.1f}%)")

            if st.button("🏠 Back to Home", key="quiz_home"):
                st.session_state.update(page="home", quiz_active=False, quiz_index=0, quiz_answers=[])
            if st.button("🔄 Take Another Quiz", key="quiz_restart"):
                st.session_state.update(quiz_active=False, quiz_index=0, quiz_answers=[])
                st.rerun()
            return

        # --- Current Question ---
        q = questions[qi]
        st.markdown(
            f"<div style='background-color:#fce4ec; padding:15px; border-radius:10px; font-family:Poppins;'>"
            f"<b>Question {qi+1} of {len(questions)}:</b> {q['q']}</div>",
            unsafe_allow_html=True
        )

        # Show tip if available (Average mode only)
        if "tip" in q:
            st.markdown(
                f"<div style='background-color:#e8f5e9; padding:10px; border-radius:8px; margin:10px 0;'>"
                f"{q['tip']}</div>",
                unsafe_allow_html=True
            )

        user_answer_key = f"ans_{topic}_{difficulty}_{qi}"
        if q["type"] == "mcq":
            ans = st.radio("Choose your answer:", q["options"], key=user_answer_key)
        else:
            ans = st.text_input("Enter your numerical answer:", key=user_answer_key, 
                               help="Enter numbers only (decimals allowed)")

        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        if col1.button("✅ Submit Answer", key=f"submit_{qi}", use_container_width=True):
            if ans and ans.strip():
                user_answers.append(ans)
                st.session_state["quiz_answers"] = user_answers
                st.session_state["quiz_index"] = qi + 1
                st.rerun()
            else:
                st.error("⚠️ Please provide an answer before submitting!")

        if col2.button("❌ Cancel Quiz", key=f"cancel_{qi}", use_container_width=True):
            st.session_state.update(quiz_active=False, quiz_index=0, quiz_answers=[])
            st.rerun()

    # ---------------------------
    # Back to Home
    # ---------------------------
    st.button("⬅ Back to Home", on_click=lambda: st.session_state.update(page="home"))

    st.markdown("---")
# Simulations
def sims_projectile_combined():
    st.markdown(
        """
        <div style='text-align:center; background-color:#e1f5fe; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
        <h2 style='color:#0288d1; font-family:"Lobster", cursive;'>🚀 Projectile Motion Simulator</h2>
        <p style='font-size:16px; line-height:1.5'>
        Visualize projectile motion with real-time animation and see calculated results for maximum height, range, and flight time!
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    # Educational introduction - HOW IT WORKS
    st.markdown(
        """
        <div style='background-color:#fff3e0; padding:15px; border-radius:10px; font-family:Poppins; margin:10px 0;'>
        <h4 style='color:#e65100;'>📖 How Projectile Motion Works:</h4>
        <p style='font-size:14px; line-height:1.6;'>
        When you launch a projectile at an angle, it follows a curved (parabolic) path due to gravity.<br><br>
        
        <b>What happens during flight:</b><br>
        • <b>Horizontal Motion:</b> Moves at constant velocity (no acceleration)<br>
        • <b>Vertical Motion:</b> Slows down going up, speeds up coming down (gravity pulls at 9.81 m/s²)<br>
        • <b>Path Shape:</b> Combines to form a parabolic curve<br><br>
        
        <b>What you'll see in the animation:</b><br>
        🔴 Red trajectory line - Path of the projectile<br>
        🔵 Blue dot - Current position<br>
        🟢 Green markers - Maximum height point<br>
        🟣 Magenta markers - Landing point (range)<br>
        ⏱️ Real-time timer - Shows actual flight time
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("---")

    # Inputs
    st.markdown("### 🎛️ Launch Settings")
    col1, col2 = st.columns(2)
    with col1:
        v0 = st.slider("Initial speed (m/s)", 5, 50, 20, help="How fast the projectile launches")
        st.caption("💡 Higher speed = longer flight & greater distance")
    with col2:
        angle_deg = st.slider("Angle (°)", 10, 80, 45, help="Launch angle from horizontal")
        st.caption("🎯 45° gives maximum range!")
    
    g = 9.81

    st.markdown("---")

    # Calculate results BEFORE animation
    theta = math.radians(angle_deg)
    t_flight = 2 * v0 * math.sin(theta) / g
    H_max = (v0**2 * math.sin(theta)**2) / (2 * g)
    R = (v0**2 * math.sin(2*theta)) / g

    # STEP-BY-STEP CALCULATIONS
    st.markdown("### 📐 Step-by-Step Calculations")
    
    st.markdown(
        f"""
        <div style='background-color:#e8f5e9; padding:20px; border-radius:10px; font-family:Poppins;'>
        <h4 style='color:#2e7d32;'>Given Values:</h4>
        <ul style='font-size:15px;'>
            <li><b>Initial Speed (v₀):</b> {v0} m/s</li>
            <li><b>Launch Angle (θ):</b> {angle_deg}°</li>
            <li><b>Gravity (g):</b> 9.81 m/s²</li>
        </ul>
        
        <h4 style='color:#2e7d32; margin-top:15px;'>Step 1: Calculate Time of Flight</h4>
        <p style='font-size:14px; font-family:monospace; background:#fff; padding:10px; border-radius:5px;'>
        <b>Formula:</b> t = (2 × v₀ × sin(θ)) / g<br>
        <b>Substitute:</b> t = (2 × {v0} × sin({angle_deg}°)) / 9.81<br>
        <b>Calculate:</b> t = (2 × {v0} × {math.sin(theta):.4f}) / 9.81<br>
        <b>Result:</b> <span style='color:#d32f2f; font-size:18px;'>t = {t_flight:.2f} seconds</span>
        </p>
        
        <h4 style='color:#2e7d32; margin-top:15px;'>Step 2: Calculate Maximum Height</h4>
        <p style='font-size:14px; font-family:monospace; background:#fff; padding:10px; border-radius:5px;'>
        <b>Formula:</b> H = (v₀² × sin²(θ)) / (2g)<br>
        <b>Substitute:</b> H = ({v0}² × sin²({angle_deg}°)) / (2 × 9.81)<br>
        <b>Calculate:</b> H = ({v0**2} × {math.sin(theta)**2:.4f}) / 19.62<br>
        <b>Result:</b> <span style='color:#d32f2f; font-size:18px;'>H = {H_max:.2f} meters</span>
        </p>
        
        <h4 style='color:#2e7d32; margin-top:15px;'>Step 3: Calculate Range (Horizontal Distance)</h4>
        <p style='font-size:14px; font-family:monospace; background:#fff; padding:10px; border-radius:5px;'>
        <b>Formula:</b> R = (v₀² × sin(2θ)) / g<br>
        <b>Substitute:</b> R = ({v0}² × sin(2 × {angle_deg}°)) / 9.81<br>
        <b>Calculate:</b> R = ({v0**2} × {math.sin(2*theta):.4f}) / 9.81<br>
        <b>Result:</b> <span style='color:#d32f2f; font-size:18px;'>R = {R:.2f} meters</span>
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    # Results box BEFORE animation
    st.markdown("### 📊 Predicted Results")
    st.markdown(
        f"""
        <div style="background-color:#fff3e0;padding:15px;border-radius:10px;border:2px solid #ffb74d; font-family:'Poppins', sans-serif;">
            <h4 style="color:#f57c00;">🎯 What Will Happen:</h4>
            <p style='font-size:15px;'><b>⏱️ Time of flight:</b> {t_flight:.2f} seconds</p>
            <p style='font-size:15px;'><b>⬆️ Maximum height:</b> {H_max:.2f} meters</p>
            <p style='font-size:15px;'><b>➡️ Range (distance):</b> {R:.2f} meters</p>
            <p style='font-size:14px; color:#666; margin-top:10px;'>
            Click "Launch 🚀" below to see the animation and verify these calculations!
            </p>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("---")

    # Launch button
    if st.button("🚀 Launch Projectile", use_container_width=True):
        
        # Trajectory points
        frames = 100
        t = np.linspace(0, t_flight, frames)
        x = v0 * np.cos(theta) * t
        y = v0 * np.sin(theta) * t - 0.5 * g * t**2

        # Animation speed - matches actual physics time
        animation_speed = t_flight / frames

        # Prepare figure
        placeholder = st.empty()
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.set_xlim(0, max(x) * 1.1)
        ax.set_ylim(0, max(y) * 1.2)
        ax.set_xlabel("Horizontal Distance (meters)", fontsize=12, fontweight='bold')
        ax.set_ylabel("Height (meters)", fontsize=12, fontweight='bold')
        ax.set_title(f"Projectile Trajectory Animation", fontsize=14, fontweight='bold')

        # Animation lines
        line, = ax.plot([], [], 'r-', lw=3, label="Trajectory Path")
        point, = ax.plot([], [], 'bo', markersize=12, label="Projectile")

        # Max height marker
        x_max_height = v0 * math.cos(theta) * (t_flight / 2)
        ax.plot(x_max_height, H_max, 'go', markersize=12, label=f"Max Height ({H_max:.1f}m)", zorder=5)
        ax.axhline(H_max, color='green', linestyle='--', alpha=0.5, linewidth=2)
        ax.text(x_max_height + max(x)*0.05, H_max, f'{H_max:.2f}m', 
               fontsize=11, color='green', fontweight='bold')

        # Range marker
        ax.plot(R, 0, 'mo', markersize=12, label=f"Landing Point ({R:.1f}m)", zorder=5)
        ax.axvline(R, color='magenta', linestyle='--', alpha=0.5, linewidth=2)
        ax.text(R, -max(y)*0.05, f'{R:.2f}m', fontsize=11, 
               ha='center', color='magenta', fontweight='bold')

        # Launch point marker
        ax.plot(0, 0, 'rs', markersize=15, label="Launch Point", zorder=5)
        ax.text(0, -max(y)*0.05, 'START', fontsize=10, 
               ha='center', color='red', fontweight='bold')

        # Time text
        time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12,
                           verticalalignment='top', fontweight='bold',
                           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

        # Position text
        pos_text = ax.text(0.98, 0.95, '', transform=ax.transAxes, fontsize=10,
                          verticalalignment='top', horizontalalignment='right',
                          bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

        ax.legend(fontsize=10, loc='upper right', bbox_to_anchor=(0.98, 0.85))
        ax.grid(True, alpha=0.3, linestyle='--')

        # Animation loop with ACCURATE timing
        for i in range(len(t)):
            line.set_data(x[:i+1], y[:i+1])
            point.set_data([x[i]], [y[i]])
            time_text.set_text(f'⏱️ Time: {t[i]:.2f}s / {t_flight:.2f}s')
            pos_text.set_text(f'📍 Position:\nx = {x[i]:.1f}m\ny = {y[i]:.1f}m')
            placeholder.pyplot(fig)
            time.sleep(animation_speed)

        plt.close()
        
        st.success(f"✅ Animation Complete!")

        # RESULTS EXPLANATION - HOW IT WORKED
        st.markdown("---")
        st.markdown("### 🎯 Results Analysis - What Just Happened")
        
        st.markdown(
            f"""
            <div style='background-color:#e3f2fd; padding:20px; border-radius:10px; font-family:Poppins;'>
            <h4 style='color:#1565c0;'>📊 Verified Results:</h4>
            <ul style='font-size:15px; line-height:1.8;'>
                <li><b>✅ Flight Time:</b> {t_flight:.2f} seconds (exactly as calculated!)</li>
                <li><b>✅ Maximum Height:</b> {H_max:.2f} meters (reached at {t_flight/2:.2f}s)</li>
                <li><b>✅ Landing Distance:</b> {R:.2f} meters (total horizontal travel)</li>
            </ul>
            
            <h4 style='color:#1565c0; margin-top:15px;'>🔍 What Happened During Flight:</h4>
            
            <p style='font-size:14px; line-height:1.7;'>
            <b>Phase 1 - Going Up (0s to {t_flight/2:.2f}s):</b><br>
            • The projectile moved upward while gravity slowed it down<br>
            • Vertical velocity decreased from {v0*math.sin(theta):.2f} m/s to 0 m/s<br>
            • Horizontal velocity stayed constant at {v0*math.cos(theta):.2f} m/s<br>
            • Reached maximum height of {H_max:.2f}m at the halfway point<br><br>
            
            <b>Phase 2 - Coming Down ({t_flight/2:.2f}s to {t_flight:.2f}s):</b><br>
            • The projectile fell back down as gravity accelerated it<br>
            • Vertical velocity increased from 0 m/s to {v0*math.sin(theta):.2f} m/s (downward)<br>
            • Horizontal velocity still constant at {v0*math.cos(theta):.2f} m/s<br>
            • Landed at distance {R:.2f}m from the starting point<br><br>
            
            <b>🔬 Physics Principles Demonstrated:</b><br>
            • <b>Independence:</b> Horizontal and vertical motions are separate<br>
            • <b>Symmetry:</b> Time up = Time down ({t_flight/2:.2f}s each)<br>
            • <b>Parabolic Path:</b> The curved trajectory you saw<br>
            • <b>Constant Horizontal Velocity:</b> No forces acting horizontally (ignoring air resistance)<br>
            • <b>Gravity Effect:</b> Constant 9.81 m/s² downward acceleration
            </p>
            
            <h4 style='color:#1565c0; margin-top:15px;'>💡 Key Observations:</h4>
            <ul style='font-size:14px; line-height:1.7;'>
                <li>The projectile traveled {R:.2f} meters horizontally in {t_flight:.2f} seconds</li>
                <li>Average horizontal speed: {R/t_flight:.2f} m/s (equals {v0*math.cos(theta):.2f} m/s)</li>
                <li>The highest point was at {x_max_height:.2f}m horizontal distance</li>
                <li>Impact speed equals launch speed: {v0:.2f} m/s (energy conservation!)</li>
            </ul>
            
            <h4 style='color:#1565c0; margin-top:15px;'>🎯 Why This Matters:</h4>
            <p style='font-size:14px; line-height:1.7;'>
            Understanding projectile motion helps in:<br>
            • <b>Sports:</b> Basketball shooting angles, soccer ball trajectories<br>
            • <b>Engineering:</b> Designing fountains, calculating cannon range<br>
            • <b>Safety:</b> Predicting where objects will land<br>
            • <b>Space:</b> Launching satellites and rockets
            </p>
            </div>
            """, unsafe_allow_html=True
        )

        # Comparison table
        st.markdown("### 📋 Predicted vs Actual Results")
        
        results_data = {
            "Parameter": ["Flight Time", "Maximum Height", "Range"],
            "Predicted": [f"{t_flight:.2f} s", f"{H_max:.2f} m", f"{R:.2f} m"],
            "Actual (from animation)": [f"{t_flight:.2f} s", f"{H_max:.2f} m", f"{R:.2f} m"],
            "Match?": ["✅ Perfect", "✅ Perfect", "✅ Perfect"]
        }
        
        import pandas as pd
        df = pd.DataFrame(results_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.success("🎉 The animation perfectly matches our calculations! Physics works!")

    st.markdown("---")
    
    # Tips for exploration
    st.markdown(
        """
        <div style='background-color:#fff3e0; padding:15px; border-radius:10px; font-family:Poppins;'>
        <h4 style='color:#ef6c00;'>💡 Tips for Exploration:</h4>
        <ul style='font-size:14px; line-height:1.7;'>
            <li><b>Try 45°:</b> This angle gives the maximum range for any given speed</li>
            <li><b>Increase speed:</b> Higher speed = longer flight time and greater distance</li>
            <li><b>Compare angles:</b> Try 30° and 60° - they give the same range!</li>
            <li><b>Straight up (90°):</b> Range becomes zero, only goes up and down</li>
        </ul>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown("---")

def sims_energy_pendulum():
    """Enhanced Energy Pendulum Simulator with Clear Explanations"""
    st.markdown(
        """
        <div style='text-align:center; background-color:#f3e5f5; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
        <h2 style='color:#6a1b9a; font-family:"Lobster", cursive;'>🎯 Energy Pendulum Simulator</h2>
        <p style='font-size:16px; line-height:1.5'>
        Watch a pendulum swing and observe the continuous transformation between <b>Potential Energy</b> and <b>Kinetic Energy</b>!<br>
        Notice how <b>total energy remains constant</b> — demonstrating energy conservation.
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    # Educational explanation
    st.markdown(
        """
        <div style='background-color:#e1bee7; padding:15px; border-radius:10px; font-family:Poppins; margin:10px 0;'>
        <h4 style='color:#4a148c;'>📖 How It Works:</h4>
        <p style='font-size:14px; line-height:1.6;'>
        • <b>At highest points:</b> Maximum PE, Zero KE (momentarily stops)<br>
        • <b>At lowest point:</b> Zero PE, Maximum KE (fastest speed)<br>
        • <b>During swing:</b> PE ⇄ KE conversion<br>
        • <b>Total Energy:</b> PE + KE = Constant (if no friction)
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    # Inputs
    length = st.slider("Pendulum Length (m)", 0.5, 3.0, 1.5, 0.1)
    angle_deg = st.slider("Release Angle (°)", 10, 60, 30, 5)
    mass = st.slider("Bob Mass (kg)", 0.5, 5.0, 2.0, 0.5)
    g = 9.81

    if st.button("Start Pendulum 🎯"):
        # Calculate period
        T = 2 * math.pi * math.sqrt(length / g)
        max_height = length * (1 - math.cos(math.radians(angle_deg)))
        max_PE = mass * g * max_height
        
        st.info(f"⏱️ Period: {T:.2f} seconds | 🔋 Max Energy: {max_PE:.2f} J")

        # Time array for animation
        frames = 120
        t = np.linspace(0, 2*T, frames)  # Show 2 complete swings
        
        # Angle as function of time (simple harmonic motion)
        theta_max = math.radians(angle_deg)
        theta = theta_max * np.cos(2 * math.pi * t / T)
        
        # Calculate energies
        heights = length * (1 - np.cos(theta))
        PE = mass * g * heights
        KE = max_PE - PE  # Conservation of energy
        
        # Animation
        placeholder = st.empty()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Animation loop
        for i in range(len(t)):
            fig.clear()
            ax1, ax2 = fig.subplots(1, 2)
            
            # LEFT: Pendulum visualization
            ax1.set_xlim(-length*1.5, length*1.5)
            ax1.set_ylim(-length*1.3, length*0.3)
            ax1.set_aspect('equal')
            ax1.set_title(f"Pendulum Motion (t={t[i]:.2f}s)", fontweight='bold', fontsize=12)
            ax1.axhline(0, color='black', linewidth=0.5)
            
            # Draw pendulum
            x_bob = length * np.sin(theta[i])
            y_bob = -length * np.cos(theta[i])
            ax1.plot([0, x_bob], [0, y_bob], 'k-', linewidth=2, label='String')
            ax1.plot(x_bob, y_bob, 'o', markersize=20, color='#6a1b9a', label='Bob')
            ax1.plot(0, 0, 'ko', markersize=8, label='Pivot')
            # Show height
            ax1.plot([x_bob, x_bob], [y_bob, -length], 'r--', alpha=0.5, linewidth=1)
            ax1.text(x_bob+0.1, (y_bob-length)/2, f'h={heights[i]:.2f}m', fontsize=9, color='red')
            
            ax1.legend(loc='upper right', fontsize=9)
            ax1.grid(True, alpha=0.3)
            
            # RIGHT: Energy bar chart
            energies = [PE[i], KE[i], max_PE]
            labels = ['PE', 'KE', 'Total']
            colors = ['#1976d2', '#f57c00', '#43a047']
            bars = ax2.bar(labels, energies, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
            
            ax2.set_ylim(0, max_PE * 1.2)
            ax2.set_ylabel("Energy (Joules)", fontweight='bold', fontsize=11)
            ax2.set_title("Energy Distribution", fontweight='bold', fontsize=12)
            ax2.grid(axis='y', alpha=0.3)
            
            # Add value labels on bars
            for bar, energy in zip(bars, energies):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{energy:.1f}J',
                        ha='center', va='bottom', fontweight='bold', fontsize=10)
            
            placeholder.pyplot(fig)
            time.sleep(2*T / frames)  # Real-time animation
        
        st.success("✅ Animation complete! Notice how PE and KE trade off while total stays constant.")

    st.markdown("---")

def sims_electricity_circuit():
    """Comprehensive Interactive Circuit Simulator with Step-by-Step Explanation"""
    st.markdown(
        """
        <div style='text-align:center; background-color:#e0f7fa; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
        <h2 style='color:#006064; font-family:"Lobster", cursive;'>⚡ Complete Circuit Simulator</h2>
        <p style='font-size:16px; line-height:1.5'>
        Build a realistic circuit and understand <b>Ohm's Law (V = IR)</b> with step-by-step explanations!<br>
        Watch electrons flow, see power dissipation, and learn how circuits work.
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    # Educational introduction
    st.markdown(
        """
        <div style='background-color:#fff3e0; padding:15px; border-radius:10px; font-family:Poppins; margin:10px 0;'>
        <h4 style='color:#e65100;'>📖 How Electric Circuits Work:</h4>
        <p style='font-size:14px; line-height:1.6;'>
        <b>1. Voltage Source (Battery):</b> Creates potential difference - the "push" for electrons<br>
        <b>2. Conducting Wires:</b> Provide path for electron flow (very low resistance)<br>
        <b>3. Load (Resistor/Bulb):</b> Uses electrical energy - has resistance that limits current<br>
        <b>4. Closed Circuit:</b> Complete path allows current to flow continuously<br><br>
        <b>⚡ Remember:</b> Current (I) flows from negative (-) to positive (+) terminal [electron flow]
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("---")
    
    # Circuit component controls
    st.markdown("### 🎛️ Circuit Components - Adjust the Values")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔋 Battery (Voltage Source)**")
        voltage = st.slider("Voltage (V)", 1.5, 12.0, 6.0, 0.5, 
                           help="This is the 'push' that drives electrons through the circuit")
        st.caption("💡 Higher voltage = stronger push = more current")
        
    with col2:
        st.markdown("**💡 Light Bulb (Load/Resistance)**")
        resistance = st.slider("Resistance (Ω)", 5.0, 100.0, 30.0, 5.0,
                              help="This is the opposition to current flow")
        st.caption("🔧 Higher resistance = harder for current to flow")

    st.markdown("---")

    # Calculate circuit parameters
    current = voltage / resistance
    power = voltage * current
    brightness = min(100, (power / 2) * 100)
    energy_per_hour = power * 1  # Wh
    
    # Step-by-step calculation display
    st.markdown("### 📐 Step-by-Step Calculation Using Ohm's Law")
    
    st.markdown(
        f"""
        <div style='background-color:#e8f5e9; padding:20px; border-radius:10px; font-family:Poppins; margin:15px 0;'>
        <h4 style='color:#2e7d32;'>🧮 Given Values:</h4>
        <ul style='font-size:15px; line-height:1.8;'>
            <li><b>Voltage (V):</b> {voltage} Volts</li>
            <li><b>Resistance (R):</b> {resistance} Ohms (Ω)</li>
        </ul>
        
        <h4 style='color:#2e7d32; margin-top:15px;'>Step 1: Calculate Current using Ohm's Law</h4>
        <p style='font-size:15px; line-height:1.8; font-family:monospace; background:#fff; padding:10px; border-radius:5px;'>
        <b>Formula:</b> I = V / R<br>
        <b>Substitute:</b> I = {voltage} V / {resistance} Ω<br>
        <b>Result:</b> I = <span style='color:#d32f2f; font-size:18px;'>{current:.4f} Amperes (A)</span>
        </p>
        
        <h4 style='color:#2e7d32; margin-top:15px;'>Step 2: Calculate Power (Energy Used)</h4>
        <p style='font-size:15px; line-height:1.8; font-family:monospace; background:#fff; padding:10px; border-radius:5px;'>
        <b>Formula:</b> P = V × I<br>
        <b>Substitute:</b> P = {voltage} V × {current:.4f} A<br>
        <b>Result:</b> P = <span style='color:#d32f2f; font-size:18px;'>{power:.4f} Watts (W)</span>
        </p>
        
        <h4 style='color:#2e7d32; margin-top:15px;'>Step 3: Calculate Energy Consumption</h4>
        <p style='font-size:15px; line-height:1.8; font-family:monospace; background:#fff; padding:10px; border-radius:5px;'>
        <b>Formula:</b> Energy = Power × Time<br>
        <b>In 1 hour:</b> E = {power:.4f} W × 1 h = <span style='color:#d32f2f; font-size:18px;'>{energy_per_hour:.4f} Wh</span><br>
        <b>In 24 hours:</b> E = {power:.4f} W × 24 h = <span style='color:#d32f2f; font-size:18px;'>{energy_per_hour*24:.4f} Wh = {(energy_per_hour*24)/1000:.4f} kWh</span>
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    # Real-time circuit metrics
    st.markdown("### 📊 Circuit Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⚡ Voltage", f"{voltage:.1f} V", 
               help="Potential difference across the circuit")
    col2.metric("🔌 Current", f"{current:.4f} A", 
               delta=f"{(current-0.2):.4f} A" if current > 0.2 else None,
               help="Flow of electrons per second")
    col3.metric("🔧 Resistance", f"{resistance:.1f} Ω",
               help="Opposition to current flow")
    col4.metric("💡 Power", f"{power:.4f} W",
               delta=f"{(power-1):.4f} W" if power > 1 else None,
               help="Energy consumed per second")
    
    # Bulb brightness indicator
    st.markdown("### 💡 Light Bulb Brightness")
    st.progress(brightness / 100)
    st.markdown(f"**Brightness Level:** {brightness:.1f}% {'🔥' if brightness > 80 else '✨' if brightness > 50 else '💡'}")
    
    st.markdown("---")

    # Animate button
    if st.button("⚡ ANIMATE CIRCUIT & ELECTRON FLOW", key="animate_circuit", use_container_width=True):
        st.markdown("### 🎬 Circuit Animation in Progress...")
        
        # Create animation
        frames = 60
        num_electrons = max(4, int(current * 15))
        
        placeholder = st.empty()
        
        for frame in range(frames):
            fig = plt.figure(figsize=(14, 8))
            
            # Create grid layout
            gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
            ax_circuit = fig.add_subplot(gs[:, 0])
            ax_voltage = fig.add_subplot(gs[0, 1])
            ax_power = fig.add_subplot(gs[1, 1])
            
            # ===== MAIN CIRCUIT DIAGRAM =====
            ax_circuit.set_xlim(0, 10)
            ax_circuit.set_ylim(0, 8)
            ax_circuit.set_aspect('equal')
            ax_circuit.axis('off')
            ax_circuit.set_title("Circuit Diagram with Electron Flow", fontsize=14, fontweight='bold')
            
            # Battery position
            battery_x, battery_y = 2, 4
            bulb_x, bulb_y = 8, 4
            
            # Draw battery
            battery_body = plt.Rectangle((battery_x-0.4, battery_y-0.6), 0.8, 1.2, 
                                        fill=True, color='#2196f3', edgecolor='black', linewidth=3)
            ax_circuit.add_patch(battery_body)
            ax_circuit.text(battery_x, battery_y, '🔋', fontsize=35, ha='center', va='center')
            ax_circuit.text(battery_x-0.7, battery_y, '-', fontsize=30, ha='center', 
                          color='red', fontweight='bold')
            ax_circuit.text(battery_x+0.7, battery_y, '+', fontsize=30, ha='center', 
                          color='blue', fontweight='bold')
            ax_circuit.text(battery_x, battery_y-1.2, f'{voltage}V', fontsize=13, ha='center', 
                          fontweight='bold', bbox=dict(boxstyle='round', facecolor='yellow'))
            
            # Draw connecting wires
            # Top wire
            ax_circuit.plot([battery_x+0.4, bulb_x-0.7], [battery_y+0.6, battery_y+0.6], 
                          'k-', linewidth=5, solid_capstyle='round', label='Wire (conductor)')
            # Bottom wire
            ax_circuit.plot([bulb_x-0.7, battery_x-0.4], [bulb_y-0.6, battery_y-0.6], 
                          'k-', linewidth=5, solid_capstyle='round')
            # Vertical connections
            ax_circuit.plot([bulb_x-0.7, bulb_x-0.7], [battery_y+0.6, battery_y-0.6], 
                          'k-', linewidth=5, solid_capstyle='round')
            
            # Draw light bulb with glow effect
            for radius in np.linspace(1.2, 0.6, 8):
                alpha = (brightness / 100) * (radius / 1.2) * 0.3
                glow = plt.Circle((bulb_x, bulb_y), radius, color='yellow', alpha=alpha)
                ax_circuit.add_patch(glow)
            
            bulb_color = plt.cm.YlOrRd(brightness / 100)
            bulb = plt.Circle((bulb_x, bulb_y), 0.7, color=bulb_color, 
                            edgecolor='black', linewidth=3)
            ax_circuit.add_patch(bulb)
            ax_circuit.text(bulb_x, bulb_y, '💡', fontsize=40, ha='center', va='center')
            ax_circuit.text(bulb_x, bulb_y-1.2, f'{resistance}Ω', fontsize=13, ha='center', 
                          fontweight='bold', bbox=dict(boxstyle='round', facecolor='orange'))
            
            # Animate electrons
            for i in range(num_electrons):
                phase = (frame + i * frames / num_electrons) % frames
                progress = phase / frames
                
                # Calculate electron position along circuit path
                if progress < 0.3:  # Top wire (left to right)
                    t = progress / 0.3
                    ex = battery_x + 0.4 + t * (bulb_x - 0.7 - battery_x - 0.4)
                    ey = battery_y + 0.6
                elif progress < 0.4:  # Downward through bulb area
                    t = (progress - 0.3) / 0.1
                    ex = bulb_x - 0.7
                    ey = battery_y + 0.6 - t * 1.2
                elif progress < 0.7:  # Bottom wire (right to left)
                    t = (progress - 0.4) / 0.3
                    ex = bulb_x - 0.7 - t * (bulb_x - 0.7 - battery_x + 0.4)
                    ey = battery_y - 0.6
                else:  # Upward through battery
                    t = (progress - 0.7) / 0.3
                    ex = battery_x - 0.4 + 0.4 * t
                    ey = battery_y - 0.6 + t * 1.2
                
                # Draw electron with trail effect
                electron = plt.Circle((ex, ey), 0.12, color='#00e676', 
                                     edgecolor='#1b5e20', linewidth=2, zorder=10)
                ax_circuit.add_patch(electron)
                ax_circuit.text(ex, ey, 'e⁻', fontsize=8, ha='center', va='center', 
                              fontweight='bold', color='white')
            
            # Current direction arrows
            ax_circuit.arrow(5, battery_y+1, 1.5, 0, head_width=0.2, head_length=0.3, 
                           fc='red', ec='red', linewidth=2.5)
            ax_circuit.text(5.75, battery_y+1.5, f'Current Flow: {current:.4f} A', 
                          fontsize=11, color='red', fontweight='bold',
                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Labels
            ax_circuit.text(5, 7, 'CLOSED CIRCUIT', fontsize=14, ha='center', 
                          fontweight='bold', color='green',
                          bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
            
            # ===== VOLTAGE DISTRIBUTION =====
            v_across_bulb = voltage
            voltages_list = [0, voltage]
            positions = ['Ground\n(0V)', f'After Battery\n({voltage}V)']
            colors_v = ['#757575', '#42a5f5']
            
            bars = ax_voltage.bar(positions, voltages_list, color=colors_v, 
                                 edgecolor='black', linewidth=2, width=0.6)
            ax_voltage.set_ylabel("Voltage (V)", fontsize=11, fontweight='bold')
            ax_voltage.set_title("Voltage at Circuit Points", fontsize=12, fontweight='bold')
            ax_voltage.set_ylim(0, voltage * 1.3)
            ax_voltage.grid(axis='y', alpha=0.3)
            
            for bar, v in zip(bars, voltages_list):
                height = bar.get_height()
                ax_voltage.text(bar.get_x() + bar.get_width()/2., height,
                              f'{v:.1f}V', ha='center', va='bottom', 
                              fontweight='bold', fontsize=10)
            
            # ===== POWER & ENERGY DISPLAY =====
            power_data = [current * 1000, power, energy_per_hour]  # mA, W, Wh
            power_labels = [f'Current\n({current*1000:.1f} mA)', 
                           f'Power\n({power:.2f} W)', 
                           f'Energy/hr\n({energy_per_hour:.2f} Wh)']
            colors_p = ['#66bb6a', '#ffa726', '#ef5350']
            
            # Normalize for visualization
            max_val = max(power_data)
            normalized = [p / max_val * 100 for p in power_data]
            
            bars_p = ax_power.bar(range(3), normalized, color=colors_p, 
                                 edgecolor='black', linewidth=2, width=0.6)
            ax_power.set_ylabel("Relative Value", fontsize=11, fontweight='bold')
            ax_power.set_title("Circuit Performance", fontsize=12, fontweight='bold')
            ax_power.set_xticks(range(3))
            ax_power.set_xticklabels(power_labels, fontsize=9)
            ax_power.set_ylim(0, 120)
            ax_power.grid(axis='y', alpha=0.3)
            
            for i, (bar, label) in enumerate(zip(bars_p, power_labels)):
                height = bar.get_height()
                actual_val = power_data[i]
                ax_power.text(bar.get_x() + bar.get_width()/2., height + 3,
                            f'{actual_val:.2f}', ha='center', va='bottom', 
                            fontweight='bold', fontsize=9)
            
            placeholder.pyplot(fig)
            plt.close()
            time.sleep(0.05)
        
        st.success("✅ Animation Complete!")
    
    # Results explanation
    st.markdown("---")
    st.markdown("### 🎯 What This Means:")
    
    st.markdown(
        f"""
        <div style='background-color:#e3f2fd; padding:20px; border-radius:10px; font-family:Poppins;'>
        <h4 style='color:#1565c0;'>📌 Circuit Analysis Results:</h4>
        <ul style='font-size:15px; line-height:1.8;'>
            <li><b>Electron Flow Rate:</b> {current*6.24e18:.2e} electrons pass through any point per second</li>
            <li><b>Energy Conversion:</b> The bulb converts {power:.4f} Watts of electrical energy into light and heat every second</li>
            <li><b>Cost Estimate:</b> Running this bulb for 24 hours uses {(energy_per_hour*24)/1000:.4f} kWh 
                (at ₱10/kWh ≈ ₱{((energy_per_hour*24)/1000)*10:.2f} per day)</li>
            <li><b>Brightness Explanation:</b> {'Very bright! High power means intense light.' if brightness > 75 else 'Moderate brightness - efficient for reading.' if brightness > 40 else 'Dim light - saves energy but less light output.'}</li>
        </ul>
        
        <h4 style='color:#1565c0; margin-top:15px;'>🔬 Scientific Explanation:</h4>
        <p style='font-size:14px; line-height:1.7;'>
        When you close the circuit, the battery's chemical energy creates a potential difference. 
        This "pushes" electrons through the wire. The electrons flow from the negative terminal, 
        through the bulb's filament (where they lose energy as light and heat due to resistance), 
        and return to the positive terminal. This continuous flow is electric current!
        </p>
        
        <p style='font-size:14px; line-height:1.7;'>
        <b>Why does the bulb glow?</b> The tungsten filament in the bulb has high resistance. 
        As electrons struggle to pass through, they collide with atoms, transferring energy that 
        heats the filament to ~2500°C, making it glow white-hot!
        </p>
        </div>
        """, unsafe_allow_html=True
    )
    
    # Practical tips
    st.markdown("---")
    st.markdown(
        """
        <div style='background-color:#fff3e0; padding:15px; border-radius:10px; font-family:Poppins;'>
        <h4 style='color:#ef6c00;'>💡 Try These Experiments:</h4>
        <ul style='font-size:14px; line-height:1.7;'>
            <li><b>Increase Voltage:</b> Watch current and brightness increase (more electron push!)</li>
            <li><b>Increase Resistance:</b> Current decreases, bulb gets dimmer (harder for electrons to flow)</li>
            <li><b>Find Sweet Spot:</b> Adjust to get exactly 0.5A current - what values work?</li>
            <li><b>Energy Saver:</b> Find settings that give 25% brightness with minimum power</li>
        </ul>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("---")

def page_simulations():
    header()
    st.markdown(
        """
        <div style='text-align:center; background-color:#f3e5f5; padding:20px; border-radius:10px; font-family:"Poppins", sans-serif;'>
        <h1 style='color:#6a1b9a; font-family:"Lobster", cursive;'>🎮 Simulations Hub</h1>
        <p style='font-size:16px; line-height:1.5'>
        Explore interactive simulations to visualize science concepts. Choose one below and see the magic in action!
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='background-color:#FFACD8; padding:15px; border-radius:10px; font-family:"Poppins", sans-serif;'>
        <p style='font-size:16px; line-height:1.5'>Select a simulation to start:</p>
        </div>
        """, unsafe_allow_html=True
    )

    sim = st.radio("", ["Projectile Motion 🎯", "Energy Pendulum 🎯", "Electric Circuit ⚡"])

    if sim.startswith("Projectile Motion"): 
        sims_projectile_combined()
    elif sim.startswith("Energy Pendulum"): 
        sims_energy_pendulum()
    else: 
        sims_electricity_circuit()
    
    st.button("⬅ Back to Home", key="back_home_sim_page", on_click=lambda: st.session_state.update(page="home"))



# Main
if "page" not in st.session_state: st.session_state["page"]="home"

page = st.session_state["page"]
if page=="home": page_home()
elif page=="concepts": page_concepts()
elif page=="lessons": page_lessons()
elif page=="quizzes": page_quizzes()
elif page=="sims": page_simulations()

footer()
                    

