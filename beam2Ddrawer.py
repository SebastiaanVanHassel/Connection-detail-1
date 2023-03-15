from math import sqrt
import streamlit as st
import matplotlib.pyplot as plt

import Profiles

#Profiles library
all_attr_Profiles = dir(Profiles)
Profile_names = ()
for attribute in all_attr_Profiles:
    obj = getattr(Profiles, attribute)
    if isinstance(obj, Profiles.Profile):
        Profile_names += (obj.name,)

# -------------------------------------------------- #
st. set_page_config(layout="wide")
st.header("Beam 2D drawer")

col1, col2 = st.columns(2)
with col1:
    sectiontype = st.radio("Section:",('Standard Rolled', 'Welded'))

    col11, col12, col13, col14, col15 = st.columns(5)
    if sectiontype == 'Standard Rolled':
        beam_name = st.selectbox("",Profile_names, 16)
        beam = getattr(Profiles, beam_name)
        with col11:
            st.write("Height \n [mm]: \n", beam.h)
        with col12:
            st.write("Width Top Flange  [mm]: ", beam.b)
            st.write("Thickness Top Flange [mm]: ", beam.tf)
        with col13:
            st.write("Web thickness  [mm]: ", beam.tw)
        with col14:
            st.write("Width Bottom Flange  [mm]: ", beam.b)
            st.write("Thickness Bottom Flange [mm]: ", beam.tf)
        with col15:
            st.write("Weld Radius [mm]: ", beam.r)
    else:
        with col11:
            h = st.number_input("Height [mm]: ", 1, 3000, 400)
        with col12:
            btf = st.number_input("Width Top Flange  [mm]: ", 1, 800, 300)
            ttf = st.number_input("Thickness Top Flange [mm]: ", 1, 100, 20)
        with col13:
            tw = st.number_input("Web thickness  [mm]: ", 1, 100, 10)
        with col14:
            bbf = st.number_input("Width Bottom Flange  [mm]: ", 1, 800, 300)
            tbf = st.number_input("Thickness Bottom Flange [mm]: ", 1, 100, 20)
        with col15:
            r = st.number_input("Weld Radius [mm]: ", 1, 100, 10)
    
    L_beam = st.number_input("Length [m]: ", 1.00, 30.00, 8.00)

with col2:
    if sectiontype == 'Standard Rolled':
        x_topflangecs = [-beam.b/2,  -beam.b/2,  beam.b/2,  beam.b/2, -beam.b/2]
        y_topflangecs = [-beam.tf, 0, 0, -beam.tf, -beam.tf]
        x_bottomflangecs = [-beam.b/2,  -beam.b/2,  beam.b/2,  beam.b/2, -beam.b/2]
        y_bottomflangecs = [-beam.h, -beam.h+beam.tf, -beam.h+beam.tf, -beam.h, -beam.h]
        x_webcs = [-beam.tw/2,  -beam.tw/2,  +beam.tw/2,  +beam.tw/2, -beam.tw/2]
        y_webcs = [-beam.h+beam.tf, -beam.tf, -beam.tf, -beam.h+beam.tf, -beam.h+beam.tf]
        # Create a new plot
        fig, ax = plt.subplots()
        # Plot the rectangle
        ax.plot(x_topflangecs, y_topflangecs, color='blue')
        ax.plot(x_bottomflangecs, y_bottomflangecs, color='blue')
        ax.plot(x_webcs, y_webcs, color='lightblue')
        # Set the x and y limits of the plot
        ax.set_xlim([-beam.b, beam.b])
        ax.set_ylim([-beam.h-15, 15])
        st.pyplot(fig)

        #side view 
        x_topflange = [beam.b,  beam.b,  beam.b+L_beam,  beam.b+L_beam, beam.b]
        y_topflange = [-beam.tf, 0, 0, -beam.tf, -beam.tf]
        x_bottomflange = [beam.b,  beam.b,  beam.b+L_beam,  beam.b+L_beam, beam.b]
        y_bottomflange = [-beam.h, -beam.h+beam.tf, -beam.h+beam.tf, -beam.h, -beam.h]
        x_web = [beam.b,  beam.b,  beam.b+L_beam,  beam.b+L_beam, beam.b]
        y_web = [-beam.h+beam.tf, -beam.tf, -beam.tf, -beam.h+beam.tf, -beam.h+beam.tf]
    else:
        st.write("welded section, image to be continued")
    

st.subheader("BricsCAD prompt generator!")
def draw_rec(x_coords, y_coords):
    assert len(x_coords) == len(y_coords), "Error: x and y coordinate arrays must have the same length"
    n = len(x_coords)

    commands = ["L"]  # start the line command
    for i in range(n):
        # add the current point to the list of commands
        x, y = x_coords[i], y_coords[i]
        commands.append(f"{x},{y}")

    # return the list of commands as a single string separated by newlines
    return "  \n  ".join(commands)

topflangecs = draw_rec(x_topflangecs, y_topflangecs)
st.write(topflangecs)
bottomflangecs = draw_rec(x_bottomflangecs, y_bottomflangecs)
st.write(bottomflangecs)
webcs = draw_rec(x_webcs, y_webcs)
st.write(webcs)
topflange = draw_rec(x_topflange, y_topflange)
st.write(topflange)
bottomflange = draw_rec(x_bottomflange, y_bottomflange)
st.write(bottomflange)
web = draw_rec(x_web, y_web)
st.write(web)