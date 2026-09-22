# -*- coding: utf-8 -*-
"""
Detailed IGCSE 0625 learning objectives (knowledge points), parsed
from 0625_y26-28_sy.pdf. Keyed by subsection code.

Each entry is either:
  {"title": ..., "points": [...]}                    (flat list), or
  {"title": ..., "subsubs": [{"code","title","points"}, ...]}  (grouped)
"""

SUBSUBS = {
 "1.1": {
  "title": "Physical quantities and measurement techniques",
  "points": [
   "Describe the use of rulers and measuring cylinders to find a length or a volume",
   "Describe how to measure a variety of time intervals using clocks and digital timers",
   "Determine an average value for a small distance and for a short interval of time by measuring multiples (including the period of oscillation of a pendulum)",
   "Understand that a scalar quantity has magnitude (size) only and that a vector quantity has magnitude and direction",
   "Know that the following quantities are scalars: distance, speed, time, mass, energy and temperature",
   "Know that the following quantities are vectors: force, weight, velocity, acceleration, momentum, electric field strength and gravitational field strength",
   "Determine, by calculation or graphically, the resultant of two vectors at right angles, limited to forces or velocities only"
  ]
 },
 "1.2": {
  "title": "Motion",
  "points": [
   "Define speed as distance travelled per unit time; recall and use the equation v = s/t",
   "Define velocity as speed in a given direction",
   "Recall and use the equation average speed = total distance ÷ total time",
   "Sketch, plot and interpret distance–time and speed–time graphs",
   "Determine, qualitatively, from given data or the shape of a distance–time graph or speed–time graph when an object is: (a) at rest (b) moving with constant speed (c) accelerating (d) decelerating",
   "Calculate speed from the gradient of a straight- line section of a distance–time graph",
   "Calculate the area under a speed–time graph to determine the distance travelled for motion with constant speed or constant acceleration",
   "State that the acceleration of free fall g for an object near to the surface of the Earth is approximately constant and is approximately"
  ]
 },
 "1.3": {
  "title": "Mass and weight",
  "points": [
   "State that mass is a measure of the quantity of matter in an object at rest relative to the observer",
   "State that weight is a gravitational force on an object that has mass",
   "Define gravitational field strength as force per unit mass; recall and use the equation g = W/m and know that this is equivalent to the acceleration of free fall",
   "Know that weights (and masses) may be compared using a balance",
   "Describe, and use the concept of, weight as the effect of a gravitational field on a mass"
  ]
 },
 "1.4": {
  "title": "Density",
  "points": [
   "Define density as mass per unit volume; recall and use the equation ρ = m/V",
   "Describe how to determine the density of a liquid, of a regularly shaped solid and of an irregularly shaped solid which sinks in a liquid (volume by displacement), including appropriate calculations",
   "Determine whether an object floats based on density data",
   "Determine whether one liquid will float on another liquid based on density data given that the liquids do not mix"
  ]
 },
 "1.5": {
  "title": "Forces",
  "subsubs": [
   {
    "code": "1.5.1",
    "title": "Effects of forces",
    "points": [
     "Know that forces may produce changes in the size and shape of an object",
     "Sketch, plot and interpret load–extension graphs for an elastic solid and describe the associated experimental procedures",
     "Determine the resultant of two or more forces acting along the same straight line",
     "Know that an object either remains at rest or continues in a straight line at constant speed unless acted on by a resultant force",
     "State that a resultant force may change the velocity of an object by changing its direction of motion or its speed",
     "Define the spring constant as force per unit extension; recall and use the equation k = F/x 10 Define and use the term ‘limit of proportionality’ for a load–extension graph and identify this point on the graph (an understanding of the elastic limit is not required) 11 Recall and use the equation F = ma and know that the force and the acceleration are in the same direction 12 Describe, qualitatively, motion in a circular path due to a force perpendicular to the motion as: (a) speed increases if force increases, with mass and radius constant (b) radius decreases if force increases, with mass and speed constant (c) an increased mass requires an increased force to keep speed and radius constant ( F = mv 2 r is not required) continued",
     "Describe solid friction as the force between two surfaces that may impede motion and produce heating",
     "Know that friction (drag) acts on an object moving through a liquid",
     "Know that friction (drag) acts on an object moving through a gas (e.g. air resistance)"
    ]
   },
   {
    "code": "1.5.2",
    "title": "Turning effect of forces",
    "points": [
     "Describe the moment of a force as a measure of its turning effect and give everyday examples",
     "Define the moment of a force as moment = force × perpendicular distance from the pivot; recall and use this equation",
     "Apply the principle of moments to situations with one force each side of the pivot, including balancing of a beam",
     "State that, when there is no resultant force and no resultant moment, an object is in equilibrium",
     "Apply the principle of moments to other situations, including those with more than one force each side of the pivot",
     "Describe an experiment to demonstrate that there is no resultant moment on an object in equilibrium"
    ]
   },
   {
    "code": "1.5.3",
    "title": "Centre of gravity",
    "points": [
     "State what is meant by centre of gravity",
     "Describe an experiment to determine the position of the centre of gravity of an irregularly shaped plane lamina",
     "Describe, qualitatively, the effect of the position of the centre of gravity on the stability of simple objects"
    ]
   }
  ]
 },
 "1.6": {
  "title": "Momentum",
  "points": [
   "Define momentum as mass × velocity; recall and use the equation p = mv",
   "Define impulse as force × time for which force acts; recall and use the equation impulse = FΔt = Δ(mv)",
   "Apply the principle of the conservation of momentum to solve simple problems in one dimension",
   "Define resultant force as the change in momentum per unit time; recall and use the equation F = Δp/Δt"
  ]
 },
 "1.7": {
  "title": "Energy, work and power",
  "subsubs": [
   {
    "code": "1.7.1",
    "title": "Energy",
    "points": [
     "State that energy may be stored as kinetic, gravitational potential, chemical, elastic (strain), nuclear, electrostatic and internal (thermal)",
     "Describe how energy is transferred between stores during events and processes, including examples of transfer by forces (mechanical work done), electrical currents (electrical work done), heating, and by electromagnetic, sound and other waves",
     "Know the principle of the conservation of energy and apply this principle to simple examples including the interpretation of simple flow diagrams",
     "Recall and use the equation for kinetic energy Ek = ½mv²",
     "Recall and use the equation for the change in gravitational potential energy ΔEp = mgΔh",
     "Know the principle of the conservation of energy and apply this principle to complex examples involving multiple stages, including the interpretation of Sankey diagrams"
    ]
   },
   {
    "code": "1.7.2",
    "title": "Work",
    "points": [
     "Understand that mechanical or electrical work done is equal to the energy transferred",
     "Recall and use the equation for mechanical working W = Fd = ΔE"
    ]
   },
   {
    "code": "1.7.3",
    "title": "Energy resources",
    "points": [
     "Describe how useful energy may be obtained, or electrical power generated, from: (a) chemical energy stored in fossil fuels (b) chemical energy stored in biofuels (c) water, including the energy stored in waves, in tides and in water behind hydroelectric dams (d) geothermal resources (e) nuclear fuel (f) light from the Sun to generate electrical power (solar cells) (g) infrared and other electromagnetic waves from the Sun to heat water (solar panels) and be the source of wind energy including references to a boiler, turbine and generator where they are used",
     "Describe advantages and disadvantages of each method in terms of renewability, availability, reliability, scale and environmental impact",
     "Understand, qualitatively, the concept of efficiency of energy transfer",
     "Know that radiation from the Sun is the main source of energy for all our energy resources except geothermal, nuclear and tidal",
     "Know that energy is released by nuclear fusion in the Sun",
     "Know that research is being carried out to investigate how energy released by nuclear fusion can be used to produce electrical energy on a large scale",
     "Define efficiency as: (a) (%) efficiency = (useful energy output) (total energy input) (× 100%) (b) (%) efficiency = (useful power output) (total power input) (× 100%) recall and use these equations"
    ]
   },
   {
    "code": "1.7.4",
    "title": "Power",
    "points": [
     "Define power as work done per unit time and also as energy transferred per unit time; recall and use the equations (a) P = W t (b) P = ΔE t"
    ]
   }
  ]
 },
 "1.8": {
  "title": "Pressure",
  "points": [
   "Define pressure as force per unit area; recall and use the equation p = F/A",
   "Describe how pressure varies with force and area in the context of everyday examples",
   "Describe, qualitatively, how the pressure beneath the surface of a liquid changes with depth and density of the liquid",
   "Recall and use the equation for the change in pressure beneath the surface of a liquid Δp = ρgΔh",
   "Thermal physics"
  ]
 },
 "2.1": {
  "title": "Kinetic particle model of matter",
  "subsubs": [
   {
    "code": "2.1.1",
    "title": "States of matter",
    "points": [
     "Know the distinguishing properties of solids, liquids and gases",
     "Know the terms for the changes in state between solids, liquids and gases (gas to solid and solid to gas transfers are not required)"
    ]
   },
   {
    "code": "2.1.2",
    "title": "Particle model",
    "points": [
     "Describe the particle structure of solids, liquids and gases in terms of the arrangement, separation and motion of the particles and represent these states using simple particle diagrams",
     "Describe the relationship between the motion of particles and temperature, including the idea that there is a lowest possible temperature (−273 °C), known as absolute zero, where the particles have least kinetic energy",
     "Describe the pressure and the changes in pressure of a gas in terms of the motion of its particles and their collisions with a surface",
     "Know that the random motion of microscopic particles in a suspension is evidence for the kinetic particle model of matter",
     "Describe and explain this motion (sometimes known as Brownian motion) in terms of random collisions between the microscopic particles in a suspension and the particles of the gas or liquid",
     "Know that the forces and distances between particles (atoms, molecules, ions and electrons) and the motion of the particles affects the properties of solids, liquids and gases",
     "Describe the pressure and the changes in pressure of a gas in terms of the forces exerted by particles colliding with surfaces, creating a force per unit area",
     "Know that microscopic particles may be moved by collisions with light fast-moving molecules and correctly use the terms atoms or molecules as distinct from microscopic particles"
    ]
   },
   {
    "code": "2.1.3",
    "title": "Gases and the absolute scale of temperature",
    "points": [
     "Describe qualitatively, in terms of particles, the effect on the pressure of a fixed mass of gas of: (a) a change of temperature at constant volume (b) a change of volume at constant temperature",
     "Convert temperatures between kelvin and degrees Celsius; recall and use the equation T (in K) = θ (in °C) + 273",
     "Recall and use the equation pV = constant for a fixed mass of gas at constant temperature, including a graphical representation of this relationship"
    ]
   }
  ]
 },
 "2.2": {
  "title": "Thermal properties and temperature",
  "subsubs": [
   {
    "code": "2.2.1",
    "title": "Thermal expansion of solids, liquids and gases",
    "points": [
     "Describe, qualitatively, the thermal expansion of solids, liquids and gases at constant pressure",
     "Describe some of the everyday applications and consequences of thermal expansion",
     "Explain, in terms of the motion and arrangement of particles, the relative order of magnitudes of the expansion of solids, liquids and gases as their temperatures rise"
    ]
   },
   {
    "code": "2.2.2",
    "title": "Specific heat capacity",
    "points": [
     "Know that a rise in the temperature of an object increases its internal energy",
     "Describe an increase in temperature of an object in terms of an increase in the average kinetic energies of all of the particles in the object",
     "Define specific heat capacity as the energy required per unit mass per unit temperature increase; recall and use the equation c = ΔE m∆θ",
     "Describe experiments to measure the specific heat capacity of a solid and a liquid"
    ]
   },
   {
    "code": "2.2.3",
    "title": "Melting, boiling and evaporation",
    "points": [
     "Describe melting and boiling in terms of energy input without a change in temperature",
     "Know the melting and boiling temperatures for water at standard atmospheric pressure",
     "Describe condensation and solidification in terms of particles",
     "Describe evaporation in terms of the escape of more-energetic particles from the surface of a liquid",
     "Know that evaporation causes cooling of a liquid",
     "Describe the differences between boiling and evaporation",
     "Describe how temperature, surface area and air movement over a surface affect evaporation",
     "Explain the cooling of an object in contact with an evaporating liquid"
    ]
   }
  ]
 },
 "2.3": {
  "title": "Transfer of thermal energy",
  "subsubs": [
   {
    "code": "2.3.1",
    "title": "Conduction",
    "points": [
     "Describe experiments to demonstrate the properties of good thermal conductors and bad thermal conductors (thermal insulators)",
     "Describe thermal conduction in all solids in terms of atomic or molecular lattice vibrations and also in terms of the movement of free (delocalised) electrons in metallic conductors",
     "Describe, in terms of particles, why thermal conduction is bad in gases and most liquids",
     "Know that there are many solids that conduct thermal energy better than thermal insulators but do so less well than good thermal conductors"
    ]
   },
   {
    "code": "2.3.2",
    "title": "Convection",
    "points": [
     "Know that convection is an important method of thermal energy transfer in liquids and gases",
     "Explain convection in liquids and gases in terms of density changes and describe experiments to illustrate convection"
    ]
   },
   {
    "code": "2.3.3",
    "title": "Radiation",
    "points": [
     "Know that thermal radiation is infrared radiation and that all objects emit this radiation",
     "Know that thermal energy transfer by thermal radiation does not require a medium",
     "Describe the effect of surface colour (black or white) and texture (dull or shiny) on the emission, absorption and reflection of infrared radiation",
     "Know that for an object to be at a constant temperature it needs to transfer energy away from the object at the same rate that it receives energy",
     "Know what happens to an object if the rate at which it receives energy is less or more than the rate at which it transfers energy away from the object",
     "Know how the temperature of the Earth is affected by factors controlling the balance between incoming radiation and radiation emitted from the Earth’s surface continued",
     "Describe experiments to distinguish between good and bad emitters of infrared radiation",
     "Describe experiments to distinguish between good and bad absorbers of infrared radiation",
     "Describe how the rate of emission of radiation depends on the surface temperature and surface area of an object"
    ]
   },
   {
    "code": "2.3.4",
    "title": "Consequences of thermal energy transfer",
    "points": [
     "Explain some of the basic everyday applications and consequences of conduction, convection and radiation, including: (a) heating objects such as kitchen pans (b) heating a room by convection",
     "Explain some of the complex applications and consequences of conduction, convection and radiation where more than one type of thermal energy transfer is significant, including: (a) a fire burning wood or coal (b) a radiator in a car",
     "Waves"
    ]
   }
  ]
 },
 "3.1": {
  "title": "General properties of waves",
  "points": [
   "Know that waves transfer energy without transferring matter",
   "Describe what is meant by wave motion as illustrated by vibrations in ropes and springs, and by experiments using water waves",
   "Describe the features of a wave in terms of wavefront, wavelength, frequency, crest (peak), trough, amplitude and wave speed",
   "Recall and use the equation for wave speed v = f λ",
   "Know that for a transverse wave, the direction of vibration is at right angles to the direction of propagation and understand that electromagnetic radiation, water waves and seismic S-waves (secondary) can be modelled as transverse",
   "Know that for a longitudinal wave, the direction of vibration is parallel to the direction of propagation and understand that sound waves and seismic P-waves (primary) can be modelled as longitudinal",
   "Describe how waves can undergo: (a) reflection at a plane surface (b) refraction due to a change of speed (c) diffraction through a narrow gap",
   "Describe the use of a ripple tank to show: (a) reflection at a plane surface (b) refraction due to a change in speed caused by a change in depth (c) diffraction due to a gap (d) diffraction due to an edge",
   "Describe how wavelength and gap size affects diffraction through a gap 10 Describe how wavelength affects diffraction at an edge"
  ]
 },
 "3.2": {
  "title": "Light",
  "subsubs": [
   {
    "code": "3.2.1",
    "title": "Reflection of light",
    "points": [
     "Define and use the terms normal, angle of incidence and angle of reflection",
     "Describe the formation of an optical image by a plane mirror and give its characteristics, i.e. same size, same distance from mirror, virtual",
     "State that for reflection, the angle of incidence is equal to the angle of reflection; recall and use this relationship",
     "Use simple constructions, measurements and calculations for reflection by plane mirrors"
    ]
   },
   {
    "code": "3.2.2",
    "title": "Refraction of light",
    "points": [
     "Define and use the terms normal, angle of incidence and angle of refraction",
     "Describe an experiment to show refraction of light by transparent blocks of different shapes",
     "Describe the passage of light through a transparent material (limited to the boundaries between two mediums only)",
     "State the meaning of critical angle",
     "Describe internal reflection and total internal reflection using both experimental and everyday examples",
     "Define refractive index, n, as the ratio of the speeds of a wave in two different regions",
     "Recall and use the equation n = sin i / sin r",
     "Recall and use the equation n = 1 / sin c",
     "Describe the use of optical fibres, particularly in telecommunications"
    ]
   },
   {
    "code": "3.2.3",
    "title": "Thin lenses",
    "points": [
     "Describe the action of thin converging and thin diverging lenses on a parallel beam of light",
     "Define and use the terms focal length, principal axis and principal focus (focal point)",
     "Draw and use ray diagrams for the formation of a real image by a converging lens",
     "Describe the characteristics of an image using the terms enlarged/same size/diminished, upright/inverted and real/virtual",
     "Know that a virtual image is formed when diverging rays are extrapolated backwards and does not form a visible projection on a screen",
     "Draw and use ray diagrams for the formation of a virtual image by a converging lens",
     "Describe the use of a single lens as a magnifying glass",
     "Describe the use of converging and diverging lenses to correct long-sightedness and short- sightedness"
    ]
   },
   {
    "code": "3.2.4",
    "title": "Dispersion of light",
    "points": [
     "Describe the dispersion of light as illustrated by the refraction of white light by a glass prism",
     "Know the traditional seven colours of the visible spectrum in order of frequency and in order of wavelength",
     "Recall that visible light of a single frequency is described as monochromatic"
    ]
   }
  ]
 },
 "3.3": {
  "title": "Electromagnetic spectrum",
  "points": [
   "Know the main regions of the electromagnetic spectrum in order of frequency and in order of wavelength",
   "Know that all electromagnetic waves travel at the same high speed in a vacuum",
   "Describe typical uses of the different regions of the electromagnetic spectrum including: (a) radio waves; radio and television transmissions, astronomy, radio frequency identification (RFID) (b) microwaves; satellite television, mobile phones (cell phones), microwave ovens (c) infrared; electric grills, short range communications such as remote controllers for televisions, intruder alarms, thermal imaging, optical fibres (d) visible light; vision, photography, illumination (e) ultraviolet; security marking, detecting fake bank notes, sterilising water (f) X-rays; medical scanning, security scanners (g) gamma rays; sterilising food and medical equipment, detection of cancer and its treatment",
   "Describe the harmful effects on people of excessive exposure to electromagnetic radiation, including: (a) microwaves; internal heating of body cells (b) infrared; skin burns (c) ultraviolet; damage to surface cells and eyes, leading to skin cancer and eye conditions (d) X-rays and gamma rays; mutation or damage to cells in the body",
   "Know that the speed of electromagnetic waves in a vacuum is 3.0 × 108 m / s and is approximately the same in air continued",
   "Know that communication with artificial satellites is mainly by microwaves: (a) some satellite phones use low orbit artificial satellites (b) some satellite phones and direct broadcast satellite television use geostationary satellites",
   "Know that many important systems of communications rely on electromagnetic radiation including: (a) mobile phones (cell phones) and wireless internet use microwaves because microwaves can penetrate some walls and only require a short aerial for transmission and reception (b) Bluetooth uses radio waves because radio waves pass through walls but the signal is weakened on doing so (c) optical fibres (visible light or infrared) are used for cable television and high-speed broadband because glass is transparent to visible light and some infrared; visible light and short wavelength infrared can carry high rates of data",
   "Know the difference between a digital and analogue signal",
   "Know that a sound can be transmitted as a digital or analogue signal 10 Explain the benefits of digital signalling including increased rate of transmission of data and increased range due to accurate signal regeneration"
  ]
 },
 "3.4": {
  "title": "Sound",
  "points": [
   "Describe the production of sound by vibrating sources",
   "Describe the longitudinal nature of sound waves",
   "State the approximate range of frequencies audible to humans as 20 Hz to 20 000 Hz",
   "Know that a medium is needed to transmit sound waves",
   "Know that the speed of sound in air is approximately 330–350 m / s",
   "Describe a method involving a measurement of distance and time for determining the speed of sound in air",
   "Describe how changes in amplitude and frequency affect the loudness and pitch of sound waves",
   "Describe an echo as the reflection of sound waves",
   "Define ultrasound as sound with a frequency higher than 20 kHz",
   "Electricity and magnetism"
  ]
 },
 "4.1": {
  "title": "Simple phenomena of magnetism",
  "points": [
   "Describe the forces between magnetic poles and between magnets and magnetic materials, including the use of the terms north pole (N pole), south pole (S pole), attraction and repulsion, magnetised and unmagnetised",
   "Describe induced magnetism",
   "State the differences between the properties of temporary magnets (made of soft iron) and the properties of permanent magnets (made of steel",
   "State the difference between magnetic and non-magnetic materials",
   "Describe a magnetic field as a region in which a magnetic pole experiences a force",
   "Draw the pattern and direction of magnetic field lines around a bar magnet",
   "State that the direction of a magnetic field at a point is the direction of the force on the N pole of a magnet at that point",
   "Describe the plotting of magnetic field lines with a compass or iron filings and the use of a compass to determine the direction of the magnetic field",
   "Describe the uses of permanent magnets and electromagnets"
  ]
 },
 "4.2": {
  "title": "Electrical quantities",
  "subsubs": [
   {
    "code": "4.2.1",
    "title": "Electric charge",
    "points": [
     "State that there are positive and negative charges",
     "State that positive charges repel other positive charges, negative charges repel other negative charges, but positive charges attract negative charges",
     "Describe simple experiments to show the production of electrostatic charges by friction and to show the detection of electrostatic charges",
     "Explain that charging of solids by friction involves only a transfer of negative charge (electrons)",
     "Describe an experiment to distinguish between electrical conductors and insulators",
     "Recall and use a simple electron model to explain the difference between electrical conductors and insulators and give typical examples",
     "State that charge is measured in coulombs",
     "Describe an electric field as a region in which an electric charge experiences a force",
     "State that the direction of an electric field at a point is the direction of the force on a positive charge at that point 10 Describe simple electric field patterns, including the direction of the field: (a) around a point charge (b) around a charged conducting sphere (c) between two oppositely charged parallel conducting plates (end effects will not be examined)"
    ]
   },
   {
    "code": "4.2.2",
    "title": "Electric current",
    "points": [
     "Know that electric current is related to the flow of charge",
     "Describe the use of ammeters (analogue and digital) with different ranges",
     "Describe electrical conduction in metals in terms of the movement of free electrons",
     "Know the difference between direct current (d.c.) and alternating current (a.c.)",
     "Define electric current as the charge passing a point per unit time; recall and use the equation I = Q/t",
     "State that conventional current is from positive to negative and that the flow of free electrons is from negative to positive"
    ]
   },
   {
    "code": "4.2.3",
    "title": "Electromotive force and potential difference",
    "points": [
     "Define electromotive force (e.m.f.) as the electrical work done by a source in moving a unit charge around a complete circuit",
     "Know that e.m.f. is measured in volts (V)",
     "Define potential difference (p.d.) as the work done by a unit charge passing through a component",
     "Know that the p.d. between two points is measured in volts (V)",
     "Describe the use of voltmeters (analogue and digital) with different ranges",
     "Recall and use the equation for e.m.f. E = W/Q",
     "Recall and use the equation for p.d. V = W/Q"
    ]
   },
   {
    "code": "4.2.4",
    "title": "Resistance",
    "points": [
     "Recall and use the equation for resistance R = V/I",
     "Describe an experiment to determine resistance using a voltmeter and an ammeter and do the appropriate calculations",
     "State, qualitatively, the relationship of the resistance of a metallic wire to its length and to its cross-sectional area",
     "Sketch and explain the current–voltage graphs for a resistor of constant resistance, a filament lamp and a diode",
     "Recall and use the following relationship for a metallic electrical conductor: (a) resistance is directly proportional to length (b) resistance is inversely proportional to cross-sectional area"
    ]
   },
   {
    "code": "4.2.5",
    "title": "Electrical energy and electrical power",
    "points": [
     "Understand that electric circuits transfer energy from a source of electrical energy, such as an electrical cell or mains supply, to the circuit components and then into the surroundings",
     "Recall and use the equation for electrical power P = IV",
     "Recall and use the equation for electrical energy E = IVt",
     "Define the kilowatt-hour (kW h) and calculate the cost of using electrical appliances where the energy unit is the kW h"
    ]
   }
  ]
 },
 "4.3": {
  "title": "Electric circuits",
  "subsubs": [
   {
    "code": "4.3.1",
    "title": "Circuit diagrams and circuit components",
    "points": [
     "Draw and interpret circuit diagrams containing cells, batteries, power supplies, generators, potential dividers, switches, resistors (fixed and variable), heaters, thermistors (NTC only), light- dependent resistors (LDRs), lamps, motors, bells, ammeters, voltmeters, magnetising coils, transformers, fuses and relays and know how these components behave in the circuit",
     "Draw and interpret circuit diagrams containing diodes and light-emitting diodes (LEDs) and know how these components behave in the circuit"
    ]
   },
   {
    "code": "4.3.2",
    "title": "Series and parallel circuits",
    "points": [
     "Know that the current at every point in a series circuit is the same",
     "Know how to construct and use series and parallel circuits",
     "Calculate the combined e.m.f. of several sources in series",
     "Calculate the combined resistance of two or more resistors in series",
     "State that, for a parallel circuit, the current from the source is larger than the current in each branch",
     "State that the combined resistance of two resistors in parallel is less than that of either resistor by itself",
     "State the advantages of connecting lamps in parallel in a lighting circuit",
     "Recall and use in calculations, the fact that: (a) the sum of the currents entering a junction in a parallel circuit is equal to the sum of the currents that leave the junction (b) the total p.d. across the components in a series circuit is equal to the sum of the individual p.d.s across each component (c) the p.d. across an arrangement of parallel resistances is the same as the p.d. across one branch in the arrangement of the parallel resistances",
     "Explain that the sum of the currents into a junction is the same as the sum of the currents out of the junction 10 Calculate the combined resistance of two resistors in parallel"
    ]
   },
   {
    "code": "4.3.3",
    "title": "Action and use of circuit components",
    "points": [
     "Know that the p.d. across an electrical conductor increases as its resistance increases for a constant current",
     "Describe the action of a variable potential divider",
     "Recall and use the equation for two resistors used as a potential divider R1/R2 = V1/V2"
    ]
   }
  ]
 },
 "4.4": {
  "title": "Electrical safety",
  "points": [
   "State the hazards of: (a) damaged insulation (b) overheating cables (c) damp conditions (d) excess current from overloading of plugs, extension leads, single and multiple sockets when using a mains supply",
   "Know that a mains circuit consists of a live wire (line wire), a neutral wire and an earth wire and explain why a switch must be connected to the live wire for the circuit to be switched off safely",
   "Explain the use and operation of trip switches and fuses and choose appropriate fuse ratings and trip switch settings",
   "Explain why the outer casing of an electrical appliance must be either non-conducting (double-insulated) or earthed",
   "State that a fuse without an earth wire protects the circuit and the cabling for a double- insulated appliance"
  ]
 },
 "4.5": {
  "title": "Electromagnetic effects",
  "subsubs": [
   {
    "code": "4.5.1",
    "title": "Electromagnetic induction",
    "points": [
     "Know that a conductor moving across a magnetic field or a changing magnetic field linking with a conductor can induce an e.m.f. in the conductor",
     "Describe an experiment to demonstrate electromagnetic induction",
     "State the factors affecting the magnitude of an induced e.m.f.",
     "Know that the direction of an induced e.m.f. opposes the change causing it",
     "State and use the relative directions of force, field and induced current"
    ]
   },
   {
    "code": "4.5.2",
    "title": "The a.c. generator",
    "points": [
     "Describe a simple form of a.c. generator (rotating coil or rotating magnet) and the use of slip rings and brushes where needed",
     "Sketch and interpret graphs of e.m.f. against time for simple a.c. generators and relate the position of the generator coil to the peaks, troughs and zeros of the e.m.f."
    ]
   },
   {
    "code": "4.5.3",
    "title": "Magnetic effect of a current",
    "points": [
     "Describe the pattern and direction of the magnetic field due to currents in straight wires and in solenoids",
     "Describe an experiment to identify the pattern of the magnetic field (including direction) due to currents in straight wires and in solenoids",
     "Describe how the magnetic effect of a current is used in relays and loudspeakers and give examples of their application",
     "State the qualitative variation of the strength of the magnetic field around straight wires and solenoids",
     "Describe the effect on the magnetic field around straight wires and solenoids of changing the magnitude and direction of the current"
    ]
   },
   {
    "code": "4.5.4",
    "title": "Force on a current-carrying conductor",
    "points": [
     "Describe an experiment to show that a force acts on a current-carrying conductor in a magnetic field, including the effect of reversing: (a) the current (b) the direction of the field",
     "Recall and use the relative directions of force, magnetic field and current",
     "Determine the direction of the force on beams of charged particles in a magnetic field"
    ]
   },
   {
    "code": "4.5.5",
    "title": "The d.c. motor",
    "points": [
     "Know that a current-carrying coil in a magnetic field may experience a turning effect and that the turning effect is increased by increasing: (a) the number of turns on the coil (b) the current (c) the strength of the magnetic field",
     "Describe the operation of an electric motor, including the action of a split-ring commutator and brushes"
    ]
   },
   {
    "code": "4.5.6",
    "title": "The transformer",
    "points": [
     "Describe the construction of a simple transformer with a soft-iron core, as used for voltage transformations",
     "Use the terms primary, secondary, step-up and step-down",
     "Recall and use the equation Vp/Vs = Np/Ns where p and s refer to primary and secondary",
     "Describe the use of transformers in high- voltage transmission of electricity",
     "State the advantages of high-voltage transmission",
     "Explain the principle of operation of a simple iron-cored transformer",
     "Recall and use the equation for 100% efficiency in a transformer IpVp = IsVs where p and s refer to primary and secondary",
     "Recall and use the equation P = I²R to explain why power losses in cables are smaller when the voltage is greater",
     "Nuclear physics"
    ]
   }
  ]
 },
 "5.1": {
  "title": "The nuclear model of the atom",
  "subsubs": [
   {
    "code": "5.1.1",
    "title": "The atom",
    "points": [
     "Describe the structure of an atom in terms of a positively charged nucleus and negatively charged electrons in orbit around the nucleus",
     "Know how atoms may form positive ions by losing electrons or form negative ions by gaining electrons",
     "Describe how the scattering of alpha (α) particles by a sheet of thin metal supports the nuclear model of the atom, by providing evidence for: (a) a very small nucleus surrounded by mostly empty space (b) a nucleus containing most of the mass of the atom (c) a nucleus that is positively charged"
    ]
   },
   {
    "code": "5.1.2",
    "title": "The nucleus",
    "points": [
     "Describe the composition of the nucleus in terms of protons and neutrons",
     "State the relative charges of protons, neutrons and electrons as +1, 0 and –1 respectively",
     "Define the terms proton number (atomic number) Z and nucleon number (mass number) A and be able to calculate the number of neutrons in a nucleus",
     "Use the nuclide notation A ZX",
     "Explain what is meant by an isotope and state that an element may have more than one isotope",
     "Describe the processes of nuclear fission and nuclear fusion as the splitting or joining of nuclei, to include the nuclide equation and qualitative description of mass and energy changes without values",
     "Know the relationship between the proton number and the relative charge on a nucleus",
     "Know the relationship between the nucleon number and the relative mass of a nucleus"
    ]
   }
  ]
 },
 "5.2": {
  "title": "Radioactivity",
  "subsubs": [
   {
    "code": "5.2.1",
    "title": "Detection of radioactivity",
    "points": [
     "Know what is meant by background radiation",
     "Know the sources that make a significant contribution to background radiation including: (a) radon gas (in the air) (b) rocks and buildings (c) food and drink (d) cosmic rays",
     "Know that ionising nuclear radiation can be measured using a detector connected to a counter",
     "Use count rate measured in counts / s or counts / minute",
     "Use measurements of background radiation to determine a corrected count rate"
    ]
   },
   {
    "code": "5.2.2",
    "title": "The three types of nuclear emission",
    "points": [
     "Describe the emission of radiation from a nucleus as spontaneous and random in direction",
     "Identify alpha (α), beta (β) and gamma (γ) emissions from the nucleus by recalling: (a) their nature (b) their relative ionising effects (c) their relative penetrating abilities (β+ are not included, β-particles will be taken to refer to β–)",
     "Describe the deflection of α-particles, β-particles and γ-radiation in electric fields and magnetic fields",
     "Explain their relative ionising effects with reference to: (a) kinetic energy (b) electric charge"
    ]
   },
   {
    "code": "5.2.3",
    "title": "Radioactive decay",
    "points": [
     "Know that radioactive decay is a change in an unstable nucleus that can result in the emission of α-particles or β-particles and/or γ-radiation and know that these changes are spontaneous and random",
     "State that during α-decay or β-decay, the nucleus changes to that of a different element",
     "Know that isotopes of an element may be radioactive due to an excess of neutrons in the nucleus and/or the nucleus being too heavy",
     "Describe the effect of α-decay, β-decay and γ-emissions on the nucleus, including an increase in stability and a reduction in the number of excess neutrons; the following change in the nucleus occurs during β-emission neutron → proton + electron",
     "Use decay equations, using nuclide notation, to show the emission of α-particles, β-particles and γ-radiation"
    ]
   },
   {
    "code": "5.2.4",
    "title": "Half-life",
    "points": [
     "Define the half-life of a particular isotope as the time taken for half the nuclei of that isotope in any sample to decay; recall and use this definition in simple calculations, which might involve information in tables or decay curves (calculations will not include background radiation)",
     "Calculate half-life from data or decay curves from which background radiation has not been subtracted",
     "Explain how the type of radiation emitted and the half-life of an isotope determine which isotope is used for applications including: (a) household fire (smoke) alarms (b) irradiating food to kill bacteria (c) sterilisation of equipment using gamma rays (d) measuring and controlling thicknesses of materials with the choice of radiations used linked to penetration and absorption (e) diagnosis and treatment of cancer using gamma rays"
    ]
   },
   {
    "code": "5.2.5",
    "title": "Safety precautions",
    "points": [
     "State the effects of ionising nuclear radiations on living things, including cell death, mutations and cancer",
     "Describe how radioactive materials are moved, used and stored in a safe way",
     "Explain safety precautions for all ionising radiation in terms of reducing exposure time, increasing distance between source and living tissue and using shielding to absorb radiation",
     "Space physics"
    ]
   }
  ]
 },
 "6.1": {
  "title": "The Earth and the Solar System",
  "subsubs": [
   {
    "code": "6.1.1",
    "title": "The Earth",
    "points": [
     "Know that the Earth is a planet that rotates on its axis, which is tilted, once in approximately 24 hours, and use this to explain observations of the apparent daily motion of the Sun and the periodic cycle of day and night",
     "Know that the Earth orbits the Sun once in approximately 365 days and use this to explain the periodic nature of the seasons",
     "Know that it takes approximately one month for the Moon to orbit the Earth and use this to explain the periodic nature of the Moon’s cycle of phases",
     "Define average orbital speed from the equation v = 2πr/T where r is the average radius of the orbit and T is the orbital period; recall and use this equation"
    ]
   },
   {
    "code": "6.1.2",
    "title": "The Solar System",
    "points": [
     "Describe the Solar System as containing: (a) one star, the Sun (b) the eight named planets and know their order from the Sun (c) minor planets that orbit the Sun, including dwarf planets such as Pluto and asteroids in the asteroid belt (d) moons, that orbit the planets (e) smaller Solar System bodies, including comets and natural satellites",
     "Know that, in comparison to each other, the four planets nearest the Sun are rocky and small and the four planets furthest from the Sun are gaseous and large, and explain this difference by referring to an accretion model for Solar System formation, to include: (a) the model’s dependence on gravity (b) the presence of many elements in interstellar clouds of gas and dust (c) the rotation of material in the cloud and the formation of an accretion disc",
     "Know that planets, minor planets and comets have elliptical orbits, and recall that the Sun is not at the centre of the elliptical orbit, except when the orbit is approximately circular",
     "Analyse and interpret planetary data about orbital distance, orbital duration, density, surface temperature and uniform gravitational field strength at the planet’s surface continued",
     "Know that the strength of the gravitational field (a) at the surface of a planet depends on the mass of the planet (b) around a planet decreases as the distance from the planet increases",
     "Calculate the time it takes light to travel a significant distance such as between objects in the Solar System",
     "Know that the Sun contains most of the mass of the Solar System and this explains why the planets orbit the Sun",
     "Know that the force that keeps an object in orbit around the Sun is the gravitational attraction of the Sun",
     "Know that the strength of the Sun’s gravitational field decreases and that the orbital speeds of the planets decrease as the distance from the Sun increases 10 Know that an object in an elliptical orbit travels faster when closer to the Sun and explain this using the conservation of energy"
    ]
   }
  ]
 },
 "6.2": {
  "title": "Stars and the Universe",
  "subsubs": [
   {
    "code": "6.2.1",
    "title": "The Sun as a star",
    "points": [
     "Know that the Sun is a star of medium size, consisting mostly of hydrogen and helium, and that it radiates most of its energy in the infrared, visible light and ultraviolet regions of the electromagnetic spectrum",
     "Know that stars are powered by nuclear reactions that release energy and that in stable stars the nuclear reactions involve the fusion of hydrogen into helium"
    ]
   },
   {
    "code": "6.2.2",
    "title": "Stars",
    "points": [
     "State that: (a) galaxies are each made up of many billions of stars (b) the Sun is a star in the galaxy known as the Milky Way (c) other stars that make up the Milky Way are much further away from the Earth than the Sun is from the Earth (d) astronomical distances can be measured in light-years, where one light-year is the distance travelled in (the vacuum of) space by light in one year",
     "Know that one light-year is equal to 9.5 × 1015 m",
     "Describe the life cycle of a star: (a) a star is formed from interstellar clouds of gas and dust that contain hydrogen (b) a protostar is an interstellar cloud collapsing and increasing in temperature as a result of its internal gravitational attraction (c) a protostar becomes a stable star when the inward force of gravitational attraction is balanced by an outward force due to the high temperature in the centre of the star (d) all stars eventually run out of hydrogen as fuel for the nuclear reaction (e) most stars expand to form red giants and more massive stars expand to form red supergiants when most of the hydrogen in the centre of the star has been converted to helium (f) a red giant from a less massive star forms a planetary nebula with a white dwarf star at its centre (g) a red supergiant explodes as a supernova, forming a nebula containing hydrogen and new heavier elements, leaving behind a neutron star or a black hole at its centre (h) the nebula from a supernova may form new stars with orbiting planets"
    ]
   },
   {
    "code": "6.2.3",
    "title": "The Universe",
    "points": [
     "Know that the Milky Way is one of many billions of galaxies making up the Universe and that the diameter of the Milky Way is approximately 100 000 light-years",
     "Describe redshift as an increase in the observed wavelength of electromagnetic radiation emitted from receding stars and galaxies",
     "Know that the light emitted from distant galaxies appears redshifted in comparison with light emitted on the Earth",
     "Know that redshift in the light from distant galaxies is evidence that the Universe is expanding and supports the Big Bang Theory",
     "Know that microwave radiation of a specific frequency is observed at all points in space around us and is known as cosmic microwave background radiation (CMBR)",
     "Explain that the CMBR was produced shortly after the Universe was formed and that this radiation has been expanded into the microwave region of the electromagnetic spectrum as the Universe expanded",
     "Know that the speed v at which a galaxy is moving away from the Earth can be found from the change in wavelength of the galaxy’s starlight due to redshift",
     "Know that the distance d of a far galaxy can be determined using the brightness of a supernova in that galaxy",
     "Define the Hubble constant H0 as the ratio of the speed at which the galaxy is moving away from the Earth to its distance from the Earth; recall and use the equation H0 = v d 10 Know that the current estimate for H0 is"
    ]
   }
  ]
 }
}
