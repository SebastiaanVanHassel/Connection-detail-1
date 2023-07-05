import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import ProfilesHILTI
#Profiles library
all_attr_Profiles = dir(ProfilesHILTI)
Profile_names = ()
for attribute in all_attr_Profiles:
    obj = getattr(ProfilesHILTI, attribute)
    if isinstance(obj, ProfilesHILTI.Profile):
        Profile_names += (obj.name,)

anchorD = [["M8", "M10", "M12"], [13.8, 23.6, 35.4]]

st. set_page_config(layout="wide")

# Create a layout with three columns
left_column, middle_column, right_column = st.columns([1.5, 3, 1.5])

# Left column
with left_column:
    st.selectbox("Shear Force V:",["100 kN"], 0)
    
    st.checkbox("Cracked concrete", True)
    st.selectbox("Concrete Class:",["C20/25"], 0)
    st.selectbox("Concrete wall thickness:",["200 mm"], 0)
 
    st.selectbox("Steel plate: ", ["260x260x10"], 0)
    st.checkbox("Rigid Baseplate", True)

    beam_name = st.selectbox("Steel Profile: ",Profile_names, 0)
    steel_profile = getattr(ProfilesHILTI, beam_name)

    
    st.selectbox("Anchor:", ["HST3"],0)
    D = st.selectbox("Bolt diameter:", anchorD[0])
    st.selectbox("Effective Embedment Depth of Anchor Bolt:", ["80 mm"], 0)

    VRk = anchorD[1][anchorD[0].index(D)]
    
    st.write("Characteristic Shear Resistance per Anchor Bolt = ", anchorD[1][anchorD[0].index(D)], "kN")
    st.latex("V_{Rd} = V_{Rk} / \gamma_{MS} ")
    st.latex("\gamma_{MS} = 1.25")
    st.write("Design Shear Resistance per Anchor Bolt = ", round(anchorD[1][anchorD[0].index(D)] / 1.25, 1), "kN")

    


with middle_column:
    st.title('HILTI Anchor Design')
    d = 10
    fig, ax = plt.subplots()

    rI = plt.Rectangle((-100, -250), 100, 500, edgecolor='grey', facecolor='none')
    ax.add_patch(rI)
    rA = plt.Rectangle((0, -130), 10, 260, edgecolor='b', facecolor='none')
    ax.add_patch(rA)
    rB = plt.Rectangle((-80, -90-0.5*d), 80, d, edgecolor='r', facecolor='none')
    ax.add_patch(rB)
    rC = plt.Rectangle((-80, +90-0.5*d), 80, d, edgecolor='r', facecolor='none')
    ax.add_patch(rC)
    rD = plt.Rectangle((10, -90-d), 8, 2*d, edgecolor='r', facecolor='none')
    ax.add_patch(rD)
    rE = plt.Rectangle((10, +90-d), 8, 2*d, edgecolor='r', facecolor='none')
    ax.add_patch(rE)
    rF = plt.Rectangle((10, -66.5), 140, steel_profile.tf, edgecolor='black', facecolor='none')
    ax.add_patch(rF)
    rG = plt.Rectangle((10, -66.5+steel_profile.tf), 140, steel_profile.h-2*steel_profile.tf, edgecolor='black', facecolor='none')
    ax.add_patch(rG)
    rH = plt.Rectangle((10, +66.5-steel_profile.tf), 140, steel_profile.tf, edgecolor='black', facecolor='none')
    ax.add_patch(rH)

    rJ = plt.Rectangle((300, -130), 260, 260, edgecolor='b', facecolor='none')
    ax.add_patch(rJ)
    rK = plt.Rectangle((360, -66.5), 140, steel_profile.tf, edgecolor='black', facecolor='none')
    ax.add_patch(rK)
    rL = plt.Rectangle((427.25, -66.5+steel_profile.tf), steel_profile.tw, steel_profile.h-2*steel_profile.tf, edgecolor='black', facecolor='none')
    ax.add_patch(rL)
    rM = plt.Rectangle((360, +66.5-steel_profile.tf), 140, steel_profile.tf, edgecolor='black', facecolor='none')
    ax.add_patch(rM)
    rN = plt.Circle((340, -90), 12, edgecolor='r', facecolor='none')
    ax.add_patch(rN)
    rO = plt.Circle((340, 90), 12, edgecolor='r', facecolor='none')
    ax.add_patch(rO)
    rP = plt.Circle((520, 90), 12, edgecolor='r', facecolor='none')
    ax.add_patch(rP)
    rQ = plt.Circle((520, -90), 12, edgecolor='r', facecolor='none')
    ax.add_patch(rQ)


    ax.autoscale()
    # Remove tick labels
    plt.xticks([])
    plt.yticks([])
    st.pyplot(fig)


    st.markdown("""---""")
    if D == "M8":
        st.error("The anchor is not able to resist the shear loads.", icon="🚨")
        st.info('To improve steel resistance, please consider: Increasing the bolt diameter.', icon="⚠️")

    elif D == "M10":
        st.error("The anchor is not able to resist the shear loads.", icon="🚨")
        st.info('To improve steel resistance, please consider: Increasing the bolt diameter.', icon="⚠️")

    elif D == "M12":
        st.success("The anchor is designed well. The steel is able to resist the shear loads.", icon="✅")
        st.markdown("_Now you have access to the resume of Sebastiaan van Hassel, download here:_ ")
        with open("CV_SJF_van_Hassel.pdf", "rb") as file:
            cv = st.download_button(
            label="Download",
            data=file,
            file_name="CV_SJF_van_Hassel.pdf", 
        )


with right_column:
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    df = pd.DataFrame({'Bolt nr.':[1, 2, 3, 4], 'V (kN)':[25, 25, 25, 25], 'N (kN)':[0, 0, 0, 0]})
    st.table(df)
    
    st.subheader("Shear")
    st.write("Steel:")
    if D == "M8":
        st.error("227%")
        st.info('The steel is not yet able to resist the shear loads. To improve steel resistance, please consider: Increasing the bolt diameter.', icon="⚠️")

    elif D == "M10":
        st.error("133%")
        st.info('The steel is not yet able to resist the shear loads. To improve steel resistance, please consider: Increasing the bolt diameter.', icon="⚠️")

    elif D == "M12":
        st.success("89%")


    st.subheader("Tension")
    st.write("Steel:")
    st.success("0%")


