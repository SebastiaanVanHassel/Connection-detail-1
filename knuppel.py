
from math import sqrt
import streamlit as st

import Profiles

#Profiles library
all_attr_Profiles = dir(Profiles)
Profile_names = ()
for attribute in all_attr_Profiles:
    obj = getattr(Profiles, attribute)
    if isinstance(obj, Profiles.Profile):
        Profile_names += (obj.name,)
print(Profile_names)


# HEADER
st. set_page_config(layout="wide")
st.header('Knüppel Anschluss')

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("BEAM")   # INPUT BEAM
    # Profile
    col1b, col1l = st.columns(2)
    with col1b:
        beam_name = st.selectbox("Profile: ",Profile_names, 16)
    beam = getattr(Profiles, beam_name)

    # Length
    with col1l:
        L_beam = st.number_input("Length [m]: ", 1.00, 30.00, 8.00)

    st.subheader("KNÜPPEL")   # INPUT KNUPPEL
    F1 = st.number_input("Kraft F1: ", 1, 10000, 525)
    col1x, col1y = st.columns(2)
    with col1x:
        x = st.number_input("x [cm]: ", 1.00, 50.00, 12.25)
    with col1y:
        y = st.number_input("y [cm]: ", 1.00, 100.00, 34.75)
    l = x + y
    alpha = x/l
    beta = y/l
    with col1x:
        F2 = F1/beta;       st.write("Kraft F2 = " , round(F2,0), " kN")
    with col1y:
        F3 = F2*alpha;      st.write("Kraft F3 = " , round(F3,0), " kN")
    M_max = F3*y    #kNcm
    V_max = F1      #kN
    #Knuppel dimensions
    
    col1li, col1re = st.columns(2)
    with col1li:
        n = st.radio("Anzahl : ",(1, 2, 3, 4), horizontal=True)
        breite = st.slider("Breite [mm]: ", 10, 100, 50, 5)
        aufL = st.slider("Auflager breite links [mm]: ", 40, 120, 80, 10)
    with col1re:
        e_k = st.number_input("e [cm] = ", 1, 20, 8)
        hohe = st.slider("Höhe [mm]: ", 10, 300, 160, 5)
        aufR = st.slider("Auflager breite rechts [mm]: ", 40, 120, 80, 10)

    
#Nachweis Knuppel
with col2:
    st.subheader("NACHWEIS KNÜPPEL")
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
    col2kl, col2kr = st.columns(2)
    with col2kl:
        st.write("Nachweis Knuppel")
    with col2kr:
        if UC_knuppel < 1.00:
            st.success(str(round(UC_knuppel,2)) +'< 1.00')
        else:
            st.error(str(round(UC_knuppel,2)) +'> 1.00')

#--------------------------------------------#
#Welds
    st.subheader("NACHWEIS WELDS")
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
    col2w2a, col2w2u = st.columns(2)
    n_welds2 = n*4
    with col2w2a:
        a2 = st.selectbox("a (Weld 2)  [mm] = ",(3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 4)
    Fw2 = F2-Fweld_Rd1
    Fweld2 = Fw2/n_welds2
    Lweld2 = hohe               #mm
    Fw_Rd2 = Fweld2/Lweld2*10         #kN/cm
    Fweld_Rd2 = fvw*a2/10
    UC_weld2 = Fw_Rd2/Fweld_Rd2
    with col2w2u:
        st.write("Nachweis weld 2")
        if UC_weld2 < 1.00:
            st.success(str(round(UC_weld2,2)) + '  < 1.00')
        else:
            st.error(str(round(UC_weld2,2)) + '> 1.00')

    # --- #3 WELD --- #
    n_welds3 = n*2
    with col2w2a:
        a3 = st.selectbox("a (Weld 3)  [mm] = ",(3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 4)
    Fw3 = F3                    #kN
    Fweld3 = Fw3/n_welds3       #kN
    Lweld3 = aufR               #mm
    Fw_Rd3 = Fweld3/Lweld3*10         #kN/cm
    Fweld_Rd3 = fvw*a3/10
    UC_weld3 = Fw_Rd3/Fweld_Rd3
    with col2w2u:
        st.write("Nachweis weld 3")
        if UC_weld3 < 1.00:
            st.success(str(round(UC_weld3,2)) +'< 1.00')
        else:
            st.error(str(round(UC_weld3,2)) +'> 1.00')

    # --- #4 WELD --- #
    n_welds4 = 2
    with col2w2a:
        a4 = st.selectbox("a (Weld 4)  [mm] = ",(3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 2)
    Fw4 = F2                    #kN
    Fweld4 = Fw4/n_welds4       #kN
    Lweld4 = 360                #mm
    Fw_Rd4 = Fweld4/Lweld4*10         #kN/cm
    Fweld_Rd4 = fvw*a4/10
    UC_weld4 = Fw_Rd4/Fweld_Rd4
    with col2w2u:
        st.write("Nachweis weld 4")
        if UC_weld4 < 1.00:
            st.success(str(round(UC_weld4,2)) +'< 1.00')
        else:
            st.error(str(round(UC_weld4,2)) +'> 1.00')

    #Nachweis vertikales Blech
    fy_blech = 35.5     #kN/cm2
    with col2w2a:
        t = st.slider("t [cm] (Dicke Blech): ", 1.0, 5.0, 2.0, 0.5)
    b = beam.b
    with col2w2a:
        st.write("Breite Blech is Breite Träger =  ", beam.b)
    bnet = b - (n*breite)/10
    Fblech = F2 - Fweld_Rd1
    sigma_blech = Fblech/t/bnet     #kN/cm2
    UC_blech = sigma_blech/fy_blech
    with col2w2u:
        st.write("Nachweis vertikales blech", )
        if UC_blech < 1.00:
            st.success(str(round(UC_blech,2)) + '< 1.00')
        else:
            st.error(str(round(UC_blech,2)) + '> 1.00')


# Knuppelanschluss and Beam visualisation
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

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

#DIMENSIONS DRAWING
arrowx = FancyArrowPatch((aufL/20, hohe/10+5), (aufL/20+x, hohe/10+5), arrowstyle='<->', mutation_scale=10, shrinkA=0, shrinkB=0)
arrowy = FancyArrowPatch((aufL/20+x, hohe/10+5), (aufL/20+x+y, hohe/10+5), arrowstyle='<->', mutation_scale=10, shrinkA=0, shrinkB=0)

#CROSS_SECTION DRAWING
Lcs = beam.b/20 +5
#Knuppels
if n == 1:
    xknuppelcs = [-Lcs-breite/20,  -Lcs-breite/20,  -Lcs+breite/20,  -Lcs+breite/20, -Lcs-breite/20]
    yknuppelcs = [           0,  hohe/10,  hohe/10,             0,             0]
elif n == 2:
    xknuppelcs = [-Lcs-breite/20-e_k/2,  -Lcs-breite/20-e_k/2,  -Lcs+breite/20-e_k/2,  -Lcs+breite/20-e_k/2, -Lcs-breite/20+e_k/2, -Lcs-breite/20+e_k/2, -Lcs+breite/20+e_k/2, -Lcs+breite/20+e_k/2]
    yknuppelcs = [           0,  hohe/10,  hohe/10,             0,             0,  hohe/10, hohe/10, 0 ]
#Beam
x_topflangecs = [-Lcs-beam.b/20,  -Lcs-beam.b/20,  -Lcs+beam.b/20,  -Lcs+beam.b/20, -Lcs-beam.b/20]
y_topflangecs = [-0.5-beam.tf/10, -0.5, -0.5, -0.5-beam.tf/10, -0.5-beam.tf/10]
x_bottomflangecs = [-Lcs-beam.b/20,  -Lcs-beam.b/20,  -Lcs+beam.b/20,  -Lcs+beam.b/20, -Lcs-beam.b/20]
y_bottomflangecs = [-0.5-beam.h/10, -0.5-beam.h/10+beam.tf/10, -0.5-beam.h/10+beam.tf/10, -0.5-beam.h/10, -0.5-beam.h/10]
x_webcs = [-Lcs-beam.tw/20,  -Lcs-beam.tw/20,  -Lcs+beam.tw/20,  -Lcs+beam.tw/20, -Lcs-beam.tw/20]
y_webcs = [-0.5-beam.h/10+beam.tf/10, -0.5-beam.tf/10, -0.5-beam.tf/10, -0.5-beam.h/10+beam.tf/10, -0.5-beam.h/10+beam.tf/10]


# Create a new plot
fig, ax = plt.subplots()

# Plot the rectangle
ax.plot(x_topflange, y_topflange, color='blue')
ax.plot(x_bottomflange, y_bottomflange, color='blue')
ax.plot(xknuppel, yknuppel, color='red')
ax.plot(xblech, yblech, color='orange')
ax.plot(xaufL, yaufL, color='red')
ax.plot(xaufR, yaufR, color='red')
ax.add_patch(arrowx)
ax.add_patch(arrowy)
plt.text(aufL/20+x/2, hohe/10+6, "x")
plt.text(aufL/20+x+y/2, hohe/10+6, "y")
ax.plot(xknuppelcs, yknuppelcs, color='red')
ax.plot(x_topflangecs, y_topflangecs, color='blue')
ax.plot(x_bottomflangecs, y_bottomflangecs, color='blue')
ax.plot(x_webcs, y_webcs, color='blue')

# Set the x and y limits of the plot
ax.set_xlim([-x/10-2*beam.b/10-10, 100])
ax.set_ylim([-beam.h/10-10, hohe/10+10])

with col3:
    st.pyplot(fig)

    col31, col32 = st.columns(2)
    with col31:
        st.write("KNÜPPEL:")
        st.write("Breite = ", n, " x ", breite, "mm")
        st.write("Höhe = ", hohe, "mm")
        st.write("x = ", x, "cm")
        st.write("y = ", y, "cm")
        st.write("WELDS:")
        st.write("a1 = ", a1, "mm")
        st.write("a2 = ", a2, "mm")
        st.write("a3 = ", a3, "mm")
        st.write("a4 = ", a4, "mm")
    
    with col32:
        st.write("Kraft F1 = ", F1, "kN")
        st.write("Max. Moment = ", round(M_max,0), "kNcm")
        st.write("Max. Shear Force = ", V_max, "kN")

        st. write("BEAM:")
        st.write(beam.name)
        st.write("Height           h  [mm]  = ", beam.h)
        st.write("Width            b  [mm]  = ", beam.b)
        st.write("Web thickness    tw [mm]  = ", beam.tw)
        st.write("Flange thickness tf [mm]  = ", beam.tf)
        st.write("Sectional area   A  [cm2] = ", beam.A)


#convert the drawing into 2D drawing propmt commands for BricsCAD
#xknuppel
#yknuppel
