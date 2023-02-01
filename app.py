import streamlit as st  # pip install streamlit
import pandas as pd
import calendar  # Core Python Module
import plotly.graph_objects as go  # pip install plotly

import io
from datetime import datetime  # Core Python Module

import folium
from streamlit_folium import st_folium
import geopy
from geopy.geocoders import Nominatim



from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from streamlit_extras.app_logo import add_logo

from st_aggrid import AgGrid, GridUpdateMode, JsCode, ColumnsAutoSizeMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


# --- DATABASE --- #
@st.cache
def load_data():
    df = pd.read_csv("CSV_samples/meesterlys.csv")
    return df


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


def get_pos(lat,lng):
    return lat,lng

def get_latitude(x):
  return x.latitude

def get_longitude(x):
  return x.longitude

def center():
   address = 'South Africa'
   geolocator = Nominatim(user_agent="id_explorer")
   location = geolocator.geocode(address)
   latitude = location.latitude
   longitude = location.longitude
   return latitude, longitude



icondict = { # https://fontawesome.com/search?q=place&o=r
    # category : icon
    "Area": ["ring", "darkgreen"],
    "Baai": ["umbrella-beach", "orange"],
    "Distrik": ["draw-polygon", "lightgreen"],
    "Gebied": ["map", "darkblue"],
    "Gebied-Dorp": ["building-columns", "cadetblue"],
    "Sendingplek": ["church", "blue"],
    "Gebied-Nywerheid": ["industry", "lightblue"],
    "Gebied-Stedelik": ["tree-city", "pink"],
    "Gedeelte": ["monument", "lightred"],
    "Nedersetting": ["house", "darkpurple"],
    "Plek": ["map-pin", "beige"],
    "Stad": ["city", "red"],
    "Streek": ["landmark", "darkred"],
    "Township": ["house-chimney", "purple"],
    "Voorstad": ["house-flag", "green"],
    "XXX-Eiland": ["earth-oceania", "COL"]
}


# -------------- SETTINGS --------------
page_title = "SA Pleknaamlys"
page_icon = ":earth_africa:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "wide"

incomes = ["Salary", "Blog", "Other Income"]
expenses = ["Rent", "Utilities", "Groceries", "Car", "Other Expenses", "Saving"]
currency = "USD"


txt_whatis = "'n Pleknaamlys dien as 'n sinchroniese woordeboek van plekname wat die amptelik goedgekeurde name binne 'n bepaalde geografiese streek lys."

# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title)

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])


# --- DATABASE INTERFACE ---
def get_all_periods():
    items = []
    periods = [item["key"] for item in items]
    return periods


# --- HIDE STREAMLIT STYLE ---



# --- THEME --- #
#primaryColor="#F63366"
#backgroundColor="#FFFFFF"
#secondaryBackgroundColor="#F0F2F6"
#textColor="#262730"
#font="sans serif"

# --- SIDEBAR ---
add_logo("https://www.taalkommissie.co.za/wp-content/uploads/2022/03/cropped-TK-logo-rooi.jpg")


# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Projek Beskrywing", "Besigtig Lys", "Wysig Lys"],
    icons=["chat-left-quote", "bi bi-clipboard-data", "bi bi-pencil-square"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- TAB: PROJEK BESKRYWING ---
if selected == "Projek Beskrywing":
    st.write("")
    with st.container():
        

        col1, col2 = st.columns([2, 1])
        col2.image("https://upload.wikimedia.org/wikipedia/commons/d/d1/SouthAfricaOMC.png", caption="Wikipedia illustrasie van SA plekname", use_column_width=True)
        
        col1.subheader("Wat is die SA Pleknaamlys?")
        col1.write("'n Pleknaamlys dien as 'n sinchroniese lys van alle amptelik goedgekeurde plekname binne 'n bepaalde geografiese streek.")
        col1.write("")
        col1.write("Die Suid-Afrikaanse pleknaamlys is 'n projek wat deur die Afrikaanse Taalkommissie gestig is om 'n deurlopende en lewende pleknamelys te bewerkstellig wat alle naamsveranderinge binne Suid-Afrika terstond vasvang en kan dien as 'n historiese rekening van wysigings uit die jare.")

        "---"
        with st.expander("Pleknaamlys as 'n gemeenskapsprojek"):
            st.write("Die doel van die projek is ‘n samevattende en lys van geografiese plekname te bewerkstellig wat deur die Afrikaanse gemeenskap onderhou word.")
            st.write("Sedert die afsterwing van die nasionale Pleknaamkomitee word pleknaamwysigings nie sistematiese teenoor die historiese name van boekgehou nie, nog minder is daar ŉ voortdurende, byderwetse bron vir plekname wat deur die publiek geraadpleeg kan word nie.")
            st.write("Ter standaardisering sou daar ‘n pleknaamwoordeboek periodies vrygestel word, maar deur middel van die internet kan sulke woordeboeke deur ‘n aanlyn databasis vervang word wat voortdurend onderhou kan word om wysigings spoedig aan te bring en onmiddellik vir die publiek beskikbaar te hou.")
        with st.expander("Wat bevat die pleknaamlys?"):
            st.write("Elke pleknaam word omskryf deur die volgende attribute:")
            st.markdown("- Huidige Pleknaam")
            st.markdown("- Moontlike wisselvorme")
            st.markdown("- Kategorie (die tipe plek waarna verwys word, e.g. Dorp, Stad, Nedersetting).")
            st.markdown("- Historiese plekname (voormalige plekname met ŉ jaar datum tot met sy wysiging)")
            st.markdown("- Google Maps skakel (GPS koördinaat van die plek)")

        with st.expander("Voortbou van die lys deur gebruikers"):
            st.write("Ons nooi graag die publiek uit om die lys te help uitbrei en onderhou.")
            st.write("Alle wysigings wat deur die gemeenskap voorgestel word kan besigtig word deur om die “Vertoon gemeenskapswysigings voorstelle”. Elke voorstel kan teen of ten gunste gestem word en sal op ŉ periodes skedule deur die TK nagegaan word vir goedkeuring en bywerking tot die meesterlys.")

        "---"
        



# --- TAB: BESIGTIG LYS ---
if selected == "Besigtig Lys":
    col1, col2 = st.columns([2, 1])
    col1.subheader("Stand van lys")

    
    col1.markdown("Die pleknaamlys word deurlopend aangepas en bygewerk met behulp van wysigingsvoorstelle uit die gebruikersgemeenskap.")
    col1.markdown("Jy kan voorstelle in dien deur om die " + "_Wysig Lys_" + " blad te besoek.")
    col2.info("Laaste bywerking is op: " + "DATUM" )
    df = load_data()
    #dftmp = df.loc[:, ~df.columns.isin(['latitude', 'longitude'])]  # hide long and lat cols


    
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_pagination(paginationAutoPageSize=True)
    gd.configure_side_bar(columns_panel=False) #Add a sidebar
    gd.configure_default_column(editable=True, groupable=True)
    gd.configure_selection('multiple', use_checkbox=True)
    gridOptions = gd.build()

    # diplay dataframe in AgGrid
    grid_return = AgGrid(df,
           gridOptions=gridOptions, 
           editable=True,
           height=450,
           width='100%',
           allow_unsafe_jscode=True,
           data_return_mode=DataReturnMode.AS_INPUT,
           columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
           )
    
    sel_row = grid_return["selected_rows"]

    # MAP
    if len(sel_row) == 0:
        map_sby = folium.Map(tiles="OpenStreetMap", location=center(), zoom_start=5)

    else:
        map_sby = folium.Map(tiles="OpenStreetMap", location=[sel_row[-1]['latitude'], sel_row[-1]['longitude']],
                             zoom_start=7)

        # add markers to map
        for r in sel_row:
            coord = str(r['latitude']) + "," + str(r['longitude'])

            # default
            boloonicon = 'location-crosshairs'
            balooncolour = 'lightgray'

            if r['Kategorie'] in icondict:
                boloonicon = icondict[r['Kategorie']][0]
                balooncolour = icondict[r['Kategorie']][1]

            # icons are not rendering
            icon = folium.Icon(color=balooncolour, icon="circle", prefix='fa', icon_color='white')
            folium.Marker(
                location=[r['latitude'], r['longitude']], popup=coord, tooltip=r['Pleknaam'], icon=icon
            ).add_to(map_sby)

    # call to render Folium map in Streamlit
    st_folium(map_sby, height=350, width=700)

    
    
    # debug
    st.write(sel_row)


    
    
    
    


# --- TAB: WYSIG LYS ---
if selected == "Wysig Lys":
    st.header("Wysig Lys")
    
    st.write("")
    st.markdown('<div style="text-align: center"> Teken in met jou Google rekening om wysigingsvoorstelle te maak. </div>', unsafe_allow_html=True)
    st.button("Teken in", key=None, help=None, on_click=None, args=None, kwargs=None)
    st.markdown('<div style="text-align: center"> Neem kennis dat alle voorstelle tot jou gebruikerprofiel gekoppel word. </div>', unsafe_allow_html=True)
    
    
    # MAP
    #m = folium.Map(location=[-30, 25], zoom_start=5)
    #m.add_child(folium.LatLngPopup())
    #map = st_folium(m, height=350, width=700)
    
    
    #data = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])

    #if data is not None:
    #    st.write(data)