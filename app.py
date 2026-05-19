import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import streamlit as st

# Sayfa arayüzü
st.set_page_config(page_title="Akıllı PC Soğutma Kontrolcüsü", layout="wide")
st.title("Bulanık Mantık - Akıllı Performans PC Soğutma Kontrolcüsü")
st.markdown("Bu sistem CPU, GPU ve Kasa İçi sıcaklık değerlerini alarak, bulanık mantık ile optimum fan dönüş hızını hesaplar.")


# Giriş Değişkenleri (Antecedents)
cpu = ctrl.Antecedent(np.arange(0, 101, 1), 'cpu')
gpu = ctrl.Antecedent(np.arange(0, 101, 1), 'gpu')
kasa = ctrl.Antecedent(np.arange(20, 61, 1), 'kasa')

fan = ctrl.Consequent(np.arange(0, 101, 1), 'fan', defuzzify_method='centroid')

# CPU Üyelik Fonksiyonları
cpu['düşük'] = fuzz.trimf(cpu.universe, [0, 0, 50])
cpu['normal'] = fuzz.trimf(cpu.universe, [30, 50, 80])
cpu['yüksek'] = fuzz.trimf(cpu.universe, [65, 100, 100])

# GPU Üyelik Fonksiyonları
gpu['düşük'] = fuzz.trimf(gpu.universe, [0, 0, 50])
gpu['normal'] = fuzz.trimf(gpu.universe, [30, 50, 80])
gpu['yüksek'] = fuzz.trimf(gpu.universe, [65, 100, 100])

# Kasa İçi Üyelik Fonksiyonları
kasa['serin'] = fuzz.trimf(kasa.universe, [20, 20, 35])
kasa['ılık'] = fuzz.trimf(kasa.universe, [30, 40, 50])
kasa['sıcak'] = fuzz.trimf(kasa.universe, [45, 60, 60])

# Fan (Çıkış) Üyelik Fonksiyonları
fan['yavaş'] = fuzz.trimf(fan.universe, [0, 0, 40])
fan['orta'] = fuzz.trimf(fan.universe, [30, 50, 70])
fan['hızlı'] = fuzz.trimf(fan.universe, [60, 80, 100])
fan['tam_güç'] = fuzz.trimf(fan.universe, [85, 100, 100])

# Kurallar
rule1 = ctrl.Rule(cpu['düşük'] & gpu['düşük'] & kasa['serin'], fan['yavaş'])
rule2 = ctrl.Rule(cpu['düşük'] & gpu['düşük'] & kasa['ılık'], fan['yavaş'])
rule3 = ctrl.Rule(cpu['düşük'] & gpu['normal'] & kasa['serin'], fan['orta'])
rule4 = ctrl.Rule(cpu['normal'] & gpu['düşük'] & kasa['serin'], fan['orta'])
rule5 = ctrl.Rule(cpu['normal'] & gpu['normal'] & kasa['serin'], fan['orta'])
rule6 = ctrl.Rule(cpu['normal'] & gpu['normal'] & kasa['ılık'], fan['hızlı'])
rule7 = ctrl.Rule(cpu['yüksek'] & gpu['düşük'] & kasa['serin'], fan['hızlı'])
rule8 = ctrl.Rule(cpu['düşük'] & gpu['yüksek'] & kasa['serin'], fan['hızlı'])
rule9 = ctrl.Rule(cpu['yüksek'] & gpu['normal'] & kasa['ılık'], fan['hızlı'])
rule10 = ctrl.Rule(cpu['normal'] & gpu['yüksek'] & kasa['ılık'], fan['hızlı'])
rule11 = ctrl.Rule(cpu['düşük'] & gpu['düşük'] & kasa['sıcak'], fan['orta'])
rule12 = ctrl.Rule(cpu['normal'] & gpu['normal'] & kasa['sıcak'], fan['hızlı'])
rule13 = ctrl.Rule(cpu['yüksek'] & gpu['yüksek'] & kasa['serin'], fan['tam_güç'])
rule14 = ctrl.Rule((cpu['yüksek'] | gpu['yüksek']) & kasa['sıcak'], fan['tam_güç'])
rule15 = ctrl.Rule(cpu['yüksek'] & gpu['yüksek'] & kasa['sıcak'], fan['tam_güç'])

# Kontrol yeri
sogutma_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, 
                                   rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15])
sogutma_sim = ctrl.ControlSystemSimulation(sogutma_ctrl)

# Arayüz

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Sistem Girişleri")
    with st.form("hesaplama_formu"):
        in_cpu = st.slider("CPU Sıcaklığı (°C)", 0, 100, 45)
        in_gpu = st.slider("GPU Sıcaklığı (°C)", 0, 100, 55)
        in_kasa = st.slider("Kasa İçi Sıcaklık (°C)", 20, 60, 32)
        
        hesapla_btn = st.form_submit_button("Sonucu Hesapla", type="primary")

with col2:
    st.header("Sonuç ve Aktivasyon")
    
    # Değerleri simülasyona aktarma
    sogutma_sim.input['cpu'] = in_cpu
    sogutma_sim.input['gpu'] = in_gpu
    sogutma_sim.input['kasa'] = in_kasa
    
    sogutma_sim.compute()
    cikis_fan = sogutma_sim.output['fan']
    
    st.success(f"### Hesaplanmış Fan Hızı: % {cikis_fan:.2f}")
    st.progress(int(cikis_fan))
    
    st.subheader("Fan Çıkışı Kural Aktivasyon Grafiği")
    
    fan.view(sim=sogutma_sim)
    fig_fan = plt.gcf() 
    st.pyplot(fig_fan)
    plt.close(fig_fan) 

st.divider()

# Üyelik Fonksiyonlarının Gösterimi
st.header("Giriş Değerlerinin Kümeler Üzerindeki Dağılımı")
st.markdown("Aşağıdaki grafiklerdeki **kırmızı kesik çizgiler**, az önce girdiğiniz sıcaklık değerlerinin hangi dilsel değişkenleri (Düşük/Normal/Yüksek) tetiklediğini göstermektedir.")

col3, col4, col5 = st.columns(3)

with col3:
    cpu.view()
    fig_cpu = plt.gcf()
    ax_cpu = fig_cpu.gca() 
    ax_cpu.axvline(x=in_cpu, color='red', linestyle='--', linewidth=2, label=f'Giriş: {in_cpu}°C')
    ax_cpu.legend()
    st.pyplot(fig_cpu)
    plt.close(fig_cpu)

with col4:
    gpu.view()
    fig_gpu = plt.gcf()
    ax_gpu = fig_gpu.gca()
    ax_gpu.axvline(x=in_gpu, color='red', linestyle='--', linewidth=2, label=f'Giriş: {in_gpu}°C')
    ax_gpu.legend()
    st.pyplot(fig_gpu)
    plt.close(fig_gpu)

with col5:
    kasa.view()
    fig_kasa = plt.gcf()
    ax_kasa = fig_kasa.gca()
    ax_kasa.axvline(x=in_kasa, color='red', linestyle='--', linewidth=2, label=f'Giriş: {in_kasa}°C')
    ax_kasa.legend()
    st.pyplot(fig_kasa)
    plt.close(fig_kasa)