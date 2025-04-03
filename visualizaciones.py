import plotly.express as px
import streamlit as st

def crear_layout():
    return dict(
        title_font_size=22,
        font=dict(family="Segoe UI", size=13, color="#333"),
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=30, r=30, t=50, b=40),
        xaxis=dict(showgrid=False, linecolor="#CCC", linewidth=1.2),
        yaxis=dict(gridcolor="#EEE", zeroline=False),
    )

def graficos_generales(df, columna_industria, columna_ingles, columna_ubicacion):
    layout = crear_layout()

    # Tabla de top 10 proyectos aprobados con mayor puntaje total
    st.subheader("🏆 Top 10 proyectos aprobados con mayor puntaje total")
    # Asegurar columna Puntaje Total
    df["Puntaje Total"] = df["Puntaje TRL 1-3"] + df["Puntaje TRL 4-7"] + df["Puntaje TRL 8-9"]

    # Filtrar solo aprobados y ordenar
    top10 = df[df["Aprobado"] == "Sí"].sort_values("Puntaje Total", ascending=False).head(10)

    # Mostrar tabla
# Verificar columnas disponibles
    columnas_top10 = [
        "Nombre del Proyecto", 
        "Puntaje TRL 1-3", 
        "Puntaje TRL 4-7", 
        "Puntaje TRL 8-9", 
        "Puntaje Total"
    ]

    # Agregar Puntaje Adicional si existe
    if "Puntaje Adicional" in df.columns:
        columnas_top10.insert(-1, "Puntaje Adicional")

    # Mostrar tabla
    st.dataframe(top10[columnas_top10])

    # NUEVO: Botón para descargar todos los proyectos aprobados
    proyectos_aprobados = df[df["Aprobado"] == "Sí"]
    csv_aprobados = proyectos_aprobados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar TODOS los proyectos aprobados",
        data=csv_aprobados,
        file_name='proyectos_aprobados.csv',
        mime='text/csv'
    )


    conteo_segmento = df["Segmento TRL"].value_counts().reset_index()
    conteo_segmento.columns = ["Segmento TRL", "Cantidad"]
    fig1 = px.bar(conteo_segmento, x="Segmento TRL", y="Cantidad", title="Distribución por segmento TRL",
                  color="Segmento TRL", color_discrete_sequence=["#1E90FF", "#117864", "#943126"])
    fig1.update_traces(marker_line_color='black', marker_line_width=1.5,
                       text=conteo_segmento["Cantidad"], textposition='outside')
    fig1.update_layout(height=400, **layout)

    fig2 = px.pie(df, names="Aprobado", title="Proporción de proyectos aprobados",
                  color_discrete_sequence=["#28B463", "#E74C3C"])
    fig2.update_traces(textinfo='percent+label', pull=[0.05, 0],
                       marker_line_color='black', marker_line_width=1.5)
    fig2.update_layout(height=400, **layout)

    fig3 = px.histogram(df, x="Segmento TRL", color="Aprobado", barmode="group",
                        title="Aprobación por segmento TRL",
                        color_discrete_map={"Sí": "#2ECC71", "No": "#E74C3C"})
    fig3.update_traces(marker_line_color='black', marker_line_width=1.5)
    fig3.update_layout(**layout)

    fig4 = px.histogram(df, x="Puntaje TRL 1-3", nbins=20, title="Puntaje TRL 1–3",
                        color_discrete_sequence=["#3498DB"])
    fig4.update_traces(marker_line_color='black', marker_line_width=1.5)
    fig4.update_layout(**layout)

    fig5 = fig6 = fig7 = None

    if columna_industria in df.columns:
        df["Industria"] = df[columna_industria].fillna("No especificada").astype(str).str.strip()
        conteo_industria = df["Industria"].value_counts().reset_index()
        conteo_industria.columns = ["Industria", "Cantidad"]
        fig5 = px.bar(conteo_industria, x="Cantidad", y="Industria", orientation="h",
                      title="Distribución por industria", color="Industria")
        fig5.update_traces(marker_line_color='black', marker_line_width=1.5)
        fig5.update_layout(**layout)

    if columna_ingles in df.columns:
        df[columna_ingles] = df[columna_ingles].astype(str)
        df["Nivel de Inglés"] = df[columna_ingles].fillna("No especificado").str.strip().str.capitalize()
        conteo_ingles = df["Nivel de Inglés"].value_counts().reset_index()
        conteo_ingles.columns = ["Nivel", "Cantidad"]
        fig6 = px.bar(conteo_ingles, x="Nivel", y="Cantidad",
                      title="Nivel de inglés de los proyectos", color="Nivel")
        fig6.update_traces(marker_line_color='black', marker_line_width=1.5)
        fig6.update_layout(**layout)

    if columna_ubicacion in df.columns:
        df[columna_ubicacion] = df[columna_ubicacion].astype(str)
        df["Ubicación"] = df[columna_ubicacion].fillna("No especificada").str.strip().str.capitalize()
        conteo_ubicacion = df["Ubicación"].value_counts().reset_index()
        conteo_ubicacion.columns = ["Ubicación", "Cantidad"]
        fig7 = px.pie(conteo_ubicacion, names="Ubicación", values="Cantidad",
                      title="Ubicación geográfica de los proyectos")
        fig7.update_traces(marker_line_color='black', marker_line_width=1.5)
        fig7.update_layout(**layout)

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7


def mostrar_en_pares(fig1, fig2, fig3, fig4, fig5=None, fig6=None, fig7=None):
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        st.plotly_chart(fig4, use_container_width=True)

    col5, col6 = st.columns(2)
    if fig5:
        with col5:
            st.plotly_chart(fig5, use_container_width=True)
    if fig6:
        with col6:
            st.plotly_chart(fig6, use_container_width=True)

    col7, _ = st.columns(2)
    if fig7:
        with col7:
            st.plotly_chart(fig7, use_container_width=True)
