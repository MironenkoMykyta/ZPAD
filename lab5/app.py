import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import StringIO

st.set_page_config(page_title="NOAA Дашборд", layout="wide")
st.title("Лабораторна робота 5: Дослідження VHI, VCI, TCI")

@st.cache_data
def load_clean_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_dir, "data")
    
    if not os.path.exists(folder_path):
        return pd.DataFrame()
        
    dataframes = []
    for filename in os.listdir(folder_path):
        if not filename.endswith('.csv'):
            continue
            
        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            if len(lines) < 3: 
                continue
                
            header = lines[1].replace('<br>', '').strip()
            body = [line.replace('<tt><pre>', '').replace('</pre></tt>', '').strip() for line in lines[2:]]
            
            csv_text = header + '\n' + '\n'.join(body)
            # ФІКС: додано index_col=False, щоб роки не з'їжджали в індекс
            df = pd.read_csv(StringIO(csv_text), skipinitialspace=True, index_col=False)
            
            df.columns = [col.strip().lower() for col in df.columns]
            df.rename(columns={'year': 'Year', 'week': 'Week', 'vci': 'VCI', 'tci': 'TCI', 'vhi': 'VHI'}, inplace=True)
            
            prov_id = int(filename.split('_')[2])
            df['Province'] = prov_id
            
            target_cols = ['Year', 'Week', 'VCI', 'TCI', 'VHI', 'Province']
            df = df[target_cols].apply(pd.to_numeric, errors='coerce').dropna(subset=['Year', 'Week'])
            dataframes.append(df)
        except Exception:
            continue
            
    if dataframes:
        return pd.concat(dataframes, ignore_index=True)
    return pd.DataFrame()

df_main = load_clean_data()

with st.sidebar:
    st.header("Налаштування фільтрів")
    
    if df_main.empty:
        st.error("Увага: Не вдалося зчитати дані. Перевірте формат файлів у папці data!")
        st.stop()
        
    target_index = st.selectbox("Оберіть індекс для аналізу:", ["VCI", "TCI", "VHI"])
    prov_list = sorted(df_main['Province'].unique().astype(int))
    selected_prov = st.selectbox("Область (ID):", prov_list)
    
    week_min, week_max = st.slider("Діапазон тижнів:", 1, 52, (1, 52))
    
    min_year = int(df_main['Year'].min())
    max_year = int(df_main['Year'].max())
    year_min, year_max = st.slider("Діапазон років:", min_year, max_year, (min_year, max_year))
    
    st.markdown("---")
    st.write("Сортування результатів:")
    sort_ascending = st.checkbox("За зростанням")
    sort_descending = st.checkbox("За спаданням")
    
    if sort_ascending and sort_descending:
        st.error("Помилка: Увімкнено обидва сортування! Оберіть лише одне.")
        st.stop()
        
    if st.button("Скинути всі налаштування", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

mask = (
    (df_main['Province'] == selected_prov) &
    (df_main['Year'] >= year_min) & (df_main['Year'] <= year_max) &
    (df_main['Week'] >= week_min) & (df_main['Week'] <= week_max)
)
filtered_data = df_main[mask].copy()

if sort_ascending:
    filtered_data.sort_values(by=target_index, ascending=True, inplace=True)
elif sort_descending:
    filtered_data.sort_values(by=target_index, ascending=False, inplace=True)

tab_data, tab_chart, tab_compare = st.tabs(["Джерельні дані", "Динаміка індексу", "Аналіз по Україні"])

with tab_data:
    st.subheader(f"Відфільтровані дані для області {selected_prov}")
    if filtered_data.empty:
        st.warning("Немає даних для відображення за обраними критеріями.")
    else:
        st.dataframe(filtered_data, use_container_width=True, hide_index=True)

with tab_chart:
    st.subheader(f"Графік показника {target_index} (Область {selected_prov})")
    if not filtered_data.empty:
        fig1, ax1 = plt.subplots(figsize=(12, 5))
        time_axis = filtered_data['Year'] + filtered_data['Week'] / 52.0
        ax1.plot(time_axis, filtered_data[target_index], color='#1f77b4', linewidth=1.5, marker='o', markersize=3)
        ax1.set_xlabel("Роки")
        ax1.set_ylabel(f"Значення {target_index}")
        ax1.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig1)

with tab_compare:
    st.subheader(f"Порівняння {target_index} обраної області з іншими")
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    for p_id in prov_list:
        prov_data = df_main[(df_main['Province'] == p_id) & 
                            (df_main['Year'] >= year_min) & 
                            (df_main['Year'] <= year_max)]
        time_val = prov_data['Year'] + prov_data['Week'] / 52.0
        if p_id == selected_prov:
            ax2.plot(time_val, prov_data[target_index], color='crimson', linewidth=2.5, label=f'Область {p_id}', zorder=10)
        else:
            ax2.plot(time_val, prov_data[target_index], color='gray', linewidth=1, alpha=0.3)
            
    ax2.set_xlabel("Роки")
    ax2.set_ylabel(target_index)
    ax2.legend(loc="upper right")
    ax2.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig2)