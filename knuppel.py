
from math import sqrt
import streamlit as st

import Profiles

st.title('Knüppel Anschluss')

all_attr_Profiles = dir(Profiles)
Profile_names = ()
for attribute in all_attr_Profiles:
    obj = getattr(Profiles, attribute)
    if isinstance(obj, Profiles.Profile):
        Profile_names += (obj.name,)
print(Profile_names)

beam_name = st.selectbox("Profile Beam : ",Profile_names, 16)
beam = getattr(Profiles, beam_name)
beam.h = beam.h
st.write("Profile  = ", beam.name)
st.write("Height           h  [mm]  = ", beam.h)
st.write("Width            b  [mm]  = ", beam.b)
st.write("Web thickness    tw [mm]  = ", beam.tw)
st.write("Flange thickness tf [mm]  = ", beam.tf)
st.write("Sectional area   A  [cm2] = ", beam.A)

L_beam = st.number_input("Length of the beam [m]: ", 1.00, 30.00, 8.00)

F1 = st.number_input("Kraft F1: ", 1, 10000, 525)
#F1 = 525    #kN

x = st.number_input("x [cm]: ", 1.00, 50.00, 12.25)
y = st.number_input("y [cm]: ", 1.00, 100.00, 34.75)
l = x + y
alpha = x/l
beta = y/l

F2 = F1/beta
st.write("Kraft F2 = " , round(F2,0), " kN")
F3 = F2*alpha
st.write("Kraft F3 = " , round(F3,0), " kN")

M_max = F3*y    #kNcm
V_max = F1      #kN

#Knuppel dimensions
n = st.selectbox("Anzahl : ",(1, 2, 3, 4))
breite = st.slider("Breite [cm]: ", 10, 100, 50, 5)
hohe = st.slider("Höhe [cm]: ", 10, 300, 160, 5)
aufL = st.slider("Auflager breite links [cm]: ", 40, 120, 80, 10)
aufR = st.slider("Auflager breite rechts [cm]: ", 40, 120, 80, 10)

#--------------------------------------------#
#Nachweis Knuppel
stahl_knuppel = st.selectbox("Stahl gute Knüppel : ",("S235", "S275", "S355", "S460"), 3)
if (stahl_knuppel == "S460") and (breite > 40):
    fy_knuppel = 41                 #kN/cm2
else:
    fy_knuppel = 44
st.write("fy knuppel = ", fy_knuppel)
W_pl =(n*breite*pow(hohe,2))/4/1000  #cm3
sigma_pl = M_max/W_pl

tau_pl = V_max/(n*breite*hohe)*100  #kN/cm2

vonMises = sqrt(pow(sigma_pl,2) + 3*pow(tau_pl,2))

UC_knuppel = vonMises/fy_knuppel
st.write("Nachweis Knuppel = ", round(UC_knuppel,2))
#--------------------------------------------#

#--------------------------------------------#
#Welds
fu_welds = 49       #kN/cm2
yM2 = 1.25
beta_w = 0.9
fvw = fu_welds/(sqrt(3)*beta_w*1.25)

# --- #1 WELD --- #
a1 = st.selectbox("a (Weld 1)  [mm] = ",(3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 4)
Fw_Rd1 = fvw*a1/10       #kN/cm
Lweld1 = breite/10      #cm
Fweld_Rd1 = Fw_Rd1*Lweld1

# --- #2 WELD --- #
n_welds2 = n*4
a2 = st.selectbox("a (Weld 2)  [mm] = ",(3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 4)
Fw2 = F2-Fweld_Rd1
Fweld2 = Fw2/n_welds2
Lweld2 = hohe               #mm
Fw_Rd2 = Fweld2/Lweld2*10         #kN/cm
Fweld_Rd2 = fvw*a2/10
UC_weld2 = Fw_Rd2/Fweld_Rd2
st.write("Nachweis weld 2 = ", round(UC_weld2,2))

# --- #3 WELD --- #
n_welds3 = n*2
a3 = st.selectbox("a (Weld 3)  [mm] = ",(3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 4)
Fw3 = F3                    #kN
Fweld3 = Fw3/n_welds3       #kN
Lweld3 = aufR               #mm
Fw_Rd3 = Fweld3/Lweld3*10         #kN/cm
Fweld_Rd3 = fvw*a3/10
UC_weld3 = Fw_Rd3/Fweld_Rd3
st.write("Nachweis weld 3 = ", round(UC_weld3,2))

# --- #4 WELD --- #
n_welds4 = 2
a4 = st.selectbox("a (Weld 4)  [mm] = ",(3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 2)
Fw4 = F2                    #kN
Fweld4 = Fw4/n_welds4       #kN
Lweld4 = 360                #mm
Fw_Rd4 = Fweld4/Lweld4*10         #kN/cm
Fweld_Rd4 = fvw*a4/10
UC_weld4 = Fw_Rd4/Fweld_Rd4
st.write("Nachweis weld 4 = ", round(UC_weld4,2))

#Nachweis vertikales Blech
fy_blech = 35.5     #kN/cm2
t = st.slider("t [cm] (Dicke Blech): ", 1.0, 5.0, 2.0, 0.5)
b = st.number_input("b [cm] (Breite Blech): ", 1.0, 100.0, 30.5)
bnet = b - (n*breite)/10
Fblech = F2 - Fweld_Rd1
sigma_blech = Fblech/t/bnet     #kN/cm2
UC_blech = sigma_blech/fy_blech
st.write("Nachweis vertikales blech = ", round(UC_blech,2))



import matplotlib.pyplot as plt

#KNUPPEL DRAWING
# Define the coordinates in cm!
xknuppel = [           0,        0,  x+y+aufL/20+aufR/20,  x+y+aufL/20+aufR/20, 0]
yknuppel = [           0,  hohe/10,  hohe/10,             0,             0]
xblech =   [       x-t/2+aufL/20,    x-t/2+aufL/20,    x+t/2+aufL/20,         x+t/2+aufL/20,         x-t/2+aufL/20]
yblech =   [-beam.h/10-0.5+beam.tf/20,  hohe/10,  hohe/10,  -beam.h/10-0.5+beam.tf/20,  -beam.h/10-0.5+beam.tf/20]
xaufL =    [0,  aufL/10,  aufL/10,     0,  0]
yaufL =    [0,        0,     -0.5,  -0.5,  0]
xaufR =    [x+y+aufL/20-aufR/20, x+y+aufL/20+aufR/20,  x+y+aufL/20+aufR/20,     x+y+aufL/20-aufR/20,  x+y+aufL/20-aufR/20]
yaufR =    [0,        0,     -0.5,  -0.5,  0]

#BEAM DRAWING
x_topflange = [aufL/20+x+t/2, aufL/20+x+t/2, aufL/20+x+t/2+L_beam*100, aufL/20+x+t/2+L_beam*100, aufL/20+x+t/2]
y_topflange = [-0.5-beam.tf/10, -0.5, -0.5, -0.5-beam.tf/10, -0.5-beam.tf/10]
x_bottomflange = [aufL/20+x+t/2, aufL/20+x+t/2, aufL/20+x+t/2+L_beam*100, aufL/20+x+t/2+L_beam*100, aufL/20+x+t/2]
y_bottomflange = [-0.5-beam.h/10, -0.5-beam.h/10+beam.tf/10, -0.5-beam.h/10+beam.tf/10, -0.5-beam.h/10, -0.5-beam.h/10]


# Create a new plot
fig, ax = plt.subplots()

# Plot the rectangle
ax.plot(xknuppel, yknuppel)
ax.plot(xblech, yblech)
ax.plot(xaufL, yaufL)
ax.plot(xaufR, yaufR)
ax.plot(x_topflange, y_topflange)
ax.plot(x_bottomflange, y_bottomflange)

# Set the x and y limits of the plot
ax.set_xlim([-x/10-10, 100])
ax.set_ylim([-beam.h/10-10, hohe/10+10])

with st.sidebar:
    st.pyplot(fig)