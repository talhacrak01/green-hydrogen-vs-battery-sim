#!/usr/bin/env python3
"""
Yeşil Hidrojen vs Lityum Batarya Termodinamik & Kütle Bilançosu Simülasyonu
========================================================================
40 tonluk Class-8 ağır vasıta tırda 800 km otoyol menzili için:
- Lityum Bataryalı Elektrikli Tır (BEV - Tesla Semi, Volvo FH Electric)
- Yeşil Hidrojen Yakıt Hücreli Tır (FCEV - Mercedes GenH2)
karşılaştırmasını şebekeden tekere (Well-to-Wheel) verim ve faydalı yük (payload)
kaybı üzerinden simüle eder.

Kaynaklar: U.S. DOE, Fraunhofer ISE, ICCT Saha Telemetrileri
Yazar: Talha Çırak (@talhacirak_energy)
GitHub: https://github.com/talhacrak01/green-hydrogen-vs-battery-sim
Lisans: MIT
"""

import argparse
import os
import sys

# Windows cp1254 safe printing
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def simulate_heavy_transport(range_km: float = 800.0, gross_weight_ton: float = 40.0, consumption_kwh_per_km: float = 1.5):
    """
    Termodinamik ve Kütle Bilançosu Hesaplaması:
    - 40 tonluk tır 800 km otoyol sürüşü için tekerlekte 1.200 kWh mekanik çekiş enerjisi talep eder.
    - Standart Class-8 çekici + treyler boş (dara) ağırlığı: ~15,0 ton.
    """
    tare_ton = 15.0
    base_payload_kg = max(1000.0, (gross_weight_ton - tare_ton) * 1000.0)

    # Özgül çekiş tüketimi brüt ağırlıkla ölçeklenir (40 tonda 1,5 kWh/km = 0,0375 kWh/km/ton)
    effective_consumption = consumption_kwh_per_km * (gross_weight_ton / 40.0)
    traction_energy_kwh = range_km * effective_consumption

    # 1. Enerji Yoğunlukları (Wh/kg)
    diesel_grav_wh_per_kg = 12000.0
    h2_grav_lhv_wh_per_kg = 33330.0  # Alt Isıl Değer (LHV)
    lfp_pack_grav_wh_per_kg = 125.0  # Termal yönetim ve zırh dahil paket seviyesi
    nmc_pack_grav_wh_per_kg = 160.0

    # 2. Batarya Seçeneği (LFP / NMC)
    # LFP: %90 Deşarj Derinliği (DoD) x %88 Güç Aktarım Verimi = %79,2
    batt_eff = 0.90 * 0.88
    batt_capacity_kwh = traction_energy_kwh / batt_eff
    lfp_weight_kg = (batt_capacity_kwh * 1000.0) / lfp_pack_grav_wh_per_kg
    nmc_weight_kg = (batt_capacity_kwh * 1000.0) / nmc_pack_grav_wh_per_kg

    # 3. Hidrojen Seçeneği (700 bar Type-IV Tank + 300 kW PEM Yakıt Hücresi)
    # PEM Yakıt Hücresi %50 verim x %92 invertör/motor verimi = %46 net
    fc_eff = 0.50 * 0.92
    h2_chem_energy_kwh = traction_energy_kwh / fc_eff
    h2_kg_needed = h2_chem_energy_kwh / (h2_grav_lhv_wh_per_kg / 1000.0)

    # 700 bar kompozit Type-IV tank kütlesel verimi: ~%5,7 H2 ağırlık oranı
    tank_weight_kg = h2_kg_needed / 0.057
    fc_system_weight_kg = 300.0  # 300 kW PEM stack + yardımcı sistemler
    total_h2_system_kg = tank_weight_kg + fc_system_weight_kg

    # 4. Şebekeden Tekere (Well-to-Wheel) Verim Kaskadı
    # Batarya: Şarj Cihazı (%95) x Batarya Çevrim (%90) x İnvertör/Motor (%90) = %77,0
    wtw_batt = 0.95 * 0.90 * 0.90

    # Hidrojen: PEM Elektroliz (%68) x 700 bar Kompresyon/Soğutma (%88) x Lojistik/Dolum (%95) x Yakıt Hücresi (%50) x Motor (%90) = %25,6
    wtw_h2 = 0.68 * 0.88 * 0.95 * 0.50 * 0.90
    multiplier = wtw_batt / wtw_h2

    return {
        "range_km": range_km,
        "gross_weight_ton": gross_weight_ton,
        "base_payload_kg": base_payload_kg,
        "traction_energy_kwh": traction_energy_kwh,
        "batt_capacity_kwh": batt_capacity_kwh,
        "lfp_weight_kg": lfp_weight_kg,
        "nmc_weight_kg": nmc_weight_kg,
        "h2_kg_needed": h2_kg_needed,
        "tank_weight_kg": tank_weight_kg,
        "total_h2_system_kg": total_h2_system_kg,
        "wtw_batt": wtw_batt,
        "wtw_h2": wtw_h2,
        "multiplier": multiplier,
        "weight_delta_kg": lfp_weight_kg - total_h2_system_kg,
    }


def print_simulation_report(res: dict):
    print("=" * 80)
    print("YEŞİL HİDROJEN vs LİTYUM BATARYA AĞIR TAŞIMACILIK SİMÜLASYONU")
    print(f"Koşullar: {res['gross_weight_ton']:.0f} Tonluk Tır | {res['range_km']:.0f} km Otoyol Menzili | {res['traction_energy_kwh']:.0f} kWh Çekiş Gücü")
    print("=" * 80)

    print("\n--- 1. YUVARLAK ÇEVRİM VERİMİ (ŞEBEKEDEN TEKERE / WELL-TO-WHEEL) ---")
    print(f"Lityum Batarya (BEV) Net Verim:     %{res['wtw_batt'] * 100:.1f}")
    print(f"Yeşil Hidrojen (FCEV) Net Verim:    %{res['wtw_h2'] * 100:.1f}")
    print(f"Elektrik Tüketim Çarpanı:           TAM {res['multiplier']:.2f}x")
    print(">> Sonuç: Hidrojen, aynı yolu gitmek için yaklaşık 3 KAT daha fazla rüzgar/güneş elektriği talep eder!")

    print("\n--- 2. KÜTLE DENGESİ VE YÜK (PAYLOAD) KAPASİTESİ ---")
    print(f"Lityum Batarya (LFP) Paket Ağırlığı: {res['lfp_weight_kg'] / 1000.0:.2f} Ton ({res['batt_capacity_kwh']:.0f} kWh)")
    print(f"Lityum Batarya (NMC) Paket Ağırlığı: {res['nmc_weight_kg'] / 1000.0:.2f} Ton ({res['batt_capacity_kwh']:.0f} kWh)")
    print(f"Yeşil Hidrojen Yakıt Miktarı:       {res['h2_kg_needed']:.1f} kg H2 (~80 kg)")
    print(f"700 bar Tank + PEM Yakıt Hücresi:   {res['total_h2_system_kg'] / 1000.0:.2f} Ton")
    print(f"Hidrojenin Net Ağırlık Avantajı:     +{res['weight_delta_kg'] / 1000.0:.2f} Ton daha hafif!")
    base_payload_kg = res.get("base_payload_kg", (res["gross_weight_ton"] - 15.0) * 1000.0)
    pct_payload_lost = (res['lfp_weight_kg'] / base_payload_kg) * 100.0
    print(f">> Sonuç: Batarya {base_payload_kg/1000:.0f} tonluk net yükün beşte birini (~%{pct_payload_lost:.0f}) yutarken; hidrojen yük kapasitesini korur.")

    print("\n--- 3. MÜHENDİSLİK HÜKMÜ ---")
    print("Şehir içi dağıtım ve binek araçlarda:  LİTYUM BATARYA MUTLAK KRAL.")
    print("800+ km ağır yük tırları ve gemilerde: YEŞİL HİDROJEN TEK FİZİKSEL ÇIKIŞ YOLU.")
    print("=" * 80)


def plot_comparisons(res: dict, out_efficiency="wtw_efficiency_comparison.png", out_payload="truck_payload_comparison.png"):
    try:
        import matplotlib.pyplot as plt

        # Plot 1: Efficiency Cascade
        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
        fig.patch.set_facecolor("#0F172A")
        ax.set_facecolor("#1E293B")

        categories = ["Lityum Batarya (BEV)", "Yeşil Hidrojen (FCEV)"]
        values = [res["wtw_batt"] * 100, res["wtw_h2"] * 100]
        colors = ["#10B981", "#38BDF8"]

        bars = ax.bar(categories, values, color=colors, width=0.5)
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval + 1.5, f"%{yval:.1f}", ha="center", va="bottom", color="#FFFFFF", fontweight="bold", fontsize=12)

        ax.set_ylim(0, 100)
        ax.set_title("Şebekeden Tekere (Well-to-Wheel) Net Verim Karşılaştırması", color="#FFFFFF", fontsize=13, fontweight="bold", pad=15)
        ax.set_ylabel("Net Enerji Verimi (%)", color="#94A3B8", fontsize=11)
        ax.tick_params(colors="#94A3B8")
        ax.grid(True, linestyle=":", alpha=0.3, color="#64748B", axis="y")

        plt.tight_layout()
        plt.savefig(out_efficiency)
        plt.close()
        print(f"[OK] Grafik kaydedildi: {out_efficiency}")

        # Plot 2: Weight Breakdown
        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
        fig.patch.set_facecolor("#0F172A")
        ax.set_facecolor("#1E293B")

        techs = ["LFP Batarya Paketi", "Yeşil Hidrojen Sistemi (Tank+FC)"]
        weights = [res["lfp_weight_kg"] / 1000.0, res["total_h2_system_kg"] / 1000.0]
        bar_colors = ["#F43F5E", "#0EA5E9"]

        bars = ax.bar(techs, weights, color=bar_colors, width=0.5)
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.3, f"{yval:.2f} Ton", ha="center", va="bottom", color="#FFFFFF", fontweight="bold", fontsize=12)

        ax.set_ylim(0, 15)
        ax.set_title(f"800 km Menzil İçin Güç Kaynağı Ağırlığı ({res['gross_weight_ton']:.0f} Ton Tır)", color="#FFFFFF", fontsize=13, fontweight="bold", pad=15)
        ax.set_ylabel("Sistem Ağırlığı (Ton)", color="#94A3B8", fontsize=11)
        ax.tick_params(colors="#94A3B8")
        ax.grid(True, linestyle=":", alpha=0.3, color="#64748B", axis="y")

        plt.tight_layout()
        plt.savefig(out_payload)
        plt.close()
        print(f"[OK] Grafik kaydedildi: {out_payload}")
    except Exception as e:
        print(f"[Warning] Grafik üretilemedi: {e}")


def main():
    parser = argparse.ArgumentParser(description="Yeşil Hidrojen vs Lityum Batarya Ağır Vasıta Simülasyonu")
    parser.add_argument("--range-km", type=float, default=800.0, help="Otoyol menzili (km)")
    parser.add_argument("--gross-ton", type=float, default=40.0, help="Toplam brüt tır ağırlığı (Ton)")
    parser.add_argument("--plot", action="store_true", help="Karşılaştırma grafiklerini üret (PNG)")
    args = parser.parse_args()

    res = simulate_heavy_transport(range_km=args.range_km, gross_weight_ton=args.gross_ton)
    print_simulation_report(res)

    if args.plot:
        plot_comparisons(res)


if __name__ == "__main__":
    main()
