import streamlit as st
import pandas as pd
from datetime import date

# Configuración inicial de la página
st.set_page_config(
    page_title="Calculadoras Laborales Perú",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# FUNCIONES AUXILIARES DE VALIDACIÓN
# ==========================================
def validar_monto(texto, nombre_campo="Monto"):
    """
    Valida y convierte un texto ingresado a float positivo.
    Retorna (valor_numerico, es_valido, mensaje_error)
    """
    if texto is None:
        return 0.0, False, f"El campo '{nombre_campo}' no puede estar vacío."
    
    texto_limpio = texto.strip()
    
    if texto_limpio == "":
        return 0.0, False, f"El campo '{nombre_campo}' no puede estar vacío o contener solo espacios."
    
    texto_limpio = texto_limpio.replace(",", "")
    
    try:
        valor = float(texto_limpio)
        if valor < 0:
            return 0.0, False, f"El campo '{nombre_campo}' no puede ser un valor negativo."
        return valor, True, ""
    except ValueError:
        return 0.0, False, f"El campo '{nombre_campo}' contiene caracteres inválidos (solo se permiten números)."

def validar_entero(texto, nombre_campo="Valor"):
    """
    Valida y convierte un texto ingresado a entero positivo.
    """
    if texto is None:
        return 0, False, f"El campo '{nombre_campo}' no puede estar vacío."
    
    texto_limpio = texto.strip()
    if texto_limpio == "":
        return 0, False, f"El campo '{nombre_campo}' no puede estar vacío."
        
    try:
        valor = int(texto_limpio)
        if valor < 0:
            return 0, False, f"El campo '{nombre_campo}' no puede ser negativo."
        return valor, True, ""
    except ValueError:
        return 0, False, f"El campo '{nombre_campo}' debe ser un número entero válido."

# ==========================================
# CONSTANTES Y PARÁMETROS INTERNOS 
# ==========================================
uit_val = 5500.0       
rmv_val = 1230.0       
asig_fam_val = 123.0   

# ==========================================
# THEME / GLOBAL CSS & DISEÑO MEJORADO
# ==========================================
st.markdown("""
<style>
    /* Estilos Generales de Fondo */
    .main {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* 🚀 SUBIR EL CONTENEDOR Y QUITAR EL MARGEN SUPERIOR DE STREAMLIT */
    .block-container {
        padding-top: 1rem !important; /* Reduce el espacio vacío superior de la página */
        padding-bottom: 2rem !important;
    }

    /* ENCABEZADO PRINCIPAL MÁS GRANDE Y ARRIBA */
    .hero-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #dc2626 100%);
        padding: 3.5rem 3rem; /* Más altura interna */
        border-radius: 20px;
        color: white;
        box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.25);
        margin-bottom: 1.5rem;
    }
    .hero-tag {
        font-size: 1rem; 
        font-weight: 700; 
        color: #fca5a5; 
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .hero-title {
        font-size: 3.2rem; /* Título más grande e imponente */
        font-weight: 800;
        margin: 0;
        color: #ffffff;
        letter-spacing: -0.03em;
        line-height: 1.15;
    }
    .hero-subtitle {
        font-size: 1.3rem; /* Subtítulo más legible y grande */
        color: #cbd5e1;
        margin-top: 1rem;
        max-width: 950px;
        line-height: 1.5;
    }

    /* Cards y Contenedores de Métricas */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.08);
    }
    .metric-label {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #475569;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
    }
    .metric-value-accent {
        color: #2563eb;
    }

    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e293b;
        padding: 10px;
        border-radius: 14px;
        overflow-x: auto;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: 700;
        font-size: 0.95rem;
        background-color: #334155;
        color: #ffffff !important;
        border: none;
        white-space: nowrap;
    }
    .stTabs [aria-selected="true"] {
        background-color: #dc2626 !important;
        box-shadow: 0 4px 14px rgba(220, 38, 38, 0.4);
    }

    /* Trust Section Estilizada */
    .trust {
        margin-top: 40px;
        padding: 25px 30px;
        background: #0f172a;
        color: white;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15);
    }
    .trust h3 {
        margin: 0 0 6px 0;
        font-size: 1.2rem;
    }
    .trust p {
        color: #94a3b8;
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    .trust-stats {
        display: flex;
        gap: 25px;
        flex-shrink: 0;
    }
    .stat strong {
        display: block;
        font-size: 1.3rem;
        color: #ffffff;
    }
    .stat span {
        font-size: 0.8rem;
        color: #94a3b8;
    }

    /* Responsive para Celulares */
    @media (max-width: 768px) {
        .hero-header {
            padding: 2rem 1.2rem;
        }
        .hero-title {
            font-size: 2.1rem;
        }
        .hero-subtitle {
            font-size: 1.05rem;
        }
        .trust {
            flex-direction: column;
            align-items: flex-start;
            gap: 15px;
        }
        .trust-stats {
            width: 100%;
            justify-content: space-between;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO SECTION / ENCABEZADO
# ==========================================
st.markdown("""
<div class="hero-header">
    <div class="hero-tag">🇵🇪 Hecho para el mercado laboral peruano</div>
    <h1 class="hero-title">Calcula tus beneficios laborales en segundos.</h1>
    <p class="hero-subtitle">Herramientas precisas y actualizadas para estimar tu sueldo, CTS, gratificaciones, vacaciones, liquidación y otros derechos laborales vigentes.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# NAVEGACIÓN PRINCIPAL (TABS UX)
# ==========================================
tab_grati, tab_cts, tab_liq,tab_neto,tab_ir5,tab_he = st.tabs([
    "🎁 Gratificaciones", 
    "🏦 CTS", 
    "📋 Liquidación", 
    "💵 Sueldo Neto (Nuevo Ingreso)", 
    "📑 Impuesto 5ta", 
    "⏰ Horas Extras"
])

# ------------------------------------------
# 1. CALCULADORA DE GRATIFICACIONES
# ------------------------------------------
with tab_grati:
    st.subheader("Cálculo de Gratificaciones (Julio / Diciembre)")
    st.write("Calcula la gratificación proporcional y bonificación extraordinaria (Ley 30334) según tu fecha de ingreso.")
    
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        sueldo_grati_txt = st.text_input("Sueldo Base Mensual (S/)", value="", placeholder="1230.00", key="g_sueldo_txt")
        sueldo_grati, valido_g, err_g = validar_monto(sueldo_grati_txt, "Sueldo Base Mensual (Gratificación)")

        tiene_hijos_grati = st.radio("¿Tiene hijos? (Asignación Familiar)", ["Sí", "No"], horizontal=True, key="g_hijos")
        
    with g_col2:
        periodo_grati = st.selectbox(
            "Seleccione el Periodo de Gratificación", 
            ["Julio (Fiestas Patrias)", "Diciembre (Navidad)"],
            key="g_periodo"
        )
        fecha_ingreso_grati = st.date_input("Fecha de Ingreso Laboral", value=date(2026, 1, 1), format="DD/MM/YYYY", key="g_fecha_ingreso")
        eps_opcion = st.radio("Aportación de Salud", ["EsSalud (9%)", "EPS / EsSalud (6.75%)"], key="g_salud", horizontal=True)

    if not valido_g:
        st.error(f"{err_g}")
    else:
        pct_bono = 0.09 if "9%" in eps_opcion else 0.0675
        monto_af_grati = asig_fam_val if tiene_hijos_grati == "Sí" else 0.0
        rem_computable_grati = sueldo_grati + monto_af_grati
        anio_actual = date.today().year

        if "Julio" in periodo_grati:
            inicio_sem_g = date(anio_actual, 1, 1)
            corte_sem_g = date(anio_actual, 6, 30)
        else:
            inicio_sem_g = date(anio_actual, 7, 1)
            corte_sem_g = date(anio_actual, 12, 31)

        if fecha_ingreso_grati <= inicio_sem_g:
            meses_efectivos_g = 6
            dias_efectivos_g = 0
            grati_base = rem_computable_grati
        elif fecha_ingreso_grati > corte_sem_g:
            meses_efectivos_g = 0
            dias_efectivos_g = 0
            grati_base = 0.0
        else:
            anios_diff_g = corte_sem_g.year - fecha_ingreso_grati.year
            meses_tot_g = anios_diff_g * 12 + (corte_sem_g.month - fecha_ingreso_grati.month)
            dias_extra_g = corte_sem_g.day - fecha_ingreso_grati.day + 1

            if dias_extra_g < 0:
                meses_tot_g -= 1
                dias_extra_g += 30
            if dias_extra_g >= 30:
                meses_tot_g += 1
                dias_extra_g -= 30

            meses_efectivos_g = max(0, min(6, meses_tot_g))
            dias_efectivos_g = max(0, dias_extra_g) if meses_efectivos_g < 6 else 0

            if dias_efectivos_g >= 30:
                meses_efectivos_g += 1
                dias_efectivos_g = 0

            if meses_efectivos_g >= 6:
                meses_efectivos_g = 6
                dias_efectivos_g = 0
                grati_base = rem_computable_grati
            else:
                v_dozavo = rem_computable_grati / 6.0
                v_treintavo = v_dozavo / 30.0
                grati_base = (v_dozavo * meses_efectivos_g) + (v_treintavo * dias_efectivos_g)

        bono_extra = grati_base * pct_bono
        monto_total_grati = grati_base + bono_extra

        st.markdown("---")
        m_col1, m_col2, m_col3 = st.columns(3)
        
        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Remuneración Computable</div>
                <div class="metric-value">S/ {rem_computable_grati:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Bonificación Extraordinaria</div>
                <div class="metric-value">S/ {bono_extra:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total a Recibir</div>
                <div class="metric-value metric-value-accent">S/ {monto_total_grati:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.info(f"⏳ **TIEMPO A COMPUTAR:** {meses_efectivos_g} MESES Y {dias_efectivos_g} DÍAS (Periodo del {inicio_sem_g.strftime('%d/%m/%Y')} al {corte_sem_g.strftime('%d/%m/%Y')})")
# ------------------------------------------
# 2. CALCULADORA DE CTS
# ------------------------------------------
with tab_cts:
    st.subheader("Compensación por Tiempo de Servicios (CTS)")
    st.write("Calcula la CTS correspondiente al periodo semestral según tu fecha de ingreso.")
    
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        sueldo_texto = st.text_input("Sueldo Base Mensual (S/)", value="", placeholder="1230.00", key="c_sueldo_txt")
        sueldo_cts, valido_c, err_c = validar_monto(sueldo_texto, "Sueldo Base Mensual (CTS)")

        tiene_hijos_cts = st.radio("¿Tiene hijos? (Asignación Familiar)", ["Sí", "No"], horizontal=True, key="c_hijos")
        
    with c_col2:
        periodo_cts = st.selectbox(
            "Seleccione el Periodo de Depósito CTS", 
            ["Mayo", "Noviembre"],
            key="c_periodo_cts"
        )
        fecha_ingreso = st.date_input("Fecha de Ingreso Laboral", value=date(2026, 1, 1), format="DD/MM/YYYY", key="c_fecha_ingreso")

    if not valido_c:
        st.error(f" {err_c}")
    else:
        monto_af = asig_fam_val if tiene_hijos_cts == "Sí" else 0.0 
        remun_computable = sueldo_cts + monto_af
        anio_actual = date.today().year

        if periodo_cts == "Mayo":
            inicio_semestre = date(anio_actual - 1, 11, 1)
            fecha_corte = date(anio_actual, 4, 30)
        else:
            inicio_semestre = date(anio_actual, 5, 1)
            fecha_corte = date(anio_actual, 10, 31)

        if fecha_ingreso <= inicio_semestre:
            meses_efectivos = 6
            dias_efectivos = 0
            total_cts = remun_computable / 2.0
        elif fecha_ingreso > fecha_corte:
            meses_efectivos = 0
            dias_efectivos = 0
            total_cts = 0.0
        else:
            anios_diff = fecha_corte.year - fecha_ingreso.year
            meses_tot = anios_diff * 12 + (fecha_corte.month - fecha_ingreso.month)
            dias_extra = fecha_corte.day - fecha_ingreso.day + 1

            if dias_extra < 0:
                meses_tot -= 1
                dias_extra += 30
            if dias_extra >= 30:
                meses_tot += 1
                dias_extra -= 30

            meses_efectivos = max(0, min(6, meses_tot))
            dias_efectivos = max(0, dias_extra) if meses_efectivos < 6 else 0

            if dias_efectivos == 30:
                meses_efectivos += 1
                dias_efectivos = 0

            if meses_efectivos >= 6:
                meses_efectivos = 6
                dias_efectivos = 0
                total_cts = remun_computable / 2.0
            else:
                valor_dozavo = remun_computable / 12.0
                valor_treintavo = valor_dozavo / 30.0
                total_cts = (valor_dozavo * meses_efectivos) + (valor_treintavo * dias_efectivos)

        sexto_grati_visual = remun_computable / 6.0

        st.markdown("---")
        m_col1, m_col2, m_col3 = st.columns(3)
        
        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">1/6 Gratificación</div>
                <div class="metric-value">S/ {sexto_grati_visual:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
                 
        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Asignación Familiar</div>
                <div class="metric-value">S/ {monto_af:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
                 
        with m_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total CTS Depositado</div>
                <div class="metric-value metric-value-accent">S/ {total_cts:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
                 
        st.info(f"⏳ **TIEMPO A COMPUTAR:** {meses_efectivos} MESES Y {dias_efectivos} DÍAS (Periodo del {inicio_semestre.strftime('%d/%m/%Y')} al {fecha_corte.strftime('%d/%m/%Y')})")
    
# ------------------------------------------
# 3. CALCULADORA DE LIQUIDACIÓN
# ------------------------------------------
with tab_liq:
    st.subheader("Liquidación de Beneficios Sociales y Vacaciones (Cese Laboral)")
    st.write("Calcula de forma precisa la CTS trunca, Gratificación trunca, Vacaciones truncas/pendientes e Indemnización (si aplica) según la normativa peruana.")

    l_col1, l_col2 = st.columns(2)
    with l_col1:
        sueldo_liq_txt = st.text_input("Sueldo Base Mensual (S/)", value="", placeholder="1230.00", key="l_sueldo_txt")
        sueldo_liq, valido_l_sueldo, err_l_sueldo = validar_monto(sueldo_liq_txt, "Sueldo Base (Liquidación)")
        tiene_hijos_liq = st.radio("¿Tiene hijos? (Asignación Familiar)", ["Sí", "No"], horizontal=True, key="l_hijos")
        regimen_lab = st.selectbox("Régimen Laboral", ["General (100%)", "Pequeña Empresa (50% Grati/CTS)", "Microempresa (0% Grati/CTS)"])
    
    with l_col2:
        fecha_ingreso_liq = st.date_input("Fecha de Ingreso", value=date(2025, 1, 15), format="DD/MM/YYYY", key="l_ingreso")
        fecha_cese_liq = st.date_input("Fecha de Cese (Salida)", value=date(2026, 6, 30), format="DD/MM/YYYY", key="l_cese")
        motivo_cese = st.selectbox("Motivo de Cese", ["Renuncia voluntaria", "Despido arbitrario (Sin causa justa)", "Mutuo acuerdo", "Vencimiento de contrato"])

    errores_liq = []
    if not valido_l_sueldo: 
        errores_liq.append(err_l_sueldo)
    if fecha_cese_liq < fecha_ingreso_liq:
        errores_liq.append("La fecha de cese no puede ser anterior a la fecha de ingreso.")

    if errores_liq:
        for err in errores_liq:
            st.error(f"{err}")
    else:
        monto_af_liq = asig_fam_val if tiene_hijos_liq == "Sí" else 0.0
        rem_comp_liq = sueldo_liq + monto_af_liq

        # Factores según régimen
        factor_grati_cts = 1.0 if "General" in regimen_lab else (0.5 if "Pequeña" in regimen_lab else 0.0)

        # 1. CTS TRUNCA (Ultimo semestre trunco desde Noviembre o Mayo anterior o desde el ingreso si es menor a 6 meses)
        # Determinamos el semestre actual de CTS al cese
        mes_cese = fecha_cese_liq.month
        anio_cese = fecha_cese_liq.year
        if mes_cese in [11, 12, 1, 2, 3, 4]:
            # Periodo Noviembre - Abril
            inicio_cts_sem = date(anio_cese - 1 if mes_cese in [11, 12] else anio_cese, 11, 1)
        else:
            # Periodo Mayo - Octubre
            inicio_cts_sem = date(anio_cese, 5, 1)

        # El periodo a computar para CTS trunca es desde el inicio del semestre o la fecha de ingreso (el que sea más reciente)
        real_inicio_cts = max(fecha_ingreso_liq, inicio_cts_sem)
        if fecha_cese_liq >= real_inicio_cts:
            dias_cts_totales = (fecha_cese_liq - real_inicio_cts).days + 1
            meses_cts_calc = dias_cts_totales // 30
            dias_cts_calc = dias_cts_totales % 30
            if meses_cts_calc > 6: 
                meses_cts_calc = 6
                dias_cts_calc = 0
            
            val_doz_cts = rem_comp_liq / 12.0
            val_treint_cts = val_doz_cts / 30.0
            cts_trunca = ((val_doz_cts * meses_cts_calc) + (val_treint_cts * dias_cts_calc)) * (1.0 if factor_grati_cts > 0 else 0)
        else:
            cts_trunca = 0.0
            meses_cts_calc, dias_cts_calc = 0, 0

        # 2. GRATIFICACIÓN TRUNCA
        # Semestre de grati al cese (Ene-Jun o Jul-Dic)
        if mes_cese in [1, 2, 3, 4, 5, 6]:
            inicio_grati_sem = date(anio_cese, 1, 1)
        else:
            inicio_grati_sem = date(anio_cese, 7, 1)

        real_inicio_grati = max(fecha_ingreso_liq, inicio_grati_sem)
        if fecha_cese_liq >= real_inicio_grati:
            dias_grati_totales = (fecha_cese_liq - real_inicio_grati).days + 1
            meses_grati_calc = dias_grati_totales // 30
            dias_grati_calc = dias_grati_totales % 30
            if meses_grati_calc > 6:
                meses_grati_calc = 6
                dias_grati_calc = 0

            v_doz_g = rem_comp_liq / 6.0
            v_treint_g = v_doz_g / 30.0
            grati_trunca = ((v_doz_g * meses_grati_calc) + (v_treint_g * dias_grati_calc)) * factor_grati_cts
        else:
            grati_trunca = 0.0

        # 3. VACACIONES TRUNCAS (30 días por año completo, o proporcional por meses y días laborados desde el aniversario o inicio)
        # Cálculo de días totales trabajados desde el ingreso hasta el cese
        dias_totales_laborados = (fecha_cese_liq - fecha_ingreso_liq).days + 1
        anos_trabajados = dias_totales_laborados / 365.25
        
        # Vacaciones proporcionales del último año no gozado (asumiendo récord trunco)
        # Fórmula: (Sueldo / 12) * meses + (Sueldo / 360) * días
        dias_restantes_vac = dias_totales_laborados % 365
        meses_vac = dias_restantes_vac // 30
        dias_vac = dias_restantes_vac % 30
        
        pago_vac_truncas = ((sueldo_liq / 12.0) * (dias_totales_laborados / 30.0)) * (0.5 if "Pequeña" in regimen_lab else (1.0 if "General" in regimen_lab else 0.5))
        # Ajuste estándar de vacaciones truncas por ley (30 días por año completo de servicio):
        # 1 día de remuneración por cada mes laborado (sueldo / 12 por mes, y sueldo / 360 por día)
        pago_vac_truncas = ((sueldo_liq / 12.0) * (meses_vac + (dias_vac / 30.0))) if "General" in regimen_lab else ((sueldo_liq / 24.0) * (meses_vac + (dias_vac / 30.0)))

        # 4. INDEMNIZACIÓN POR DESPIDO ARBITRARIO (Solo si aplica)
        indemnizacion = 0.0
        if "Despido arbitrario" in motivo_cese and "General" in regimen_lab:
            # 1.5 remuneraciones ordinarias por cada año completo de servicios y proporcional por meses/días
            indemnizacion = sueldo_liq * 1.5 * anos_trabajados
        elif "Despido arbitrario" in motivo_cese and "Pequeña" in regimen_lab:
            # 20 remuneraciones diarias por cada año completo con máximo de 120 remuneraciones diarias
            indemnizacion = (sueldo_liq / 30.0) * 20 * anos_trabajados

        total_liquidacion = cts_trunca + grati_trunca + pago_vac_truncas + indemnizacion

        st.markdown("---")
        st.markdown("### 📋 Resumen Detallado de Liquidación de Beneficios Sociales")
        
        df_liq = pd.DataFrame({
            "Concepto Laboral": [
                "CTS Trunca (Periodo Semestral)", 
                "Gratificación Trunca + Bonificación (9%)", 
                "Vacaciones Trtruncas / Pendientes", 
                "Indemnización por Despido Arbitrario" if indemnizacion > 0 else "Indemnización (No aplicable)"
            ],
            "Monto Estimado (S/)": [
                f"S/ {cts_trunca:,.2f}", 
                f"S/ {grati_trunca + (grati_trunca * 0.09 if factor_grati_cts > 0 else 0):,.2f}", 
                f"S/ {pago_vac_truncas:,.2f}", 
                f"S/ {indemnizacion:,.2f}"
            ]
        })
        st.table(df_liq)
        
        st.success(f"💰 **TOTAL NETO A PAGAR EN LIQUIDACIÓN:** S/ {total_liquidacion:,.2f}")
        st.info(f"ℹ️ **Detalle de tiempo laboral computado:** Desde el {fecha_ingreso_liq.strftime('%d/%m/%Y')} hasta el {fecha_cese_liq.strftime('%d/%m/%Y')} ({dias_totales_laborados} días totales en régimen **{regimen_lab}**).")
        
        # ------------------------------------------
# 0. CALCULADORA DE SUELDO NETO
# ------------------------------------------
with tab_neto:
    st.subheader("Simulador de Sueldo Neto (Ingreso de Nuevo Trabajador)")
    st.write("Calcula el sueldo líquido que recibirá el colaborador en su cuenta bancaria, descontando AFP/ONP y sumando asignación familiar si corresponde.")

    n_col1, n_col2 = st.columns(2)
    with n_col1:
        sueldo_base_n_txt = st.text_input("Sueldo Bruto Mensual (S/)", value="", placeholder="2500.00", key="n_sueldo_txt")
        sueldo_base_n, valido_n, err_n = validar_monto(sueldo_base_n_txt, "Sueldo Bruto Mensual")
        tiene_hijos_n = st.radio("¿Tiene hijos? (Asignación Familiar S/ 123.00)", ["Sí", "No"], horizontal=True, key="n_hijos")
    
    with n_col2:
        sistema_pension = st.selectbox("Sistema de Pensiones", ["AFP (Promedio 11.83%)", "ONP (13%)", "Ninguno / Exonerado"])
        comision_afp_tipo = st.selectbox("Tipo de Comisión AFP", ["Flujo (aprox. 1.47%)", "Mixta (aprox. 0.55%)"]) if "AFP" in sistema_pension else None

    if not valido_n:
        st.error(f"{err_n}")
    else:
        monto_af_n = asig_fam_val if tiene_hijos_n == "Sí" else 0.0
        remuneracion_bruta_total = sueldo_base_n + monto_af_n

        descuento_pension = 0.0
        if "ONP" in sistema_pension:
            descuento_pension = remuneracion_bruta_total * 0.13
        elif "AFP" in sistema_pension:
            comision = 0.0147 if "Flujo" in comision_afp_tipo else 0.0055
            tasa_afp = 0.10 + 0.0135 + comision
            descuento_pension = remuneracion_bruta_total * tasa_afp

        sueldo_neto_final = remuneracion_bruta_total - descuento_pension

        st.markdown("---")
        st.markdown("### 📊 Desglose de Boleta del Nuevo Ingreso")
        
        df_neto = pd.DataFrame({
            "Concepto Remunerativo / Descuento": [
                "Sueldo Bruto Base", 
                "Asignación Familiar", 
                "Remuneración Bruta Total", 
                f"Descuento Sistema de Pensiones ({sistema_pension})", 
                "NETO A RECIBIR (En Cuenta)"
            ],
            "Monto (S/)": [
                f"S/ {sueldo_base_n:,.2f}",
                f"S/ {monto_af_n:,.2f}",
                f"S/ {remuneracion_bruta_total:,.2f}",
                f"- S/ {descuento_pension:,.2f}",
                f"S/ {sueldo_neto_final:,.2f}"
            ]
        })
        st.table(df_neto)
        st.success(f"💵 **El colaborador recibirá líquidos cada mes:** S/ {sueldo_neto_final:,.2f}")

# ------------------------------------------
# 4. CALCULADORA DE IMPUESTO A LA RENTA (5TA)
# ------------------------------------------
with tab_ir5:
    st.subheader("Impuesto a la Renta de Quinta Categoría")
    st.write("Cálculo oficial de retenciones mensuales para trabajadores en planilla basado en la UIT vigente (S/ 5,500.00).")

    ir_col1, ir_col2 = st.columns(2)
    with ir_col1:
        sueldo_ir_txt = st.text_input("Ingreso Mensual Bruto (S/)", value="", placeholder="6500.00", key="ir_sueldo_txt")
        sueldo_ir, valido_ir, err_ir = validar_monto(sueldo_ir_txt, "Ingreso Mensual Bruto (5ta Cat)")
        meses_restantes_ir = st.slider("Meses restantes en el ejercicio gravable", 1, 12, 12, key="ir_meses")
    with ir_col2:
        gratificaciones_anuales_estimadas = st.text_input("Gratificaciones Proyectadas (Julio + Dic S/)", value="13000.00", key="ir_grati_txt")
        grati_anual_val, valido_g_ir, err_g_ir = validar_monto(gratificaciones_anuales_estimadas, "Gratificaciones Proyectadas")

    if not valido_ir or not valido_g_ir:
        st.error(f"{err_ir if not valido_ir else err_g_ir}")
    else:
        ingreso_anual_proyectado = (sueldo_ir * 12) + grati_anual_val
        deduccion_7uit = 7 * uit_val
        renta_neta = max(0.0, ingreso_anual_proyectado - deduccion_7uit)

        impuesto_anual = 0.0
        if renta_neta > 0:
            tramo1 = min(renta_neta, 5 * uit_val)
            impuesto_anual += tramo1 * 0.08
            if renta_neta > (5 * uit_val):
                tramo2 = min(renta_neta - (5 * uit_val), 15 * uit_val)
                impuesto_anual += tramo2 * 0.14
            if renta_neta > (20 * uit_val):
                tramo3 = min(renta_neta - (20 * uit_val), 15 * uit_val)
                impuesto_anual += tramo3 * 0.17
            if renta_neta > (35 * uit_val):
                tramo4 = min(renta_neta - (35 * uit_val), 10 * uit_val)
                impuesto_anual += tramo4 * 0.20
            if renta_neta > (45 * uit_val):
                tramo5 = renta_neta - (45 * uit_val)
                impuesto_anual += tramo5 * 0.30

        retencion_mensual = impuesto_anual / meses_restantes_ir if meses_restantes_ir > 0 else 0.0

        st.markdown("---")
        ir_m1, ir_m2, ir_m3 = st.columns(3)
        with ir_m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Renta Bruta Anual Proyectada</div><div class="metric-value">S/ {ingreso_anual_proyectado:,.2f}</div></div>', unsafe_allow_html=True)
        with ir_m2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Renta Neta Imponible (-7 UIT)</div><div class="metric-value">S/ {renta_neta:,.2f}</div></div>', unsafe_allow_html=True)
        with ir_m3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Retención Mensual Sugerida</div><div class="metric-value metric-value-accent">S/ {retencion_mensual:,.2f}</div></div>', unsafe_allow_html=True)

# ------------------------------------------
# 5. CALCULADORA DE HORAS EXTRAS
# ------------------------------------------
with tab_he:
    st.subheader("Cálculo de Horas Extras y Recargos")
    st.write("Calcula el pago adicional con recargos del 25% (primeras 2 horas) y 35% (horas restantes).")

    he_col1, he_col2 = st.columns(2)
    with he_col1:
        sueldo_he_txt = st.text_input("Sueldo Base Mensual (S/)", value="", placeholder="2000.00", key="he_sueldo_txt")
        sueldo_he, valido_he_sueldo, err_he_sueldo = validar_monto(sueldo_he_txt, "Sueldo Base (Horas Extras)")
        horas_25_txt = st.text_input("Número de Horas Extras (25%)", value="4", key="h25_txt")
        horas_25, valido_h25, err_h25 = validar_entero(horas_25_txt, "Horas Extras 25%")
    with he_col2:
        horas_35_txt = st.text_input("Número de Horas Extras (35%)", value="2", key="h35_txt")
        horas_35, valido_h35, err_h35 = validar_entero(horas_35_txt, "Horas Extras 35%")
        incluir_nocturno = st.checkbox("¿Incluye recargo por trabajo nocturno (35% adicional sobre la hora ordinaria)?")

    errores_he = []
    if not valido_he_sueldo: errores_he.append(err_he_sueldo)
    if not valido_h25: errores_he.append(err_h25)
    if not valido_h35: errores_he.append(err_h35)

    if errores_he:
        for err in errores_he:
            st.error(f"{err}")
    else:
        valor_hora_ordinaria = sueldo_he / 240.0 
        pago_h25 = horas_25 * (valor_hora_ordinaria * 1.25)
        pago_h35 = horas_35 * (valor_hora_ordinaria * 1.35)
        
        recargo_nocturno_total = 0.0
        if incluir_nocturno:
            recargo_nocturno_total = (horas_25 + horas_35) * (valor_hora_ordinaria * 0.35)

        total_he = pago_h25 + pago_h35 + recargo_nocturno_total

        st.markdown("---")
        st.info(f"💡 **Valor Hora Ordinaria (Sueldo / 240h):** S/ {valor_hora_ordinaria:.2f}")
        
        h_m1, h_m2, h_m3 = st.columns(3)
        with h_m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Monto H.E. (25%)</div><div class="metric-value">S/ {pago_h25:,.2f}</div></div>', unsafe_allow_html=True)
        with h_m2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Monto H.E. (35%)</div><div class="metric-value">S/ {pago_h35:,.2f}</div></div>', unsafe_allow_html=True)
        with h_m3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Recargo Nocturno</div><div class="metric-value">S/ {recargo_nocturno_total:,.2f}</div></div>', unsafe_allow_html=True)
            
        st.success(f"💵 **TOTAL A PAGAR POR HORAS EXTRAS Y RECARGOS:** S/ {total_he:,.2f}")
# =========================
# TRUST / VALUE
# =========================
st.markdown("""
<div class="trust">
    <div>
        <h3>Información clara para tomar mejores decisiones</h3>
        <p>Diseñada para que cualquier trabajador o reclutador pueda entender su resultado sin complicaciones.</p>
    </div>
    <div class="trust-stats">
        <div class="stat"><strong>6+</strong><span>Calculadoras</span></div>
        <div class="stat"><strong>100%</strong><span>Online</span></div>
        <div class="stat"><strong>🇵🇪</strong><span>Perú</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown("""
<div style="background: #1e293b; color: #cbd5e1; padding: 1.5rem 2rem; border-radius: 14px; text-align: center; font-size: 0.85rem; margin-top: 2rem; line-height: 1.6;">
    <p style="margin: 0 0 8px 0; color: #ffffff; font-weight: 600;">⚖️ Nota Legal Importante</p>
    <p style="margin: 0 0 12px 0; color: #94a3b8; font-size: 0.8rem; max-width: 800px; margin-left: auto; margin-right: auto;">
        Esta aplicación ofrece estimaciones referenciales basadas en las normativas laborales del Perú (CTS, Gratificaciones, Liquidaciones, Quinta Categoría, Sueldo Neto). Los resultados no sustituyen un cálculo oficial de recursos humanos, contadores colegiados o autoridades competentes (MTPE/SUNAT).
    </p>
    <hr style="border: none; border-top: 1px solid #334155; margin: 12px 0;">
    <p style="margin: 0; color: #64748b;">
        Calculadoras Laborales Perú © 2026 — Diseñado para una toma de decisiones informada.
    </p>
</div>
""", unsafe_allow_html=True)