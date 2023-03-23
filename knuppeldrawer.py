from math import sqrt
import streamlit as st
import matplotlib.pyplot as plt


# -------------------------------------------------- #
st. set_page_config(layout="wide")
st.header("Knüppel drawer")

import Profiles
#Profiles library
all_attr_Profiles = dir(Profiles)
Profile_names = ()
for attribute in all_attr_Profiles:
    obj = getattr(Profiles, attribute)
    if isinstance(obj, Profiles.Profile):
        Profile_names += (obj.name,)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Beam")   # INPUT BEAM
    beam_name = st.selectbox("Profile:",Profile_names, 16)
    # col11, col12, col13, col14, col15 = st.columns(5)
    beam = getattr(Profiles, beam_name)

    st.subheader("KNÜPPEL")   # INPUT KNUPPEL
    F1 = st.number_input("Kraft F1: ", 1, 10000, 525)
    col1x, col1y = st.columns(2)
    with col1x:
        x = st.number_input("x [mm]: ", 10.0, 500.0, 122.5, 0.50)
    with col1y:
        y = st.number_input("y [mm]: ", 10.0, 1000.0, 347.5, 0.50)
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
        n = st.radio("Anzahl : ",(1, 2), horizontal=True)
        b = st.number_input("Breite [mm]: ", 10, 100, 50, 5)
        aufL = st.number_input("Auflager breite links [mm]: ", 40, 120, 80, 10)
    with col1re:
        if n > 1:
            e_k = st.number_input("e [mm]: ", 10, 200, 120+b, 5)
        else:
            e_k = 0
        h = st.number_input("Höhe [mm]: ", 10, 300, 160, 5)
        aufR = st.number_input("Auflager breite rechts [mm]: ", 40, 120, 80, 10)

    voff = st.number_input("Vertical Offset [mm]: ",  5, 200, 30, 5)
    hoff = st.number_input("Horizontal Offset [mm]: ",  5, 200, 30, 5)
    ktol = st.number_input("Knüppel tolerance [mm]: ",  1, 25, 5, 1)
    btol = st.number_input("Beam tolerance [mm]: ",  0, 50, 15, 5)

    t = st.number_input("Thickness vertical plate [mm]: ",  5, 50, 20, 5)

    hanger = st.radio("Include lifting eye: ",("no", "yes"), horizontal=True)
    if hanger == "yes":
        radius = st.number_input("radius of curve knuppel: ", 10, 300, 60, 10)
        r_eye = st.number_input("radius of eye: ", 5, 100, 19, 1)
    
    language = st.radio("Language: ",("English", "Deutsch"), horizontal=True)

#points of Knuppel
p1 = (0, 0)
p2 = (0, ktol+voff)
p3 = (aufL/2+x-t/2-hoff, ktol+h)
if hanger == "no":
    p4 = (p3[0]+2*hoff+t, ktol+h)
    p5 = (x+y+aufL/2+aufR/2 , ktol+voff)
else:
    p4 = (p3[0]+hoff+t/2+y+aufR/2-radius, ktol+h)
    p5 = (x+y+aufL/2+aufR/2 , ktol+h-radius)
p6 = (x+y+aufL/2+aufR/2 , 0)
p7 = (x+y+aufL/2-aufR/2 , 0)
p8 = (x+y+aufL/2-aufR/2 , ktol)
p9 = (aufL, ktol)
p10 = (aufL, 0)
knuppelpoints = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p1]
xcoordskn, ycoordskn = zip(*knuppelpoints)

# points of plate
pp1 = (aufL/2+x-t/2, ktol+h)
pp2 = (aufL/2+x+t/2, ktol+h)
pp3 = (aufL/2+x+t/2, -beam.h+beam.tf/2)
pp4 = (aufL/2+x-t/2, -beam.h+beam.tf/2)
platepoints = [pp1, pp2, pp3, pp4, pp1]
xcoordspl, ycoordspl = zip(*platepoints)

# points of cross-section knuppel plate
pc1 = (-beam.b-beam.b, ktol+voff)
pc2 = (-beam.b-beam.b/2-e_k/2-b/2-hoff, ktol+h)
pc3 = (-beam.b-beam.b/2+e_k/2+b/2+hoff, ktol+h)
pc4 = (-beam.b, ktol+voff)
pc5 = (-beam.b, -beam.h+beam.tf/2)
pc6 = (-beam.b-beam.b, -beam.h+beam.tf/2)
crosssectionplatepoints = [pc1, pc2, pc3, pc4, pc5, pc6, pc1]
xcoordspc, ycoordspc = zip(*crosssectionplatepoints)

# Beam Cross-Section
x_topflangecs = [-beam.b-beam.b,  -beam.b-beam.b,  -beam.b,  -beam.b, -beam.b-beam.b]
y_topflangecs = [-beam.tf, 0, 0, -beam.tf, -beam.tf]
x_bottomflangecs = [-beam.b-beam.b,  -beam.b-beam.b,  -beam.b,  -beam.b, -beam.b-beam.b]
y_bottomflangecs = [-beam.h, -beam.h+beam.tf, -beam.h+beam.tf, -beam.h, -beam.h]
x_webcs = [-beam.b-beam.b/2-beam.tw/2,  -beam.b-beam.b/2-beam.tw/2,  -beam.b-beam.b/2+beam.tw/2,  -beam.b-beam.b/2+beam.tw/2, -beam.b-beam.b/2-beam.tw/2]
y_webcs = [-beam.h+beam.tf, -beam.tf, -beam.tf, -beam.h+beam.tf, -beam.h+beam.tf]

#Knuppel cross-section
if n == 1:
    xknuppelcs = [-beam.b-beam.b/2-b/2,  -beam.b-beam.b/2-b/2,  -beam.b-beam.b/2+b/2,  -beam.b-beam.b/2+b/2, -beam.b-beam.b/2-b/2]
    yknuppelcs = [           0,  ktol+h,  ktol+h,             0,             0]
elif n == 2:
    xknuppelcs = [-beam.b-beam.b/2-e_k/2-b/2,  -beam.b-beam.b/2-e_k/2-b/2,  -beam.b-beam.b/2-e_k/2+b/2,  -beam.b-beam.b/2-e_k/2+b/2, -beam.b-beam.b/2+e_k/2-b/2, -beam.b-beam.b/2+e_k/2-b/2, -beam.b-beam.b/2+e_k/2+b/2, -beam.b-beam.b/2+e_k/2+b/2]
    yknuppelcs = [           0,  ktol+h,  ktol+h,             0,             0,  ktol+h, ktol+h, 0 ]


#plot in web app
fig, ax = plt.subplots()
ax.scatter(xcoordskn, ycoordskn, s=10, color='black')
ax.plot(xcoordskn, ycoordskn, color='blue')
ax.plot(xcoordspl, ycoordspl, color='purple')
ax.plot(xcoordspc, ycoordspc, color='purple')
ax.plot(x_topflangecs, y_topflangecs, color='black')
ax.plot(x_bottomflangecs, y_bottomflangecs, color='black')
ax.plot(x_webcs, y_webcs, color='black')
ax.plot(xknuppelcs, yknuppelcs, color='blue')
ax.set_aspect('equal')
with col2:
    st.pyplot(fig)


# --- BricsCAD prompt generator --- #
def draw_element(x_coords, y_coords):
    assert len(x_coords) == len(y_coords), "Error: x and y coordinate arrays must have the same length"
    n = len(x_coords)
    commands = ["L"] 
    for i in range(n):
        x, y = x_coords[i], y_coords[i]
        commands.append(f"{x},{y}")
    commands.append("\n")
    return "\n".join(commands)

st.subheader("BricsCAD prompt generator!")
knuppel2D = draw_element(xcoordskn, ycoordskn)
plate2D   = draw_element(xcoordspl, ycoordspl)
csplate2D = draw_element(xcoordspc, ycoordspc)
cstopflange = draw_element(x_topflangecs, y_topflangecs)
csbottomflange = draw_element(x_bottomflangecs, y_bottomflangecs)
csweb = draw_element(x_webcs, y_webcs)
csknuppel = draw_element(xknuppelcs, yknuppelcs)

if language == "English":
    circle = "C"
    arc = "A"
    center = "C"
else:
    circle = "K"
    arc = "B"
    center = "Z"
# lifting eye
if hanger == "yes":
    arcs = []
    arcs.append(f"{circle}")
    arcs.append(f"{p4[0]},{p5[1]}")
    arcs.append(f"{r_eye}")

    arcs.append(f"{arc}")
    arcs.append(f"{center}")
    arcs.append(f"{p4[0]},{p5[1]}")
    arcs.append(f"{p4[0]},{p4[1]}")
    arcs.append(f"{p5[0]},{p5[1]}")
    arcs.append("\n")
    
    arcs = "\n".join(arcs)
else:
    arcs = "\n"

st.text_area(":)",  knuppel2D + plate2D + csplate2D + cstopflange + csbottomflange + csweb + csknuppel + arcs + "U\n", height=1000)
